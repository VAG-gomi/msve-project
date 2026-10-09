# MSVE Continuity Package — 07 SOURCE MANIFEST AND CROSS REFERENCE

All hashes independently recalculated 2026-10-09 (this export). [OBSERVED EXECUTION]

## Final candidate (0.8.8.1-FINAL)

| File | SHA-256 | Bytes | Role | Inspected |
|---|---|---|---|---|
| `work-order-0.8.8.1-candidate/MSVE_DESIGN_SPEC_v0.8.md` | `dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782` | 96366 | Normative spec | Yes (quoted) |
| `work-order-0.8.8.1-candidate/audit_model_0881.py` | `fc6eb49f50eae04595495af05058d52f7c27b0d5b29aa3e16254a33f66be31ae` | 21788 | Z3 formal model | Yes (quoted) |
| `work-order-0.8.8.1-candidate/run_audit_0881.py` | `c750ef5c37a132893908c1bfaf4070e67d5a842e7043684e95f05a1936711f83` | 10120 | Regression script | Yes |
| `work-order-0.8.8.1-candidate/run_audit_0881_raw.log` | `525cd40667f96be4d297f5be39a8c02e72ddf7f1644b7e3a31c73006082b480a` | 852 | Raw execution log | Yes |
| `work-order-0.8.8.1-candidate/sat_models_0881.json` | `f67c8dbfd26e39b77edb85c6e6177341847bcbb89ddd106e1461b383587748e0` | 7613 | SAT witnesses (truncated) | Referenced |
| `work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_NORMATIVE_REVIEW.md` | `8a3b8dffe3e69171ac5382b3db10c46f9c9b86dc86c9662a9090d79d298e9943` | 2677 | Normative review report | Yes (quoted) |
| `work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_MODEL_REVIEW.md` | `5fe16ba74ace45cd7fe336211ed867185dad49e7741d45c0e93a50a3b5209826` | 2555 | Model review report | Yes (quoted) |
| `work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_RECONCILIATION.md` | `483e3992a39afccf589b3f315c7d2d9f9f1737f66ffa200371d2a80ae54f361f` | 2426 | Finding reconciliation | Yes |
| `work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_FINAL_HANDOFF.md` | `0fc7d61ef05c56b4f8a56c79f45cb3345486b04ce5384141db934abc23277cfc` | 2034 | Owner handoff | Yes |
| `work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_FINAL_MANIFEST.json` | `44915c5a101aa12f6cece79c027153ad63b75d050c509073e7cd026cbade72be` | 2818 | Manifest | Yes |

## Prior candidates (preserved unchanged)

| File | SHA-256 | Bytes | Role |
|---|---|---|---|
| `work-order-0.8.8-candidate/MSVE_DESIGN_SPEC_v0.8.md` | `69828cb4c1048f2e233d6d6fefeecc86b4a1e337e6566405293e65d8eef2505f` | 95530 | 0.8.8 spec (superseded) |
| `work-order-0.8.8-candidate/audit_model_088.py` | `2a3222a9022df0da45bc5f4ba460936c3f4ded6fd800e829ba849260ce6f1762` | 19714 | 0.8.8 model (superseded) |
| `work-order-0.8.7-candidate/MSVE_DESIGN_SPEC_v0.8.md` | `48707955c81c4731e8533fa5135de2001388fd11461e2b0cef5a518730c4080e` | 90498 | 0.8.7 spec (historical) |
| `work-order-0.8.7-candidate/audit_model_087.py` | `7239f6060378b90adffe8de2dd43982ea117d0506a39c85bbe7c19cb000a77df` | 18391 | 0.8.7 model (historical) |

**Note:** The 0.8.7.2 forensic review established that Report C's cited model hash `e49aee04a0c2b5ecee8d4981d0abc46b5d3b355bc9f23ed721b2eb6a7acaac56` was stale (pre-R1-4-fix); the manifest hash `7239f606…` above is correct for the final 0.8.7 model. [OBSERVED]

## Cross-reference map (finding → clause → constraint → test → evidence → disposition)

| Finding | Normative | Model | Test | Raw evidence | Disposition |
|---|---|---|---|---|---|
| R1-1 | §E.6b descriptor | `claim_descriptor_present` | C3, O1 | 9/9 log | Repaired, reviewed |
| N-1/F2 | §E.6b outcome table | `_outcome_compatible` | O1/O2/O3 | 9/9 log | Repaired, reviewed |
| N-2 | Spec 1166-1180 | Slot fields | D4 | 9/9 log | Repaired, reviewed |
| N-3 | Inv 29 | `Implies(bases, has_claim_id)` | C5 (0.8.8) | 16/16 log (0.8.8) | Repaired, reviewed |
| F-20 | Inv 10 | `is_packaging_error` | R1 | 9/9 log | Repaired, reviewed |
| F-21 | §E.6a, inv 24-28 | Basis linkage | C2 | 9/9 log | Repaired, reviewed |
| N-0.8.8.1-1 | §E.6b unresolved note | Falls to False | — | — | Marked unresolved |
| N-0.8.8.1-2 | Inv 25/26/28 | `v['spec_version']` | V5 | 9/9 log | Repaired, reviewed |
| N-0.8.8.1-3 | ResultRecord fields | `R['spec_version']` | — | — | Repaired, reviewed |
| M1 | §E.6b table | Lines 375/377 | O1 | 9/9 log | Repaired, re-inspected |

## Report → source dependencies

- File 00 depends on: final manifest, both reviewer reports, handoff.
- File 01 depends on: all work-order directories, MEMORY.md (dated 2026-10-09 entries).
- File 02 depends on: reviewer reports, reconciliation table, correction reports.
- File 03 depends on: final spec (quoted sections), final model (quoted functions).
- File 04 depends on: raw logs, manifests, witness files.
- File 05 depends on: reviewer reports (quoted, not paraphrased beyond summary).
- File 06 depends on: handoff, unresolved notes in spec.
- File 07 (this file): independently calculated hashes above.

## Missing or incomplete sources

- The 0.8.7 second-run (post-R1-4) full stdout was never preserved; only the tail was observed. Labeled historical, not tied to final 0.8.7 model.
- Reviewer B's 0.8.1 collision-sweep script was not preserved (noted in 0.8.1 bundle).
- The 2,998-value sweep (F-19) was never preserved; unfillable provenance gap.
- `sat_models_0881.json` contains truncated model strings (2000 chars each); described as truncated evidence.
- Early work orders (0–0.2, 0.4) predate the manifest discipline; their hashes are reported from MEMORY.md, not independently recalculated in this export.
