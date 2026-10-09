# MSVE v0.8.8 Owner Handoff

**Work Order:** 0.8.8 — Canonical Claim Identity and Solver Evidence Linkage
**Date:** 2026-10-09
**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED

## What was implemented

**Claim identity (Option A):** `ClaimDescriptor` with stored `claim_id`,
`solver_invocations` (3-tuple with inputs_ref), formally defined
`outcome_compatible`, invariant 29 (`bases ≠ [] ⇒ claim_id = Some(_)`).

**All four bases** linked to canonical `claim_id`. No sentinel.

## Verification

16/16 adversarial tests pass (z3 5.1.0), post all repairs. Raw log
preserved for final files (spec `69828cb4…`, model `2a3222a9…`).

## Independent reviews

**Normative:** 3 blocking findings (N-1, N-2, N-3) — all repaired and re-verified.
**Model:** 2 blocking findings (F1, F2):
- F1(a) inputs_ref: repaired (model checks invocation inputs_ref)
- F1(b) outcome_compatible: normative definition exists; mechanical enforcement is normative-only (documented limitation)
- F2: repaired via N-1
- F3-F7: non-blocking/informational, acknowledged

## Distinctions

- **Implemented:** ClaimDescriptor, solver_invocations, claim_id linkage, outcome_compatible (normative), inv 29, no sentinel.
- **Exercised:** 16 regression cases.
- **Independently reviewed:** Both reviews complete; blocking findings repaired.
- **Attested not verifiable:** Checker independence/authorization; query faithfully encodes claim; solver actually ran.
- **Limitations:** Outcome compatibility table is normative-only (not mechanically enforced); descriptor 6-field completeness not modeled; spec_version not constrained.

## Schema changes (proposals, pending owner acceptance)

1. `ResultRecord.claim_id: Option<Hash>`
2. `VerificationRecord.claim_id: Hash`
3. `ClaimDescriptor.claim_id: Hash` (stored) + 6 fields
4. `EvidenceBundle.claim_descriptors`
5. `EvidenceBundle.solver_invocations`
6. `SolverInvocation.claim_kind: String`

No baseline, release, or implementation authorized.
