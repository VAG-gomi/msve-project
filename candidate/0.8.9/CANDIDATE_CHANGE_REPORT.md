# Candidate Change Report — 0.8.8.1 → 0.8.9 (WO-1.9)

**Status:** candidate for owner review. Not approved. Not frozen.
**Base:** `candidate/0.8.8.1/` (unmodified; hashes: spec `dbc610c3a97d…`,
model `fc6eb49f50ea…`, driver `c750ef5c37a1…`).
**New:** `candidate/0.8.9/` (this directory).
**Authority:** owner rulings D1–D9; approved amendments A1, A2, A4, A5, A6;
D3 scope ruling Option A (solver-fragment first), all 2026-10-11.

## A1 — D1 weak SOLVER_BACKED (DEC-027)

- **Spec:** §E.5 UNKNOWN row extended: genuine UNKNOWN + INCONCLUSIVE may
  carry weak SOLVER_BACKED; never a positive conclusion; observation bound
  to claim, query, spec version; timeout-induced UNKNOWN is the
  demonstrated case; D2 bar takes precedence.
- **Model:** Inv 30 (`WEAK_SOLVER_BACKED` basis; requires UNKNOWN +
  INCONCLUSIVE; excludes HOLDS/VIOLATED).
- **Prototype:** `pipeline.py` binds `claim_id` and `spec_version` into
  the solver observation (new); `assurance.py` weak chain unchanged
  (verified).
- **Tests:** model W1 (consistent) / W2 (HOLDS rejected);
  `test_wo19_amendments.py::test_a1_*` (2).

## A2 — D2 assurance bar (DEC-028)

- **Spec:** §E.5 seven-kinds paragraph strengthened: no SOLVER_BACKED,
  weak or otherwise, via admission or direct assurance evaluation; bar
  evaluated before the D1 exception.
- **Model:** Inv 31 (seven kinds → ¬SOLVER_BACKED ∧ ¬WEAK_SOLVER_BACKED).
- **Prototype:** `admission.py` / `assurance.py` unchanged (verified
  already correct).
- **Tests:** model W3 (contradiction + weak rejected) / W3b (no_solution
  + strong rejected); existing `test_wo13_hardening.py` (14 cases).

## A4 — D4 checker independence (DEC-029)

- **Spec:** §E.6a recompute basis extended: separately implemented
  validation core; disclosed shared infrastructure; lineage; claim/query/
  spec-version/checker/bound/execution binding; independently produced
  checkable witness for SAT; no-witness → INCONCLUSIVE, never UNSAT
  proof; common-mode failures and lying checker remain trust boundaries.
- **Model:** Inv 33 (INDEPENDENT_RECOMPUTE → checker_independent ∧
  witness_checkable); vr slots extended.
- **Prototype:** `checker.py` / `DEPENDENCIES.md` unchanged (verified
  already correct: 0 z3 refs, disclosed sharing).
- **Tests:** model W5 (non-independent checker rejected).

## A5 — D5 explicit capacity (DEC-030)

- **Spec:** new §B.8a: `max_verification_records` 10000 (1–1,000,000);
  `max_descriptors` 1000 (1–100,000); precedence explicit > embedded >
  defaults; out-of-range → `INVALID_INPUT` (`capacity-out-of-range`,
  `capacity-not-an-object`, `capacity-missing-key`); overflow → explicit
  recorded failure; no silent truncation. Closed admission-error list
  extended 27 → 30 codes.
- **Error-code reconciliation:** the amendment draft used INVALID_INPUT;
  the prototype used INVALID_CONFIG. **Resolved for INVALID_INPUT**,
  following the spec's existing precedent
  (`INVALID_INPUT(timeout-out-of-range)`, §B.8). The prototype's
  `INVALID_CONFIG` is retired; contract and runtime agree.
- **Model:** Inv 34 (capacity ranges); codelists extended.
- **Prototype:** `capacity.py` (normative bounds/defaults; INVALID_INPUT);
  `config/default.json` (10000/1000); contract §1/§6 updated.
- **Tests:** model W6; `test_wo19_amendments.py::test_a5_*` (5);
  updated `test_admission.py`, `test_schema_alignment.py`.

## A6 — D6 msve-descriptor-1 (DEC-031)

- **Spec:** §E.6b `|`-joining replaced by `msve-descriptor-1`: null/absent
  → `0x00`; else `0x01` + u32be length + NFC UTF-8; assumptions sorted
  bytewise, u32be count + tagged elements (explicit collection boundary);
  fixed field order; encoding version hashed into the preimage (version
  binding); SHA-256, lowercase hex. Prospective only: historical hashes
  never recomputed.
- **Model:** Inv 35 (claim_id present → encoding = `msve-descriptor-1`);
  byte-level framing verified by Python vectors (documented as beyond
  Z3's expressible scope).
- **Prototype:** `identity.py` rewritten to `msve-descriptor-1`;
  `ENCODING.md` rewritten; `vectors/canonical_vectors.json` 7 → 16
  (recomputed under new encoding + new cases: empty/multi/duplicate
  assumptions, null vs empty, boundary attacks, NFC, version binding).
- **Tests:** model W7; `test_wo19_amendments.py::test_a6_*` (5);
  `test_identity.py` (10, all passing under new encoding).

## D3 — solver fragment (DEC-032, scope Option A)

- **New normative document:** `D3_SOLVER_FRAGMENT_SCHEMA.md`:
  `msve-arith-v1` input schema, declarations/types/binding, operators and
  semantics, typing rules, assertion requirements, kind/outcome mappings,
  **assumptions as non-semantic metadata** (recorded, in identity, never
  in solver reasoning; assurance attaches to the query as stated),
  admission/rejection/unsupported/underspecified, query/claim identity
  and provenance, solver-vs-prose boundary (`claim_query_link:
  UNVERIFIED` preserved). Other kinds' schemas explicitly deferred.
- **Spec:** new §E.4a referencing the schema document.
- **Model:** Inv 32 (solver-backed assurance → `query_language =
  "msve-arith-v1"`).
- **Prototype:** `queries.py` verified against the schema (no change
  needed); contract §3/§10 consistent.
- **Tests:** model W4; `test_wo19_amendments.py::test_d3_*` (2).

## Files changed (archival)

- `candidate/0.8.9/` (new): spec, model, driver, D3 schema.
- `decision-ledger/MSVE_BRAINSTORM_DECISION_LEDGER.csv`: DEC-027–DEC-032.
- `candidate/0.8.8.1/`: unmodified.

## Files changed (prototype)

- `src/msve/identity.py`, `capacity.py`, `pipeline.py`
- `config/default.json`, `ENCODING.md`, `PROTOTYPE_CONTRACT.md`,
  `DECISION_TRACEABILITY.md`, `README.md`
- `vectors/canonical_vectors.json` (16)
- `tests/test_wo19_amendments.py` (new, 14), `test_admission.py`,
  `test_schema_alignment.py` (error-code updates)

## Compatibility and transition effects

- Claim identities change (encoding version in preimage): all
  pre-0.8.9 `claim_id` values are historical and must not be recomputed.
- Error code `INVALID_CONFIG` → `INVALID_INPUT` (with reason strings).
- Capacity defaults for the two normative parameters increase to
  10000/1000 (previously 2/2 in the prototype).
- No other behavioural changes; all 114 pre-existing tests pass
  unmodified except the two error-code assertions.
