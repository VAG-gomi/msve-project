# MSVE v0.8.8 — Source-to-Constraint Mapping

**Spec:** `MSVE_DESIGN_SPEC_v0.8.md` (`d194537c…`)
**Model:** `audit_model_088.py` (`2182f3be…`)

## New 0.8.8 constraints

| Normative rule | Model constraint | Tests |
|---|---|---|
| §E.6b: claim_id required for bases | `R['has_claim_id']` in inv 25–28 antecedents | C5 (reject no claim_id) |
| §E.6b: descriptor in evidence | `claim_descriptor_present(R)` = `has_claim_id ∧ resolves_in(claim_id, descriptors)` | C4 (reject missing) |
| Inv 25: proof linked to claim_id | `v['claim_id'] == R['claim_id']` in `kp_evidence` | C1 (reject wrong), C2 (accept) |
| Inv 26: recompute linked + DERIVED_VALUE | `v['claim_id'] == R['claim_id']` + `is_DERIVED_VALUE` gate | B13 (reject), B14 (accept) |
| Inv 27: solver invocation linked | `_solver_linked(R)`: `provenance_ref` resolves to invocation with matching `claim_id` | S6/S8/S9 (reject), S7 (accept) |
| Inv 28: test linked + inputs | `v['claim_id'] == R['claim_id']` + `inputs_ref` match | B16 (reject inputs), C3 (accept HOLDS) |
| §E.6b: no sentinel | No `__no_claim_key__`; missing → `has_claim_id` false → basis rejected | C5 |

## Retained (unchanged from 0.8.7)

Invariants 1–24 (except 25–28 revised), F-20 (inv 10), hash validation,
`resolves_in` membership, two-slot bounds, inv 3/12 omissions, inv
20/21/23 weakenings.
