"""Generate the vendored documents that are build artifacts of a sibling repo.

Most vendored sources in this archive are copies (`.vendored-sources.yml` pins
the upstream hash and ``check_drift.py`` reports when upstream runs ahead). A
copy can only ever *detect* drift, and only in one direction: the pin is of the
upstream file, so an edit made **here** is invisible to it. `amp-diff.md` and
its upstream had in fact diverged in three places while the guard read "in sync".

A *generated* entry closes that hole by construction. This script reads the
upstream file, applies the transform declared in `.vendored-transforms.yml`, and
writes the local copy. Reverse drift becomes impossible rather than merely
detected: a hand edit here is reverted by the next ``publish.py`` and fails CI.

The transform is small and every step is asserted, so nothing is lost silently:

  * the upstream title/author block is dropped and this archive's frontmatter
    kept (the shape of the block must match, or the build fails);
  * figure paths are rewritten upstream-SVG -> published-PNG, with an expected
    substitution count and an existence check on every image target;
  * declared `overrides` replace passages this archive publishes differently —
    each must match its upstream text exactly once, so an upstream rewrite of
    the same passage is a build failure, not a silent discard;
  * references are renumbered in order of first citation, which is what keeps
    ``fix_ref_nums.py --check-only`` green without a human touching the file.

Usage::

    python scripts/generate_vendored.py                  # regenerate
    python scripts/generate_vendored.py --check-only      # CI guard; mutates nothing
    python scripts/generate_vendored.py --only amp-diff.md
    python scripts/generate_vendored.py --upstream-root _upstream --require-upstream

A sibling repo that is not checked out is SKIPPED with a visible notice, as in
``check_drift.py`` — except under ``--require-upstream``, which CI passes so a
mis-wired checkout fails loudly instead of vacuously passing.
"""
import argparse
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archive  # noqa: E402
import fix_ref_nums  # noqa: E402
import yaml  # noqa: E402

TRANSFORMS = os.path.join(archive.repo_root, ".vendored-transforms.yml")

FRONTMATTER_PAT = re.compile(r"\A---\n.*?\n---\n", re.S)
# The upstream title block: an H1 title, an H2 author, an H2 email, then a rule.
TITLE_BLOCK_PAT = re.compile(r"\A# [^\n]+\n\n## [^\n]+\n\n## [^\n]+\n\n---\n\n")
IMAGE_PAT = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def load_transforms(path=TRANSFORMS):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("transforms", [])


def upstream_dir(t, root, upstream_root):
    """Where this entry's sibling repo lives.

    Normally `upstream_repo` is a path relative to the archive root (`../entviz`).
    `--upstream-root DIR` instead resolves the sibling by its basename under DIR,
    for CI, where a second `actions/checkout` must land inside the workspace.
    """
    if upstream_root:
        return os.path.join(upstream_root, os.path.basename(t["upstream_repo"].rstrip("/")))
    return os.path.join(root, t["upstream_repo"])


def frontmatter_of(text):
    m = FRONTMATTER_PAT.match(text)
    return m.group(0) if m else None


def _substitute(text, spec_version):
    return text.replace("${spec_version}", spec_version or "")


def render(t, upstream_text, frontmatter, label):
    """Apply the declared transform. Returns the generated text, or None on error.

    Pure: no filesystem, no globals besides `archive.complain` for diagnostics.
    """
    body = upstream_text
    spec_version = str(t.get("spec_version", ""))

    if t.get("strip_title_block"):
        m = TITLE_BLOCK_PAT.match(body)
        if not m:
            archive.complain(
                f"{label}: upstream no longer opens with the expected "
                f"title/author/email block — the transform would lose or keep the "
                f"wrong heading. Reconcile by hand, then update "
                f"strip_title_block handling.")
            return None
        body = body[m.end():]

    for rw in t.get("rewrites", []):
        body, n = re.subn(rw["pattern"], rw["replacement"], body)
        expect = rw.get("expect")
        if expect is not None and n != expect:
            archive.complain(
                f"{label}: rewrite '{rw['id']}' matched {n} time(s), expected "
                f"{expect}. Upstream added or removed something the transform "
                f"maps; update `expect` once you have checked what changed.")
            return None

    for ov in t.get("overrides", []):
        old = _substitute(ov["old"], spec_version)
        new = _substitute(ov["new"], spec_version)
        n = body.count(old)
        if n != 1:
            archive.complain(
                f"{label}: override '{ov['id']}' matched {n} time(s) in upstream, "
                f"expected exactly 1. Upstream probably rewrote the passage this "
                f"archive publishes differently — reconcile the two, do not "
                f"loosen the match.")
            return None
        body = body.replace(old, new)

    out = frontmatter + body

    if t.get("renumber_refs"):
        out = fix_ref_nums.renumber(out, label, verbose=False)

    return out


