import os
import re
import sys
import yaml

external_url_pat = re.compile('^https?://.*')
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Item:
    """
    Class representing an item in the archive.
    """
    def __init__(self, url: str, meta: dict = None):
        self.url = url
        self._meta = meta
        self._paired = None
    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.url == other.url
    def __hash__(self):
        return hash(self.url)
    @property
    def is_external(self) -> bool:
        return bool(external_url_pat.match(self.url))
    @property
    def paired_path(self) -> str:
        """For markdown files that have a corresponding .pdf, return the pdf's path."""
        if self._paired is None:
            if self.is_external:
                self._paired = ''
            else:
                self._paired = self.path[:-3] + '.pdf'
                if not os.path.isfile(self._paired):
                    self._paired = ''
        return self._paired
    @property
    def meta(self) -> dict:
        if self._meta is None:
            if self.is_external:
                data = _get_ext_yaml_data()
                for number in data:
                    meta = data[number]
                    if meta.get('url') == self.url:
                        self._meta = meta
                        break
            else:
                self._meta = load_yaml_front_matter(os.path.join(repo_root, self.url))
        return self._meta
    @property
    def path(self) -> str:
        return '' if self.is_external else os.path.join(repo_root, self.url)
    @property
    def cat_index(self):
        """
        Return the index of this item's category in about.md, or -1 if
        the category is not found.
        """
        category = self.meta.get('category')
        return cat_index(category) if category else -1

_indexed_items = None
def indexed_items():
    """
    Yield Items that have been published in index.md. The intent is for
    these to be the union of the disjoint sets, local and external.
    However, it is possible that the index includes items that don't
    exist in one of those places, or that it lacks some items that
    do exist in one of those places. The script generate_index.py
    resolves this; except when running that script, we assume this
    list is definitive."""
    index_path = os.path.join(repo_root, 'index.md')
    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    item_re = re.compile(r'- \[(.+?)\]\((.+?)\) \((.+?)\)')
    for line in lines:
        m = item_re.match(line.strip())
        if m:
            title, url, date = m.groups()
            yield Item(url, {"title": title, "date": date})

_non_articles = ['index.md', 'about.md']
_internal_items = None
def internal_items():
    """Yield Items that exist in the repo that's backing storage for the archive."""
    global _internal_items
    if _internal_items is None:
        _internal_items = []
        files = [f for f in os.listdir(repo_root) if f.endswith('.md')]
        for f in files:
            if f[0] != '.' and f not in _non_articles:
                _internal_items.append(Item(url=f))
    for item in _internal_items:
        yield item

_external_items = None
def external_items():
    """Yield Items that are declared in .external-items.yml."""
    global _external_items
    if _external_items is None:
        _external_items = []
        with open(os.path.join(repo_root, '.external-items.yml'), 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        for url, properties in data.items():
            meta = {k: v for d in properties for k, v in d.items()}
            _external_items.append(Item(url, meta))
    for item in _external_items:
        yield item

def load_yaml_front_matter(md_path) -> dict:
    """Return a dict representing the YAML front matter in a markdown file."""
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
    return yaml.safe_load(yaml_str)

_cats = None
_comparable_cats = None
def categories():
    """Generate every category declared in about.md"""
    global _cats, _comparable_cats
    if _cats is None:
        _cats = []
        dt_pat = re.compile(r'<dt(?:\s+class="[^"]*")?>([^<]+)</dt>', re.IGNORECASE)
        with open(os.path.join(repo_root, 'about.md'), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            m = dt_pat.search(line)
            if m:
                cat = m.group(1).strip()
                if cat:
                    _cats.append(cat)
        _comparable_cats = [c.lower()[:4] for c in _cats]
    for c in _cats:
        yield c

def cat_index(cat_name: str) -> int:
    """
    Given a category name, return the index of its corresponding category
    in about.md. Comparison is case-insensitive.
    """
    # Force _comparable_cats to be populated.
    for x in categories(): break
    comparable_name = cat_name.lower()[:4]
    for i, c in enumerate(_comparable_cats):
        if comparable_name == c[:4]:
            return i
    return -1

exit_code = 0

def complain(msg, update_exit_code=True):
    global exit_code
    sys.stderr.write(msg + '\n')
    if update_exit_code: exit_code = 1

if __name__ == '__main__':
    print("\nCategories:")
    for c in categories():
        print(f"  {c}")
    print("\nIndexed Items:")
    for item in indexed_items():
        print(f"  {item.url} ({item.meta.get('title')})")
    print("\nInternal Items:")
    for item in internal_items():
        print(f"  {item.url} ({item.meta.get('title')})")
    print("\nExternal Items:")
    for item in external_items():
        print(f"  {item.url} ({item.meta.get('title')})")