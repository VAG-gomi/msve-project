# MSVE v0.8.3 Correction Report

**Work Order:** 0.8.3 · **Date:** 2026-10-09
**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW PENDING

## Objective

Targeted correction pass over the v0.8 design documents for findings
F-01–F-19 identified during owner review of the Markdown transfer.
Originals untouched; all corrections are in candidate copies under
`work-order-0.8.3-candidate/`.

## Dispositions

| Finding | Confirmed in source | Type | Correction | Verification |
|---|---|---|---|---|
| F-01 | Yes | Normative defect | `base_code` operation defined (§B.9); all four closure predicates test `base_code(e)`; added to builtins; M8 BUILTINS + corpus case | EXECUTED_TEST (parse/type) + SPECIFICATION_REVIEW (semantics) |
| F-02 | Yes | Cross-doc inconsistency | Exact field paths `assurance_required`/`assurance_bases`/`assurance_achieved`/`assurance_shortfall` throughout spec, acceptance plan, diagrams | MECHANICAL_DOCUMENT_CHECK (grep) |
| F-03 | Yes | Normative defect | §B.4b rewritten with exact rounding intervals + 6 adversarial examples | SPECIFICATION_REVIEW (exact arithmetic derivation) |
| F-04 | Yes | Normative defect | `is_nan: Binary64->Bool` added to inventory; M8 BUILTINS + scheme + corpus case | EXECUTED_TEST (parse/type) |
| F-05 | Yes | Normative defect | Rule 8 restricted to `type T` / list expressions; set unavailability stated | SPECIFICATION_REVIEW |
| F-06 | Yes | Normative defect | New invariant 1b enforces predicates at record boundary | SPECIFICATION_REVIEW |
| F-07 | Yes | Normative defect | Invariant 20: `inputs_ref = evidence.verification_inputs_ref` | SPECIFICATION_REVIEW |
| F-08 | Yes | Cross-doc inconsistency | Change summary: 27 / 3 (was 15 / 2) | MECHANICAL_DOCUMENT_CHECK |
| F-09 | Yes | Cross-doc inconsistency | Corpus counts reconciled: 46 at gate, 48 candidate (36 was pre-Phase-D) | MECHANICAL_DOCUMENT_CHECK + EXECUTED_TEST (48/48) |
| F-10 | Yes | Cross-doc inconsistency | Acceptance plan + Diagram 2 aligned with invariant 15b | SPECIFICATION_REVIEW |
| F-11 | Yes | Cross-doc inconsistency | Review table: bare-brace `Atom` alternative (not `RecordLit`) | MECHANICAL_DOCUMENT_CHECK |
| F-12 | Yes | Normative defect | Canonical type names: `record{}` and `()->t` legal; M8 `check_typename` updated + vectors | EXECUTED_TEST |
| F-13 | Yes | Normative defect | §B.4b scope paragraph: Binary64 ops only; Nat/Int/Real/Rat exact | SPECIFICATION_REVIEW |
| F-14 | Yes | Normative defect | Raw UTF-8 rule + surrogate prohibition added to §G.2; M8 already enforced (vectors added) | EXECUTED_TEST + SPECIFICATION_REVIEW |
| F-15 | Yes | Normative defect | Blob digest: lowercase hex normative; M8 `check_envelope` now validates + vectors | EXECUTED_TEST |
| F-16 | Yes | Normative defect | Invariant 1 `assurance_achieved`; inv 10 `reason` binding; inv 15 `value_ref` bound; inv 15b `base_code` | SPECIFICATION_REVIEW |
| F-17 | Yes | Evidence-record defect | Matrix totals: 11 SUPPORTED + 1 PARTIALLY_SUPPORTED | MECHANICAL (recomputed) |
| F-18 | Yes | Evidence-record defect | CLM-09 split into per-finding evidence categories | SPECIFICATION_REVIEW |
| F-19 | Yes | Evidence limitation | Recorded as historical limitation; candidate sources hashed | N/A (limitation, not correctable) |

## What was not reproduced

- Reviewer B's 2,998-value sweep (still EVIDENCE_NOT_AVAILABLE).
- Pre-fix gate states (not preserved; final states re-verified).
- No MSVE engine exists; no semantic execution was performed.

## Requires owner judgement

- Whether the F-03 interval wording is now exact (derivation recorded in verification evidence).
- Whether invariant 15b is *sufficient* (joint satisfiability of all 23 invariants not demonstrated).
- Whether the v0.8.3 candidate is accepted as the new baseline.
