# Codecraft Papers

[![CI](https://github.com/dhh1128/papers/actions/workflows/ci.yml/badge.svg)](https://github.com/dhh1128/papers/actions/workflows/ci.yml)

A curated archive of original technical and scholarly writings by Daniel Hardman
on digital identity, trust, cryptography, and related standards. Published at
**[dhh1128.github.io/papers](https://dhh1128.github.io/papers)** under CC BY 4.0.

This is the scholarly archive — its sister repo, `../codecraft.co`
("**Codecraft**"), holds older, informal essays. Both share the `Codecraft` name
and `CC` id namespace.

- **Start here:** [about.md](about.md) — the editorial policy and the MECE
  category taxonomy that governs how documents are classified.
- **Index:** [index.md](index.md) — generated, categorized table of contents.
- **For AI collaborators:** [AGENTS.md](AGENTS.md) — purpose, principles, and
  operating rules (read first). The plan is in [ROADMAP.md](ROADMAP.md);
  conventions in [docs/conventions.md](docs/conventions.md).

## Working in this repo

```
pip install -r requirements.txt
pytest                                   # prove the corpus invariants
python scripts/check_requirements.py     # metadata / required fields
python scripts/fix_ref_nums.py --check-only --except .hyperlinks-only *.md
python scripts/generate_index.py --check-only
```

CI (`.github/workflows/ci.yml`) runs all of the above on every push and PR.
Every quality goal pairs a script in [`scripts/`](scripts/) with a prover test
in [`tests/`](tests/); work test-first (see AGENTS.md).
