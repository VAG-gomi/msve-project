# MSVE v0.8.6 Verification Evidence

**Date:** 2026-10-09 · **Solver:** z3 5.1.0 · **Timeout:** 30 s per check
**Model:** `audit_model_086.py` (extends the 0.8.4 `audit_model.py`:
corrected invariant 10 + invariants 24–28; verification-record slots
extended with `source_item`, `artifact`; 31 shared constraints)
**Tests:** `run_audit_086.py` — exit status 0.

## Regression results (13/13 as expected)

| ID | Case | Expected | Actual |
|---|---|---|---|
| R1 | `output-not-encodable` failure, result present | sat | sat |
| R2 | `canonicalization-failure` failure, result present | sat | sat |
| R3a | `output-not-encodable` failure, result missing | unsat | unsat |
| R3b | `canonicalization-failure` failure, result missing | unsat | unsat |
| R4 | Level A + KERNEL_PROOF + proof evidence | sat | sat |
| R5 | Level A + KERNEL_PROOF label, no evidence | unsat | unsat |
| R6 | Level A + RECOMPUTE + agreement evidence | sat | sat |
| R7 | Level A + RECOMPUTE label, no agreement | unsat | unsat |
| R8 | Level A achieved on INCONCLUSIVE | unsat | unsat |
| R9 | Level A required, Level B achieved, shortfall | sat | sat |
| R10 | Level B + solver/test linked evidence | sat | sat |
| R11 | PASS proof record, unresolved artifact | unsat | unsat |
| R12 | Level A claim, proof record FAIL | unsat | unsat |

Raw output: `run_audit_086.py` stdout (13 lines + summary), preserved
in working notes. R11/R12 initially returned sat because the solver used
the unconstrained second verification-record slot to satisfy the
existential; constraining the spare slot (`present = False`) produced
the intended unsat — the final run above reflects the corrected test
harness, and the cause is documented here rather than hidden.

## What the evidence establishes

- The corrected invariant 10 rejects result-dropping packaging failures
  for both base codes (R3a/R3b) while admitting the intended states
  (R1/R2).
- Invariants 24–28 reject the F-21 counterexamples (R5, R7, R8, R11,
  R12) while admitting evidenced claims (R4, R6, R10) and the legitimate
  shortfall (R9).
- The 31-constraint system remains jointly satisfiable (R1, R2, R4, R6,
  R9, R10 are witnesses).

## Limitations

- Constraint-solver results are not proofs that the natural-language
  specification is correctly formalized; the formalization step rests on
  the 0.8.4 two-reviewer convergence plus the 0.8.6 normative drafting.
- `resolves` remains hash-membership (interpretation); invariants 20/21/23
  remain weakened; 3/12 remain omitted (per 0.8.4/0.8.5 scope).
- Checker independence (§E.6a) is attested, not mechanically derived.
- No engine exists; these are model-level checks, not conformance tests.
