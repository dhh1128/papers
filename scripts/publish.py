"""One command to publish: regenerate everything derived, optionally bump a
document's version, validate, and report exactly what to commit.

This is the maintainer entry point — you shouldn't need to remember the
individual tools. Typical flow:

    python scripts/new_doc.py --title "…" --category Papers   # create
    # …write the content, replace the TODO abstract/keywords…
    python scripts/publish.py                                 # publish
    git add -A && git commit -s -m "Add …" && git push

Modes:
    publish.py                      regenerate cards/descriptions/index, rebuild
                                    stale PDFs, validate. No version change.
    publish.py --revise <slug> …    minor version bump (errata) on those docs +
                                    revision_date=today, then regenerate.
    publish.py --revise <slug> --major   major bump (new edition; resets minor).
    publish.py --revise             (no slug) list docs with uncommitted changes.
    publish.py --check              validate only; change nothing.
    publish.py --pdfs all|none      force / skip the PDF rebuild (default: stale).
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys

import yaml

from archive import (internal_items, repo_root, normalize_version, bump_version)

SCRIPTS = os.path.join(repo_root, "scripts")
# Records the hash of each doc's PDF-relevant inputs at last build, so a PDF is
# rebuilt only when its rendered content would change — NOT on description/image
# (SEO-only) edits. Committed, so the state is shared and survives clones.
MANIFEST = os.path.join(repo_root, ".pdf-manifest.json")


def pdf_input_hash(path):
    """Hash the inputs that affect the rendered PDF (read fresh from disk).

    Covers the frontmatter fields pandoc uses (version via its canonical form)
    plus the body — deliberately NOT `description`/`image`, which are SEO-only.
    """
    lines = open(path, encoding="utf-8").read().split("\n")
    end = lines.index("---", 1)
    meta = yaml.safe_load("\n".join(lines[1:end])) or {}
    body = "\n".join(lines[end + 1:])
    ver = normalize_version(meta["version"]) if meta.get("version") is not None else ""
    fields = [str(meta.get(k, "")) for k in
              ("title", "author", "authors", "keywords", "item_id", "date", "revision_date")]
    return hashlib.sha256(("\x1f".join(fields + [ver]) + "\x1e" + body).encode()).hexdigest()


def load_manifest():
    try:
        return json.load(open(MANIFEST, encoding="utf-8"))
    except FileNotFoundError:
        return {}


def save_manifest():
    data = {it.url[:-3]: pdf_input_hash(it.path) for it in internal_items()}
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")


def run(label, args):
    """Run a toolkit script; print its output under `label`; return its rc."""
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, args[0]), *args[1:]],
                       cwd=repo_root, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    status = "ok" if r.returncode == 0 else "FAILED"
    print(f"  [{status}] {label}")
    if out and (r.returncode != 0 or args[0] in ("make_cards.py", "build_pdfs.py")):
        print("\n".join("       " + ln for ln in out.splitlines()[-12:]))
    return r.returncode


def set_field(path, key, value):
    """Set/replace a single-line frontmatter field; return True if changed."""
    lines = open(path, encoding="utf-8").read().split("\n")
    end = lines.index("---", 1)
    fm = lines[1:end]
    new = f"{key}: {value}"
    idx = next((i for i, l in enumerate(fm) if l.startswith(key + ":")), None)
    if idx is not None and fm[idx] == new:
        return False
    if idx is not None:
        fm[idx] = new
    else:
        fm.append(new)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(["---"] + fm + lines[end:]))
    return True


def normalize_versions():
    """Store every existing `version` as a quoted MAJOR.MINOR string."""
    changed = [it.url for it in internal_items()
               if it.meta.get("version") is not None
               and set_field(it.path, "version", f'"{normalize_version(it.meta["version"])}"')]
    if changed:
        print(f"  normalized version format on {len(changed)} doc(s)")


def revise(slugs, major, today):
    by_url = {it.url: it for it in internal_items()}
    for slug in slugs:
        url = slug if slug.endswith(".md") else slug + ".md"
        it = by_url.get(url)
        if it is None:
            sys.exit(f"--revise: no such document '{slug}'")
        new = bump_version(it.meta.get("version"), major=major)
        set_field(it.path, "version", f'"{new}"')
        set_field(it.path, "revision_date", today)
        kind = "major" if major else "minor"
        print(f"  revised {url}: version -> {new} ({kind}), revision_date -> {today}")


def stale_pdf_slugs(mode, manifest):
    if mode == "none":
        return []
    out = []
    for it in internal_items():
        slug = it.url[:-3]
        pdf = os.path.join(repo_root, slug + ".pdf")
        if (mode == "all" or not os.path.isfile(pdf)
                or manifest.get(slug) != pdf_input_hash(it.path)):
            out.append(slug)
    return out


def changed_docs():
    r = subprocess.run(["git", "diff", "--name-only", "--", "*.md"],
                       cwd=repo_root, capture_output=True, text=True)
    metas = {os.path.basename(it.url) for it in internal_items()}
    return [f for f in r.stdout.split() if os.path.basename(f) in metas]


def validate():
    """Run the read-only guards + tests; return overall ok."""
    mds = sorted(os.path.basename(p) for p in glob.glob(os.path.join(repo_root, "*.md")))
    print("validate:")
    rcs = [
        run("metadata schema + PDF/card present", ["validate_metadata.py"]),
        run("descriptions in sync", ["sync_descriptions.py", "--check-only"]),
        run("social cards present", ["make_cards.py", "--check-only"]),
        run("index up to date", ["generate_index.py", "--check-only"]),
        run("reference numbering", ["fix_ref_nums.py", "--check-only",
                                    "--except", ".hyperlinks-only", *mds]),
    ]
    pt = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=repo_root,
                        capture_output=True, text=True)
    print(f"  [{'ok' if pt.returncode == 0 else 'FAILED'}] pytest")
    if pt.returncode:
        print("\n".join("       " + ln for ln in pt.stdout.splitlines()[-15:]))
    return all(rc == 0 for rc in rcs) and pt.returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--revise", nargs="*", metavar="SLUG",
                    help="Bump version (minor) on these docs; no slug = list changed docs.")
    ap.add_argument("--major", action="store_true", help="With --revise: bump the major version.")
    ap.add_argument("--pdfs", choices=["stale", "all", "none"], default="stale")
    ap.add_argument("--check", action="store_true", help="Validate only; change nothing.")
    args = ap.parse_args()
    today = datetime.date.today().isoformat()

    if args.check:
        ok = validate()
        print("\n" + ("All checks passed — ready to commit." if ok
                      else "Problems above — fix, then re-run `publish.py`."))
        sys.exit(0 if ok else 1)

    if args.revise is not None and len(args.revise) == 0:
        cd = changed_docs()
        print("Documents with uncommitted changes (name them to --revise):")
        print("  " + (", ".join(c[:-3] for c in cd) if cd else "(none)"))
        return

    print("regenerate:")
    normalize_versions()
    if args.revise:
        revise(args.revise, args.major, today)
    run("social cards", ["make_cards.py"])
    run("descriptions <- abstracts", ["sync_descriptions.py"])
    run("index.md", ["generate_index.py"])
    stale = stale_pdf_slugs(args.pdfs, load_manifest())
    if stale:
        print(f"  rebuilding {len(stale)} PDF(s): {', '.join(stale)}")
        run("PDFs", ["build_pdfs.py", "--out", ".", "--only", *stale])
    else:
        print("  PDFs up to date")
    save_manifest()  # record current inputs so unchanged docs aren't rebuilt next time

    print()
    ok = validate()

    print("\n" + "=" * 60)
    gs = subprocess.run(["git", "status", "--short"], cwd=repo_root,
                        capture_output=True, text=True).stdout.strip()
    if not ok:
        print("NOT ready: fix the problems above, then re-run `python scripts/publish.py`.")
        sys.exit(1)
    if not gs:
        print("Everything is up to date and valid. Nothing to commit.")
        return
    print("Ready to publish. Review and commit:\n")
    print(gs)
    print("\n  git add -A && git commit -s -m \"<message>\" && git push")


if __name__ == "__main__":
    main()
