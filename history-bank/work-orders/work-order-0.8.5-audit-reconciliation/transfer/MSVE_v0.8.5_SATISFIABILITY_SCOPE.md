# MSVE v0.8.5 Satisfiability Scope (Task 2)

**Work Order:** 0.8.5 · **Date:** 2026-10-09
**Formalization source checked:** `MSVE_v0.8.4_FORMALIZATION_RECONCILIATION.md`
(and the underlying A/B drafts), not a summary.

## The shared constraint set in each SAT query

Every expected-SAT check (C-02..C-29, C-31, C-32, C-33) asserts the identical shared set
`invariants(R)` from `audit_model.py`: **26 Z3 constraints** =

- invariants 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19,
  20, 21, 22, 23 (21 constraints),
- invariant 1b as 2 constraints (admission/unsupported),
- invariant 15b as 3 constraints (⟹; restricted ⟸; PACKAGING_OK exclusion).

Plus per-check scenario constraints. The solver must satisfy the shared
set jointly in every SAT result.

## Per-invariant encoding status

| Invariant | Status in the encoding |
|---|---|
| 1, 1b, 2, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 18, 19, 22 | **Exact** — direct rendering of the reconciled formalization |
| 10 | **Exact as written** (`output-not-encodable` only); F-20 gap noted, not silently repaired |
| 15b | **Exact** under the reconciled restricted-existential ⟸ (R1); literal universal reading rejected as inconsistent with NEW-C2 |
| 3, 12 | **Omitted** — unformalizable as record constraints (reference the check corpus / frozen spec, external to the record) |
| 20, 21, 23 | **Abstracted/weakened** — existential forms; the *aboutness* qualifiers ("the check property", "search record", projection linkage) have no schema discriminator |
| `resolves(h, L)` | **Interpretation** — hash-membership; the spec never defines "resolves" |

## Explicit satisfying assignment (S1 witness, C-02)

Recorded in `s1_assignment.json`. The assignment:

- `admission = ACCEPTED`, `execution = COMPLETED`,
  `output_packaging = PACKAGING_OK`
- `semantic_result = DERIVED_VALUE(value_ref=Some(a…a), derivation_ref=b…b)`
- `resolves(a…a, constructed_artifacts) = true`,
  `resolves(b…b, derivation_records) = true`
- `assurance_required = LEVEL_A`, `assurance_achieved = LEVEL_A`,
  `assurance_shortfall = false`, bases = {`KERNEL_PROOF`}
- `verification_summary = NOT_RUN`, no verification records present,
  no partial results, no solver observation, no discrepancies

Checked against the reconciled formalization invariant-by-invariant:

- Inv 1, 1b: antecedents false (admission is ACCEPTED) — vacuously satisfied.
- Inv 2: execution is COMPLETED — antecedent false.
- Inv 4: summary is NOT_RUN — antecedent false.
- Inv 5: `shortfall=false`; shortfall rule evaluates false
  (required=LEVEL_A, achieved=LEVEL_A) — biconditional holds.
- Inv 6: achieved=LEVEL_A with KERNEL_PROOF ∈ bases — holds.
- Inv 7: achieved≠LEVEL_B — antecedent false.
- Inv 8, 17, 18, 19, 22: semantic alternative is DERIVED_VALUE — antecedents false.
- Inv 9: derivation_ref=b…b resolves in derivation_records — holds.
- Inv 10: execution is not INTERNAL_ERROR — antecedent false.
- Inv 11: no solver observation — antecedent false.
- Inv 13: no partial results — antecedent false.
- Inv 14: no verification records — antecedent false.
- Inv 15: PACKAGING_OK ∧ DERIVED_VALUE → value_ref=Some(a…a) resolving in
  constructed_artifacts — holds.
- Inv 15b: packaging is PACKAGING_OK; no INTERNAL_ERROR — all three
  constraints satisfied.
- Inv 16: alternative is not ARTIFACT_CONSTRUCTED — antecedent false.
- Inv 20, 21, 23: alternative is not HOLDS/NO_SOLUTION/UNIQUE_UNDER_PROJECTION
  — antecedents false.

All 26 shared constraints hold on this assignment. It was produced by z3
5.1.0 (`s.check() == sat`) and verified by inspection against the
reconciled formalization source above.

## What the SAT results do and do not establish

- Establish: the 26-constraint formalized fragment is jointly
  satisfiable; the S1 assignment above is an explicit witness.
- Do not establish: a proof of the natural-language specification. The
  translation step (prose → reconciled formalization) rests on the
  two-reviewer convergence and the recorded ambiguity dispositions, not
  on the solver. Invariants 3/12 are outside the fragment; 20/21/23 are
  weakened; `resolves` is an interpretation. These boundaries are part of
  the claim, not footnotes to it.
