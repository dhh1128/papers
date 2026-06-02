# AGENTS.md — Project context for AI collaborators

> This file is the single source of truth for working in this repository.
> `CLAUDE.md` and any `GEMINI.md` are thin redirects here. Read this first.
> The live, tickable task list lives in [ROADMAP.md](ROADMAP.md).
> The metadata schema, category taxonomy, and ID convention live in
> [docs/conventions.md](docs/conventions.md).

## What this repository is

**Codecraft Papers** is a curated archive of original technical and scholarly
writings by Daniel Hardman, on digital identity, trust, cryptography, and
related standards (KERI, ACDC/CESR, verifiable credentials, vLEI, X.509/PKI,
privacy). It is published as a site at **dhh1128.github.io/papers** (CC BY 4.0).

Unlike its sister repo `../codecraft.co` — a WordPress export of older,
informal essays being mechanically restored — the documents here are **original,
actively authored works** written to a formal house style. The editorial intent
is scholarly: these are meant to read and be cited as technical literature, not
as a blog. The governing editorial policy is [about.md](about.md).

## The vision (what "done" means)

1. Reads as a curated scholarly archive — a categorized index, stable per-item
   IDs, explicit versions and dates; indexers and AI see citable literature, not
   a blog (see `.reorg-ideas.md` for the discoverability goals).
2. Every document is correctly classified into exactly **one** category under
   the MECE taxonomy in [about.md](about.md).
3. Complete, schema-valid metadata on every document; Papers meet their stricter
   bar.
4. Consistent, correct reference/citation numbering and a resolving References
   section in every document that cites sources.
5. No broken links (internal or external), enforced in CI.
6. A current PDF available for every document, built reproducibly.
7. A **tested Python toolkit** (`scripts/`) + **pytest suite** (`tests/`) that
   *proves* the goals above. `pytest` green + the `--check-only` guards == ready.

## Guiding principles

- **Prose: propose, never silently change.** These are the author's own
  finished works. AI may *propose* improvements toward the house style in
  [.standard-initial-prompt.md](.standard-initial-prompt.md) — but only as
  reviewable diffs/suggestions the author approves, never applied unprompted.
  Mechanical, structural, metadata, citation, and reference-numbering fixes may
  be applied directly. When in doubt whether a change is "prose," ask.
- **The category taxonomy is MECE and authoritative.** Every document belongs to
  exactly one category from [about.md](about.md), assigned by editorial intent
  (use the tiebreak rules there). Do **not** introduce multi-valued tags — that
  is a deliberate difference from the sister repo. Status, version, maturity, and
  topic are metadata, never categories.
- **IDs are permanent.** Once a document has an `item_id` (`CC-XXX-YYMMOO`), it
  never changes — not when the filename, slug, category, or version changes. See
  [docs/conventions.md](docs/conventions.md).
- **Every quality goal is a script + a test.** When you add a capability, add the
  fixer/checker in `scripts/` (with a `--check-only` mode) *and* the prover test
  in `tests/`. CI runs the tests and the guards.
- **Work test-first (red → green).** For any new fixer, check, or fix, write or
  extend the prover test *first* and **observe it fail** (red) before
  implementing; then implement until it **passes** (green). Report both
  observations explicitly. Never claim a task done before seeing the test green.
- **Scripts must fail honestly.** Accumulate problems with `archive.complain()`
  and exit via `archive.exit_with_status()` / `sys.exit(archive.exit_code)` —
  never a stale `from archive import exit_code`. (That by-value import silently
  neutered all three CI guards before Phase 1; see ROADMAP.)
- **Surface, don't guess.** If a referenced tool, fixture, or convention is
  missing, or contradicts what's described here, stop and ask — don't improvise a
  replacement.
- **Keep CI hygienic.** New/edited GitHub Actions pin to `node24`-runtime
  versions (`actions/checkout@v6`, `actions/setup-python@v6`; `lychee-action`
  ≥ `v2.8.0`). Verify a tag's runtime with
  `curl -sL https://raw.githubusercontent.com/<org>/<action>/<tag>/action.yml | grep -E '^\s*using:'`
  (want `node24`/`composite`/`docker`, never `node20`). Keep the Dependabot
  security tab clean as standing hygiene.
- **Sign off commits** with `-s` (the author works in DCO-enforced repos).

## Decisions already made (do not relitigate without the author)

