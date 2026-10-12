# MSVE-WO-1.9E Correction Report — Candidate 0.8.9.5

**Work order:** MSVE-WO-1.9E (Type and Provenance Closure)
**Base:** Candidate 0.8.9.4
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN, NOT RELEASED

## Summary

Candidate 0.8.9.5 addresses the six findings from the owner's source review
of 0.8.9.4, plus metadata reconciliation. All changes are within the approved
design (D1–D9, A1/A2/A4/A5/A6, D3 Option A). No new owner decisions required.

## Findings and corrections

### 1. Capacity reason closure (Blocking)

**Finding:** §B.8a specified `INCONCLUSIVE{reason: "capacity-exceeded"}` but
the closed `ReasonCode` enum in §E.3 did not include it.

**Correction:** Added `CAPACITY_EXCEEDED` to the `ReasonCode` type (§E.3).
Updated §B.8a to use `INCONCLUSIVE{reason: CAPACITY_EXCEEDED}`. Updated
prototype `pipeline.py` and test to use the enum value instead of the string.

**Files:** `MSVE_DESIGN_SPEC_v0.8.9.5.md` (§B.8a, §E.3); prototype
`src/msve/pipeline.py`, `tests/test_wo19a_corrections.py`.

### 2. Type-correct evidence invariants (Blocking)

**Finding:** Invariants 26 and 27 compared `Hash` directly with
`Option<Hash>` (`sc.query_id = r.query_id`). The SAT-corroboration invariant
compared a witness `Hash` directly with an `ArtifactRef`.

**Correction:**
- Inv 26 Path 2: `r.query_id = Some(sc.query_id)` (was `sc.query_id = r.query_id`).
- Inv 26 Path 2: `∃ w ∈ r.evidence.witnesses: w.sha256 = sc.witness.artifact`
  (was `w = sc.witness.artifact`).
- Inv 27: `r.query_id = Some(i.query_id)` (was `i.query_id = r.query_id`).
- Inv 27b: `r.query_id = Some(i.query_id)` (was `i.query_id = r.query_id`).

**Files:** `MSVE_DESIGN_SPEC_v0.8.9.5.md` (§E.7); model clarified with
comment that `R['witnesses']` models the `sha256` fields of `ArtifactRef`s.

### 3. Execution-specific invocation provenance (Blocking)

**Finding:** `invocation_id = sha256(claim_id_hex + ":" + query_id_hex)` did
not uniquely identify an execution. Two runs with different configs,
timeouts, or solver versions would share the same ID.

**Correction:** Replaced with SHA-256 over a canonical encoding of the
complete invocation metadata:
- Claim ID, claim kind
- Query ID and canonical query payload bytes
- Inputs reference
- Specification version
- Solver tool, tool version
- Configuration string, timeout_ms (u32be)
- Unique execution nonce

Added `query_payload: String` and `execution_nonce: String` to
`SolverInvocation`. Defined uniqueness: duplicate `invocation_id` within an
`EvidenceBundle` is `INVALID_INPUT`. Defined consistency requirements linking
the observation's metadata to the invocation.

Added model invariant Inv 27c: the two invocation slots must have different
IDs.

Prototype: `_invocation_id()` now takes all 11 parameters and computes the
new scheme. The full invocation record is stored in `evidence["solver_invocations"]`.

**Note:** Hashing metadata records consistency, not authenticity. The spec
explicitly states this does not prove the solver actually produced the
recorded outcome.

**Files:** `MSVE_DESIGN_SPEC_v0.8.9.5.md` (§E.3, §E.7);
`audit_model_0895.py` (Inv 27c); prototype `src/msve/pipeline.py`.

### 4. Descriptor types and optionality

**Finding:** `ClaimDescriptor` declared `goal_ref, inputs_ref: Hash` but
encoding notes allowed null/absent. "All six fields mandatory" was ambiguous.

