# Candidate Manifest — 0.8.9.1 (WO-1.9A)

**Identity:** correction revision of the 0.8.9 review candidate
(WO-1.9A findings C1–C6). Retains design-specification version 0.8.
**Status:** candidate for owner review. Not approved. Not frozen.

## Normative artefacts (candidate/0.8.9.1/)

| Artefact | SHA-256 (prefix) |
|---|---|
| `MSVE_DESIGN_SPEC_v0.8.9.1.md` | `15e027cf52da…` |
| `D3_SOLVER_FRAGMENT_SCHEMA.md` | `a9fde598e972…` |
| `audit_model_0891.py` | `b8dc9ae988fd…` |
| `run_audit_0891.py` | `9dee35cee3f3…` |

## Supporting evidence (candidate/0.8.9.1/)

- `CORRECTION_REPORT_WO19A.md` (`7ac922f9ce21…`) — findings → corrections → evidence
- `model_audit_0891.log` — 24/24 formal-model checks
- `sat_models_0891.json` — SAT models from the audit

## Prototype (separate repository, D9)

- Implementation revision with matching corrections (identity, capacity,
  pipeline, checker, decode, result, vectors, tests).
- Suite: 139/139 passed; 16/16 vectors; UNKNOWN reproduced.

## Preserved history

- `candidate/0.8.8.1/` — original correction candidate, unmodified.
- `candidate/0.8.9/` — reviewed candidate, unmodified.
- `decision-ledger/` — DEC-027–DEC-032 (0.8.9); WO-1.9A corrections
  recorded in the correction report (this revision).
