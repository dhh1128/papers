"""Validate every document's frontmatter against the docs/conventions.md schema.

Tiers:
  ERROR (fails CI): title, date, category, item_id, abstract, keywords,
    author/authors. Papers + Specifications additionally require version +
    revision_date.
  WARN  (advisory): none currently. (abstract/keywords graduated from WARN to
    ERROR once the Phase 2 backfill completed.)

Run `validate_metadata.py --report` for a per-field coverage punch-list.
"""
import argparse
import os
import sys

import archive
from archive import (internal_items, external_items, indexed_items, cat_index,
                     complain, exit_with_status, repo_root)

CORE_REQUIRED = ['title', 'date', 'category', 'item_id', 'abstract', 'keywords']
SOFT_REQUIRED = []                             # (abstract/keywords graduated to ERROR)
VERSIONED_CATS = {'Papers', 'Specifications'}  # require version + revision_date
EXTERNAL_REQUIRED = ['category', 'title', 'date']


def has_author(meta):
    return bool(meta.get('author') or meta.get('authors'))


def field_problems(meta):
    """Return (errors, warnings) for one internal document's metadata.

    Pure function over a dict so it is unit-testable without the filesystem.
    """
    errors = [f"missing required field '{f}'"
              for f in CORE_REQUIRED if not meta.get(f)]
    if not has_author(meta):
        errors.append("missing required field 'author'/'authors'")
    cat = str(meta.get('category', ''))
    if cat in VERSIONED_CATS:
        for f in ('version', 'revision_date'):
            if not meta.get(f):
                errors.append(f"{cat} requires '{f}'")
    warnings = [f"missing field '{f}'" for f in SOFT_REQUIRED if not meta.get(f)]
    return errors, warnings


def report():
    """Print a per-field coverage punch-list. Never fails (exit 0)."""
    docs = sorted(internal_items(), key=lambda i: i.url)
    n = len(docs)
    fields = CORE_REQUIRED + ['author/authors'] + SOFT_REQUIRED + ['version', 'revision_date']
    print(f"Metadata coverage — {n} internal documents\n")
    for f in fields:
        if f == 'author/authors':
            missing = [i.url for i in docs if not has_author(i.meta)]
        else:
            missing = [i.url for i in docs if not i.meta.get(f)]
        tag = 'complete' if not missing else f"missing {len(missing)}"
        print(f"  {f:16} {tag}")
        if missing:
            print(f"        {', '.join(m[:-3] for m in missing)}")
    print("\n(version/revision_date are required only for Papers + Specifications.)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', action='store_true',
                        help='Print a coverage punch-list and exit 0 (no enforcement).')
    parser.add_argument('--check-only', action='store_true',
                        help='Accepted for CI symmetry; this tool never mutates files.')
    args = parser.parse_args()

    if args.report:
        report()
        exit_with_status()
        return

    # 1. Every internal document referenced by the index must exist on disk.
    for item in indexed_items():
        if not item.is_external and not os.path.isfile(item.path):
            complain(f"Indexed file missing: {item.url}")
    # 2. Internal documents: full schema.
    for item in internal_items():
        meta = item.meta
        if not meta:
            complain(f"Could not load metadata for: {item.url}")
            continue
        errors, warnings = field_problems(meta)
        for e in errors:
            complain(f"{item.url}: {e}")
        for w in warnings:
            complain(f"{item.url}: {w}", update_exit_code=False)
        # Every document must ship a committed PDF (served at /papers/<slug>.pdf).
        pdf = os.path.join(repo_root, item.url[:-3] + '.pdf')
        if not os.path.isfile(pdf):
            complain(f"{item.url}: missing committed PDF ({item.url[:-3]}.pdf) — "
                     f"run `python scripts/build_pdfs.py --out .`")
    # 3. External items: must carry enough to render in the index.
    for item in external_items():
        miss = [f for f in EXTERNAL_REQUIRED if not item.meta.get(f)]
        if miss:
            complain(f"{item.url}: external item missing {', '.join(miss)}")

    exit_with_status("All metadata requirements met.")


if __name__ == '__main__':
    main()
