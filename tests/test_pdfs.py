"""PDF build helpers (scripts/pandoc.py + scripts/build_pdfs.py).

These pin the pure logic without invoking the heavy xelatex render:
  - metadata prep accepts author/authors and list/str keywords, defaults version;
  - webp image refs are rewritten to png (xelatex cannot embed webp);
  - the build reports a TRUE process exit code (the old os.system/sys.exit(ret)
    wrapped failures mod 256, so a failed pandoc could report success).

One integration test (``test_every_embedded_image_survives_to_pdf``) does invoke
pandoc (to LaTeX, not the full xelatex render) because raw-HTML image dropping is
only observable end-to-end; it is skipped when pandoc is absent.
"""
import re
import shutil
import subprocess

import pytest

import pandoc

# A source image is either Markdown `![alt](src)` or a raw-HTML `<img ... src=>`
# (the docs use raw-HTML <figure> blocks so the website gets styled captions).
_SRC_IMG = re.compile(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*\bsrc\s*=', re.I | re.S)


@pytest.mark.skipif(not shutil.which('pandoc'), reason='pandoc not installed')
def test_every_embedded_image_survives_to_pdf(doc_paths):
    """Every image a document embeds must reach the rendered output.

    xelatex's writer silently drops raw HTML, so a `<figure><img>` block in the
    source vanishes from the PDF unless the build rewrites it to a Pandoc figure.
    This renders each doc to LaTeX through the real build transform and asserts no
    image is lost (one `\\includegraphics` per source image).
    """
    failures = []
    for p in doc_paths:
        text = p.read_text(encoding='utf-8')
        n_src = len(_SRC_IMG.findall(text))
        if not n_src:
            continue
        prepared, _ = pandoc.prepare_markdown(text)
        r = subprocess.run(
            ['pandoc', '-', '--from=' + pandoc.PANDOC_FROM, '--to=latex'],
            input=prepared, capture_output=True, text=True,
        )
        n_out = r.stdout.count(r'\includegraphics')
        if n_out < n_src:
            failures.append(f"{p.name}: {n_src} image(s) in source, "
                            f"{n_out} reached the PDF")
    assert not failures, (
        "Embedded images dropped from the PDF render:\n  " + "\n  ".join(failures))


def test_metadata_authors_list_becomes_string():
    m = pandoc.pdf_metadata({"title": "T", "date": "2026-01-01", "item_id": "X",
                             "authors": [{"name": "Ann"}, {"name": "Bob"}]})
    assert m["author"] == "Ann, Bob"


def test_metadata_author_string_passthrough():
    m = pandoc.pdf_metadata({"title": "T", "date": "2026-01-01", "item_id": "X",
                             "author": "Daniel Hardman"})
    assert m["author"] == "Daniel Hardman"


def test_metadata_keywords_list_becomes_string():
    m = pandoc.pdf_metadata({"title": "T", "date": "2026-01-01", "item_id": "X",
                             "author": "D", "keywords": ["a", "b", "c"]})
    assert m["keywords"] == "a, b, c"


def test_metadata_version_defaults_to_1():
    m = pandoc.pdf_metadata({"title": "T", "date": "2026-01-01", "item_id": "X",
                             "author": "D"})
    assert str(m["version"]) == "1"


def test_short_title_truncates_long_titles():
    long = "A very long title that certainly exceeds the forty character cap for headers"
    assert len(pandoc._short_title(long)) < len(long)
    assert pandoc._short_title("Short One") == "Short One"


def test_rewrite_webp_refs_markdown_and_html():
    text = ("![x](assets/3d.webp)\n"
            '<figure><img src="assets/envelope.webp"></figure>\n'
            "keep assets/normal.png\n")
    new, pairs = pandoc.rewrite_webp_refs(text)
    assert "assets/3d.png" in new and "assets/envelope.png" in new
    assert ".webp" not in new
    assert "assets/normal.png" in new          # non-webp untouched
    assert ("3d.webp", "3d.png") in pairs
    assert ("envelope.webp", "envelope.png") in pairs


def test_rewrite_webp_refs_noop_when_none():
    text = "no images here, just assets/foo.png"
    new, pairs = pandoc.rewrite_webp_refs(text)
    assert new == text and pairs == []