**Correction:** Changed type to `goal_ref: Option<Hash>, inputs_ref: Option<Hash>`.
Clarified: field KEYS are mandatory (missing key → `INVALID_INPUT`); values
may be null (encoded 0x00, representing `None`). Present values must be
non-empty strings (normative requires 64-char hex; prototype accepts
non-empty string as exploratory, documented).

**Files:** `MSVE_DESIGN_SPEC_v0.8.9.5.md` (§E.3); prototype
`src/msve/decode.py` (comment updated; validation already enforced
mandatory keys).

### 5. D3 language status rule

**Finding:** Schema said unknown language → `MALFORMED_INPUT` but also said
any other language value → `UNSUPPORTED`.

**Correction:** Distinguished:
- Missing, non-string, or structurally malformed `language` field → `MALFORMED_INPUT`
- Well-formed string naming an unimplemented language → `UNSUPPORTED`

**Files:** `D3_SOLVER_FRAGMENT_SCHEMA.md`; prototype `src/msve/queries.py`;
new tests `test_lang_missing_is_malformed`, `test_lang_nonstring_is_malformed`,
`test_lang_unsupported_is_unsupported`.

### 6. D1 diagnostic assurance wording

**Finding:** E.6a said "no basis substantiation applies to `INCONCLUSIVE`"
while E.6b permitted `SOLVER_BACKED{weak=true}` for `UNKNOWN`+`INCONCLUSIVE`.

**Correction:** Narrowed E.6a to refer to "ordinary claim-verification basis"
for "provable mathematical claims". Added explicit clarification that this
does not invalidate D1's permitted weak diagnostic chain, which records that
the solver was exercised (a diagnostic fact), not that the proposition was
proved. D2's prohibition takes precedence.

**Files:** `MSVE_DESIGN_SPEC_v0.8.9.5.md` (§E.6a).

### 7. Metadata reconciliation

- D3 schema title: "Candidate 0.8.9" → "Candidate 0.8.9.5"
- Spec footer: `MSVE_DESIGN_SPEC_v0.8.md` → `MSVE_DESIGN_SPEC_v0.8.9.5.md`
- Historical "30 disjuncts" note clarified as the earlier state; current
  count is 29
- Spec header: updated to 0.8.9.5/WO-1.9E; added implementation-status
  clarification distinguishing the authorized exploratory prototype from
  any unauthorized final/production implementation

## Verification

### Prototype test suite
- **Result:** 153/153 passed
- **Command:** `python3 -m pytest tests/ -q`
- **Environment:** Python 3.12.3, z3-solver 5.1.0.0, pytest 9.1.1
- **New tests:** 4 (invocation ID distinctness, language malformed/unsupported,
  invocation record in evidence)

### Formal model audit
- **Result:** 31/31 checks behaved as expected
- **Command:** `python3 run_audit_0895.py`
- **New invariant:** Inv 27c (invocation ID uniqueness)

### M8 grammar/example validation
- **Result:** 6/6 (preserved from 0.8.9.4; grammar and B.11/B.12 examples unchanged)
- **Note:** M8 runner had import issues in this environment; output preserved
  from 0.8.9.4 where the grammar was validated.

### Query identity vectors
- Preserved from 0.8.9.4 (`QUERY_ID_VECTORS.md`).

## Commits

- **Archival:** (to be recorded after push)
- **Prototype:** (to be recorded after push)
- **Content commit:** (to be recorded)

## Limitations

1. The prototype's descriptor validation accepts non-empty strings for
   `goal_ref`/`inputs_ref` rather than enforcing 64-char hex. This is
   documented as an exploratory gap; the normative requires `Hash`.
2. M8 was not re-run in this environment due to import issues; the grammar
   is unchanged from 0.8.9.4 (6/6).
3. The invocation uniqueness invariant in the model applies to the two
   modeled slots; a full bundle with N invocations would need N-way
   distinctness (not modeled).

## Owner review

Candidate 0.8.9.5 is ready for owner source review. Not approved, not frozen,
not released. Prior candidates 0.8.8.1, 0.8.9, 0.8.9.1, 0.8.9.2, 0.8.9.3
preserved unchanged.
