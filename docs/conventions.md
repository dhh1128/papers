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
"Req" marks fields enforced (or planned to be enforced) by
`scripts/check_requirements.py` and the pytest suite.

| Field | Req | Type | Notes |
|---|---|---|---|
| `title` | ✓ | string | Display title. The body must not repeat it. |
| `date` | ✓ | date | Original publication date (ISO 8601). Drives the id ordinal and index sort. |
| `category` | ✓ | enum | Exactly one of the seven categories above. |
| `item_id` | ✓ | string | Permanent id, `CC-XXX-YYMMOO` (see below). Assigned once, never changed. |
| `abstract` | ✓ | string | One-paragraph summary. Feeds meta description / PDF subject. The body must not repeat it. |
| `keywords` | ✓ | list/string | For SEO and PDF metadata. |
| `author` *or* `authors` | ✓¹ | string / list | Single author string, or a list of `{name, affiliation}`. To be normalized to one form in Phase 2. |
| `pdf_url` | rec² | string | Path/URL of the rendered PDF. Becoming a CI-built, validated field. |
| `version` | rec | int/str | Bump on substantive revision. |
| `revision_date` | rec | date | Date of last substantive revision. |
| `language` | — | string | Defaults to `en`. |

¹ Papers are the strict tier: `check_requirements.py` hard-requires
`title`, `date`, `abstract`, `item_id`, `category`. `author`/`authors` and
`pdf_url`/`keywords` are surfaced as warnings during the current transition.

² `pdf_url` is *recommended* (warn-only) until the Phase 3 PDF build lands; it
will then be validated against an actually-produced artifact.

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

Documents that cite sources use ACM-style inline numbers (`[1]`, `[2, 3]`) with a
matching `References` (or `Works Cited` / `Endnotes`) section at the end.
`scripts/fix_ref_nums.py` checks and renumbers these:

- every inline citation has a matching expanded entry and vice versa;
- numbering has no gaps and is in first-cited order.

Documents that are link-only (no formal references) are listed in
[.hyperlinks-only](../.hyperlinks-only) and skipped by the check.
