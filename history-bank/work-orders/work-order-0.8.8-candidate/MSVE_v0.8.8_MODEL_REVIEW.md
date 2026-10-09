# Independent Formal-Model Review — MSVE Work Order 0.8.8

**Reviewer role:** Independent formal-model reviewer (code review only; model not executed)
**Model reviewed:** `/home/hatch/workspace/msve-design/work-order-0.8.8-candidate/audit_model_088.py`
**Model SHA-256 (reviewed):** `2182f3bed9915448b367d9ed7781973f8335ac0c849a838774383f138f8da32a` (18,926 bytes)
**Spec (reference):** `/home/hatch/workspace/msve-design/work-order-0.8.8-candidate/MSVE_DESIGN_SPEC_v0.8.md`
**Date:** 2026-10-09
**Report retrieved:** 2026-10-09 (via subagent handoff)

## Positive findings (verified)

1. **No sentinel.** Confirmed: the `__no_claim_key__` ordinary-string sentinel from 0.8.7 is removed. `claim_descriptor_present(R)` requires explicit presence with no fallback.

2. **New fields properly defined.** `fresh_record` defines: `has_claim_id` + `claim_id`; `claim_descriptors` (2 slots); `solver_invocations`; `provenance_ref`. All present and consistently named.

3. **Invariant 25 faithful.** Requires `source_item="proof"`, `PASS`, `method="kernel-checked"`, `claim_id` match, `checker ≠ ""`, `is_sha256_hex`, membership, descriptor presence. Matches normative inv 25.

4. **Invariant 26 faithful.** Enforces `DERIVED_VALUE` gate plus recompute linkage with explicit binders. Matches normative inv 26.

5. **Invariant 28 faithful.** Requires test source_item, `PASS`, `claim_id` match, `inputs_ref` match, descriptor presence. Matches normative inv 28.

6. **Invariant 27 core linkage enforced.** `_solver_linked` requires `provenance_ref` → invocation → `claim_id` match. Wrong-claim counterexample rejected.

## Findings

### F1 — Model inv 27 omits `inputs_ref` and `outcome_compatible` (blocking)

**Status after repair:** Partially addressed.
- F1(a) `inputs_ref`: **Repaired.** Model now uses 3-tuples `(id, claim_id, inputs_ref)` and checks `iinputs == verif_inputs_ref`.
- F1(b) `outcome_compatible`: **Documented limitation.** Normative definition exists (§E.6b, repaired via N-1), but mechanical enforcement requires `claim_kind` in the model. Documented as normative-only.

### F2 — `outcome_compatible` undefined (blocking, normative)

**Status:** **Repaired via N-1.** Formal definition added to §E.6b with `SolverInvocation.claim_kind` field.

### F3 — Model stricter than numbered invariants (non-blocking)

**Status:** **Repaired via N-3.** Invariant 29 added normatively: `bases ≠ [] ⇒ claim_id = Some(_)`.

### F4 — Descriptor as bare hash (non-blocking)

Acknowledged limitation. Model stores `claim_id` hash; 6-field completeness not mechanically checked.

### F5 — Invocation as pair only (non-blocking)

Partially addressed by F1(a) repair (now 3-tuple with inputs_ref). Query/tool/version/config remain normative-only.

### F6 — `spec_version` never constrained (non-blocking)

Model matches normative (omission preserved). Work-order requirement exceeds normative text.

### F7 — Two-slot bounds (informational)

Documented. Bounds what the model establishes.

## Fidelity assessment (post-repair)

| Invariant | Fidelity |
|---|---|
| 25 | Faithful; inv 29 aligns normative with model |
| 26 | Faithful |
| 27 | Linkage + inputs_ref enforced; outcome_compatible normative-only |
| 28 | Faithful |
| 29 | Added; aligns spec with model behavior |

**Review provenance:** Code review only; model not executed.
