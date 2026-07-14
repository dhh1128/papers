# Roadmap

The plan for hardening the Codecraft Papers archive: a tested toolkit and
rigorous CI first, then a quality/consistency pass, then PDFs, then PDF
publication + SEO on Jekyll. Tick items as completed. See [AGENTS.md](AGENTS.md)
for vision and principles, [docs/conventions.md](docs/conventions.md) for schema.

_Created 2026-06-01._

**Locked decisions:** prose = propose-as-diffs only (never silently edited);
single MECE **category** per document (no tags); **stay on Jekyll** (Zensical
migration evaluated and declined); PDFs built reproducibly in CI (publication
model — commit vs deploy — is the one open decision, Phase 4).

---

## Phase 0 — AI context & scaffolding
- [x] Write `AGENTS.md` (vision, principles, locked decisions, open questions)
- [x] Add `CLAUDE.md` redirect to `AGENTS.md`
- [x] Create `ROADMAP.md` (this file)
- [x] Consolidate schema + taxonomy + item-id rule into `docs/conventions.md`
      (replaced `.item-id-convention.md`, now removed)
- [x] Add a `README.md` with CI badge and quickstart

## Phase 1 — Testing discipline + rigorous CI _(the safety net; done first)_
- [x] Scaffold `tests/` (pytest) + `requirements.txt`
- [x] **Fix the CI no-op bug:** scripts imported `archive.exit_code` by value, so
      `check_requirements`, `generate_index`, and `fix_ref_nums --check-only` all
      exited 0 regardless of detected problems. Added `archive.exit_with_status()`
      and made scripts read the live `archive.exit_code`. _(red→green)_
- [x] **Fix the dead Papers check:** `check_requirements.py` evaluated synthesized
      index meta (no `category`), so the Papers branch never ran and referenced an
      undefined `required_fields`. Rewrote it to validate real frontmatter. _(red→green)_
- [x] **Fix inverted ref-num flag:** `fix_ref_nums` passed `not check_only` to
      `complain`, so `--check-only` never failed on a gap. _(red→green)_
- [x] Tests: category parse, item-id format/uniqueness/segment-consistency,
      external-item fields, requirements logic, ref-num exit codes
- [x] Modernize CI → `ci.yml`: `node24` actions, runs guards + `pytest` on every
      push/PR; scheduled link-check bumped to `lychee-action@v2.8.0`/`checkout@v6`
- [x] Fix `make_item_id` docstring (`YYOOMM` → `YYMMOO`)
- [x] **Teach `fix_ref_nums` range notation** (`[3–5]`/`[3-5]`/`[1, 3–5, 7]`).
      The newly-working guard initially flagged `cfa-paper.md` refs [3–5] as
      "uncited" — but they ARE cited via en-dash ranges; the tool, not the
      document, was incomplete. Checker now expands ranges; the in-place fixer
      refuses range files rather than mangle them. _(red→green)_
- [x] Least-privilege `permissions: contents: read` on all workflows.

## Phase 2 — Quality & consistency audit → backlog
**Decisions:** author = singular `author` (norm), `authors` list only for
multi-author/affiliations; version+revision_date required for Papers+Specs only
(backfill `1.0`/pub-date); abstracts for thin docs drafted by AI as proposals.

- [x] Add `validate_metadata.py` + `tests/test_metadata.py` enforcing the schema
      with ERROR/WARN tiers + a `--report` punch-list (supersedes the Papers-only
      `check_requirements.py`; wired into CI). _(red→green)_
- [x] Decide + apply the `version`/`revision_date` policy: backfilled all 7
      Papers (version 1.0 / revision_date = pub date where unset).
- [x] Normalize author form: added `author: "Daniel Hardman"` to `ctf`, `kspqs`,
      `ppred`; `prog-a` keeps its multi-author `authors` list. Convention
      documented in `docs/conventions.md`.
- [x] Backfill `abstract`+`keywords` on the 9 thin docs (ai-coca, aold, crna,
      sss, svce, telco-ev-reqs, wbca, x509-prob, zh) — AI-drafted, author-approved;
      graduated abstract/keywords from WARN to ERROR in the validator. Also fixed
      `telco-ev-reqs` category `Position` → `Positions`.
- [x] Close the authoring-time metadata gap: `scripts/new_doc.py` scaffolds a
      schema-valid stub and mints the next `item_id` (`archive.next_item_id`);
      `.standard-initial-prompt.md` updated to the enforced schema. _(red→green)_
- [x] Verify external-item entries in `.external-items.yml` still resolve
      (all 5 return 200 as of 2026-06-01)
- [ ] _(optional)_ deeper multi-persona content audit via a workflow

## Phase 3 — PDF build pipeline
- [x] Make `pandoc.py` reproducible + importable: extract `pdf_metadata`
      (handles `author`/`authors`, list/str keywords, default version) and
      `build_pdf`. Fix the silent exit-code bug (`sys.exit(os.system(...))`
      wrapped failures mod 256 → a failed render reported success). _(red→green)_
- [x] Build-time **webp → png** conversion (xelatex can't embed webp; 5 docs use
      it). Non-destructive: converts in a temp dir, leaves web assets untouched.
