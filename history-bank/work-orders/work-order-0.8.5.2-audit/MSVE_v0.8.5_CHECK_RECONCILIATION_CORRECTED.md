# MSVE v0.8.5 Check Reconciliation (Task 1)

**Work Order:** 0.8.5 · **Date:** 2026-10-09
**Source of truth:** `run_audit_raw_output.txt` (re-run 2026-10-09,
`python3 run_audit.py`, exit status 1 — nonzero solely because the
joint-SAT check did not meet its expectation; see C-01).
**Solver:** z3 5.1.0 · **Timeout:** 30 s per check.
**Audit model:** `~/workspace/msve-design/work-order-0.8.4-audit/audit_model.py`
(shared `invariants(R)` = 26 Z3 constraints: the 23 §E.7 invariants with
15b as 3 constraints, minus excluded 3/12).
**Evidence:** `run_audit.py` in the 0.8.4 directory (read-only input).

## Count reconciliation and correction

The 0.8.4 completion report stated "31 SAT scenarios, 13 UNSAT variants,
one UNKNOWN query" and "13/13 rejections". The exact counts from the
solver log are:

- **32 expected-SAT checks:** 31 returned `sat`, 1 returned `unknown`.
- **14 expected-UNSAT checks:** all 14 returned `unsat`.
- **Total: 46 checks; 45 behaved as expected.**

**Correction:** the 0.8.4 report undercounted the expected-UNSAT variants
as 13 instead of 14 (the `X12 evidence-missing` variant was grouped
mentally with its S12 sibling and dropped from the hand count). The
"missing forty-sixth check" is that fourteenth UNSAT variant, which was
present in the run and behaved as expected. No check was omitted from
execution; only the report's arithmetic was wrong. Cause: manual counting
instead of deriving counts from the log — the table below is generated
programmatically from `run_audit_raw_output.txt` to prevent recurrence.

## Exact check table

| Check ID | Scenario | Expected | Actual | Disposition |
|---|---|---|---|---|
| C-01 | joint-SAT | sat | unknown | INCONCLUSIVE-check |
| C-02 | S1 derived+packaged | sat | sat | expected-pass |
| C-03 | S2 artifact+packaged | sat | sat | expected-pass |
| C-04 | S3 unencodable+15b | sat | sat | expected-pass |
| C-05 | S4 internal-error | sat | sat | expected-pass |
| C-06 | S5 invalid-input | sat | sat | expected-pass |
| C-07 | S6 unsupported | sat | sat | expected-pass |
| C-08 | S7 alt-derived | sat | sat | expected-pass |
| C-09 | S7 alt-artifact | sat | sat | expected-pass |
| C-10 | S7 alt-no_solution | sat | sat | expected-pass |
| C-11 | S7 alt-proved | sat | sat | expected-pass |
| C-12 | S7 alt-disproved | sat | sat | expected-pass |
| C-13 | S7 alt-holds | sat | sat | expected-pass |
| C-14 | S7 alt-violated | sat | sat | expected-pass |
| C-15 | S7 alt-unique_proj | sat | sat | expected-pass |
| C-16 | S7 alt-underdet | sat | sat | expected-pass |
| C-17 | S7 alt-contradiction | sat | sat | expected-pass |
| C-18 | S7 alt-inconclusive | sat | sat | expected-pass |
| C-19 | S8 levelA-no-shortfall | sat | sat | expected-pass |
| C-20 | S8 levelA-shortfall | sat | sat | expected-pass |
| C-21 | S8 levelB-shortfall | sat | sat | expected-pass |
| C-22 | S9 summary-pass | sat | sat | expected-pass |
| C-23 | S9 summary-fail | sat | sat | expected-pass |
| C-24 | S9 summary-divergence | sat | sat | expected-pass |
| C-25 | S9 summary-inconclusive | sat | sat | expected-pass |
| C-26 | S10 timeout-partial | sat | sat | expected-pass |
| C-27 | S10 interrupted-partial | sat | sat | expected-pass |
| C-28 | S11 unique-projection | sat | sat | expected-pass |
| C-29 | S12 evidence-present | sat | sat | expected-pass |
| C-30 | X12 evidence-missing | unsat | unsat | expected-pass |
| C-31 | S13 detailed-admission | sat | sat | expected-pass |
| C-32 | S13 detailed-unsupported | sat | sat | expected-pass |
| C-33 | S13 detailed-packaging | sat | sat | expected-pass |
| C-34 | X13 invalid-code | unsat | unsat | expected-pass |
| C-35 | X13 colon-no-space | unsat | unsat | expected-pass |
| C-36 | X packaging-failed+completed | unsat | unsat | expected-pass |
| C-37 | X packaging-ok+encodable-error | unsat | unsat | expected-pass |
| C-38 | X invalid-input+semres | unsat | unsat | expected-pass |
| C-39 | X levelA-without-basis | unsat | unsat | expected-pass |
| C-40 | X shortfall-inconsistent | unsat | unsat | expected-pass |
| C-41 | X unique-no-evidence | unsat | unsat | expected-pass |
| C-42 | X required-fail+pass-summary | unsat | unsat | expected-pass |
| C-43 | X partial+completed | unsat | unsat | expected-pass |
| C-44 | X derived-ok+value-missing | unsat | unsat | expected-pass |
| C-45 | X derived-failed+value-present | unsat | unsat | expected-pass |
| C-46 | X verif-input-mismatch | unsat | unsat | expected-pass |

## Notes

- **C-01 (joint-SAT):** the only check not behaving as expected. The
  unconstrained joint query returned `unknown` (z3 search limitation on
  the heavily quantified problem within 30 s). Recorded as an
  INCONCLUSIVE check, **not** converted to SAT: joint satisfiability is
  established separately by entailment — every C-02..C-29, C-31, C-32, C-33 SAT model
  satisfies all 26 shared constraints.
- **C-02..C-29, C-31, C-32, C-33 (expected-SAT):** each adds scenario constraints to the
  identical 26-constraint shared set; all 31 returned `sat`.
- **C-30, C-34..C-46 (expected-UNSAT):** each adds an invalid condition to the
  identical shared set; all 14 returned `unsat`, each for an identifiable
  invariant violation (see the witness catalog's countermodel table).
- Exit status of the run script: 1 (one expectation unmet: C-01).
  Per-check solver verdicts above are the primary record.
