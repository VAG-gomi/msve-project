# MSVE v0.8.6 Transfer — Report D: Verification Execution Record

**Scope:** test and solver evidence for F-20/F-21 in the 0.8.6 candidate.
Tests were **not** re-run for this transfer (per Work Order 0.8.6.1).

## Recorded execution

- **Command:** `cd ~/workspace/msve-design/work-order-0.8.6-candidate && python3 run_audit_086.py`
- **Date of execution:** 2026-10-09 (during Work Order 0.8.6).
- **Python:** 3.12.3. **Solver:** z3 5.1.0 (`z3.get_version_string()` → `5.1.0`).
- **Timeout:** 30,000 ms per check (`Solver.set('timeout', 30000)`).
- **Exit status:** 0.
- **Model file hash at execution:** `audit_model_086.py`
  SHA-256 `99d68de70bddec92e0f45f4cee1863856a7ec7d10e6fec6868d67d472ac562de`
  (16341 bytes). **Test file:** `run_audit_086.py`
  SHA-256 `e91cc967e8d39271822b761213d1841e9bec8ee22fb868302b6f288852486ead`
  (10278 bytes); both files unchanged since execution.

## Observed output (transcribed from the execution record; no log file preserved)

**No raw log file was saved** during the 0.8.6 test run. The output
below is transcribed from the observed execution result as recorded in
the 0.8.6 working notes. It is labeled here as observed output, not as
a preserved log file. Expected source path for such a log, had one been
saved: `~/workspace/msve-design/work-order-0.8.6-candidate/run_audit_086_output.txt`
(this file does not exist).

```
PASS [R1 pkg-fail encodable, result present] solver=sat expected=sat
PASS [R2 pkg-fail canonicalization, result present] solver=sat expected=sat
PASS [R3a pkg-fail encodable, result missing] solver=unsat expected=unsat
PASS [R3b pkg-fail canonicalization, result missing] solver=unsat expected=unsat
PASS [R4 Level A + KERNEL_PROOF + evidence] solver=sat expected=sat
PASS [R5 Level A + KERNEL_PROOF, no evidence] solver=unsat expected=unsat
PASS [R6 Level A + RECOMPUTE + agreement] solver=sat expected=sat
PASS [R7 Level A + RECOMPUTE, no agreement] solver=unsat expected=unsat
PASS [R8 Level A on INCONCLUSIVE] solver=unsat expected=unsat
PASS [R9 shortfall Level A->B, inconclusive] solver=sat expected=sat
PASS [R10 Level B + solver/test evidence] solver=sat expected=sat
PASS [R11 proof record, unresolved artifact] solver=unsat expected=unsat
PASS [R12 Level A claim, proof record FAIL] solver=unsat expected=unsat

13/13 0.8.6 regression checks behaved as expected
```

**Result:** 13/13 checks behaved as expected. No failing, skipped,
unavailable, or inconclusive checks in this run.

## Execution note (recorded, not hidden)

R11 and R12 initially returned `sat` (against expectation) because the
solver satisfied the proof-evidence existential using the unconstrained
second verification-record slot. Constraining the spare slot
(`vr[1].present = False`) produced the intended `unsat`. The final
output above reflects the corrected harness. This is a **recorded
execution result** (the harness was fixed and re-run during 0.8.6), not
a specification-review judgement.

## Statement classification

- The 13/13 outcome, per-check solver verdicts, versions, and exit
  status: **recorded execution results**.
- The claim that the constraints "reject the known counterexamples":
  **inference** from the UNSAT verdicts plus the identified responsible
  invariants (Report C).
- The claim that the formalization faithfully renders the normative
  text: **specification-review judgement** (rests on the 0.8.4
  two-reviewer convergence and 0.8.6 normative drafting, not on the
  solver).
- The absence of a raw log file: **recorded fact** (verified by
  filesystem inspection 2026-10-09).
