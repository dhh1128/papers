# Conventions

Canonical definitions for this repository. Referenced by [AGENTS.md](../AGENTS.md).
This consolidates the metadata schema, category taxonomy, and item-id rule
(the last formerly in `.item-id-convention.md`, now removed).

## Categories (MECE taxonomy)

Every document belongs to **exactly one** category, assigned by editorial intent
(not topic). The authoritative list, assignment tests, and tiebreak rules are in
[about.md](../about.md). The seven categories are:

**Specifications · Papers · Analyses · Primers · Comparisons · Guidance · Positions**

Tiebreak order when a document seems to fit several: normative conformance →
advocacy → teaching → action → multiple-objects. Status, maturity, version,
narrative style, and topic are **metadata, never categories**.

Unlike the sister `../codecraft.co` collection (which uses multi-valued `tags`),
this archive uses single mutually-exclusive categories. This is deliberate and
should not be changed without the author.

## Frontmatter schema

Each document is a Markdown file whose YAML frontmatter carries the fields below.
The tiers are enforced by `scripts/validate_metadata.py` (and the pytest suite):
**ERROR** fails CI; **WARN** is advisory. Run `validate_metadata.py --report`
for a per-field coverage punch-list.

| Field | Tier | Type | Notes |
|---|---|---|---|
| `title` | ERROR | string | Display title. The body must not repeat it. |
| `date` | ERROR | date | Original publication date (ISO 8601). Drives the id ordinal and index sort. |
| `category` | ERROR | enum | Exactly one of the seven categories above. |
| `item_id` | ERROR | string | Permanent id, `CC-XXX-YYMMOO` (see below). Assigned once, never changed. |
| `author` *or* `authors` | ERROR | string / list | See author convention below. |
| `version` | ERROR¹ | str | `MAJOR.MINOR` (quoted). `1.0` baseline; bump on every content edit (errata). |
| `revision_date` | ERROR¹ | date | Date of last revision (= publication date until first errata). |
| `abstract` | ERROR² | string | One-paragraph summary. Feeds meta description / PDF subject. The body must not repeat it. |
| `keywords` | ERROR² | list/string | For SEO and PDF metadata. |
| `citations` | ERROR | enum | Citation discipline: `acm` \| `hyperlinks` \| `none`. Single source of truth for whether the ref-number guard applies (only `acm`). See below. |
| `pdf_url` | ERROR³ | string | Absolute URL of **this site's** copy of the rendered PDF: `https://dhh1128.github.io/papers/<slug>.pdf`. |
| `doi` | —⁴ | string | A full DOI (`10.<prefix>/<suffix>`) when the work has one. Omit otherwise. |
| `language` | — | string | Defaults to `en`. |
| `listed` | — | bool | Defaults to `true`. Set `false` to keep an otherwise-valid document (e.g. a not-yet-ready draft) out of `index.md`; the document still validates and builds. |
| `ed_review_on` | — | date | Date an editorial-panel review was completed. See below. |
| `ed_review_version` | — | str | The `version` that was reviewed — lets a later revision reveal a review as stale. |
| `ed_review_depth` | — | enum | `rigorous` (full multi-persona panel) or `stylistic` (typo/consistency pass). |

¹ `version` + `revision_date` are required (ERROR) on **every internal
document**, regardless of category — the whole archive is citable, versioned
literature. Originals carry `version: "1.0"`, `revision_date` = publication date.
**Every content edit (body or reference) is errata and must bump the version** —
use `scripts/publish.py --revise <slug>` so the bump and `revision_date` are
recorded, never a plain hand-edit. Pure-metadata fixes are not errata.

² `abstract` + `keywords` are required (ERROR). They were WARN-tier during the
Phase 2 backfill and graduated to ERROR once every document carried them.

³ `pdf_url` graduated from warn-only to ERROR once Phase 3/4 landed (PDFs are
built reproducibly and committed at the repo root, so every document has one).
It is now checked for *value*, not just presence: it must be exactly this site's
own `<slug>.pdf`. The layout feeds it to `citation_pdf_url` and the JSON-LD
`contentUrl`, and Google Scholar has to be able to fetch that URL and get a PDF.
**Never point it at an external version of record.** Four SSRN documents did,
using a `papers.ssrn.com/sol3/Delivery.cfm/…` link that is Cloudflare-gated and
returns HTML to any crawler; the external pointer belongs in `doi`.

