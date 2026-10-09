# MSVE v0.8.6 F-20 Verification

**Finding:** invariant 10's packaging condition omitted
`canonicalization-failure`. **Status in candidate:** corrected.

## Normative change

Candidate spec §E.7 invariant 10 now reads (fully bound variables):
```
∀ r: ResultRecord. ∀ e: String.
  (r.execution = INTERNAL_ERROR(e) ∧ is_packaging_error(e))
  ⟹ r.semantic_result ≠ None
```
`is_packaging_error(e) ⟺ base_code(e) ∈ {output-not-encodable,
canonicalization-failure}` (spec §B.9/§E.1, lines 1097–1098).

## Consistency analysis (specification review)

- **Invariant 15b:** uniform across both base codes (biconditional +
  PACKAGING_OK exclusion). The corrected invariant 10 aligns with it;
  previously 10 was strictly narrower.
- **Invariants 15, 16:** `PACKAGING_FAILED(_)` handling is
  base-code-agnostic (payload refs → None; result itself preserved).
  Consistent.
- **`is_packaging_error`:** the defined predicate; the correction uses
  it directly rather than re-listing codes.
- **§G.2:** both `output-not-encodable: <type>` and
  `canonicalization-failure: <detail>` are specified packaging failures
  joint with `output_packaging` per 15b. Consistent.
- **D-019 status model:** "a valid result with an unserializable output
  is never INVALID_INPUT" — applies to both codes; the correction
  extends the protection the model already intended.

## Solver verification (z3 5.1.0; `run_audit_086.py`, exit 0)

| Case | Expected | Actual |
|---|---|---|
| R1: `output-not-encodable` failure, result present | sat | sat |
| R2: `canonicalization-failure` failure, result present | sat | sat |
| R3a: `output-not-encodable` failure, result missing | unsat | unsat |
| R3b: `canonicalization-failure` failure, result missing | unsat | unsat |

The original F20-W/F20-X pair is preserved: F20-W SAT under both old and
new text; F20-X SAT under old text (gap), UNSAT under corrected text.

## Temporal limitation (retained honestly)

The static record establishes the semantic result's presence and its
evidence linkage. It cannot prove the historical transition from the
pre-packaging to the post-packaging state, nor compare the current
result against an unavailable earlier state. This limitation is stated
in the corrected invariant's prose note.
