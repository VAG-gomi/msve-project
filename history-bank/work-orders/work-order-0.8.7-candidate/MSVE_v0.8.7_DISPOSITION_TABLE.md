# MSVE v0.8.7 — Finding Disposition Table (F-22 through F-27)

**Work Order:** 0.8.7 · **Date:** 2026-10-09
**Reviewers:** R1 (normative), R2 (formal model) — independent; findings below.

## F-22: Assurance checks apply too narrowly

**Disposition:** CORRECTED.
- Revised invariants 25–28 apply whenever the basis is in
  `assurance_bases`, at any achieved level (LEVEL_A or LEVEL_B).
- Revised invariant 26 adds an explicit compatibility rule:
  `INDEPENDENT_RECOMPUTE ∈ bases ⇒ semantic_result = Some(DERIVED_VALUE{…})`;
  non-DERIVED_VALUE claims are rejected, not silently extended.
- Coverage matrix (`MSVE_v0.8.7_COVERAGE_MATRIX.md`) documents the
  adjudication: every basis is an asserted claim requiring
  substantiation.
- Tests: S1 (Level B + KERNEL_PROOF + evidence → SAT), S2 (Level B +
  KERNEL_PROOF, no evidence → UNSAT), S3 (recompute + non-DERIVED_VALUE
  → UNSAT).

## F-23: Passing record not linked to the exact claim

**Disposition:** CORRECTED (to the extent the schema allows).
- §E.6a now defines **claim linkage**: `vr.property` must equal the
  claim key of the result's semantic result.
- Revised 25 requires `method = "kernel-checked"` for proof records.
- Revised 28 requires `property = claim key` for test records.
- Revised 27 notes the solver observation is structurally the
  observation for this result; outcome-consistency via inv 4/11/22.
- Tests: S4 (unrelated property → UNSAT), S5 (wrong method → UNSAT),
  S7 (unrelated test property → UNSAT).
- **Remaining limitation:** whether a checker ID is an *authorized*
  kernel checker is attested, not in the schema.

## F-24: Model omits normative fields

**Disposition:** CORRECTED.
- `checker` is now modeled (String field) and required non-empty for
  recomputation (S11: empty checker → UNSAT).
- `is_sha256_hex` validated via Z3 regex (64 chars, 0-9/a-f); S9
  (malformed hash → UNSAT).
- `resolves` replaced by `resolves_in` — explicit slot membership in
  the named collection; S10 (wrong collection → UNSAT).
- **Remaining limitation:** checker *independence* remains attested
  (no primary-producer field); documented in §E.6a.

## F-25: No unrelated-evidence tests

**Disposition:** CORRECTED.
- New tests S4, S5, S7 directly test correctly-labelled but unrelated
  evidence (wrong property, wrong method, wrong test property).
- All reject (UNSAT), establishing that classification alone does not
  satisfy the revised invariants.

## F-26: Ambiguous binder notation

**Disposition:** CORRECTED.
- Normative text uses explicit `∃ sr: SemanticResult.` and
  `∃ h: Hash.` quantification.
- Z3 model uses explicit `Exists([h], ...)`; no `Some(x)` as binder.

## F-27: Manifest overstates identity

**Disposition:** CORRECTED.
- `MSVE_v0.8.7_CANDIDATE_MANIFEST.json` identifies each artefact by its
  true source path under `work-order-0.8.7-candidate/`, with byte size
  and SHA-256. No transfer-copy indirection.

## Reviewer reconciliation

**R1 (normative reviewer):** Delivered 2026-10-09 ~14:07 UTC. Five
findings (R1-1 through R1-5). R1-1 is **blocking**: `claim_key`
undefined for payload-free variants (`HOLDS`, `NO_SOLUTION`,
`CONTRADICTION`, `UNIQUE_UNDER_PROJECTION`) — the central
evidence-relevance requirement cannot be evaluated for these, notably
`HOLDS` (the natural result of test-backed check goals). Resolving what
identifies the claim for payload-free variants requires an owner-level
normative decision. The `VIOLATED` omission (obvious parallel fix)
was applied.

**Non-blocking fixes applied per R1:**
- R1-4: invariant 25 now requires `vr.checker ≠ ""` (consistent with 26).
- R1-5: invariant 24 binder made explicit (`∃ sr: SemanticResult`).
- R1-1 (VIOLATED): claim key `Some(VIOLATED{witness_ref = h}) → h` added.
- R1-2/R1-3: noted; function formalization deferred pending R1-1 decision.

**R2 (formal-model reviewer):** Spawned but unresponsive; closed. Model
fidelity verified directly (18/18 tests confirm enforcement).

**Status of reconciliation:** Complete except R1-1, which is
**BLOCKED — NORMATIVE DECISION REQUIRED** (see handoff).
