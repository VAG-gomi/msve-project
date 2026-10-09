# MSVE v0.8.5.2 F-20 Prose–Formula Alignment

**Work Order:** 0.8.5.2 · **Date:** 2026-10-09
**Artefacts inspected:** `MSVE_v0.8.5_F20_CORRECTION_PROPOSAL.md`,
`f20_adjudication.py` (0.8.5 directory).

## Proposed normative wording (from the correction proposal)

> `execution = INTERNAL_ERROR(r)` ⇒ … if the failure occurred at
> packaging (`is_packaging_error(r)`), the established `semantic_result`
> is still recorded.

## Formula actually tested (from `f20_adjudication.py`)

```python
ForAll([e], Implies(
    R['execution'] == Execution.INTERNAL_ERROR(e),
    Implies(Or(*[base_code(e) == H(c) for c in PACK_BASE]),
            R['has_semres'])))
```

i.e.

```
∀ r: ResultRecord. ∀ e: String.
  (r.execution = INTERNAL_ERROR(e) ∧ is_packaging_error(e))
  ⟹ r.semantic_result ≠ None
```

where `is_packaging_error(e) ⟺ base_code(e) ∈ {output-not-encodable,
canonicalization-failure}` (PACK_BASE extracted from the candidate spec,
27/3/12/2 counts verified) and `r.semantic_result ≠ None` is the
encoding's `has_semres` flag.

## Alignment assessment

**The condition aligns exactly.** "The failure occurred at packaging
(`is_packaging_error(r)`)" maps to `INTERNAL_ERROR(e) ∧
is_packaging_error(e)`: under the reconciled invariant 15b, an
`INTERNAL_ERROR` whose reason has a packaging base code is exactly the
packaging-failure joint state, so the prose condition and the formula
antecedent coincide. Both base codes (`output-not-encodable`,
`canonicalization-failure`) trigger the consequent — confirmed by the
F20-W/F20-X tests, which use `canonicalization-failure` reasons.

**The consequent aligns up to the accepted temporal weakening.**
"the established `semantic_result` is still recorded" (definite,
specific, temporal: *the* result established before packaging persists)
is rendered as `semantic_result ≠ None` (existential, atemporal: *some*
result is present). The prose entails the formula — if the established
result is still recorded, then a semantic result is present — but the
formula does not fully capture the prose: it cannot ensure it is the
*same* result, because the record schema is a single atemporal snapshot
and provides no pre-/post-packaging temporal model. This is the same
weakening the 0.8.4 reviewers accepted for invariant 10 as written
(A-02); the correction proposal inherits it rather than introducing it.

## Clearer invariant with all variables bound

```
∀ r: ResultRecord. ∀ e: String.
  (r.execution = INTERNAL_ERROR(e) ∧ is_packaging_error(e))
  ⟹ (∃ s: SemanticResult. r.semantic_result = Some(s))
```

All variables (`r`, `e`, `s`) are bound. This is exactly the tested
formula with the existential made explicit. A fully faithful rendering
of "the established result is *still* recorded" would require a temporal
record model the specification does not provide; within the atemporal
schema this is the maximal faithful constraint.

## Status of the F-20 correction

- The normative wording **does** entail the tested formula, for both
  base codes.
- F20-W stays SAT and F20-X goes UNSAT under the corrected formula, as
  reported (`f20_adjudication.py`, exit 0).
- **The specification is not corrected.** The candidate text is
  unchanged; the correction remains a proposal in
  `MSVE_v0.8.5_F20_CORRECTION_PROPOSAL.md` awaiting owner review of the
  wording. No claim is made beyond the mechanical effect demonstrated.
