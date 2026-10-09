# MSVE v0.8.4 Verification Evidence (Phase D)

**Date:** 2026-10-09 · **Tool:** `audit_model.py` + `run_audit.py`
**Solver:** z3 5.1.0 (`z3.get_version_string()` → `5.1.0`),
pip-installed 2026-10-09 for this audit.
**Environment:** Python 3.12.3, Linux.

## What was run

```
cd ~/workspace/msve-design/work-order-0.8.4-audit && python3 run_audit.py
```

Exit status: 0. Per-scenario `z3.Solver()` instances, 30 000 ms timeout
each. Total wall time ≈ 35 s. Raw per-scenario output (solver verdict vs
expectation):

- 31 expected-SAT scenario instances → `sat` (all 13 families, incl. all
  11 `SemanticResult` alternatives, all 5 summary states, all assurance
  combinations, F-01 detailed codes).
- 13 expected-UNSAT invalid variants → `unsat` (each rejected for an
  identifiable invariant violation; see witness catalog).
- 1 unconstrained joint query → `unknown` (solver search limitation;
  joint satisfiability established by entailment from the SAT witnesses).

**45/46 checks behaved as expected.**

## Code and test artefacts (in this directory)

- `audit_model.py` — Z3 encoding of the reconciled formalization:
  datatypes for `Admission`/`Execution`/`Packaging`/`SemanticResult` (11
  alternatives)/assurance/verification/summary; `base_code` via Z3 string
  theory (`IndexOf`/`SubString`, exact F-01 semantics); the four closure
  predicates as explicit disjunctions over code lists extracted
  programmatically from the candidate spec (27/3/12/2); `resolves` as an
  uninterpreted predicate; all 23 invariants per the reconciliation
  (3 and 12 excluded; 20/21/23 weakened; 15b restricted existential).
- `run_audit.py` — the 46 scenario checks.
- `dump_witnesses.py` — readable witness extraction.

## What the evidence establishes and does not establish

- Establishes: the *formalized fragment* of the §E.7 invariants is jointly
  satisfiable; every intended scenario family is realizable under the
  joint constraints; the 13 targeted contradictions are rejected.
- Does not establish: satisfiability of invariants 3 and 12 (excluded as
  unformalizable — they reference the check corpus and the frozen spec,
  not record fields); the *aboutness* content of invariants 20/21/23
  (weakened forms checked); faithfulness of the formalization to the prose
  (that step rests on the two-reviewer convergence + reconciliation, not
  on the solver); MSVE-engine behavior; implementation conformance.
- The `unknown` on the unconstrained joint query is reported as-is; no
  stronger claim is drawn from it than the entailment noted above.
