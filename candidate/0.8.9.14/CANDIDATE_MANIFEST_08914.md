# Candidate Manifest — MSVE 0.8.9.14

**Work order:** MSVE-WO-1.9P
**Base:** 0.8.9.13 (preserved unchanged)
**Date:** 2026-10-13

## Repository revisions

- Archival (pre-0.8.9.14): `8c6fe809c16929f37eef97c0a1ba23f7c410a58f`
- Prototype (182 tests): `215e9f5d2d2447f7adf26ae1f153e82f3f009309`

## File hashes (SHA-256)

- `MSVE_DESIGN_SPEC_v0.8.9.14.md`: `403a9adf4fcd158e5090f6027c346b0628f5ae4cd674346bcc7e2e89953d6cf0`
- `D3_SOLVER_FRAGMENT_SCHEMA.md`: `6b9ce2ac1e95f11f0647213ee079dad37556b89ae8ad3a3c90fa4104aeae10db`
- `INVOCATION_VECTORS.md`: `cc9923948bb1a6a63954209c526dcaecb422639929199104b98ac5c31048e967`
- `QUERY_ID_VECTORS.md`: `747e3b899cacfb8b64dc22395bae3888c261d7dddba56c43e9c730419e4e81dd`
- `MODEL_COVERAGE_08914.md`: `80eb707ff6f5bda259da28ad0a9856e04e2ea310788aa870af3ea3f0abeb8eb7`
- `MSVE_CAPABILITY_MATRIX_v0.8.md`: `28838a24eeae5a81557a86fb3c6beb64e32fb17e27e32aeaea94a017a7691d2f`
- `MSVE_ACCEPTANCE_PLAN_v0.8.md`: `3f9fcaf291f1e79fe563fd9b9d679db1820d6d3af13af4df0cc4c7e8bc89395d`
- `MSVE_REGRESSION_LEDGER_v0.8.md`: `e04a05e68e92ce541349138395a42308d172998b2fd309fe2963ede6cdf22bf1`
- `audit_model_08914.py`: `9952d88407ade92a7834b2605fe5074e50def4f5e07c68d0daab99a7e540ca2f`
- `run_audit_08914.py`: `f33532bb27ced1a3cec18eb3e6b544be8caf04a67e8b3e29a2799f5285000d95`
- `codelists.json`: `2a6eec1ead342619ef452eb2a24d9e1cfad8165566fb3528fd6a539f98a5e26f`
- `CORRECTION_REPORT_WO19P.md`: `3daa984e313f5e21603803d22fdc0f78c400a882f9217138bbd9075c304eeff4`
- `outputs/audit_08914.txt`: `9d9a6a18152f69d8c84081daa286193efdf3539a0f5721899d9fcaaf7f46c7ed`

## Verification evidence

- Prototype suite: 182/182 passed at `215e9f5d2d2447f7adf26ae1f153e82f3f009309`
- Formal-model audit: 32 PASS / 0 FAIL / 5 INCONCLUSIVE (37 total; see output)
- Verdict self-test: 6/6 PASS (UNKNOWN never PASS)
- M8: 6/6 inherited from 0.8.9.4

## Status
Correction candidate awaiting owner review. Not approved, frozen, or released.
