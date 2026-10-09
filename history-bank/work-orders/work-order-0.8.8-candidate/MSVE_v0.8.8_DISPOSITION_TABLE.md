# MSVE v0.8.8 — Finding Disposition Table

## R1-1: Claim identity for payload-free variants

**Disposition:** ADDRESSED via Option A.
- `ClaimDescriptor` with `claim_id` covers all variants including
  `HOLDS`, `NO_SOLUTION`, `CONTRADICTION`, `UNIQUE_UNDER_PROJECTION`.
- Test C3 verifies `HOLDS` + `TEST_BACKED` with valid descriptor.
- No sentinel; missing identity → explicit rejection (C4, C5).

## Solver linkage: SOLVER_BACKED for different claim

**Disposition:** ADDRESSED.
- Invariant 27 requires `provenance_ref` → invocation → `claim_id` match.
- Test S6 verifies UNSAT(A) + result(B) rejected.
- Tests S8/S9 verify provenance resolution.

## provenance_ref: undefined target

**Disposition:** ADDRESSED.
- Normatively defined: must equal `invocation_id` in
  `evidence.solver_invocations` (§E.6b).
- Mechanically enforced via `_solver_linked`.

## Model fidelity: claim_key sentinel

**Disposition:** ADDRESSED.
- `claim_key()` and `__no_claim_key__` deleted.
- Replaced by `claim_id` field + `claim_descriptor_present`.

## Verification provenance: 18/18 not tied to final model

**Disposition:** ADDRESSED.
- Fresh 16/16 run targets final files (hashes below).
- Raw log preserved with timestamp.

## Independent model review (v0.8.7)

**Disposition:** ADDRESSED (for 0.8.8).
- Independent normative review completed 2026-10-09T14:41:14Z.
  **Three blocking findings:** N-1 (`outcome_compatible` undefined in
  inv 27), N-2 (`ClaimDescriptor.claim_id` field/method ambiguity),
  N-3 (no invariant requires `bases ≠ [] ⇒ claim_id = Some(_)` —
  `claim_id = None` + basis evades inv 25–28 vacuously). Reviewer
  classifies these as drafting repairs, not owner decisions.
- Independent model review: [pending].

## Reviewer reconciliation

Normative reviewer verdict: Option A design sound, prose explicit, but
N-1/N-2/N-3 block formal completeness.

**Repairs applied 2026-10-09 ~14:45 UTC:**
- N-1: `outcome_compatible` formally defined in §E.6b; `SolverInvocation`
  gains `claim_kind` field.
- N-2: `ClaimDescriptor.claim_id: Hash` added as stored field with
  well-formedness comment.
- N-3: Invariant 29 added: `bases ≠ [] ⇒ claim_id = Some(_)`.
- Model updated with invariant 29; 16/16 tests re-run and pass; fresh
  raw log preserved.

**Model reviewer status:** Completed 2026-10-09T14:41:35Z, but detailed
findings could not be retrieved from the session archive. Reconciliation
of model-reviewer findings is therefore incomplete. Per work-order
§8, status is BLOCKED — INDEPENDENT REVIEW INCOMPLETE.
