"""Drift guard: fail when a vendored upstream source no longer matches its pin.

A few documents and figures in this archive are *vendored* — copied in from
sibling repos (``../entviz``, ``../entviz-adversarial``) and then published here
as self-contained, citable works. Publication is self-contained on purpose, but
the upstream can move ahead. ``.vendored-sources.yml`` is the provenance ledger:
each entry pins the ``sha256`` of the upstream file as it was at vendoring time.

This guard recomputes the current upstream hash and compares:

  * **fail** severity (the papers and their figures) — a divergence is a hard
    error, so CI / ``publish.py --check`` catches an upstream that ran ahead of
    the published copy. Resolving the drift means reconciling the change here
    (errata — bump the version via ``publish.py --revise``) and then re-pinning.
  * **warn** severity (the spec) — the papers analyze a pinned spec version and
    may intentionally lag a newer one, so a divergence is advisory only.

A sibling repo that is not checked out (e.g. in cloud PR CI) is **skipped** with
a visible notice — never a silent pass. The guard is therefore most useful on an
author's machine (and in a scheduled job that fetches the siblings); see
AGENTS.md.

Usage::

    python scripts/check_drift.py                 # report drift (human-readable)
    python scripts/check_drift.py --check-only     # identical; the CI-guard form
    python scripts/check_drift.py --repin          # re-pin every hash to current
                                                   #   upstream (AFTER reconciling)

``--repin`` only updates the pins; it never touches the vendored copies. The
workflow is report-and-repin: review the upstream diff, reconcile the prose by
hand (respecting propose-don't-silently-edit), then re-pin.
"""
import argparse
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archive  # noqa: E402
import yaml  # noqa: E402

LEDGER = os.path.join(archive.repo_root, ".vendored-sources.yml")

_HEADER = """\
# Provenance ledger for vendored upstream sources (the "drift guard").
#
# Each entry is an artifact copied in from a sibling repo and published here as a
# self-contained work. `sha256` pins the UPSTREAM file at vendoring time;
# scripts/check_drift.py fails (severity: fail) or warns (severity: warn) when the
# current upstream no longer matches. Regenerate the pins with:
#   python scripts/check_drift.py --repin
# Managed by check_drift.py — comments above the `sources:` key are preserved.
"""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_ledger(path=LEDGER):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("sources", [])


def _upstream_abspath(entry, root):
    return os.path.join(root, entry["upstream_repo"], entry["upstream_path"])


def entry_status(entry, root):
    """Classify one ledger entry against the current filesystem.

    Returns one of: ``ok``, ``drift``, ``skip-upstream`` (sibling not checked
    out), or ``missing-local`` (the vendored copy that should live here is gone).
    """
    local = entry.get("local")
    if local and not local.startswith("("):
        if not os.path.exists(os.path.join(root, local)):
            return "missing-local"
    upstream = _upstream_abspath(entry, root)
    if not os.path.exists(upstream):
        return "skip-upstream"
    return "ok" if sha256_file(upstream) == entry.get("sha256") else "drift"


def _label(entry):
    return entry.get("local") or f"{entry['upstream_repo']}/{entry['upstream_path']}"


def repin(ledger_path, root):
    with open(ledger_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    changed = 0
    for entry in data.get("sources", []):
        upstream = _upstream_abspath(entry, root)
        if not os.path.exists(upstream):
            print(f"  skip (sibling absent): {_label(entry)}")
            continue
        new = sha256_file(upstream)
        if new != entry.get("sha256"):
            print(f"  re-pinned {_label(entry)}: {str(entry.get('sha256'))[:8]} -> {new[:8]}")
            entry["sha256"] = new
            changed += 1
    with open(ledger_path, "w", encoding="utf-8") as f:
        f.write(_HEADER)
        yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False,
                       allow_unicode=True)
    print(f"re-pinned {changed} source(s)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check-only", action="store_true",
                    help="CI-guard form (exit nonzero on fail-severity drift). "
                         "Identical to the default behaviour; nothing is mutated.")
    ap.add_argument("--repin", action="store_true",
                    help="Re-pin every hash to the current upstream, then exit.")
    ap.add_argument("--ledger", default=LEDGER, help="Ledger path (default: %(default)s).")
    ap.add_argument("--root", default=archive.repo_root,
                    help="Root the upstream_repo paths resolve against.")
    args = ap.parse_args(argv)

    if args.repin:
        repin(args.ledger, args.root)
        return 0

    sources = load_ledger(args.ledger)
    ok = warned = skipped = 0
    for entry in sources:
        status = entry_status(entry, args.root)
        label = _label(entry)
        severity = entry.get("severity", "fail")
        if status == "ok":
            ok += 1
        elif status == "skip-upstream":
            skipped += 1
            print(f"SKIP  {label}: sibling {entry['upstream_repo']} not checked out "
                  f"— drift unchecked")
        elif status == "missing-local":
            archive.complain(f"DRIFT {label}: the vendored copy is missing from this repo")
        else:  # drift
            pin = str(entry.get("sha256") or "")[:8]
            cur = sha256_file(_upstream_abspath(entry, args.root))[:8]
            up = f"{entry['upstream_repo']}/{entry['upstream_path']}"
            base = (f"{label}: upstream {up} changed since vendoring "
                    f"(pinned {pin} != current {cur})")
            if severity == "warn":
                warned += 1
                print(f"WARN  {base} — advisory; re-pin once you've confirmed the "
                      f"published analysis still holds")
            else:
                archive.complain(
                    f"DRIFT {base}\n      -> reconcile the change here (errata: "
                    f"publish.py --revise), then: python scripts/check_drift.py --repin")
    archive.exit_with_status(
        f"drift guard: {ok} in sync, {warned} warned, {skipped} skipped")
    return archive.exit_code


if __name__ == "__main__":
    main()
