import os
import re
import sys
import yaml
import datetime

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

# Top-level .md files that are project meta-docs, not archive documents.
# Single source of truth: tests import this (see tests/conftest.py) so the two
# can't drift. Add any new root-level dev/meta markdown here.
_non_articles = ['index.md', 'about.md', 'README.md', 'AGENTS.md',
                 'CLAUDE.md', 'ROADMAP.md', 'ZENSICAL-MIGRATION-KT.md']
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
        _comparable_cats = [c.lower()[:3] for c in _cats]
    for c in _cats:
        yield c

def cat_index(cat_name: str) -> int:
    """
    Given a category name, return the index of its corresponding category
    in about.md. Comparison is case-insensitive.
    """
    # Force _comparable_cats to be populated.
    for x in categories(): break
    comparable_name = cat_name.lower()[:3]
    for i, c in enumerate(_comparable_cats):
        if comparable_name == c:
            return i
    return -1

def make_item_id(item, counter=None):
    """
    Generate a document ID according to the convention:
    CC-XXX-YYMMOO
    - CC: literal prefix
    - XXX: first three letters of category, uppercased
    - YY: last two digits of year
    - MM: two-digit month
    - OO: two-digit ordinal (counter, zero-padded)

    If counter is provided, it must be a dict that tracks
    how many items of a given type have been seen so far
    in a year.
    """
    category = item.meta['category'].upper()[:3]
    date = item.meta['date']
    # Accepts YYYY-MM-DD or YYYY-MM or datetime.date/datetime.datetime
    if isinstance(date, (datetime.date, datetime.datetime)):
        year = f"{date.year % 100}"
        month = f"{date.month:02d}"
    elif isinstance(date, str):
        parts = date.split('-')
        year = f"{int(parts[0][-2:]):02d}"
        month = f"{int(parts[1]):02d}"
    if counter is not None:
        ordinal = counter.get(year, 0) + 1
        counter[year] = ordinal
    else:
        ordinal = 1
    return f"CC-{category}-{year}{month}{ordinal:02d}"

_id_pat = re.compile(r'^CC-[A-Z]{3}-(\d{6})$')
def next_item_id(category, date):
    """Return the next available item id for a NEW document.

    `CC-XXX-YYMMOO`, where OO is one greater than the highest ordinal already
    used in that YYMM period across ALL categories — so the YYMMOO segment is
    unique within the month and the full id cannot collide. `date` accepts an
    ISO 'YYYY-MM-DD' string or a date/datetime.
    """
    cat3 = category.upper()[:3]
    if isinstance(date, (datetime.date, datetime.datetime)):
        period = f"{date.year % 100:02d}{date.month:02d}"
    else:
        parts = str(date).split('-')
        period = f"{int(parts[0][-2:]):02d}{int(parts[1]):02d}"
    max_oo = 0
    for it in internal_items():
        m = _id_pat.match(str(it.meta.get('item_id', '')))
        if m and m.group(1)[:4] == period:
            max_oo = max(max_oo, int(m.group(1)[4:]))
    return f"CC-{cat3}-{period}{max_oo + 1:02d}"

def normalize_version(v):
    """Return a canonical `MAJOR.MINOR` string for a version value.

    YAML reads `version: 1.10` as the float 1.1, so versions are stored as quoted
    strings; this canonicalizes any current value (float/int/str) to `M.N`.
    """
    s = str(v)
    if '.' not in s:
        s += '.0'
    major, minor = s.split('.', 1)
    return f"{int(major)}.{int(minor)}"


def bump_version(current, major=False):
    """Return the next version string. Minor bump by default (errata); `major`
    bumps the major and resets the minor (a new edition). Absent -> treat as 1.0."""
    maj, minr = (int(x) for x in normalize_version(current if current is not None else "1.0").split('.'))
    if major:
        return f"{maj + 1}.0"
    return f"{maj}.{minr + 1}"


exit_code = 0

def complain(msg, update_exit_code=True):
    global exit_code
    sys.stderr.write(msg + '\n')
    if update_exit_code: exit_code = 1

def exit_with_status(ok_message=None):
    """Exit the process using the LIVE accumulated exit_code.

    Scripts must call this (or read archive.exit_code) rather than a stale
    ``from archive import exit_code`` binding: that binding captures the value
    at import time (0) and never reflects later complain() calls, which would
    let a script print problems yet exit 0 — silently neutering CI.
    """
    if exit_code == 0 and ok_message:
        print(ok_message)
    sys.exit(exit_code)

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
    counter = {}
    ii = sorted([i for i in internal_items()], key=lambda x: x.meta['date'])
    for item in ii:
        id = make_item_id(item, counter)
        print(f"{item.url}: {id}")
