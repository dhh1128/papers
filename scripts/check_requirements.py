import os
import sys
import yaml
import re

exit_code = 0
_ext_yaml_data = None

# Generator for published items in index.md
def published_items():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(repo_root, 'index.md')
    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    item_re = re.compile(r'- \[(.+?)\]\((.+?)\) \((.+?)\)')
    for line in lines:
        m = item_re.match(line.strip())
        if m:
            title, link, date = m.groups()
            yield {'title': title, 'link': link, 'date': date}

# Lazy-load external-items.yaml
def get_ext_yaml_data():
    global _ext_yaml_data
    if _ext_yaml_data is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ext_yaml_path = os.path.join(repo_root, 'external-items.yaml')
        if os.path.exists(ext_yaml_path):
            with open(ext_yaml_path, 'r', encoding='utf-8') as f:
                _ext_yaml_data = yaml.safe_load(f)
        else:
            _ext_yaml_data = {}
    return _ext_yaml_data

# Load metadata for an item
def load_metadata(item_name):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if item_name.endswith('.md'):
        md_path = os.path.join(repo_root, item_name)
        if not os.path.exists(md_path):
            return None
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if not lines or not lines[0].startswith('---'):
            return None
        yaml_lines = []
        for line in lines[1:]:
            if line.startswith('---'):
                break
            yaml_lines.append(line)
        yaml_str = ''.join(yaml_lines)
        try:
            data = yaml.safe_load(yaml_str)
            return data
        except Exception:
            return None
    ext_yaml_data = get_ext_yaml_data()
    if item_name.endswith('.pdf'):
        meta = ext_yaml_data.get(item_name)
        if meta:
            return {k: v for d in meta for k, v in d.items()}
        return None
    elif item_name.startswith('http'):
        for k in ext_yaml_data:
            if isinstance(k, int) or (isinstance(k, str) and k.isdigit()):
                meta = ext_yaml_data[k]
                for d in meta:
                    if d.get('url') == item_name:
                        return {k: v for d in meta for k, v in d.items()}
        return None
    return None

def complain(msg):
    global exit_code
    sys.stderr.write(msg + '\n')
    exit_code = 1

def check_meta(item, meta):
    """
    Checks metadata for required fields if item is of category 'Papers'.
    Complains if any required field is missing.
    """
    required_fields = ['title', 'author', 'date', 'pdf_url']
    # Accept category as either string or list
    category = meta.get('category')
    if isinstance(category, list):
        is_paper = any(c.strip().lower() == 'papers' for c in category)
    elif isinstance(category, str):
        is_paper = category.strip().lower() == 'papers'
    else:
        is_paper = False
    if is_paper:
        missing = [field for field in required_fields if not meta.get(field)]
        if missing:
            complain(f"{item['link']}: missing required metadata fields for Papers: {', '.join(missing)}")

def main():
    for item in published_items():
        link = item['link']
        if not link.startswith('http'):
            repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(repo_root, link)
            if not os.path.exists(file_path):
                complain(f"Missing file: {link}")
                continue
        meta = load_metadata(link)
        if meta is None:
            complain(f"Could not load metadata for: {link}")
        else:
            check_meta(item, meta)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
