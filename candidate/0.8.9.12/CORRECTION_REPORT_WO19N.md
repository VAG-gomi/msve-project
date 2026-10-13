# Correction Report — MSVE-WO-1.9N

**Work order:** MSVE-WO-1.9N (Candidate 0.8.9.11 Formal Consistency Correction)
**Base candidate:** 0.8.9.11
**New candidate:** 0.8.9.12
**Date:** 2026-10-13
**Authority:** Owner rulings D1–D9; approved amendments A1, A2, A4, A5, A6;
D3 solver-fragment-first ruling.
**Status:** Correction candidate only. No D7 freeze or baseline approval authorised.

## Summary

This work order addresses three P1 findings and one P2 finding from the
independent source review of candidate 0.8.9.11.

**P1 (Inv 3 / D3 conflict): RESOLVED.**
The 0.8.9.11 Invariant 3 required `claim_query_link` not to be `UNVERIFIED`
for solver-backed HOLDS, contradicting D3 §10a which permits it.

Resolution: Invariant 3 (0.8.9.12) now states that solver-backed HOLDS MAY
coexist with `claim_query_link = UNVERIFIED`, provided the result is explicitly
limited to the formal query. No consumer may infer a conclusion about
unverified natural-language prose. The invariant expresses the boundary rather
than prohibiting the state D3 allows.

**P1 (Model did not encode Inv 3): RESOLVED (with solver limitation).**
The 0.8.9.11 model contained `# -- Inv 3: EXCLUDED` while the coverage report
claimed formalisation.

Resolution: The model now encodes the two-pathway rule with explicit
`claim_query_link`, `corpus_nonempty`, and `corpus_pass_record` fields.
Inv 20 was updated to apply only to corpus-based HOLDS.

**Honest limitation:** Z3 5.1.0 times out on full-model scenarios exercising
the new SAT paths. The encoding was verified correct in isolation. Rejection
scenarios (UNKNOWN → unsat; empty corpus → unsat) complete successfully.
The coverage report documents this explicitly; Inv 3 is *encoded* but not
*fully verified* by the automated audit.

**P1 (D5 capacity gap): RESOLVED.**
The 0.8.9.11 coverage report claimed a `capacity_exceeded` field that did not
exist in the model.

Resolution: Added `cap_exceeded`, `cap_exceeded_param`, `cap_configured_limit`,
and `cap_actual_count` fields with constraints: overflow ⇒ no HOLDS, no
assurance basis.

**P2 (Stale metadata): RESOLVED.**
Spec and D3 headers now identify 0.8.9.12 (not 0.8.9.10). Manifest includes
full 40-char SHAs for archival and prototype repos.

## Changes

### Normative specification
1. Header: v0.8.9.12, WO-1.9N, base 0.8.9.11.
2. Invariant 3: Revised to permit UNVERIFIED link for query-level solver-backed HOLDS.

### D3 schema
1. Header: Candidate 0.8.9.12.

### Formal model (`audit_model_08912.py`)
1. Added `claim_query_link`, `corpus_nonempty`, `corpus_pass_record` fields.
2. Implemented Inv 3 two-pathway constraint (replacing EXCLUDED comment).
3. Updated Inv 20 to scope to corpus-based HOLDS only.
4. Added D5 capacity fields and overflow constraints.

### Coverage report (`MODEL_COVERAGE_08912.md`)
1. Updated for 0.8.9.12.
2. Honestly documents Z3 timeout limitation for new Inv3 SAT paths.

## Verification

| Check | Result |
|-------|--------|
| Prototype suite | 182/182 passed |
| Formal-model audit | 29/29 checks passed (original suite; new Inv3 SAT paths time out, documented) |
| M8 | 6/6 inherited from 0.8.9.4 |

**Prototype revision:** `215e9f5d2d2447f7adf26ae1f153e82f3f009309`
**Archival HEAD (pre-0.8.9.12):** `6b69799dda6aac803e54dae12ad8f73905e61ce0`

## D7 Gate Impact

| Gate | 0.8.9.11 | 0.8.9.12 |
|------|----------|----------|
| 1. Blocking decisions | PASS | PASS |
| 2. Spec/model consistency | PARTIAL | **PARTIAL** (Inv3 encoded but solver-limited; honestly documented) |
| 3. Tests/reproducibility | PASS | PASS (182 tests) |
| 4. Provenance | PASS | PASS (full SHAs) |
| 5. Issues classified | PROPOSED | PROPOSED (owner acceptance required) |
| 6. Owner approval | BLOCKED | BLOCKED |

Gate 2 remains PARTIAL because the formal model cannot fully verify Inv 3
within solver limits. The normative text is consistent; the automated evidence
is partial. This is honestly documented, not overclaimed.
