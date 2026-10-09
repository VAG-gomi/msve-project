# MSVE v0.8.8 — Claim Identity and Solver Linkage Design Note

## Claim identity (Option A, implemented)

**Design:** `ClaimDescriptor` with `claim_id = sha256(canonical_encoding)`.
Canonical encoding: `claim_kind|proposition|goal_ref|inputs_ref|assumptions|spec_version`.

**Identity policy:** Syntactic. Distinct goal/proposition/inputs →
distinct `claim_id`, even if outputs coincide. Owner selected this
direction; semantic equivalence not attempted.

**Why not output hash:** `derive 2+2` and `derive 8/2` share output `4`
but are different mathematical claims (different propositions). Test C1
confirms a proof for one does not satisfy the other.

**Payload-free variants:** `HOLDS`, `NO_SOLUTION`, `CONTRADICTION`,
`UNIQUE_UNDER_PROJECTION` use descriptors with their check property /
search problem as `proposition`. No output hash needed. Test C3
confirms `HOLDS` + `TEST_BACKED` works.

**No sentinel:** Missing `claim_id` (`has_claim_id` false) or absent
descriptor → basis rejected (C4, C5). The `__no_claim_key__` string is
deleted.

## Solver linkage (implemented)

**Design:** `evidence.solver_invocations: [SolverInvocation]` with
`invocation_id`, `claim_id`, `query`, `inputs_ref`, `spec_version`,
`tool`, `version`, `config`. `SolverObs.provenance_ref` must equal an
`invocation_id` whose `claim_id` matches the result's.

**Four conditions (separate):**
1. Observation recorded (`has_solver`).
2. Correctly linked (`provenance_ref` → invocation → `claim_id` match).
3. Outcome compatible (per §E.6b interpretation table; currently
   minimal — see limitation).
4. Assurance justified (inv 27).

**Limitation:** Outcome compatibility is currently only the linkage
(claim_id match), not a full per-goal interpretation table. The
interpretation table (holds+UNSAT→HOLDS, etc.) is normative (§E.6b)
but not fully encoded. Tests S6/S8/S9 verify linkage rejection; S7
verifies linked acceptance.

## Schema changes (all in 0.8.8 candidate, pending owner acceptance)

1. `ResultRecord.claim_id: Option<Hash>` (new).
2. `VerificationRecord.claim_id: Hash` (new).
3. `EvidenceBundle.claim_descriptors: [ClaimDescriptor]` (new).
4. `EvidenceBundle.solver_invocations: [SolverInvocation]` (new).
5. `ClaimDescriptor` type (new).
6. `SolverInvocation` type (new).

No existing field semantics changed.
