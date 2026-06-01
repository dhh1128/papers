"""Scaffold a new archive document with complete, schema-valid frontmatter.

Mints the next item_id (see archive.next_item_id), writes `<slug>.md` with every
required field populated, and reminds you to replace the `abstract`/`keywords`
placeholders. The goal is that authoring *produces* schema-valid documents rather
than relying on CI (validate_metadata.py) to reject invalid ones.

Usage:
  python scripts/new_doc.py --title "My Title" --category Papers
  python scripts/new_doc.py --title "..." --category Primers --date 2026-06-01 --slug my-slug

After it runs, fill in the body and replace the TODO abstract/keywords, then:
  python scripts/validate_metadata.py
"""
import argparse
import datetime
import os
import re
import sys

import archive
from archive import next_item_id, categories, repo_root

DEFAULT_AUTHOR = "Daniel Hardman"
VERSIONED_CATS = {"Papers", "Specifications"}  # require version + revision_date


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def canonical_category(name):
    """Return the exact MECE category name matching `name` (by 3-char prefix), or None."""
    for c in categories():
        if c.lower()[:3] == name.lower()[:3]:
            return c
    return None


def frontmatter_stub(title, category, date, item_id, author=DEFAULT_AUTHOR):
    """Return the YAML frontmatter (with `---` fences) for a new document.

    abstract/keywords are non-empty TODO placeholders, so the stub is
    schema-valid; the author replaces them with real content.
    """
    lines = ["---",
             f'title: "{title}"',
             f'author: "{author}"',
             f"date: {date}",
             f"category: {category}",
             f"item_id: {item_id}",
             'language: "en"']
    if category in VERSIONED_CATS:
        lines += ["version: 1.0", f"revision_date: {date}"]
    lines += ['keywords: "TODO, replace, with, real, keywords"',
              "abstract: |",
              "  TODO: one-paragraph summary of purpose, scope, and result. Replace before publishing.",
              "---",
              ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Scaffold a new archive document.")
    p.add_argument("--title", required=True)
    p.add_argument("--category", required=True, help="One MECE category (see about.md).")
    p.add_argument("--date", default=None, help="ISO YYYY-MM-DD (default: today).")
    p.add_argument("--slug", default=None, help="Filename without .md (default: from title).")
    p.add_argument("--author", default=DEFAULT_AUTHOR)
    args = p.parse_args()

    category = canonical_category(args.category)
    if not category:
        sys.exit(f"Unknown category '{args.category}'. Valid: {', '.join(categories())}")
    date = args.date or datetime.date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        sys.exit(f"--date must be ISO YYYY-MM-DD, got '{date}'")
    slug = args.slug or slugify(args.title)
    path = os.path.join(repo_root, slug + ".md")
    if os.path.exists(path):
        sys.exit(f"Refusing to overwrite existing file: {slug}.md")

    item_id = next_item_id(category, date)
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter_stub(args.title, category, date, item_id, args.author))

    print(f"Created {slug}.md  (item_id {item_id}, category {category})")
    print("NEXT: write the body, then replace the TODO 'abstract' and 'keywords'.")
    print("Verify with: python scripts/validate_metadata.py")


if __name__ == "__main__":
    main()
