# Correction Report — MSVE-WO-1.9M

**Work order:** MSVE-WO-1.9M (D3 Result Semantics and D7 Model Consistency)
**Base candidate:** 0.8.9.10
**New candidate:** 0.8.9.11
**Date:** 2026-10-12
**Authority:** Owner rulings D1–D9; approved amendments A1, A2, A4, A5, A6;
D3 solver-fragment-first ruling.
**Status:** Not approved; no freeze, baseline, or release authorised.

## Summary

This work order resolves two specification-level blockers identified in the
independent D7 review of candidate 0.8.9.10, plus completes the formal-model
coverage assessment and normative document reference resolution.

**Blocker 1 (D3 outcomes vs ResultRecord): RESOLVED.**
The D3 schema used `MALFORMED_INPUT` and `UNDERSPECIFIED` as outcomes, but
the normative `ResultRecord` only defined `ACCEPTED`, `INVALID_INPUT`, and
`UNSUPPORTED` admission states.

Resolution (spec §E.3a):
- D3 `MALFORMED_INPUT` → `INVALID_INPUT(reason: AdmissionError)` with
  query-structure error codes. The D3 label is descriptive; normatively
  these are admission rejections.
- D3 `UNDERSPECIFIED` → `ACCEPTED` + `INCONCLUSIVE{reason:
  UNDERSPECIFIED_ASSUMPTIONS}` (new reason code). The query is well-formed;
  the limitation is in the claim's assurance requirements. No assurance
  basis is awarded.
- D3 `UNSUPPORTED` → `UNSUPPORTED(reason: UnsupportedReason)` (unchanged).

This preserves all three D3 distinctions without inventing new admission
outcomes or silently collapsing underspecification.

**Blocker 2 (Two HOLDS pathways): RESOLVED.**
D3 maps `holds` + UNSAT(negation) → `HOLDS`, but Invariants 3 and 20 required
non-empty corpus + verification record for all HOLDS.

Resolution (Inv 3 and Inv 20 revised):
- **Corpus-based HOLDS:** requires non-empty check corpus AND passing
  verification record. Anti-vacuity preserved.
- **Solver-backed HOLDS:** requires UNSAT observation + provenance binding
  (query_id, claim_id, spec_version). Does NOT require corpus.
- Neither path allows vacuous HOLDS.
- `claim_query_link: UNVERIFIED` boundary preserved: solver results apply
  to the formal query, not the natural-language proposition.

## Changes

### Normative specification (`MSVE_DESIGN_SPEC_v0.8.9.11.md`)
1. §E.3: Added `UNDERSPECIFIED_ASSUMPTIONS` to INCONCLUSIVE reason codes.
2. §E.3a (new): D3 outcome mapping table with rationale.
3. `ReasonCode` type: Added `UNDERSPECIFIED_ASSUMPTIONS`.
4. Invariant 3: Revised to two-pathway disjunction.
5. Invariant 20: Revised to distinguish corpus vs solver-backed requirements.
6. Normative document references: Updated to candidate-local paths with hashes.

### D3 schema (`D3_SOLVER_FRAGMENT_SCHEMA.md`)
1. UNDERSPECIFIED outcome: Added normative mapping note.
2. §10a (new): Solver-backed vs corpus-based HOLDS distinction.

### Formal model (`audit_model_08911.py`)
1. Docstring updated for 0.8.9.11 changes.
2. Invariant 3 now formalised (two-pathway).

### Supporting documents (new in candidate)
1. `MODEL_COVERAGE_08911.md`: Property-by-property coverage report.
2. `MSVE_CAPABILITY_MATRIX_v0.8.md`: Canonical copy with hash.
3. `MSVE_ACCEPTANCE_PLAN_v0.8.md`: Canonical copy with hash.
4. `MSVE_REGRESSION_LEDGER_v0.8.md`: Canonical copy with hash.

### Prototype
1. `tests/test_wo19m_d3_mapping.py`: 4 new regression tests.
2. Full suite: 182 passed (178 + 4 new).

## Verification

| Check | Result |
|-------|--------|
| Prototype suite | 182/182 passed |
| Formal-model audit | 32/32 behaved as expected |
| Genuine UNKNOWN experiment | Not re-run (semantics unchanged for UNKNOWN path) |
| M8 | 6/6 inherited from 0.8.9.4 |

## D7 Gate Impact

| Gate | Before | After |
|------|--------|-------|
| 1. Blocking decisions closed | PARTIAL | **PASS** (D3 mapping resolved) |
| 2. Spec/model consistency | PARTIAL | **PASS** (HOLDS pathways reconciled; coverage documented) |
| 3. Tests/reproducibility | PASS | PASS (182 tests, 32 checks) |
| 4. Provenance gaps | PASS* | **PASS** (normative docs hashed and included) |
| 5. Issues classified | BLOCKED | **PROPOSED** (register below; owner acceptance required) |
| 6. Owner approval | BLOCKED | BLOCKED (owner decision required) |

## Proposed Blocking/Non-Blocking Register (for owner review)

**Blocking (must resolve before freeze):**
- None identified in this work order. The two D7 blockers are resolved.

**Non-blocking (documented limitations for owner acceptance):**
1. Formal model excludes Inv 12 (policy judgment) — owner must assess Level B sufficiency.
2. Formal model weakens Inv 20/21/23 — alternative evidence identified in coverage report.
3. Two-slot abstractions — scale properties covered by prototype tests, not model.
4. M8 6/6 inherited from 0.8.9.4 — not re-run on 0.8.9.11.
5. Solver soundness assumed — not proven by model.

**Owner decision required:** Accept or reject the above limitations; approve or
defer D7 freeze.

## Files in candidate 0.8.9.11

See `CANDIDATE_MANIFEST_08911.md` for full manifest with SHA-256 hashes.
