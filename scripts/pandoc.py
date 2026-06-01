"""Render an archive document to PDF (pandoc + xelatex).

Importable helpers (pdf_metadata, rewrite_webp_refs, build_pdf) are unit-tested
in tests/test_pdfs.py and orchestrated for the whole corpus by build_pdfs.py.

Two issues this module fixes vs. the original:
  - exit codes: build_pdf returns pandoc's TRUE return code (the old
    `sys.exit(os.system(...))` wrapped failures mod 256, so a failed render
    could report success);
  - webp: xelatex cannot embed .webp, so referenced webp images are converted
    to .png in a throwaway work dir and the markdown is rewritten to match —
    the author's web assets are left untouched.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime as dt

from archive import internal_items, repo_root

PANDOC_FROM = ('markdown+autolink_bare_uris+yaml_metadata_block'
               '+implicit_figures+link_attributes')
_webp_ref = re.compile(r'assets/([\w.-]+)\.webp')


def date_as_pdfdate(d):
    return f"D:{d:%Y%m%d}"


def _short_title(title):
    if len(title) > 40:
        i = title[:41].rfind(' ')
        return (title[:i] + '…') if i > 10 else (title[:39] + '…')
    return title


def _tex_escape(s):
    """Escape LaTeX special characters for a text context (e.g. the header)."""
    repl = {'&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_', '$': r'\$'}
    return ''.join(repl.get(c, c) for c in str(s))


def pdf_metadata(meta, fallback_mtime=None):
    """Normalize frontmatter into the values the PDF needs.

    Accepts `author` (str/list) or `authors` (list of {name,...}); list/str
    `keywords`; defaults `version` to 1 and `revision_date` to fallback_mtime.
    """
    author = meta.get('author')
    if not author and meta.get('authors'):
        author = [a['name'] if isinstance(a, dict) else a for a in meta['authors']]
    if isinstance(author, list):
        author = ', '.join(author)
    keywords = meta.get('keywords', '')
    if isinstance(keywords, list):
        keywords = ', '.join(keywords)
    elif isinstance(keywords, str) and keywords.startswith('"'):
        keywords = keywords[1:-1]
    title = meta.get('title', '')
    return {
        'title': title,
        'short_title': _short_title(title),
        'author': author or '',
        'keywords': keywords,
        'item_id': meta.get('item_id', ''),
        'version': meta.get('version', 1),
        'date': meta['date'],
        'revision_date': meta.get('revision_date') or fallback_mtime,
    }


def rewrite_webp_refs(text):
    """Return (text_with_webp_refs_as_png, [(name.webp, name.png), ...])."""
    pairs = [(f"{stem}.webp", f"{stem}.png") for stem in
             dict.fromkeys(_webp_ref.findall(text))]
    new = _webp_ref.sub(lambda m: f'assets/{m.group(1)}.png', text)
    return new, pairs


def _write_meta_tex(path, m):
    d = date_as_pdfdate(m['date'])
    md = date_as_pdfdate(m['revision_date'])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(r'\AtBeginDocument{' + '\n  \\hypersetup{\n')
        f.write(r'    pdftitle={' + m['title'] + '},\n')
        f.write(r'    pdfauthor={' + m['author'] + '},\n')
        f.write(r'    pdfcreationdate={' + d + '000000Z},\n')
        f.write(r'    pdfmoddate={' + md + '000000Z},\n')
        f.write(r'    pdfsubject={Codecraft Papers (item: ' + m['item_id']
                + ', version: ' + str(m['version']) + ')},\n')
        f.write(r'    pdfkeywords={' + m['keywords'] + '}\n  }\n}\n')
        f.write(r'\newcommand{\ccitemid}{' + _tex_escape(m['item_id']) + '}\n')
        f.write(r'\newcommand{\ccversion}{' + _tex_escape(m['version']) + '}\n')
        f.write(r'\newcommand{\cctitle}{' + _tex_escape(m['short_title']) + '}\n')


def _prepare_source(input_path, work_dir):
    """Copy the markdown into work_dir, converting any referenced .webp to .png.

    Returns the path to the build-ready markdown. Non-webp docs are still copied
    so the build never touches the source tree.
    """
    text = open(input_path, encoding='utf-8').read()
    new_text, pairs = rewrite_webp_refs(text)
    if pairs:
        assets_out = os.path.join(work_dir, 'assets')
        os.makedirs(assets_out, exist_ok=True)
        for webp, png in pairs:
            src = os.path.join(repo_root, 'assets', webp)
            subprocess.run(['convert', src, os.path.join(assets_out, png)],
                           check=True, capture_output=True)
    out_md = os.path.join(work_dir, os.path.basename(input_path))
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(new_text)
    return out_md


def build_pdf(item, out_dir):
    """Build item -> <out_dir>/<slug>.pdf. Return (returncode, log, output_path)."""
    os.makedirs(out_dir, exist_ok=True)
    slug = os.path.basename(item.url)[:-3]
    output_path = os.path.join(out_dir, slug + '.pdf')
    mtime = dt.fromtimestamp(os.path.getmtime(item.path))
    m = pdf_metadata(item.meta, fallback_mtime=mtime)
    work = tempfile.mkdtemp(prefix='ccpdf-')
    try:
        src_md = _prepare_source(item.path, work)
        meta_tex = os.path.join(work, 'pdfmeta.tex')
        _write_meta_tex(meta_tex, m)
        hdr = os.path.join(repo_root, 'scripts', 'pandoc')
        resource_path = os.pathsep.join([
            work, os.path.join(work, 'assets'),
            repo_root, os.path.join(repo_root, 'assets')])
        cmd = ['pandoc', src_md, '-o', output_path,
               '--from=' + PANDOC_FROM, '--pdf-engine=xelatex',
               '--resource-path=' + resource_path,
               '-V', 'papersize=letter', '-V', 'fontsize=11pt',
               '-V', 'geometry:margin=2.7cm',
               '-V', 'mainfont=TeX Gyre Pagella', '-V', 'monofont=Inconsolata',
               '-V', 'microtypeoptions=protrusion=true',
               '--include-in-header=' + os.path.join(hdr, 'pkgs.tex'),
               '--include-in-header=' + meta_tex,
               '--include-in-header=' + os.path.join(hdr, 'header.tex')]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr), output_path
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(item, out_dir=None):
    out_dir = out_dir or os.path.join(repo_root, 'build', 'pdfs')
    rc, log, output_path = build_pdf(item, out_dir)
    if rc:
        sys.stderr.write(log)
        sys.stderr.write(f"\nFailed to build {item.url} (pandoc exit {rc}).\n")
    else:
        print(f"Built {output_path}")
    sys.exit(0 if rc == 0 else 1)


if __name__ == '__main__':
    url = sys.argv[1]
    for it in internal_items():
        if it.url == url:
            main(it)
    sys.stderr.write(f"Item {url} doesn't appear to exist in the archive.\n")
    sys.exit(1)
