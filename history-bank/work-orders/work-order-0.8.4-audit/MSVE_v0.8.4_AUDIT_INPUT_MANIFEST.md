# MSVE v0.8.4 Audit Input Manifest (Phase A)

**Work Order:** 0.8.4 · **Date:** 2026-10-09
**Status:** REVIEW-TOOL WORK ONLY — no normative changes.

## Checksum correction

The 0.8.3 completion report gave the candidate ZIP checksum as
`1d04b8989a7c4b647dc06649329ce0e7964bf13b62d24c850` (56 hex chars —
truncated in reporting). The actual full SHA-256, verified 2026-10-09
against the bytes, is:

`1d04b8989a7c4b647dc2fdf772316220dc06649329ce0e7964bf13b62d24c850`

(64 hex chars). The candidate manifest's per-file hashes were generated
programmatically and were correct; only the hand-reported ZIP hash was
truncated. This record corrects it.

## Frozen audit inputs (all hashes verified 2026-10-09)

| Artefact | Path | Bytes | SHA-256 |
|---|---|---|---|
| Candidate ZIP | `~/workspace/msve-design/MSVE_v0.8.3_CANDIDATE_BUNDLE.zip` | 540286 | `1d04b8989a7c4b647dc2fdf772316220dc06649329ce0e7964bf13b62d24c850` |
| Candidate spec | `work-order-0.8.3-candidate/MSVE_DESIGN_SPEC_v0.8.md` | 83036 | `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003` |
| Candidate manifest | `work-order-0.8.3-candidate/MSVE_v0.8.3_CANDIDATE_MANIFEST.json` | 29268 | `180eea00d8b9ad977a25e723aaccbe1a9964af05b26ec54905a9e3c57ca4bb7c` |
| Acceptance plan | `work-order-0.8.3-candidate/MSVE_ACCEPTANCE_PLAN_v0.8.md` | 8935 | `92b234d20f67c10bf74e1f4781dc1dc3214b9530a3eca006ee033a0fc6d8b2d3` |
| Regression ledger | `work-order-0.8.3-candidate/MSVE_REGRESSION_LEDGER_v0.8.md` | 34625 | `e04a05e68e92ce541349138395a42308d172998b2fd309fe2963ede6cdf22bf1` |
| Readiness matrix | `work-order-0.8.3-candidate/MSVE_v0.8_READINESS_EVIDENCE_MATRIX.md` | 11367 | `608e2c89e03bb1ba13c873a957f34153d1aee597ad1cce021640ac4d15ec077f` |

All new findings in this audit refer to these hashes, not to the label "v0.8.3".

## Environment

- Python 3.12.3 (system).
- z3-solver 5.1.0 (pip-installed 2026-10-09 specifically for this audit;
  `z3.get_version_string()` → `5.1.0`).
- No MSVE engine exists; no acceptance execution.

## Missing / unavailable

- Reviewer B's 2,998-value sweep script (still EVIDENCE_NOT_AVAILABLE).
- No historical reviewer inspected these candidate bytes (their records
  predate the 0.8.3 corrections); no claim is made otherwise.
- Z3 models the logical structure of the invariants; string-heavy rules
  (base_code, escape policies) are checked by the transparent Python
  checker alongside, not inside, the solver.
