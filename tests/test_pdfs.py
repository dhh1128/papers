"""PDF build helpers (scripts/pandoc.py + scripts/build_pdfs.py).

These pin the pure logic without invoking the heavy xelatex render:
  - metadata prep accepts author/authors and list/str keywords, defaults version;
  - webp image refs are rewritten to png (xelatex cannot embed webp);
  - the build reports a TRUE process exit code (the old os.system/sys.exit(ret)
    wrapped failures mod 256, so a failed pandoc could report success).
"""
import pandoc


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
