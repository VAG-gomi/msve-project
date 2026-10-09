# Reproducibility records — MSVE Python sources

This directory records which Python sources in the repository can actually
be executed, under what conditions, and with what evidence. Every relevant
Python source has an inventory entry and a disposition; not every source
executed successfully, and the records distinguish the two.

- [`PYTHON_SOURCE_INVENTORY.csv`](PYTHON_SOURCE_INVENTORY.csv) — one row per
  original/source tracked `.py` file (46 rows at commit `4f395ef`): identity,
  hashes, category, purpose, status, evidence path. The nine derived
  reproduction harnesses under `harnesses/` are tracked `.py` files but are
  **not** in this CSV; they are catalogued separately in
  [`harnesses/PROVENANCE.md`](harnesses/PROVENANCE.md). Total tracked `.py`
  files at the audited commit: 55 (46 source + 9 harnesses).
- [`REPRODUCIBILITY_MATRIX.csv`](REPRODUCIBILITY_MATRIX.csv) — per distinct
  source: what was attempted, the exact command, environment, result.
- [`ENVIRONMENT_REGISTER.md`](ENVIRONMENT_REGISTER.md) — interpreters and
  dependencies used.
- [`KNOWN_BLOCKERS.md`](KNOWN_BLOCKERS.md) — what could not be reproduced
  and why.
- [`runs/`](runs/) — one directory per verified run: captured stdout/stderr,
  exit status, generated outputs.
- [`harnesses/`](harnesses/) — patched driver copies used for reproduction,
  each derived from an archived original with the change documented.
  Archived originals are untouched.
- [`reports/`](reports/) — per-group evidence notes.

## Key results (2026-10-09)

| Group | Result |
|---|---|
| 0.8.8.1 regression (9 checks) | REPRODUCED — 9/9, outcome lines identical to archived log |
| 0.8.8 regression (16 checks) | REPRODUCED — 16/16, identical to archived log |
| 0.8.7 regression (18 checks) | REPRODUCED — 18/18, identical to archived log |
| 0.8.6 regression (13 checks) | REPRODUCED — 13/13, matches correction report |
| 0.8.4 audit (46 checks) | REPRODUCED — 45/46 with the documented joint-SAT `unknown` miss |
| 0.8.5 / 0.8.5.2 analysis scripts | REPRODUCED — all ran as documented |
| M8 test suites | PASSED — canonical, grammar conformance (both variants) |
| M8 CLI + tools | PASSED — corpus 0 failures, check_f64 M6 OK, grammar/identifier checks OK |
| M8 library modules | STATIC-ONLY — import verified, no execution semantics to test |

All Z3 runs used reconstructed code lists, explicitly labelled
**RECONSTRUCTED — NOT THE HISTORICAL ORIGINAL**. A successful run shows the
calculation works today against the pinned bytes; it does not recreate any
historical event.

## Status definitions

- **REPRODUCED** — documented behaviour reproduced under recorded conditions.
- **TESTS-PASSED** — an existing test suite passed with command and output recorded.
- **STATIC-ONLY** — module/fragment; import verified, direct execution not applicable.
- **BLOCKED-*** / **FAILED** / **HISTORICAL-ONLY** / **UNRESOLVED** — none
  assigned in this pass; every source received one of the three statuses above.
