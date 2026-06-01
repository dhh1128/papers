# tests/

The pytest suite that **proves** the archive meets its publication goals.
`pytest` green is the working definition of "publishable": metadata is complete
and schema-valid, item-ids are well-formed and stable, the index is in sync, and
reference numbering is consistent.

Each test corresponds to a script in [`../scripts`](../scripts). Tests run
against the whole corpus and fail loudly with the specific files/fields at
fault. Subprocess-based tests deliberately exercise real script **exit codes**
(what CI depends on), which import-level tests cannot observe.

Run locally:

```
pip install -r requirements.txt
pytest
```

CI (`.github/workflows/ci.yml`) runs this suite plus the `--check-only` mode of
the guard scripts on every push and PR.

Work **test-first**: for any new fixer or check, add/extend the prover test, see
it go red, then implement until it goes green. See [../AGENTS.md](../AGENTS.md).
