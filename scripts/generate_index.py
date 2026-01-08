import os
import sys
import re
import yaml  # Requires PyYAML

def get_categories_from_policy(policy_path):
    cats = []
    dt_re = re.compile(r'<dt(?:\s+class="[^"]*")?>([^<]+)</dt>', re.IGNORECASE)
    with open(policy_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = dt_re.search(line)
            if m:
                cat = m.group(1).strip()
                if cat:
                    cats.append(cat)
    return cats


def get_yaml_front_matter(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines or not lines[0].startswith('---'):
        return {}
    yaml_lines = []
    for line in lines[1:]:
        if line.startswith('---'):
            break
        yaml_lines.append(line)
    yaml_str = ''.join(yaml_lines)
    try:
        data = yaml.safe_load(yaml_str)
        if isinstance(data, dict):
            return {k.lower(): v for k, v in data.items()}
        else:
            return {}
    except Exception as e:
        sys.stderr.write(f'YAML parse error in {md_path}: {e}\n')
        return {}


def get_external_items(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return {}, []
    pdf_meta = {}
    external_list = []
    # PDF keys
    for k, v in data.items():
        if isinstance(k, int): continue
        if k.endswith('.pdf') and isinstance(v, list):
            meta = {item_key: item_val for d in v for item_key, item_val in d.items()}
            pdf_meta[k] = meta
    # Numeric keys for external links
    i = 1
    while i in data:
        v = data[i]
        if isinstance(v, list):
            meta = {item_key: item_val for d in v for item_key, item_val in d.items()}
            if all(x in meta for x in ('category', 'title', 'date', 'url')):
                external_list.append(meta)
        i += 1
    return pdf_meta, external_list


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    policy_path = os.path.join(repo_root, 'about.md')
    external_yaml_path = os.path.join(repo_root, 'external-items.yaml')
    cat_list = get_categories_from_policy(policy_path)
    folded_cat_list = [cat.casefold() for cat in cat_list]
    articles_by_cat = [[] for cat in cat_list]
    bad_list = []
    # Markdown articles
    for fname in os.listdir(repo_root):
        if not fname.endswith('.md') or fname == 'index.md':
            continue
        md_path = os.path.join(repo_root, fname)
        yaml = get_yaml_front_matter(md_path)
        cat = str(yaml.get('category', '')).casefold()
        if cat:
            title = str(yaml.get('title', fname))
            date = str(yaml.get('date', ''))
            try:
                i = folded_cat_list.index(cat)
                articles_by_cat[i].append((fname, title, date))
            except ValueError:
                bad_list.append((fname, cat))
    # PDF articles from external-items.yaml
    pdf_meta, external_list = get_external_items(external_yaml_path)
    for fname in os.listdir(repo_root):
        if not fname.endswith('.pdf'):
            continue
        if fname in pdf_meta:
            meta = pdf_meta[fname]
            cat = str(meta.get('category', '')).casefold()
            title = str(meta.get('title', fname))
            date = str(meta.get('date', ''))
            try:
                i = folded_cat_list.index(cat)
                articles_by_cat[i].append((fname, title, date))
            except ValueError:
                bad_list.append((fname, cat))
        else:
            bad_list.append((fname, 'no metadata in external-items.yaml'))
    # External links from external-items.yaml
    for meta in external_list:
        cat = str(meta.get('category', '')).casefold()
        title = str(meta.get('title', ''))
        date = str(meta.get('date', ''))
        url = str(meta.get('url', ''))
        try:
            i = folded_cat_list.index(cat)
            articles_by_cat[i].append((url, title, date))
        except ValueError:
            bad_list.append((url, cat))
    if bad_list:
        sys.stderr.write('Error: Some files have bad categories:\n')
        for fname, badcat in bad_list:
            sys.stderr.write(f'  {fname}: {badcat}\n')
        sys.exit(1)
    # Write index.md
    index_path = os.path.join(repo_root, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as idx:
        idx.write("""---
author: "Daniel Hardman"
language: "en"
publisher: "Codecraft"
journal_title: "Codecraft Papers"
layout: meta
---

[About This Archive](about.md)
""")
        for i, cat in enumerate(cat_list):
            idx.write(f'\n## {cat}\n')
            articles = sorted(articles_by_cat[i], key=lambda tup: tup[1].casefold())
            for url, title, date in articles:
                idx.write(f'- [{title}]({url}) ({date})\n')

if __name__ == '__main__':
    main()
