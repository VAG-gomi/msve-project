# Correction Report — WO-1.9A (Candidate 0.8.9 → 0.8.9.1)

**Status:** correction candidate for owner review. Not approved. Not frozen.
**Base:** `candidate/0.8.9/` (reviewed candidate, preserved unchanged).
**New:** `candidate/0.8.9.1/` (this correction revision; retains design-spec
version 0.8).
**Authority:** D1–D9; A1, A2, A4, A5, A6; D3 scope Option A.

## Finding 1 — A5 admission-error predicate (C1)

**Gap:** spec listed 30 admission-error codes but `is_admission_error`
had 27 disjuncts (the three `capacity-*` codes missing from the predicate).
**Correction:** added the three disjuncts; prose list, predicate,
codelists, and model assertion (30) reconciled. Inv 1b covers the new
codes via the updated codelists.
**Evidence:** model scenario C1 (30/30 accepted, 3 unknown rejected);
`MSVE_DESIGN_SPEC_v0.8.9.1.md` §B.9.

## Finding 2 — D1 query-identity binding gap (C2)

**Gap:** D3 schema referenced a result-record `query_id` field the E.1
schema never declared; invocation identity used an undocumented
delimiter scheme.
**Correction:**
- E.1 `ResultRecord` gains `query_id: Option<Hash>`; `SolverInvocation`
  gains `query_id: Hash`.
- Normative binding rules (i)–(iv): result query_id = invocation
  query_id; invocation claim_id/spec_version = result's;
  provenance_ref resolves to the invocation; mismatch blocks
  SOLVER_BACKED (weak or strong).
- `invocation_id = sha256(claim_id_hex + ":" + query_id_hex)` with both
  operands fixed 64-char hex — the delimiter is at deterministic byte 64,
  parse unique without further framing (precise justification, normatively
  stated). Prototype asserts the widths.
- Prototype result record gains top-level `query_id`.
**Evidence:** model C2a (stale query_id rejected), C2b (claim_id mismatch
rejected), C2c (correct linkage accepted); prototype
`test_wo19a_corrections.py::test_c2_*` (3).

## Finding 3 — checker-witness vs derived-value recomputation (C3)

**Gap:** Inv 33 required a checkable witness for every
INDEPENDENT_RECOMPUTE, but derived-value recomputation (path 1) involves
no witness; the SAT-corroboration path (path 2) was not distinguished
from it in the model, and Inv 26 blocked path 2 entirely (required
DERIVED_VALUE).
**Correction:**
- Spec §E.6a: three paths distinguished normatively — (1) derived-value
  equality, (2) SAT corroboration with independently generated witness
  checked against the exact formal query, (3) bounded no-witness →
  INCONCLUSIVE. No new basis invented.
- Model: Inv 26 revised to allow path 1 OR path 2; Inv 33 scoped so the
  witness requirement applies only when `sat_corroboration` is true.
- Prototype: `checker.validate_witness()` added; `agrees_with_solver`
  validates the witness and returns it; recompute record carries the
  validated witness.
**Evidence:** model C3a (derived-value needs no witness), C3b (SAT +
witness accepted), C3c (SAT without witness rejected); prototype
`test_wo19a_corrections.py::test_c3_*` (4).

## Finding 4 — A6 scalar types and normalization (C4)

**Gap:** type representation and normalization policy under-specified;
null/empty/absent distinctions per field unstated.
**Correction:** normative text now states: types by FIXED TYPED FIELD
POSITIONS with mandatory validation (the 0x00/0x01 tag distinguishes
null/absent from present only — not a type tag); encoder NORMALISES to
NFC (not rejection); recorded fields stored verbatim, identity over the
normalised encoding; per-field null/empty/absent rules
(kind/proposition/spec_version required non-empty; goal_ref/inputs_ref
null-or-non-empty with "" ≠ null; assumptions required list of
non-null strings). Prototype `decode.py` relaxed to permit null refs;
`ENCODING.md` and `identity.py` updated.
**Evidence:** prototype `test_wo19a_corrections.py::test_c4_*` (4);
16 golden vectors (null-vs-empty, NFC pairs).

## Finding 5 — capacity-parameter inventory (C5)

**Gap:** relationship between normative A5 parameters and
prototype-specific limits unclear.
**Correction:** `CAPACITY_INVENTORY.md` documents every parameter's
source, default, range, precedence, and overflow behaviour; disambiguates
`max_descriptors` (normative: claim descriptors per run) from
`max_invocations` (prototype: solver runs). A5 values unchanged.
**Evidence:** document + existing A5 tests.

## Finding 6 — version and source identity (C6)

**Correction:** spec header identifies 0.8.9.1 as a correction revision
of the 0.8.9 review candidate, retaining design-spec version 0.8.
`CANDIDATE_MANIFEST_0891.md` (this directory) lists full SHAs/hashes and
marks normative vs supporting artefacts. All historical candidates and
decision records preserved; nothing described as accepted or frozen.

## Verification summary

| Check | Result |
|---|---|
| Formal model audit | **24/24** behaved as expected (exit 0) |
| Prototype suite | **139/139** passed |
| Golden vectors | 16/16 match |
| UNKNOWN experiment | reproduced (genuine, timeout) |
| M8 spec-examples | skipped (tooling path-bound to v0.8 filename; pre-existing; amended sections don't touch grammar/examples) |

No test success manufactured; no expected outputs altered to hide
discrepancies.
