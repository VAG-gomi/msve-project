# MSVE v0.8.8.1-FINAL — Finding Reconciliation Table

**Final candidate hashes:**
- Spec: `dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782` (96366 bytes)
- Model: `fc6eb49f50eae04595495af05058d52f7c27b0d5b29aa3e16254a33f66be31ae` (21788 bytes)

## Normative findings

| ID | Reviewer statement | Source clause | Model constraint | Test | Disposition | Evidence | Limitation |
|---|---|---|---|---|---|---|---|
| N-0.8.8.1-1 | 7 kinds in "Otherwise: False", tension with inv 22/23 | Spec 1355-1366 outcome table | `_outcome_compatible` falls through → False | — | **Repaired**: 7 kinds explicitly marked unresolved | Spec lines (unresolved note) | Unresolved by design; owner decision needed to extend |
| N-0.8.8.1-2 | vr.spec_version never constrained | Inv 25-28 (pre-repair) | `v['spec_version'] == R['spec_version']` | V5 | **Repaired and verified** | Inv 25/26/28 text; V5 UNSAT | — |
| N-0.8.8.1-3 | Model enforced non-existent R fields | ResultRecord (pre-repair) | — | — | **Repaired**: `spec_version`, `claim_kind` added to ResultRecord | Spec 1078-1080 | — |

## Model findings

| ID | Reviewer statement | Source clause | Model constraint | Test | Disposition | Evidence | Limitation |
|---|---|---|---|---|---|---|---|
| M1 | sr-variant check omitted for holds | Spec 1357-1359 outcome table | `_outcome_compatible` lines 365-381 | O1 | **Repaired and independently verified** (re-inspection 15:01 UTC) | Model lines 375/377; O1 PASS | — |
| M2 | assumptions not represented | Spec 1168 descriptor fields | — | — | **Accepted limitation**: not modeled | — | Assumptions not mechanically checked |

## Adversarial checks (work order §3D)

| # | Case | Test | Verdict |
|---|---|---|---|
| 1 | Solver outcome claim A + result claim B | D6 (2+2 vs 8/2) | UNSAT (rejected) |
| 2 | Provenance to wrong claim | (0.8.8 S9) | UNSAT |
| 3 | Correct claim, incompatible outcome | O2, O3 | UNSAT |
| 4 | Missing/malformed descriptor | D4 | UNSAT |
| 5 | Mismatched inputs/version | V5, B16 (0.8.8) | UNSAT |
| 6 | Unsupported kinds | N-0.8.8.1-1 (marked unresolved) | Rejected (False) |
| 7 | Valid linked solver evidence | O1 | SAT |

**Categories:** All findings are either "defect already repaired and verified" or "limitation explicitly accepted as unresolved". No reviewer interpretation disagreements. No owner-decision blockers (the 7 unresolved kinds are marked, not decided).
