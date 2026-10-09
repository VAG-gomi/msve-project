# MSVE v0.8.6 Correction Report

**Work Order:** 0.8.6 · **Date:** 2026-10-09
**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW PENDING
**Candidate directory:** `~/workspace/msve-design/work-order-0.8.6-candidate/`

This is not owner acceptance, design freeze, repository creation,
implementation authorization, or an MSVE-engine correctness claim.

## Basis

Read-only inputs: the v0.8.3 candidate
(spec SHA-256 `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`)
and the audit records of Work Orders 0.8.4, 0.8.5, 0.8.5.2.
Owner decisions (2026-10-09): accept F-20 correction in principle;
require evidence for achieved assurance (F-21), covering independent
recomputation as well as kernel proofs; reject Level A on inconclusive
results while preserving the valid Level A-required / Level B-achieved
shortfall case.

## F-20 — Packaging failure must preserve the established result

**Defect:** §E.7 invariant 10's "occurred at packaging" test covered
only `base_code(r) = "output-not-encodable"`, leaving
`canonicalization-failure` outside the "semantic_result still recorded"
consequent, although both are packaging base codes per
`is_packaging_error`, §G.2, and invariant 15b.

**Correction applied** (candidate spec §E.7, invariant 10):
```
∀ r: ResultRecord. ∀ e: String.
  (r.execution = INTERNAL_ERROR(e) ∧ is_packaging_error(e))
  ⟹ r.semantic_result ≠ None
```
Both `output-not-encodable` and `canonicalization-failure` now trigger
preservation. Fully bound variables. Temporal limitation retained
honestly: the static record establishes presence and evidence linkage,
not the historical packaging transition.

**Consistency:** verified against invariants 15, 15b, 16 (uniform
`PACKAGING_FAILED(_)` handling), the `is_packaging_error` definition,
and §G.2. No other invariant required changes.

## F-21 — Evidence must support achieved assurance

**Defect:** no invariant required that an achieved assurance level be
substantiated by evidence. The 0.8.5.2 audit demonstrated via solver
(F21-2, F21-3b, F21-5 — all SAT under the old invariants) that the
schema admitted: Level A + `KERNEL_PROOF` with no proof artifact and no
verification record; `INDEPENDENT_RECOMPUTE` with no agreement evidence;
and `LEVEL_A` achieved on an `INCONCLUSIVE` result.

**Normative principle adopted** (§E.6a): an assurance basis recorded as
achieved must be supported by an identifiable, appropriate verification
record and the evidence required to substantiate that basis. Basis
membership alone is not sufficient.

**New invariants** (candidate spec §E.7):
- **24:** `assurance_achieved = LEVEL_A ⟹ semantic_result = Some(sr) ∧
  sr ≠ INCONCLUSIVE{_}`. Achieved Level A requires an actual,
  non-inconclusive result. Preserves the invariant-11 shortfall case
  (Level A required, Level B achieved, `INCONCLUSIVE{
  ASSURANCE_REQUIREMENT_UNMET}` — achieved is LEVEL_B there).
- **25:** `LEVEL_A` achieved ∧ `KERNEL_PROOF ∈ assurance_bases ⟹ ∃
  verification record with `source_item = "proof"`, `result = PASS`,
  and `artifact` = the proof artifact's sha256 resolving in
  `evidence.proof_artifacts` (per §E.6a).
- **26:** `LEVEL_A` achieved ∧ `INDEPENDENT_RECOMPUTE ∈ assurance_bases`
  (on `DERIVED_VALUE`) ⟹ ∃ verification record with `source_item =
  "recompute"`, `result = PASS`, `inputs_ref` = verification inputs,
  and `artifact` = the primary result hash (value hash, else derivation
  hash) per §E.6a. `PASS` normatively attests exact agreement (§D.6);
  checker independence is attested via `checker` (§E.6a limitation noted).
- **27:** `LEVEL_B` achieved ∧ `SOLVER_BACKED ∈ assurance_bases ⟹
  solver_observation = Some(_)`.
- **28:** `LEVEL_B` achieved ∧ `TEST_BACKED ∈ assurance_bases ⟹ ∃
  verification record with `source_item ∈ {"test:differential",
  "test:property-fuzz"}` and `result = PASS`.

**Schema-change determination (§E.6a, invariant 26):** no new field was
introduced. The recomputation linkage is expressed through normatively
constrained existing fields (`source_item`, `result`, `checker`,
`artifact` as the result hash, `inputs_ref`). Checker independence
remains an attested (not mechanically derivable) property, documented as
a limitation — the record carries no primary-producer field.

## Verification

Extended Z3 model (`audit_model_086.py`): corrected invariant 10 +
invariants 24–28 (31 shared constraints). **13/13 regression checks
behaved as expected** (z3 5.1.0):
- R1/R2 (both packaging codes, result present): sat.
- R3a/R3b (either code, result missing): unsat — F-20 closed.
- R4/R6 (Level A with kernel-proof / recompute evidence): sat.
- R5/R7 (Level A with unevidenced bases): unsat — F-21 closed.
- R8 (Level A on INCONCLUSIVE): unsat.
- R9 (Level A required, Level B achieved, shortfall inconclusive): sat
  — legitimate shortfall preserved.
- R10 (Level B with linked solver/test evidence): sat.
- R11/R12 (unresolved artifact; FAILing proof record): unsat.

## Documents revised

Candidate copies of all eight documents were prepared; normative changes
are confined to the specification (§E.6a, §E.7 invariants 10, 24–28),
the regression ledger (F-20, F-21 entries), and the acceptance plan (new
model-level checks, model-vs-engine evidence distinction). Historical
D-001–D-033 and NEW-A/B/C/D findings preserved.

## What remains

Owner review of this candidate. The F-21 linkage definitions (§E.6a)
add normative content (notably the `artifact`-as-hash rule and the
independence attestation); they are proposed, not derived. No freeze,
acceptance, or implementation is authorized.
