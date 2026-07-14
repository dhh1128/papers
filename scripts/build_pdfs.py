"""Build a PDF for every internal document into .build.tmp/pdfs/ (gitignored).

This is the CI gate that proves the whole corpus is renderable: it exits nonzero
if any document fails to build. Build a single document instead with:
    python scripts/pandoc.py <slug>.md
"""
import argparse
import os
import sys

import archive
from archive import internal_items, repo_root, complain, exit_with_status
import pandoc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', default=os.path.join(repo_root, '.build.tmp', 'pdfs'),
                        help='Output directory (default: .build.tmp/pdfs).')
    parser.add_argument('--only', nargs='*',
                        help='Limit to these slugs (e.g. --only kspqs 3dim).')
    args = parser.parse_args()

    items = sorted(internal_items(), key=lambda i: i.url)
    if args.only:
        want = {s if s.endswith('.md') else s + '.md' for s in args.only}
        items = [i for i in items if i.url in want]

    built = 0
    for it in items:
        rc, log, out = pandoc.build_pdf(it, args.out)
        if rc:
            complain(f"FAIL  {it.url} (pandoc exit {rc})")
            sys.stderr.write(log[-1500:].rstrip() + '\n')
        else:
            built += 1
            print(f"ok    {it.url} -> {os.path.relpath(out, repo_root)}")
    print(f"\nBuilt {built}/{len(items)} PDFs into {os.path.relpath(args.out, repo_root)}.")
    exit_with_status()


if __name__ == '__main__':
    main()
