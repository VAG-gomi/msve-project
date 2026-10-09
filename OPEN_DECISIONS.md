# OPEN_DECISIONS.md

Unresolved owner decisions. Nothing here has been decided; do not treat
descriptions of options as rulings.

## 1. Normative/model divergence over Z3 UNKNOWN

The specification's outcome-compatibility table states `UNKNOWN →
sr = Some(INCONCLUSIVE)` ("never a positive conclusion"). The formal model
enforces `outcome ≠ UNKNOWN` for `SOLVER_BACKED`, i.e. an UNKNOWN solver
observation can never support the basis at all.

Two coherent interpretations:
- **(a)** UNKNOWN observations never support any basis. INCONCLUSIVE stands
  on its own (it needs no assurance). The table's UNKNOWN row should read
  `outcome_compatible = False`. *Current lean; not a ruling.*
- **(b)** UNKNOWN + INCONCLUSIVE + SOLVER_BACKED is a legitimate weak chain
  ("the solver couldn't determine, so we're inconclusive, documented by the
  observation"). The model should permit it.

The owner has not selected either policy.

## 2. Disposition of the seven unresolved claim kinds

`no_solution`, `contradiction`, `unique_under_projection`, `violated`,
`underdetermined`, `disproved`, `artifact_constructed` have no defined
solver-outcome interpretation. They are explicitly marked unresolved in the
specification (not silently excluded).

Options: (a) extend the per-kind outcome table; (b) declare these kinds
explicitly unsupported for SOLVER_BACKED in V0 (note: invariants 22/23
contemplate solver observations for CONTRADICTION and
UNIQUE_UNDER_PROJECTION); (c) leave unresolved (current state; blocks any
claim of formal closure).

## 3. Approval boundary for the next stage

No design freeze, baseline acceptance, engine implementation, or experimental
run has been authorised. The criteria proposed for a future freeze decision
are recorded in `records/continuity-export-01/06_OWNER_DECISIONS_AND_OPEN_QUESTIONS.md`.
The owner has not approved them as binding.
