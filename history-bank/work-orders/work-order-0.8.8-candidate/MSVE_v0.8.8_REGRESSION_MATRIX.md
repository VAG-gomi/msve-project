# MSVE v0.8.8 — Adversarial Regression Matrix

**Run:** 16/16 pass. Raw log: `run_audit_088_raw.log`.

| ID | Adversarial scenario | Expected | Actual | Responsible |
|---|---|---|---|---|
| R1 | Packaging preserves result | sat | sat | inv 10 |
| R3a | Packaging drops result | unsat | unsat | inv 10 |
| C1 | Proof for different goal, same output value | unsat | unsat | inv 25 (claim_id) |
| C2 | Proof, correct claim_id | sat | sat | inv 25 |
| C3 | HOLDS + TEST_BACKED, valid descriptor | sat | sat | inv 28 |
| C4 | Missing descriptor | unsat | unsat | descriptor presence |
| C5 | No claim_id with basis (no sentinel) | unsat | unsat | inv 25 (has_claim_id) |
| S6 | UNSAT(A) + result(B), SOLVER_BACKED | unsat | unsat | inv 27 (claim linkage) |
| S7 | Solver linked, compatible | sat | sat | inv 27 |
| S8 | Provenance target missing | unsat | unsat | inv 27 (resolution) |
| S9 | Provenance for other claim | unsat | unsat | inv 27 (claim_id) |
| S10 | Valid result, no basis | sat | sat | (no basis → no check) |
| B13 | Recompute, unrelated claim | unsat | unsat | inv 26 (claim_id) |
| B14 | Recompute, correct linkage | sat | sat | inv 26 |
| B16 | Test, mismatched inputs | unsat | unsat | inv 28 (inputs_ref) |
| B17 | Proof, wrong method | unsat | unsat | inv 25 (method) |

**What the matrix establishes:** Claim identity distinguishes
same-output goals (C1); solver wrong-claim rejected (S6); provenance
must resolve to the right claim (S8, S9); no sentinel fallback (C5).
**What it does not establish:** Full outcome-interpretation table;
spec_version checking; third-record scenarios (two-slot bound).
