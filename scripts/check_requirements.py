import os
import sys

import archive
from archive import (internal_items, indexed_items, cat_index, complain,
                     exit_with_status)

PAPER_CAT = cat_index('Papers')

# Hard requirements for a Papers-category document. CI fails if any is absent.
PAPER_REQUIRED = ['title', 'date', 'abstract', 'item_id', 'category']

# Recommended fields: surfaced as warnings, do not fail CI (yet).
#   - pdf_url is becoming a CI-built artifact (see ROADMAP Phase 3), so it is
#     not hard-required during the transition.
#   - author/authors is checked specially (either form satisfies it).
PAPER_RECOMMENDED = ['pdf_url', 'keywords']


def has_author(meta):
    return bool(meta.get('author') or meta.get('authors'))


def paper_problems(meta):
    """Return (errors, warnings) for a Papers-category metadata dict.

    Pure function over a meta dict so it is unit-testable without touching the
    filesystem. ``errors`` fail CI; ``warnings`` are advisory.
    """
    errors = [f"missing required field '{f}'"
              for f in PAPER_REQUIRED if not meta.get(f)]
    warnings = []
    if not has_author(meta):
        warnings.append("no author/authors (recommended)")
    warnings += [f"missing recommended field '{f}'"
                 for f in PAPER_RECOMMENDED if not meta.get(f)]
    return errors, warnings


def check_internal(item):
    """Validate one internal document against its REAL frontmatter."""
    meta = item.meta
    if not meta:
        complain(f"Could not load metadata for: {item.url}")
        return
    if cat_index(str(meta.get('category', ''))) != PAPER_CAT:
        return
    errors, warnings = paper_problems(meta)
    for e in errors:
        complain(f"{item.url}: {e}")
    for w in warnings:
        complain(f"{item.url}: {w}", update_exit_code=False)


def main():
    # 1. Every internal document referenced by the index must exist on disk.
    for item in indexed_items():
        if not item.is_external and not os.path.isfile(item.path):
            complain(f"Indexed file missing: {item.url}")
    # 2. Every internal document must parse; Papers must meet their field reqs.
    for item in internal_items():
        check_internal(item)
    exit_with_status("All requirements met.")


if __name__ == '__main__':
    main()