⁴ `doi` is optional — most documents have none — but when present it is
format-checked as a real DOI: registrant prefix, slash, suffix. A bare SSRN
abstract id (`6979798`) is **not** a DOI; SSRN's DOI for that paper is
`10.2139/ssrn.6979798`. Three documents carried the bare id, which made the
rendered `https://doi.org/<id>` link a 404 and the `citation_doi` invalid.
Do not write the `https://doi.org/…` URL form either — the layout builds that
link itself from the bare DOI.

**Author convention:** use the singular `author` (a string) for single-author
documents — the norm. Use the plural `authors` (a list of `{name, affiliation}`
maps) only when a document has multiple authors or affiliations matter (e.g.
`prog-a.md`). Tooling (`validate_metadata.py`, `pandoc.py`, the layout) accepts
either form.

Notes:
- The body must **not** repeat the title or abstract; the layout renders those.
- The house style for prose is in
  [.standard-initial-prompt.md](../.standard-initial-prompt.md). Prose is the
  author's; AI proposes, never silently edits (see AGENTS.md).

## External items

Documents published elsewhere (e.g. specs hosted on other sites) are not files
in this repo. They are declared in [.external-items.yml](../.external-items.yml)
with `category`, `title`, and `date`, and merged into `index.md` by
`generate_index.py`.

## Item-ID convention

Each document gets a stable, human-readable identifier:

**`CC-XXX-YYMMOO`** — for example `CC-PAP-260501`.

- `CC` — the Codecraft namespace.
- `XXX` — first three letters of the category, uppercased (`PAP`, `SPE`,
  `ANA`, `PRI`, `COM`, `GUI`, `POS`).
- `YY` — two-digit year of original publication.
- `MM` — two-digit month of original publication.
- `OO` — two-digit ordinal within that period.

The identifier is **permanent and immutable**. It refers to the conceptual work,
not to any representation (HTML, PDF) or to the filename/slug/URL, and does not
change when the document is recategorized or revised. Versioning is handled
separately via the `version` field. Git hashes or UUIDs may be recorded as
internal provenance but are never the public id.

The two Codecraft collections coexist under the shared `CC` namespace and stay
distinguishable: **papers** ids always carry a 3-letter category segment
(`CC-XXX-YYMMOO`); **essay** ids in `../codecraft.co` never do (`CC-YYMMOO`).

> Note on ordinals: existing ordinals are author-assigned and stable; they are
> not mechanically recomputed (so tooling validates id *format*, *uniqueness*,
> and that the category/date segments agree with frontmatter, but does not
> reorder them).

## Reference / citation numbering

Every document declares its citation discipline in the `citations` frontmatter
field (one of four values):

- **`acm`** — the house style: ACM-style inline numbers (`[1]`, `[2, 3]`) with a
  matching `References` (or `Works Cited` / `Endnotes`) section at the end.
- **`hyperlinks`** — sources are cited inline as hyperlinks, no numbered References.
- **`none`** — the document makes no source claims / needs no formal citations.

Only `acm` documents are checked by `scripts/fix_ref_nums.py`, which verifies:

- every inline citation has a matching expanded entry and vice versa;
- numbering has no gaps and is in first-cited order.

The set of `acm` documents is `archive.acm_documents()` — the **single source of
truth** consumed by both `publish.py` and CI. `fix_ref_nums.py` itself is a
repo-agnostic file-list checker; the repo-aware selection lives in `archive.py`.
(This replaced the former `.hyperlinks-only` sidecar file; the exemption now
travels with each document in its frontmatter.) **Papers** are expected to use
`acm`; a Paper on any other value is an editorial exception worth revisiting.

## Editorial review

A document that has passed an editorial-panel review records it in three optional
frontmatter fields: `ed_review_on` (the completion date), `ed_review_version` (the
`version` reviewed), and `ed_review_depth` (`rigorous` for a full multi-persona
panel, `stylistic` for a lighter typo/consistency pass). Recording the reviewed
version is deliberate: when a later errata bumps `version` past `ed_review_version`,
the review is visibly stale and a re-review is due. These fields are advisory
(no tier), and adding or updating them is metadata — not errata — so it does **not**
bump the document version.
