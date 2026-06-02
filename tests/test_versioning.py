"""Version helpers (archive.normalize_version / bump_version) for publish.py.

Versions are MAJOR.MINOR strings. Stored quoted to avoid YAML reading 1.10 as
the float 1.1. Minor bump = errata; major bump = new edition (resets minor).
"""
import archive


def test_normalize_to_major_minor_string():
    assert archive.normalize_version(1.0) == "1.0"
    assert archive.normalize_version(1.5) == "1.5"
    assert archive.normalize_version(5) == "5.0"        # bare int -> .0
    assert archive.normalize_version("0.9") == "0.9"
    assert archive.normalize_version("1.10") == "1.10"  # string preserves minor >= 10


def test_minor_bump():
    assert archive.bump_version("1.3") == "1.4"
    assert archive.bump_version("0.9") == "0.10"        # errata past 9
    assert archive.bump_version("5.0") == "5.1"


def test_major_bump_resets_minor():
    assert archive.bump_version("1.4", major=True) == "2.0"
    assert archive.bump_version("0.9", major=True) == "1.0"


def test_bump_handles_missing_and_floats():
    assert archive.bump_version(None) == "1.1"          # treat absent as 1.0
    assert archive.bump_version(1.0) == "1.1"
