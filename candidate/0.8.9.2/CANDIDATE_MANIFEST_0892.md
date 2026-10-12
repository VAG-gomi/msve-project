# Candidate Manifest — 0.8.9.2

**Archival content commit:** `9a6a6c32e582cd263184836b082e9c5d4c8da1bc`
(This manifest was added in a subsequent commit; the content commit
above contains the candidate files whose hashes are listed below.)

**Prototype commit:** `5ec3cbdd43c5bcc37300cf0e8988a03a9a30d719`

**Date:** 2026-10-12

## Artifact SHA-256 (full)

| File | SHA-256 |
|---|---|
| `MSVE_DESIGN_SPEC_v0.8.9.2.md` | `b1c71f213e885fa54b31f69f5d482490145cc121ca0f7745004853098ea2b394` |
| `D3_SOLVER_FRAGMENT_SCHEMA.md` | `c76fc303149d34bb341d2c607ca439cf4e2a93d3b7a2dffe6c80d1a72a8be29a` |
| `audit_model_0892.py` | `dadf6eb625bfba21cdc476772a92b47cac43a86fadde7037aeafc2e0032f390f` |
| `run_audit_0892.py` | `383acedc4a8897ad4d06fcafe94fe3157152011d1cb886b984daa3c8f625430e` |
| `QUERY_ID_VECTORS.md` | `747e3b899cacfb8b64dc22395bae3888c261d7dddba56c43e9c730419e4e81dd` |
| `CORRECTION_REPORT_WO19B.md` | `8ba8ae1882017afde5aac8f7cac93149d7ac1595c5970472027d2dfb777c61fa` |
| `m8_output_0892.txt` | `5358700c0cd4c38ff62a9806521060507c77a37740580dc56b4374fa21ca6bc2` |

## Classification

- Normative: `MSVE_DESIGN_SPEC_v0.8.9.2.md`, `D3_SOLVER_FRAGMENT_SCHEMA.md`
- Formal model: `audit_model_0892.py`, `run_audit_0892.py`
- Supporting: `QUERY_ID_VECTORS.md`, `CORRECTION_REPORT_WO19B.md`, `m8_output_0892.txt`

## Verification

- Formal model: 27/27 scenarios
- Prototype: 151/151 tests
- M8: 5/6 examples (1 failure documented in correction report)
