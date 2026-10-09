# MSVE v0.8.5 F-20 Correction Proposal (candidate text, not applied)

**Status:** PROPOSAL ONLY. The v0.8.3 candidate documents are unchanged.
This text is offered for a future correction pass if the owner accepts
the F-20 adjudication.

## Current invariant 10 text (candidate spec §E.7)

> `execution = INTERNAL_ERROR(r)` ⇒ the `reason` field `r` is recorded; if the failure
> occurred at packaging (`base_code(r) = output-not-encodable`),
> the established `semantic_result` is still recorded (D-019: a valid
> result with an unserializable output is never INVALID_INPUT).

## Proposed replacement

> `execution = INTERNAL_ERROR(r)` ⇒ the `reason` field `r` is recorded; if the failure
> occurred at packaging (`is_packaging_error(r)`, i.e. `base_code(r) ∈
> {output-not-encodable, canonicalization-failure}`),
> the established `semantic_result` is still recorded (D-019: a valid
> result with an unserializable output is never INVALID_INPUT).

## Rationale

Aligns invariant 10 with the defined `is_packaging_error` semantics and
with invariants 15b, 15, and 16, which all treat both packaging base
codes uniformly. See `MSVE_v0.8.5_F20_ADJUDICATION.md` for the full
adjudication, solver evidence (F20-W SAT / F20-X SAT-then-UNSAT), and the
remaining specification-review judgement.

## Affected companions

- Candidate spec §E.7 invariant 10 text (one predicate).
- No M8 change (M8 parses but does not evaluate this invariant).
- No regression-ledger change required beyond referencing F-20.
