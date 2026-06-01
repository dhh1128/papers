import os
import sys
import argparse
import io

import archive
from archive import *

def categorize(item, articles_by_cat):
    i = cat_index(item.meta.get('category'))
    if i == -1:
        complain(f"Bad category, {item.meta.get('category')}, for {item.url}.")
    articles_by_cat[i].append(item)


def write_index(articles_by_cat, check_only=False):
    index_path = os.path.join(repo_root, 'index.md')
    buf = io.StringIO()
    buf.write("""---
author: "Daniel Hardman"
language: "en"
publisher: "Codecraft"
journal_title: "Codecraft Papers"
layout: meta
---

[About This Archive](about.md)
""")
    for i, cat in enumerate(categories()):
        buf.write(f'\n## {cat}\n')
        try:
            articles = sorted(articles_by_cat[i], key=lambda x: x.meta.get('date'), reverse=True)
        except TypeError as e:
            missing = [x.url for x in articles_by_cat[i] if x.meta.get('date') is None]
            sys.exit(f"Sort failed for category '{cat}' — missing date in: {missing}. ({e})")
        for item in articles:
            buf.write(f'- [{item.meta.get("title")}]({item.url}) ({item.meta.get("date")})\n')
    new_content = buf.getvalue()
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
    else:
        old_content = ''
    if new_content == old_content:
        print("Index is up to date.")
    else:
        if check_only:
            print("Index is out of date.")
        else:
            with open(index_path, 'w', encoding='utf-8') as idx:
                idx.write(new_content)
            print("Index updated.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true', help='Only check, do not write index.md')
    args = parser.parse_args()
    articles_by_cat = [[] for _ in categories()]
    for item in internal_items():
        try:
            categorize(item, articles_by_cat)
        except Exception as e:
            sys.exit(f"Error processing {item.url}: {e}")
    for item in external_items():
        try:
            categorize(item, articles_by_cat)
        except Exception as e:
            sys.exit(f"Error processing {item.url}: {e}")
    # Read archive.exit_code live: a bare `exit_code` here is the stale
    # by-value import (always 0) and would mask categorization errors.
    if archive.exit_code == 0:
        write_index(articles_by_cat, check_only=args.check_only)
    sys.exit(archive.exit_code)


if __name__ == '__main__':
    main()
