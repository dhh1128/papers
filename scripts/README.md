# scripts/

The durable toolkit for the Codecraft Papers archive. Each script should be
**idempotent**, support a **`--check-only`** mode (so CI can assert a goal
without mutating files), and exit with a **live, accurate status code**.

> Exit codes: scripts accumulate problems via `archive.complain()` (which bumps
> the module-global `archive.exit_code`) and must terminate via
> `archive.exit_with_status()` or `sys.exit(archive.exit_code)`. Never
> `from archive import exit_code` and exit on that name — it is a by-value copy
> captured at import time (always 0) and will silently let a script report
> problems yet pass CI.

Every quality goal pairs a script here with a prover test in
[`../tests`](../tests); CI runs both.

| Script | Purpose | `--check-only` |
|---|---|---|
| `publish.py` | **Maintainer entry point.** Orchestrates the others: regenerate cards/descriptions/index + stale PDFs, `--revise` bumps a version, then validate | (writes) |
| `archive.py` | Shared library: Item model, category parse, frontmatter load, id minting (`next_item_id`), version helpers | — |
| `new_doc.py` | Scaffold a new document: mints the next `item_id`, writes a complete schema-valid frontmatter stub | (writes one file) |
| `validate_metadata.py` | Validate all docs against the schema; `--report` prints a coverage punch-list | (read-only) |
| `sync_descriptions.py` | Mirror each doc's `abstract` into a `description` field (the SEO meta description) | ✓ |
| `make_cards.py` | Render a 1200×630 social-share card (`og:image`) per doc → `assets/cards/<slug>.png` | ✓ |
| `check_seo.py` | Validate the RENDERED `<head>` SEO/scholarly metadata of a built site (scheduled `seo-check.yml`) | (read-only) |
| `generate_index.py` | Regenerate the categorized `index.md` | ✓ |
| `fix_ref_nums.py` | Normalize inline/expanded reference numbering (ACM style) | ✓ |
| `generate_vendored.py` | Rebuild each **generated** vendored document from its upstream sibling, per `.vendored-transforms.yml` | ✓ |
| `check_drift.py` | Report when a **copied** vendored source's upstream has run ahead of its pin in `.vendored-sources.yml` | ✓ |
| `pandoc.py` | Render a document to PDF | — |

Planned (see [../ROADMAP.md](../ROADMAP.md)):
`build_pdfs.py`, a citation/link reconciler.

## Vendored documents: generated vs copied

Some documents here are vendored from sibling repos. Two postures, and the
difference matters:

* **Copied** (`m-glance.md`, the `assets/amp-diff/` figures). `check_drift.py`
  pins the upstream's sha256 and reports when it moves; reconciling is a human
  edit. Because the pin is of the *upstream*, this can only ever catch drift in
  one direction — an edit made **here** is invisible to it.
* **Generated** (`amp-diff.md`). The local file is a build artifact:
  `generate_vendored.py` reads `../entviz/docs/entviz-paper.md` and applies the
  transform declared in `.vendored-transforms.yml` (strip the upstream title
  block, keep this archive's frontmatter, rewrite figure paths, apply the few
  reviewed text overrides, renumber references). **Never edit a generated file** —
  `publish.py` reverts it and CI fails. Reverse drift is impossible rather than
  merely detected.

Every step of the transform is asserted, so nothing is dropped in silence: an
upstream that changes its title block, adds a figure, or rewrites a passage this
archive publishes differently fails the build and asks for a decision.
