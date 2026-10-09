# MSVE v0.8.4 Formalization Reconciliation (Phase B)

**Work Order:** 0.8.4 · **Date:** 2026-10-09
**Sources:** `formalization-A-draft.md`, `formalization-B-draft.md`
(both derived independently from candidate spec SHA-256
`9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`).

## Agreement (substantive convergence)

- Typed models match: all 11 `SemanticResult` alternatives with exact
  payload fields, exact assurance field names, `VerificationRecord`
  (incl. `inputs_ref: Hash`, `required: Bool`), `EvidenceBundle`
  collections, `PartialResult`, `Discrepancy`.
- Invariants 1, 1b, 2, 4, 5, 6, 7, 8, 9, 11, 13, 14, 17, 18, 19: identical
  in substance.
- Both mark invariants 3 and 12 **unformalizable** (external references:
  "the check corpus", "the frozen spec"). Excluded from solver encoding.
- Both mark 20, 21, 23 as **weakened** (A-06/A-07/A-08 = AMB-20/AMB-21/AMB-23):
  "for the check property", "a search record", and the vacuous projection
  binding `p` have no schema-level discriminator.
- Both define `resolves(h, L)` as hash-membership and flag it as an
  *interpretation*, not a quoted rule (A-04 / AMB-R1).
- Both render invariant 10's "still recorded" as `semantic_result ≠ None`
  and note the vacuous "reason is recorded".
- Variable bindings verified by both; invariant 14's `required` correctly
  scoped to `VerificationRecord.required`.

## Disagreements resolved

### R1 — Invariant 15b ⟸ direction (A-05 vs B's biconditional)

- A: the ⟸ direction as written leaves `r` unbound and, read literally,
  contradicts NEW-C2's open `INTERNAL_ERROR` domain; proposes a restricted
  reading (packaging base codes only) and requests an owner decision.
- B: formalizes the biconditional universally and notes non-packaging base
  codes are "unconstrained — correctly so, since then no `r` with matching
  base code exists."

**Resolution:** B's universal-universal reading is too strong — it would
force `PACKAGING_FAILED(r)` for *every* `r` sharing a base code, including
`r` strings the record never carried. A's restricted existential reading
is adopted:

```
(execution = INTERNAL_ERROR(e) ∧ base_code(e) ∈ PackBase)
⟹ ∃p. (output_packaging = PACKAGING_FAILED(p) ∧ base_code(p) = base_code(e))
```

This is not a free owner choice: it is the *only* reading consistent with
NEW-C2 (open `INTERNAL_ERROR` reasons such as `division-by-zero` must not
force packaging failure) and with the second paragraph of 15b. The literal
universal reading is rejected as inconsistent with the rest of the spec.
Recorded here as a resolved formalization decision, not a spec defect —
but the spec's prose should eventually state the ⟸ direction existentially.

### R2 — Invariant 10 omits `canonicalization-failure` (B's AMB-10; new finding)

B observes invariant 10's "occurred at packaging" test mentions only
`base_code(r) = "output-not-encodable"`, leaving `canonicalization-failure`
packaging errors outside its "semantic_result still recorded" consequent.
A formalized the same text without flagging the gap.

**Resolution:** confirmed as a genuine coverage gap in the candidate spec.
Invariant 15b's second paragraph covers both packaging base codes, but
invariant 10's conditional does not. **New finding F-20** (see consistency
report): invariant 10 should test `base_code(r) ∈ PackBase`.

### R3 — Invariant 16's "or" (convergent)

A and B agree in substance (inclusive-or; the inner biconditional forces
`PACKAGING_FAILED ⟹ artifact_ref = None` for `ARTIFACT_CONSTRUCTED`).
A's note about interaction with invariant 15's structure is acknowledged:
the two invariants jointly determine `artifact_ref`/`value_ref` handling
across the two packaging states with no conflict. No action needed.

## Unified formalization adopted for Phase D

The reconciled constraint set = A's formalizations with:
- 15b's ⟸ replaced by the restricted existential reading (R1);
- invariants 3 and 12 **excluded** (unformalizable);
- invariants 20, 21, 23 in weakened form (existential, with logged caveat);
- `resolves` as hash-membership (interpretation, logged);
- invariant 10 as written (with F-20 gap noted, not silently repaired).

Every disagreement was resolved by citing normative text (NEW-C2, §E.1,
the `PackagingError` definition) except R2, which is recorded as a new
finding for the owner rather than a silent fix.
