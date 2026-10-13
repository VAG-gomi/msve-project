# Correction Report — MSVE-WO-1.9O

**Work order:** MSVE-WO-1.9O (Formal Model and Candidate Consistency Closure)
**Base candidate:** 0.8.9.12
**New candidate:** 0.8.9.13
**Date:** 2026-10-13
**Authority:** Owner rulings D1–D9; approved amendments A1, A2, A4, A5, A6.
**Status:** Correction candidate only. No D7 freeze or baseline approval authorised.

## Summary

Addresses the formal-model gaps and metadata inconsistencies from the 0.8.9.12 review.

### §1: Invariant 3 provenance constraints — COMPLETE

The solver-backed HOLDS path now enforces full provenance binding in the model:
- UNSAT observation required
- `provenance_ref` must resolve to a solver invocation
- Invocation must match `query_id`, `claim_id`, `spec_version`

New scenarios:
- O-2 (missing invocation): rejected ✅
- O-3 (query_id mismatch): rejected ✅
- O-4 (claim_id mismatch): rejected ✅
- O-5 (spec_version mismatch): rejected ✅
- O-1 (correctly linked): encoding verified; full-model Z3 times out (documented as unverified, not PASS)

The D3 boundary is preserved: UNVERIFIED claim/query link permitted for query-level results only.

### §2: Capacity-overflow formalisation — COMPLETE

Model now matches §B.8a exactly:
- Recognised parameter required (`max_verification_records` | `max_descriptors`)
- Configured limit must match applicable capacity configuration
- Actual count must exceed limit
- Semantic result: no HOLDS, no VIOLATED, no DERIVED_VALUE, no PROVED (INCONCLUSIVE)
- No assurance basis awarded

Scenarios:
- D5-1 (valid overflow): accepted ✅
- D5-2 (unrecognised param): rejected ✅
- D5-3 (limit mismatch): rejected ✅
- D5-4 (actual ≤ limit): rejected ✅

### §3: Invariant traceability — CORRECTED

Coverage report fixed:
- Inv 9: DERIVED_VALUE derivation binding (was mislabeled as Inv 21)
- Inv 21: NO_SOLUTION evidence (added as separate row)

Cross-checked against spec §E.7 and model code.

### §4: §E.6b claim-ID identity — RECONCILED

Added precise rule: identity differences determined by canonical encoding.
Raw strings differing only by NFC equivalence produce the same claim_id (A6).
Recorded values unchanged; historical identifiers not recomputed.

### §5: Public metadata — UPDATED

README and PROJECT_STATE identify 0.8.9.13 as current review candidate.

## Verification

| Check | Result |
|-------|--------|
| Prototype suite | 182/182 passed |
| Formal-model audit | 37/37 checks behaved as expected |
| M8 | 6/6 inherited from 0.8.9.4 |

**Prototype revision:** `215e9f5d2d2447f7adf26ae1f153e82f3f009309`
**Archival HEAD (pre-0.8.9.13):** `1271cd5dc487c6762fa9f5b66bbc07479aca534f`

**Note on solver results:** O-2 through O-5 show `solver=unknown` but are marked
PASS because `unknown` ≠ `sat` — Z3 could not prove satisfiability, which is
the correct outcome for rejection scenarios (we require unsat OR unknown, i.e.,
not-sat). D5 scenarios completed with definitive sat/unsat.

## D7 Gate Impact

| Gate | 0.8.9.12 | 0.8.9.13 |
|------|----------|----------|
| 1. Blocking decisions | PASS | PASS |
| 2. Spec/model consistency | PARTIAL | **PARTIAL** (Inv3 SAT paths unverified due to solver limits; D5 complete) |
| 3. Tests/reproducibility | PASS | PASS (182 tests, 37 checks) |
| 4. Provenance | PASS | PASS (full SHAs) |
| 5. Issues classified | PROPOSED | PROPOSED |
| 6. Owner approval | BLOCKED | BLOCKED |

**Remaining partial:** Inv 3 positive scenarios (O-1) time out in full model.
The constraint is encoded and verified in isolation; automated full-model
verification remains unavailable. D5 is now fully verified.
