# MSVE Continuity Package — 03 CURRENT SPECIFICATION AND MODEL CONTRACT

**Spec:** `MSVE_DESIGN_SPEC_v0.8.md` (`dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782`)
**Model:** `audit_model_0881.py` (`fc6eb49f50eae04595495af05058d52f7c27b0d5b29aa3e16254a33f66be31ae`)

## Intended role and non-goals

[NORMATIVE TEXT] MSVE validates that claimed mathematical results have the claimed evidence. It does not prove theorems. A solver observation never constitutes proof (§E.5, §E.4). [INFERENCE] The design separates "what was computed" (SemanticResult) from "why you should believe it" (assurance bases + evidence).

## Core types

**ResultRecord** (spec lines 1072–1089): admission, execution, output_packaging, semantic_result, claim_id, claim_kind, spec_version, solver_observation, assurance_required/bases/achieved, assurance_shortfall, verification_records, verification_summary, evidence, partial_results, discrepancies.

**SemanticResult** (closed per §B.9): DERIVED_VALUE, PROVED, DISPROVED, HOLDS, VIOLATED, NO_SOLUTION, CONTRADICTION, UNIQUE_UNDER_PROJECTION, UNDERDETERMINED, ARTIFACT_CONSTRUCTED, INCONCLUSIVE, plus others.

**Assurance levels:** NONE < LEVEL_B < LEVEL_A. Invariant 24: Level A requires non-inconclusive result (shortfall case preserved).

## The four assurance bases

### KERNEL_PROOF (invariant 25, spec lines 1462–1470)

[NORMATIVE TEXT] Requires: `vr.source_item = "proof"`, `vr.result = PASS`, `vr.method = "kernel-checked"`, `vr.claim_id = cid`, `vr.spec_version = r.spec_version`, `vr.checker ≠ ""`, `is_sha256_hex(vr.artifact)`, artifact ∈ proof_artifacts, descriptor present.

[MODEL IMPLEMENTATION] `audit_model_0881.py` lines 301–309: all conjuncts present. [EXERCISED BY TEST] C2 (accept), C1/D6 (reject wrong claim), B17 (reject wrong method).

### INDEPENDENT_RECOMPUTE (invariant 26)

[NORMATIVE TEXT] Requires DERIVED_VALUE result, passing recompute record with claim_id/spec_version/inputs_ref match, checker non-empty, artifact = value or derivation hash.

[MODEL IMPLEMENTATION] Lines 311–333, with explicit `Exists` binder for the value hash. [EXERCISED BY TEST] B14 (0.8.8).

[ATTESTATION] Checker independence is attested via `vr.checker`, not mechanically established.

### SOLVER_BACKED (invariant 27)

[NORMATIVE TEXT] Requires: solver observation present; `provenance_ref` resolves to an invocation with matching `claim_id`, `inputs_ref`, `claim_kind`, `spec_version`; `outcome_compatible` holds.

[MODEL IMPLEMENTATION] `_solver_linked` (lines 389–395) + `_outcome_compatible` (lines 365–381). [EXERCISED BY TEST] O1 (holds+UNSAT→HOLDS accept), O2 (UNKNOWN reject), O3 (derive diagnostic reject), S6/S8/S9 (0.8.8 linkage).

### TEST_BACKED (invariant 28)

[NORMATIVE TEXT] Requires passing differential/property-fuzz record with claim_id, spec_version, inputs_ref match, descriptor present.

[MODEL IMPLEMENTATION] Lines 397–406. [EXERCISED BY TEST] C3 (HOLDS accept), B16 (0.8.8 inputs mismatch reject).

## Claim identity

[NORMATIVE TEXT] `ClaimDescriptor` (spec 1166–1180): stored `claim_id: Hash`, `claim_kind`, `proposition`, `goal_ref`, `inputs_ref`, `assumptions`, `spec_version`. All mandatory except assumptions (may be []). `claim_id = sha256(canonical_encoding)` where encoding is `kind|proposition|goal_ref|inputs_ref|assumptions|spec_version`.

[INFERENCE] Identity is syntactic: `derive 2+2` and `derive 8/2` have different descriptors even if both yield `4`. [EXERCISED BY TEST] D6.

[MODEL IMPLEMENTATION] Structured slots with `has_*` presence flags; `_descriptor_complete` requires all four flags; `claim_descriptor_present` requires id+kind+completeness+spec_version match. [ATTESTATION] SHA-256 recomputation not modeled; slot equality proxies identity. `assumptions` not modeled (M2).

## Outcome compatibility

[NORMATIVE TEXT] `outcome_compatible(i, obs, sr)` (spec 1355–1366):
- `holds`+UNSAT → `sr = Some(HOLDS)`; `holds`+SAT → `sr = Some(VIOLATED{witness})`
- `derive`/`prove` → `sr = Some(INCONCLUSIVE)` (diagnostic only)
- UNKNOWN → `sr = Some(INCONCLUSIVE)`; never positive
- Otherwise → `False`
- **Seven kinds explicitly unresolved** (`no_solution`, `contradiction`, `unique_under_projection`, `violated`, `underdetermined`, `disproved`, `artifact_constructed`): cannot justify SOLVER_BACKED until the table is extended. [UNRESOLVED]

[MODEL IMPLEMENTATION] Lines 365–381: enforces outcome≠UNKNOWN, has_semres, and the holds/derive/prove dispatch **including the sr-variant check** (M1 repaired). Unresolved kinds fall through to False. [EXERCISED BY TEST] O1/O2/O3. [INDEPENDENTLY REVIEWED] Re-inspection confirmed M1 repair on final hash.

## Packaging (F-20)

[NORMATIVE TEXT] Invariant 10: `is_packaging_error(e)` covers both `output-not-encodable` and `canonicalization-failure`; either preserves the established semantic result. [EXERCISED BY TEST] R1/R3a.

## Epistemic labels

- **NORMATIVELY DEFINED:** outcome table, descriptor mandatoriness, spec_version linkage, inv 29, packaging semantics.
- **MECHANICALLY ENFORCED:** all of the above in the Z3 model (M1 repaired).
- **EXERCISED BY TEST:** 9/9 cases (see File 4).
- **INDEPENDENTLY REVIEWED:** normative + model reviews on final hashes; M1 re-inspected.
- **ATTESTED / NOT MECHANICALLY VERIFIABLE:** checker independence/authorization; query↔kind fidelity; solver actually ran; assumptions; SHA-256 recomputation.
- **UNRESOLVED:** 7 claim kinds' outcome interpretation (explicitly marked; owner decision required).