- [x] `scripts/build_pdfs.py`: build one PDF per internal doc into `.build.tmp/pdfs/`
      (gitignored); exits nonzero if any doc fails — the CI gate.
- [x] `.github/workflows/build-pdfs.yml`: installs pandoc/xelatex/fonts/
      ImageMagick, builds the whole corpus, uploads the PDFs as an artifact
      (node24 actions; `upload-artifact@v7`; verified 32/32 build on the runner).
- [x] `tests/test_pdfs.py`: metadata prep, webp rewrite, exit-code semantics.
- [x] **XMP metadata** restored: `hyperxmp` deferred via etoolbox `\AtEndPreamble`
      so it loads after pandoc's hyperref (newer hyperxmp enforces the order).
      Verified via the xelatex log + the embedded XMP packet. PDFs are richly
      indexable (dc:title/dc:creator/pdf:Keywords/dates) plus `/Info`.

## Phase 4 — PDF publication & metadata reconciliation (Jekyll)
> Zensical/MkDocs migration was evaluated and **declined** — no compelling need;
> the scholarly `<head>` metadata already lives in `_layouts/default.html` and
> the PDF story works on Jekyll. The analysis is preserved in
> `ZENSICAL-MIGRATION-KT.md` should it ever be reconsidered.

On plain GitHub Pages Jekyll, the live site serves committed repo files. Today
built PDFs are CI artifacts only, so ~12 `pdf_url`s 404 on the live site and a
few committed PDFs are dead weight nothing links to.

- [x] **Publication model = commit the built PDFs** (Jekyll serves them). All 32
      committed at repo root as `<slug>.pdf`; fixes the ~12 live 404s.
- [x] Reconcile `pdf_url`: absolute site URL on all 30 non-SSRN docs; the 2 SSRN
      docs keep `pdf_url` → SSRN (version of record) and also publish a local copy.
- [x] Removed the stale `rendered/intent-monograph.pdf`; regenerated the other
      committed PDFs from current source (now reproducible via `SOURCE_DATE_EPOCH`).
- [x] `validate_metadata.py` requires a committed `<slug>.pdf` per document +
      `tests/test_metadata.py` test. _(red→green)_
- [ ] _(nice-to-have)_ a `.gitattributes` to pin `*.md` to LF (ai-coca was CRLF).

## Phase 5 — SEO / scholarly-indexing hardening (Jekyll)
The `.reorg-ideas.md` goals — make indexers and AI see a scholarly archive, not a
blog. Audit (2026-06-02) against the LIVE rendered head found the engine works
for single-author/string-keyword docs but has real gaps, several on the
multi-author paper `prog-a`. Tasks, by priority:

**Enabler (done):** local rendering fidelity via a `Gemfile` (github-pages gem)
— `JEKYLL_GITHUB_TOKEN=$(gh auth token) bundle exec jekyll build` renders
`default.html` + `{% seo %}` identically to GH Pages, so SEO fixes are testable
test-first (JSON-LD validated with `json.loads`). `Gemfile.lock` is gitignored.

**High — scholarly-metadata correctness (the core goal):**
- [x] **Multi-author loss fixed:** `citation_author` now handles `authors` (list
      of dicts) + `citation_author_institution`; the JSON-LD author array carries
      every author + affiliation (prog-a regained Karla McKenna). _(verified locally)_
- [x] **`citation_keywords`** now joins list-valued keywords.
- [x] **JSON-LD `@type`:** emit a complete `ScholarlyArticle`/`TechArticle` node
      (author(s), headline, datePublished, abstract-as-description, joined
      keywords, identifier, version, isPartOf Periodical, PDF encoding) — valid
      across single/multi-author, DOI, and no-version docs.
- [x] **og/meta `description`** now per-page (mirrors the abstract via
      `sync_descriptions.py`); `url`/`baseurl` set so og:image/canonical are absolute.

**Medium:**
- [x] `robots.txt`: advertise `Sitemap:`.
- [x] `jekyll-seo-tag` + `jekyll-default-layout` explicit in `_config.yml` plugins.
- [x] **Per-paper social cards** (`make_cards.py`) — 1200×630 `og:image` +
      `summary_large_image`, committed; richer than a single default image.
- [x] `check_seo.py` + `tests/test_seo.py`: validates the RENDERED head
      (citation_* incl. multi-author, JSON-LD `@type`, og:image absolute,
      canonical, per-page description, CollectionPage). Runs in the **scheduled**
      `seo-check.yml` workflow (~every 6 months) since it needs a full site build.

**Low / optional:**
- [x] Index JSON-LD as a `CollectionPage` that `isPartOf` the Periodical and
      lists every document as `hasPart`.

---

## Housekeeping / deferred
- [x] Removed `.item-id-convention.md` (content now in `docs/conventions.md`)
- [ ] Keep the Dependabot security tab clean as standing hygiene (see AGENTS.md)
- [ ] `.todo.txt` legacy notes ("collapse tags into keywords") — now obsolete
      (keywords are populated corpus-wide); delete the stale note.