def check_image_targets(t, text, root, label):
    """Every image the generated document points at must exist in this archive."""
    missing = sorted({p for p in IMAGE_PAT.findall(text)
                      if not p.startswith(("http://", "https://", "data:", "#"))
                      and not os.path.exists(os.path.join(root, p.lstrip("/")))})
    for p in missing:
        archive.complain(f"{label}: generated document references a missing image: {p}")


def spec_version_advisory(t, up_dir, label):
    """Note when upstream's SPEC_VERSION has moved past the version [8] cites.

    Advisory only. A published paper analyzes the spec revision it was written
    against and may deliberately lag; bumping the citation is an editorial act.
    """
    src = t.get("spec_version_source")
    if not src or not t.get("spec_version"):
        return
    path = os.path.join(up_dir, src["path"])
    try:
        with open(path, "r", encoding="utf-8") as f:
            m = re.search(src["pattern"], f.read())
    except OSError:
        return
    if m and m.group(1) != str(t["spec_version"]):
        print(f"NOTE  {label}: cites spec version {t['spec_version']}; upstream is "
              f"now at {m.group(1)}. Deliberate lag is fine — bump `spec_version` "
              f"in .vendored-transforms.yml when you re-vendor against the newer "
              f"spec, and `publish.py --revise` the paper.")


def process(t, root, upstream_root, check_only, require_upstream):
    label = t["local"]
    up_dir = upstream_dir(t, root, upstream_root)
    up_file = os.path.join(up_dir, t["upstream_path"])
    local_file = os.path.join(root, label)

    if not os.path.exists(up_file):
        msg = (f"{label}: upstream {t['upstream_repo']}/{t['upstream_path']} not "
               f"checked out — cannot regenerate")
        if require_upstream:
            archive.complain(f"MISSING {msg} (--require-upstream)")
        else:
            print(f"SKIP  {msg}")
        return

    if not os.path.exists(local_file):
        archive.complain(f"{label}: the local copy is missing; nothing to take "
                         f"frontmatter from. Restore it from git, then regenerate.")
        return

    current = open(local_file, encoding="utf-8").read()
    frontmatter = frontmatter_of(current)
    if frontmatter is None:
        archive.complain(f"{label}: no YAML frontmatter to preserve. The generator "
                         f"keeps this archive's frontmatter and replaces only the body.")
        return

    with open(up_file, encoding="utf-8") as f:
        upstream_text = f.read()

    out = render(t, upstream_text, frontmatter, label)
    if out is None:
        return
    check_image_targets(t, out, root, label)
    spec_version_advisory(t, up_dir, label)

    if out == current:
        print(f"ok    {label}: regenerates identically from "
              f"{t['upstream_repo']}/{t['upstream_path']}")
        return
    if check_only:
        diff = list(difflib.unified_diff(
            current.splitlines(True), out.splitlines(True),
            fromfile=f"{label} (committed)", tofile=f"{label} (regenerated)", n=0))
        archive.complain(
            f"STALE {label}: does not match what the transform produces from "
            f"{t['upstream_repo']}/{t['upstream_path']}.\n"
            f"      -> python scripts/generate_vendored.py\n"
            + "".join("      " + ln for ln in diff[:40]).rstrip())
        return
    with open(local_file, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {label} from {t['upstream_repo']}/{t['upstream_path']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check-only", action="store_true",
                    help="CI guard: exit nonzero if a local copy differs from what "
                         "the transform produces. Mutates nothing.")
    ap.add_argument("--only", metavar="LOCAL", action="append",
                    help="Restrict to this local path (repeatable).")
    ap.add_argument("--transforms", default=TRANSFORMS,
                    help="Transform declarations (default: %(default)s).")
    ap.add_argument("--root", default=archive.repo_root,
                    help="Archive root (default: the repo this script lives in).")
    ap.add_argument("--upstream-root", metavar="DIR",
                    help="Resolve each sibling by basename under DIR instead of by "
                         "its `upstream_repo` path. For CI, where the sibling is "
                         "checked out inside the workspace.")
    ap.add_argument("--require-upstream", action="store_true",
                    help="Fail instead of skipping when a sibling is not checked out.")
    args = ap.parse_args(argv)

    transforms = load_transforms(args.transforms)
    if args.only:
        wanted = set(args.only)
        transforms = [t for t in transforms if t["local"] in wanted]
        for name in sorted(wanted - {t["local"] for t in transforms}):
            archive.complain(f"--only {name}: no such transform in {args.transforms}")

    for t in transforms:
        process(t, args.root, args.upstream_root, args.check_only, args.require_upstream)

    archive.exit_with_status(f"generated sources: {len(transforms)} checked")
    return archive.exit_code


if __name__ == "__main__":
    main()
