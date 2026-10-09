# MSVE v0.8.6 Owner Handoff

**Work Order:** 0.8.6 — F-20 and F-21 Normative Corrections
**Date:** 2026-10-09
**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW PENDING

This is not acceptance, design freeze, implementation authorization, or
an MSVE-engine correctness claim.

## Decisions implemented (per owner 2026-10-09)

| Finding | Decision | Candidate status |
|---|---|---|
| F-20 packaging preservation | Accept correction | **Closed in candidate:** invariant 10 tests `is_packaging_error(e)` (both base codes), fully bound variables |
| F-21 assurance without evidence | Accept requirement | **Specified in candidate:** §E.6a + invariants 24–28 |
| Level A on inconclusive | Reject | **Closed in candidate:** invariant 24 forbids; shortfall case preserved |
| Recomputation evidence | Resolve explicitly | **Specified in candidate:** invariant 26 + §E.6a; no new field; independence attested (limitation noted) |

## Acceptance criterion check

- ✅ An achieved assurance level must be evidenced: invariants 25–28
  require identifiable, appropriate evidence per basis; R5/R7/R11/R12
  reject unevidenced claims.
- ✅ Packaging failures must not erase an established result:
  corrected invariant 10; R3a/R3b reject result-dropping.
- ✅ Constraints reject the known counterexamples without excluding
  legitimate shortfall states: R8 unsat (Level A on inconclusive),
  R9 sat (Level A required / Level B achieved / shortfall).

## What the candidate shows in its normative rules

- §E.6a: assurance-evidence linkage definitions (proof artifact hash
  rule, recomputation record requirements, solver/test basis rules).
- §E.7: corrected invariant 10; new invariants 24–28.
- Acceptance plan: the new model-level checks named explicitly, with
  the model-vs-engine evidence distinction stated.

## Remaining owner judgements

1. Whether §E.6a's normative content (especially the `artifact`-as-hash
   rule and the independence attestation) matches intent.
2. Whether invariants 24–28 are correctly scoped (evidence required only
   for bases claimed for the achieved level).
3. Whether the candidate should become a baseline (no freeze implied).

## Artefacts

`~/workspace/msve-design/work-order-0.8.6-candidate/`:
candidate document copies (8), `audit_model_086.py`,
`run_audit_086.py`, six reports above, and
`MSVE_v0.8.6_CANDIDATE_MANIFEST.json` (full SHA-256 per artefact).

All prior artefacts (0.8.3 candidate, 0.8.4/0.8.5/0.8.5.2 audits)
unchanged.
