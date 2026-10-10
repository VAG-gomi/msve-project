# OPEN_DECISIONS.md

Owner decisions recorded 2026-10-10 (MSVE-WO-1.0 §4); full text in
`decision-ledger/MSVE_BRAINSTORM_DECISION_LEDGER.csv` (DEC-008–DEC-016,
DEC-025). Sections below retain their option descriptions for provenance;
the rulings supersede them.

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

**Ruled 2026-10-10 (D1):** Policy (B) — an UNKNOWN observation paired
with INCONCLUSIVE may qualify for a weak SOLVER_BACKED chain; it must
never imply proof or a positive conclusion.

## 2. Disposition of the seven unresolved claim kinds

`no_solution`, `contradiction`, `unique_under_projection`, `violated`,
`underdetermined`, `disproved`, `artifact_constructed` have no defined
solver-outcome interpretation. They are explicitly marked unresolved in the
specification (not silently excluded).

**Ruled 2026-10-10 (D2):** Preserve recording of all seven kinds
wherever the contract permits; undefined interpretations cannot justify
SOLVER_BACKED. (Invariants 22/23 recording roles stand.)

## 3. Approval boundary for the next stage

**Ruled 2026-10-10 (D7):** Freeze requires closure of blocking
decisions, demonstrated spec/model consistency, passing required tests
and reproducibility checks, documented provenance gaps, and explicit
owner approval; remaining issues classified and accepted as non-blocking.
**Ruled 2026-10-10 (D8):** A bounded exploratory prototype is authorised
(MSVE-WO-1.0); its results are experimental evidence, not verified
capability. **Ruled 2026-10-10 (D9):** The archival bank and
implementation responsibilities stay separate; spec §H governs the future
implementation repository.
