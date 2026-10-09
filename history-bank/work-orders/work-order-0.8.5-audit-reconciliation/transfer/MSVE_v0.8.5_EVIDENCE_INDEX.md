# MSVE v0.8.5 Evidence Index (Task 4)

**Work Order:** 0.8.5 · **Date:** 2026-10-09
The four evidence layers are kept separate. The 0.8.4 reports are
unchanged; where 0.8.5 corrects a 0.8.4 count, the correction is
documented in `MSVE_v0.8.5_CHECK_RECONCILIATION.md`, not by editing 0.8.4.

## Layer 1 — Normative source interpretation

- Candidate spec: `~/workspace/msve-design/work-order-0.8.3-candidate/MSVE_DESIGN_SPEC_v0.8.md`
  SHA-256 `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`
  (re-verified 2026-10-09; unchanged).
- 0.8.4 formalizations A/B + reconciliation (read-only inputs, unchanged).
- F-20 adjudication (`MSVE_v0.8.5_F20_ADJUDICATION.md`): specification-review
  judgement that D-019's rationale extends to `canonicalization-failure`,
  based on the textual uniformity of 15b/15/16 and the absence of any
  stated distinction. Labeled as review, not solver-established.

## Layer 2 — Formalization and reconciliation

- `audit_model.py` (0.8.4, read-only): 26 Z3 constraints; per-invariant
  encoding status in `MSVE_v0.8.5_SATISFIABILITY_SCOPE.md` (exact /
  omitted 3+12 / weakened 20+21+23 / `resolves` as interpretation /
  15b restricted-existential per R1).
- F-20 correction: the corrected invariant-10 variant exists only inside
  `f20_adjudication.py`'s test harness; the candidate text is untouched.
  The proposal is recorded separately
  (`MSVE_v0.8.5_F20_CORRECTION_PROPOSAL.md`).

## Layer 3 — Solver execution and concrete assignments

- Command: `cd ~/workspace/msve-design/work-order-0.8.4-audit &&
  python3 run_audit.py` — exit status **1** (C-01 expectation unmet),
  45/46 checks as expected. Raw output preserved:
  `run_audit_raw_output.txt`.
- Command: `python3 f20_adjudication.py` — exit status **0**; raw output:
  `F20-W valid (current encoding): sat`,
  `F20-X adversarial (current encoding): sat`,
  `F20-X adversarial (corrected inv-10): unsat`,
  `F20-W valid (corrected inv-10): sat`.
- Command: `python3 dump_assignment.py` — explicit S1 assignment in
  `s1_assignment.json`, verified invariant-by-invariant in
  `MSVE_v0.8.5_SATISFIABILITY_SCOPE.md`.
- Solver: z3 5.1.0 (`z3.get_version_string()` → `5.1.0`), 30 s timeout
  per check. Environment: Python 3.12.3, Linux.
- **UNKNOWN preserved as UNKNOWN:** C-01's `unknown` is recorded as an
  inconclusive check; joint satisfiability is claimed only by entailment
  from the 31 SAT witnesses, each satisfying all 26 shared constraints.

## Layer 4 — Conclusions depending on assumptions or external objects

- The consistency claim covers the **formalized fragment** (26
  constraints). It assumes: the reconciled formalization faithfully
  renders the prose (evidence: two-reviewer convergence + documented
  ambiguity dispositions); `resolves` = hash-membership (interpretation);
  the weakened forms of 20/21/23.
- Invariants 3 and 12 are **outside** the claim (external objects: check
  corpus, frozen spec).
- The F-20 correction proposal depends on the Layer-1 review judgement;
  the solver confirms only its mechanical effect.

## Artefact manifest

`MSVE_v0.8.5_AUDIT_MANIFEST.json` (this directory) carries full SHA-256
values for every newly created artefact. No 0.8.3/0.8.4 artefact was
modified (hashes re-verified where referenced).
