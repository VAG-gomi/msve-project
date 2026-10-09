# MSVE v0.8.5 F-20 Adjudication (Task 3)

**Finding:** invariant 10's "occurred at packaging" test covers only
`base_code(r) = "output-not-encodable"`, while `canonicalization-failure`
is also a packaging base code.
**Question:** must `canonicalization-failure` also trigger preservation of
the established semantic result?

## Normative texts inspected

1. **Invariant 10** (spec §E.7): "`execution = INTERNAL_ERROR(r)` ⇒ …
   if the failure occurred at packaging (`base_code(r) =
   output-not-encodable`), the established `semantic_result` is still
   recorded (D-019: a valid result with an unserializable output is never
   INVALID_INPUT)."
2. **`is_packaging_error`** (§B.9/§E.1): covers exactly
   `{output-not-encodable, canonicalization-failure}` (spec lines
   1097–1098).
3. **§G.2 / NEW-C2** (spec lines 1102–1108): `canonicalization-failure:
   <detail>` is a specified packaging failure, "joint with
   `output_packaging` per inv. 15b".
4. **Invariant 15b**: treats both packaging base codes uniformly —
   `PACKAGING_FAILED(r)` ⟺ `INTERNAL_ERROR(e)` with matching base code;
   `PACKAGING_OK` excludes `INTERNAL_ERROR` with either base code.
5. **Invariants 15, 16**: `PACKAGING_FAILED(_)` handling is uniform across
   both base codes (payload refs forced to `None`; the semantic result
   itself remains recorded).
6. **D-019 status model** (§G.2, spec lines 1488–1494): a value with no
   canonical form reaching packaging is not INVALID_INPUT; the
   established semantic result is still recorded.

## Adjudication: YES

`canonicalization-failure` must also trigger preservation. Reasons:

- The spec gives **no principled distinction** between the two base codes
  that would justify different preservation behavior. Every other rule
  touching packaging failures (15b, 15, 16, `is_packaging_error`) treats
  them uniformly; only invariant 10 singles out `output-not-encodable`.
- The D-019 rationale — "a valid result with an unserializable output is
  never INVALID_INPUT" — applies equally: a canonicalization failure at
  packaging means the computation was valid and only the canonical
  encoding failed. Dropping the semantic result would contradict the
  status model's intent.
- Under the reconciled 15b ⟸, any `INTERNAL_ERROR` with base code
  `canonicalization-failure` already forces `PACKAGING_FAILED`; leaving
  invariant 10 narrower creates an incoherent pair: the linkage is
  enforced but the preservation is not.

The narrower reading is therefore an oversight (the invariant was written
against the `output-not-encodable` case), not an intended distinction.

## Smallest coherent candidate correction

In invariant 10, replace:

```
if the failure occurred at packaging (`base_code(r) = output-not-encodable`)
```

with:

```
if the failure occurred at packaging (`is_packaging_error(r)`)
```

i.e. `base_code(r) ∈ {output-not-encodable, canonicalization-failure}`.
This uses the defined packaging-error semantics, touches one predicate in
one invariant, and aligns invariant 10 with 15b/15/16. Affected companion
documents: the candidate spec's §E.7 invariant 10 text only. No M8 change
(M8 does not evaluate this invariant). The full proposed text is in
`MSVE_v0.8.5_F20_CORRECTION_PROPOSAL.md` (proposal only — the candidate
is not modified).

## Targeted witnesses (solver-verified, z3 5.1.0)

- **F20-W (valid):** `INTERNAL_ERROR("canonicalization-failure: digest
  mismatch")` + `PACKAGING_FAILED("canonicalization-failure: blob exceeds
  1MiB")` (base codes match, details differ per F-01) +
  `DERIVED_VALUE(value_ref=None, derivation_ref → derivation_records)`.
  **SAT** under the current encoding and under the corrected invariant 10.
  The intended state is realizable either way.
- **F20-X (adversarial):** same record with `semantic_result = None`.
  **SAT under the current encoding** — confirming the gap: the spec as
  written permits dropping the established result on
  canonicalization-failure. **UNSAT under the corrected invariant 10** —
  the correction closes exactly this hole and nothing else (F20-W stays
  SAT).

Tool: `f20_adjudication.py` (all four checks behaved as expected).

## Remaining judgement (specification review, not solver-established)

The solver confirms the *mechanical* effect of the correction. The
*intent* judgement — that D-019's rationale extends to
canonicalization-failure — is specification review based on the textual
uniformity of 15b/15/16 and the absence of any stated distinction. If the
owner holds that canonicalization-failure can occur without an
established semantic result (e.g. failure while canonicalizing
not-yet-established intermediates), that would be a substantive semantic
claim requiring new normative text, not a reading of the current text.
