# MSVE v0.8.7 Owner Handoff

**Work Order:** 0.8.7 — Assurance Claim Linkage and Formal Fidelity
**Date:** 2026-10-09
**Status:** BLOCKED — NORMATIVE DECISION REQUIRED

This is not acceptance, baseline freeze, implementation authorization,
or an MSVE-engine correctness claim.

## Why blocked

Reviewer 1 (normative) found a material hole (R1-1): the claim-key
definition does not cover payload-free `SemanticResult` variants —
`HOLDS`, `NO_SOLUTION`, `CONTRADICTION`, `UNIQUE_UNDER_PROJECTION`.
For these, "evidence relevant to the exact claim" cannot be evaluated
because the claim has no key. Notably, `HOLDS` is the natural result of
test-backed `check` goals, so the `TEST_BACKED` + `HOLDS` combination —
a core intended path — is affected.

Resolving what identifies the claim for a payload-free result (the
check property from the goal? a prohibition on claiming bases? another
linkage?) is a normative decision requiring owner judgement, not a
drafting fix. The candidate is therefore not presentable as a complete
correction.

## Findings addressed (F-22 through F-27)

| Finding | Disposition |
|---|---|
| F-22: checks too narrow | **Corrected:** invariants 25–28 apply at any level; recomputation requires DERIVED_VALUE |
| F-23: evidence not linked to claim | **Corrected:** `property` must equal claim key; `method="kernel-checked"` for proofs |
| F-24: model omits fields | **Corrected:** checker modeled; hash form validated; `resolves_in` is real membership |
| F-25: no unrelated-evidence tests | **Corrected:** S4/S5/S7 test unrelated property/method |
| F-26: ambiguous binders | **Corrected:** explicit existentials in text and model |
| F-27: manifest overstates identity | **Corrected:** true source paths in manifest |

## Central requirement

A verification record no longer substantiates a basis by label alone.
It must have the right `method`, its `property` must be the result's
claim key, its artifact must be a well-formed hash resolving in the
correct collection, and (for recomputation) its checker must be
identified. Tests S4/S5/S7/S9/S10/S11 confirm that correctly-classified
but irrelevant or malformed evidence is rejected.

## Verification

18/18 checks pass (z3 5.1.0). Raw log preserved:
`run_audit_087_raw.log`. SAT witnesses in `sat_models_087.json`.

## Remaining owner decisions

1. Whether the claim-key definition covers all semantic-result variants
   adequately, or needs extension.
2. Whether checker *independence* remaining attested (not derived) is
   acceptable, or requires a schema change (proposed separately, not
   introduced).
3. Whether the candidate should proceed toward baseline (no freeze
   implied).

## Artefacts

`~/workspace/msve-design/work-order-0.8.7-candidate/` with
`MSVE_v0.8.7_CANDIDATE_MANIFEST.json` (true source paths, SHA-256).
