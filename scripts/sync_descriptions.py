"""Keep each document's `description` in sync with its `abstract`.

jekyll-seo-tag emits the HTML `<meta name="description">` / `og:description` from
`page.description`, which our docs don't otherwise set — so without this they all
share the generic site tagline. We mirror the abstract (collapsed to one line)
into a `description` field so every page gets a unique, meaningful snippet.

Default: write/update `description` on every document.
`--check-only`: exit nonzero if any document's description is missing or stale
(the CI guard) — re-run without the flag to fix.
"""
import argparse
import json

from archive import internal_items, complain, exit_with_status


def normalized(text):
    return ' '.join(str(text).split())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check-only', action='store_true',
                    help='Report drift without writing (for CI).')
    args = ap.parse_args()

    for item in internal_items():
        abstract = item.meta.get('abstract')
        if not abstract:
            continue
        want = normalized(abstract)
        have = item.meta.get('description')
        if have is not None and normalized(have) == want:
            continue
        if args.check_only:
            complain(f"{item.url}: 'description' missing or out of sync with 'abstract'")
            continue
        text = open(item.path, encoding='utf-8').read()
        lines = text.split('\n')
        end = lines.index('---', 1)              # closing frontmatter fence
        fm = lines[1:end]
        new_line = 'description: ' + json.dumps(want, ensure_ascii=False)
        idx = next((i for i, l in enumerate(fm) if l.startswith('description:')), None)
        if idx is not None:
            fm[idx] = new_line
        else:
            fm.append(new_line)
        with open(item.path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(['---'] + fm + lines[end:]))
        print(f"synced description: {item.url}")

    exit_with_status("Descriptions in sync." if args.check_only else None)


if __name__ == '__main__':
    main()
