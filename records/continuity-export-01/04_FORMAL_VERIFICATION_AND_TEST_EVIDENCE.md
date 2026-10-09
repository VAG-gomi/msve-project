# MSVE Continuity Package — 04 FORMAL VERIFICATION AND TEST EVIDENCE

## Latest run: 0.8.8.1-FINAL (9/9)

[OBSERVED EXECUTION]
- **Candidate:** `~/workspace/msve-design/work-order-0.8.8.1-candidate/`
- **Spec:** `dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782` (96366 bytes)
- **Model:** `fc6eb49f50eae04595495af05058d52f7c27b0d5b29aa3e16254a33f66be31ae` (21788 bytes)
- **Test script:** `c750ef5c37a132893908c1bfaf4070e67d5a842e7043684e95f05a1936711f83` (10120 bytes)
- **Command:** `python3 run_audit_0881.py` (working dir: candidate)
- **Timestamp:** 2026-10-09T14:52:51Z; Python 3.12.3; Z3 5.1.0; timeout 30000ms/check; exit 0
- **Raw log:** `run_audit_0881_raw.log` (`525cd40667f96be4d297f5be39a8c02e72ddf7f1644b7e3a31c73006082b480a`, 852 bytes)
- **Witnesses:** `sat_models_0881.json` (`f67c8dbfd26e39b77edb85c6e6177341847bcbb89ddd106e1461b383587748e0`, 7613 bytes; truncated model strings — described as truncated evidence, not complete assignments)

| Test | Expected | Observed | Rule | Constraint | Legitimate conclusion |
|---|---|---|---|---|---|
| R1 packaging preserves | SAT | SAT | Inv 10 | `is_packaging_error` | Packaging failure with result present is satisfiable |
| C2 proof correct | SAT | SAT | Inv 25 | claim_id linkage | Correctly linked proof satisfies inv 25 |
| C3 HOLDS+TEST_BACKED | SAT | SAT | Inv 28 | claim_id + inputs | Payload-free HOLDS can carry TEST_BACKED |
| O1 holds+UNSAT | SAT | SAT | Inv 27 | outcome_compatible | holds+UNSAT+HOLDS satisfies solver linkage |
| O2 holds+UNKNOWN | UNSAT | UNSAT | Inv 27 | UNKNOWN rejection | UNKNOWN cannot justify SOLVER_BACKED |
| O3 derive+UNSAT | UNSAT | UNSAT | Inv 27 | diagnostic-only | Solver cannot justify positive derive conclusion |
| D4 missing field | UNSAT | UNSAT | Descriptor | `_descriptor_complete` | Incomplete descriptor rejected |
| V5 version mismatch | UNSAT | UNSAT | Inv 25 | spec_version | Stale-version evidence rejected |
| D6 2+2 vs 8/2 | UNSAT | UNSAT | Inv 25 | claim_id | Same-output goals are distinct claims |

**What the tests do NOT establish:** Real-world mathematical correctness; SHA-256 collision resistance; that any actual solver was run; checker authorization; the 7 unresolved kinds.

## Historical: 0.8.8 (16/16)

[OBSERVED EXECUTION] Spec `69828cb4…`, model `2a3222a9…`, raw log `57f5f7cf…` (1251 bytes). 16 adversarial cases covering claim identity, solver linkage, and all four bases. Superseded by 0.8.8.1 (narrower scope, deeper checks).

## Historical: 0.8.7 (18/18) — provenance gap

[OBSERVED EXECUTION] The preserved raw log timestamp is 2026-10-09T14:05:48Z. The R1-4 model fix (adding `checker ≠ ""` to inv 25) was applied at ~14:08:11Z. **The 18/18 log therefore records a run against the pre-fix model** (`e49aee04…`, 18333 bytes), not the final model (`7239f606…`, 18391 bytes). A second 18/18 run was observed post-fix but its full stdout was not preserved — only the tail. [INFERENCE] The 18/18 result is historical evidence for the pre-fix model only; it cannot be tied to the final 0.8.7 model file.

## Historical: 0.8.4/0.8.5 solver-count reconciliation

[OBSERVED EXECUTION] 0.8.4 reported 45/46 checks as expected: 31 SAT (valid), 13 UNSAT (invalid), 1 `unknown` (joint satisfiability query — solver search limit). 0.8.5 reconciled from the raw log: the correct count was **14** expected-UNSAT (X12 had been dropped from the hand count), so 45/46 = 31 + 14. The `unknown` was **preserved as UNKNOWN**, not converted to SAT — a deliberate honesty decision. Joint satisfiability was established by entailment instead.

## What "passing" means here

[INFERENCE] A Z3 SAT result means the encoded constraints admit a model — it is evidence that the *formalization* is consistent and that the *test scenario* satisfies the *modeled* invariants. It is not a proof of the natural-language specification, nor of real-world correctness. The two-slot bounds, omitted invariants (3, 12), and weakened invariants (20, 21, 23) limit what the model establishes. These limits are disclosed, not hidden.
