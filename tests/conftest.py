"""Shared fixtures: discover and parse the document corpus once per session.

Tests import the toolkit in ``scripts/`` directly (it is added to ``sys.path``
below), and run against the live corpus of top-level Markdown documents.
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))  # let tests import the toolkit (archive, etc.)

import archive  # noqa: E402  (after sys.path setup)

# Top-level .md files that are NOT archive documents. Single source of truth is
# archive._non_articles, so the toolkit and the tests can never disagree.
META_FILES = set(archive._non_articles)


def _doc_paths():
    return sorted(p for p in ROOT.glob("*.md") if p.name not in META_FILES)


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture(scope="session")
def doc_paths():
    return _doc_paths()


@pytest.fixture(scope="session")
def docs():
    """List of (Path, frontmatter dict-or-None)."""
    out = []
    for p in _doc_paths():
        text = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        try:
            fm = yaml.safe_load(m.group(1)) if m else None
        except yaml.YAMLError:
            fm = None
        out.append((p, fm))
    return out


@pytest.fixture(scope="session")
def run_script():
    """Run a toolkit script as a subprocess; return CompletedProcess.

    Subprocess (not import) is deliberate: it exercises the real exit code
    that CI depends on, which import-level testing cannot observe.
    """
    def _run(*args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / args[0]), *args[1:]],
            cwd=str(ROOT), capture_output=True, text=True,
        )
    return _run