- **Prose:** propose-as-diffs only (see principle above). Original works, formal
  house style; the author edits, AI assists.
- **Taxonomy:** single mutually-exclusive **category** per document (MECE, per
  about.md). No tags.
- **Publishing platform: stay on Jekyll.** GitHub Pages' built-in Jekyll
  (remote `minimal` theme; no `Gemfile`). A Zensical/MkDocs migration was
  evaluated and **declined** — no compelling need. The scholarly `<head>`
  metadata (JSON-LD, Highwire `citation_*`) already lives in `_layouts/`, and
  the PDF story is handled on Jekyll. Revisit only if Jekyll becomes a blocker.
- **PDFs:** built reproducibly by `scripts/build_pdfs.py` (Phase 3), produced in
  CI, and embedding full XMP + `/Info` metadata. *How they reach the live site*
  (commit vs Actions-deploy) is the one open decision — see ROADMAP Phase 4;
  `pdf_url`/`canonical_pdf_url` reconciliation rides on it.
- **External items:** specs published elsewhere are declared in
  [.external-items.yml](.external-items.yml) and merged into `index.md`.

## Open questions (decide when relevant, don't assume)

- **PDF publication model on Jekyll.** Built PDFs currently upload as a CI
  artifact only; they are not on the live site, so ~12 `pdf_url`s 404. Decide how
  they get served on plain GitHub Pages Jekyll: commit the built PDFs, or switch
  Pages to an Actions build+deploy. This gates retiring the committed `*.pdf`
  blobs and the `pdf_url`/`canonical_pdf_url` reconciliation. See ROADMAP Phase 4.

_(Resolved earlier: platform = Jekyll; `author` singular with `authors` only for
multi-author docs; `version`/`revision_date` required for Papers + Specifications
— all recorded in [docs/conventions.md](docs/conventions.md).)_

## Repository layout

```
*.md                 documents (one file per work; slug == filename)
about.md             the editorial policy + MECE category taxonomy (authoritative)
index.md             generated categorized table of contents (internal + external)
.external-items.yml  externally-hosted items merged into the index
assets/              images
_layouts/ _includes/ Jekyll layouts/partials, _config.yml
scripts/             durable Python toolkit — see scripts/README.md
tests/               pytest suite that proves the goals — see tests/README.md
docs/                conventions (frontmatter schema, taxonomy, item-id rule)
.github/workflows/   CI (ci.yml: guards + pytest) and scheduled link-check
ROADMAP.md           the tickable project plan
.standard-initial-prompt.md   the house style brief for drafting new documents
```

## Frontmatter & IDs (summary)

Canonical definition in [docs/conventions.md](docs/conventions.md). In brief,
each document's YAML frontmatter carries `title`, `date`, `category` (one MECE
category), `item_id` (`CC-XXX-YYMMOO`), `abstract`, `keywords`, and `author` (or
`authors`); Papers additionally aim for `pdf_url`, `version`, `revision_date`.
The body must **not** repeat the title or abstract — the layout renders those.

## How to add or edit a document

1. Decide the single category by editorial intent (about.md tiebreak rules).
2. Scaffold it with `python scripts/new_doc.py --title "…" --category <Cat>` —
   this mints the permanent `item_id` and writes a complete, schema-valid
   frontmatter stub (replace the TODO `abstract`/`keywords`). The authoring house
   style is in [.standard-initial-prompt.md](.standard-initial-prompt.md); the
   schema is in [docs/conventions.md](docs/conventions.md).
3. Never hand-fabricate an `item_id`; it is permanent and minted by `new_doc.py`.
4. Prose changes follow the propose-don't-silently-edit rule above.
5. **Build and commit the PDF.** PDFs are committed at the repo root as
   `<slug>.pdf` (Jekyll serves them at `/papers/<slug>.pdf`, which is what
   `pdf_url` points to). Regenerate after a content change and commit it:
   `python scripts/pandoc.py <slug>.md` (writes to `build/pdfs/`; copy to root)
   or rebuild the whole corpus with `python scripts/build_pdfs.py --out .`.
   Builds are timestamp-deterministic (`SOURCE_DATE_EPOCH`), so a PDF only
   changes when its content does — regenerate only the docs you touched.
6. Run `pytest`, `python scripts/validate_metadata.py`, and the `--check-only`
   guards before committing; CI is the backstop. Work test-first for new tooling.
