# MSVE v0.8.7 Transfer Manifest

**Work Order:** 0.8.7.1 · **Date:** 2026-10-09
**Integrity check command:** `sha256sum <file>` and `cmp <source> <transfer>`
for each entry below.

| # | Source path | Transfer path | Bytes | SHA-256 (source) | SHA-256 (transfer) | Byte-compared | Provenance |
|---|---|---|---|---|---|---|---|
| 1 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/MSVE_DESIGN_SPEC_v0.8.md` | `(extraction source; see Reports)` | 90498 | `48707955c81c4731e8533fa5135de2001388fd11461e2b0cef5a518730c4080e` | `(n/a)` | N/A (source for extraction) | candidate specification (normative) |
| 2 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/audit_model_087.py` | `(extraction source; see Reports)` | 18391 | `7239f6060378b90adffe8de2dd43982ea117d0506a39c85bbe7c19cb000a77df` | `(n/a)` | N/A (source for extraction) | formal model |
| 3 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/run_audit_087.py` | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/run_audit_087.py` | 12576 | `c343ea23022e575dfa3466db71657b5edde6541f46057b329912fd7a63f54474` | `c343ea23022e575dfa3466db71657b5edde6541f46057b329912fd7a63f54474` | YES | test script |
| 4 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/run_audit_087_raw.log` | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/run_audit_087_raw.log` | 1385 | `94816387678c057f760086df1e6e025cfac50e389fc552687602b8375c6890b3` | `94816387678c057f760086df1e6e025cfac50e389fc552687602b8375c6890b3` | YES | raw solver log |
| 5 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/sat_models_087.json` | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/sat_models_087.json` | 9586 | `3e37f98f52509b9522268f316e8c57c4f527f02cc674a6e93bdb93a64b8dbf27` | `3e37f98f52509b9522268f316e8c57c4f527f02cc674a6e93bdb93a64b8dbf27` | YES | SAT witness models |
| 6 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/MSVE_v0.8.7_COVERAGE_MATRIX.md` | `(extraction source; see Reports)` | 2316 | `8a3a15cc1d0a19c5718f830e012d5af7155c7d2cace5d114401f793e1630062b` | `(n/a)` | N/A (source for extraction) | coverage matrix |
| 7 | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/MSVE_v0.8.7_DISPOSITION_TABLE.md` | `(extraction source; see Reports)` | 4116 | `241ddaf14e882145f2f25a922ae2cec9d268b55afd672cfd08338a14034ba98e` | `(n/a)` | N/A (source for extraction) | disposition table |
| 8 | (created in transfer dir by extraction/analysis) | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/MSVE_v0.8.7_TRANSFER_NORMATIVE_TEXT.md` | 11732 | `(n/a — created)` | `1944ce6169efc5dd095f9756aa9d5cf84aba94a3403518f25b3d13807456427f` | N/A (single artefact) | Report A (verbatim extraction) |
| 9 | (created in transfer dir by extraction/analysis) | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/MSVE_v0.8.7_TRANSFER_SOLVER_LINKAGE.md` | 7245 | `(n/a — created)` | `d095f544d3b041558501a2f7104e7e1450117bc1ba83e0de7241c5a782c7b7cd` | N/A (single artefact) | Report B (analysis) |
| 10 | (created in transfer dir by extraction/analysis) | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/MSVE_v0.8.7_TRANSFER_MODEL_LINKAGE.md` | 5741 | `(n/a — created)` | `9e6f658fd0c363cadedb9ae866961846d0693f9fc1bef22640ec331de7840017` | N/A (single artefact) | Report C (extraction + analysis) |
| 11 | (created in transfer dir by extraction/analysis) | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/MSVE_v0.8.7_TRANSFER_REGRESSION_EVIDENCE.md` | 5654 | `(n/a — created)` | `db473631c85d156fa62c2dae2eab801953a722a56a37f2a30a1af6a41bc7157a` | N/A (single artefact) | Report D (evidence transfer) |
| 12 | (created in transfer dir by extraction/analysis) | `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/owner-review-transfer/MSVE_v0.8.7_TRANSFER_REVIEW_STATUS.md` | 1830 | `(n/a — created)` | `2fdf6a075c639c5201a9ecaeceb4a134940f4dff6bd6e5fa6e01703666a12d89` | N/A (single artefact) | Report E (provenance) |

**Limitations:**
- Reports A–E were created by extraction/analysis; they have no
  separate source file. Their provenance is stated per report.
- Matching hashes establish byte-identity, not normative correctness.
- `sat_models_087.json` was regenerated after the R1-4 model fix; the
  transfer copy matches the current source.
