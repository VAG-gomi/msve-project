# MSVE v0.8.3 Residual Defect Ledger

**Work Order:** 0.8.3 · **Date:** 2026-10-09

Historical defects D-001–D-033 and NEW-A/B/C/D findings retain their
identifiers and dispositions from the v0.8 ledger (summarized here; full
entries in `MSVE_REGRESSION_LEDGER_v0.8.md`). F-01–F-19 are new.

## Historical summary (dispositions unchanged)

- D-001–D-024: v0.6/v0.7 corrections stand or were superseded as recorded.
- D-025–D-033: v0.8 corrections (B-01–B-05 areas); all green at gate.
- NEW-A1–A10, NEW-B1–B7, NEW-C1–C5, NEW-D1–D3: 24 unique Phase-D findings,
  corrected in v0.8 (NEW-C3 duplicates NEW-B7).
- D-007: grouped under "D-006–D-008 (v0.6 corrections stand)" — real defect,
  grouped entry. D-011: referenced in D-023's root cause only. D-012: no
  v0.8 ledger entry (mentioned by Reviewer C as a conditional assumption
  about `decode_candidates`).

## F-01–F-19 (new; linked to candidate changes)

| ID | Finding | Normative location | Candidate change | Evidence |
|---|---|---|---|---|
| F-01 | Detail-suffix/predicate mismatch | §B.9 | `base_code` op; predicates test `base_code(e)`; builtins; M8 | Corpus `f01-base-code.msve` PASS; spec review |
| F-02 | Assurance field naming | §E.1/E.7, plans | Exact `assurance_*` paths everywhere | Grep verification |
| F-03 | Rounding intervals | §B.4b | Exact intervals + 6 examples | Derivation (verification evidence) |
| F-04 | Missing `is_nan` | §B.4 r.3/r.11 | Builtin added; M8 | Corpus `f04-is-nan-typed.msve` PASS |
| F-05 | Set quantification scope | §B.4 r.8 | List-only v0 domains | Spec review |
| F-06 | Domain enforcement | §E.7 inv 1b | Record-boundary invariant | Spec review |
| F-07 | `inputs_ref` resolution | §E.7 inv 20 | Equality with `verification_inputs_ref` | Spec review |
| F-08 | Stale error counts | Spec change summary | 27 / 3 | Count check |
| F-09 | Corpus counts | Spec/review/matrix | 46 gate / 48 candidate | Manifest + CLI run |
| F-10 | Packaging agreement | Acc. plan §9, Diagram 2 | Aligned with inv 15b | Spec review |
| F-11 | `RecordLit` shorthand | Review B-01 table | Bare-brace `Atom` | Grammar check |
| F-12 | Type-name coverage | §G.2 | `record{}`, `()->t`; M8 | `test_canonical` vectors PASS |
| F-13 | Binary64 scope | §B.4b opening | Scope paragraph | Spec review |
| F-14 | Escape policy completeness | §G.2 | Raw UTF-8 + surrogate ban | `test_canonical` vectors PASS |
| F-15 | Blob digest case | §G.2 | Lowercase normative; M8 | `test_canonical` vectors PASS |
| F-16 | Invariant binding | §E.7 inv 1/10/15/15b | Bindings fixed | Spec review |
| F-17 | Matrix totals | Readiness matrix | 11 + 1 | Mechanical recompute |
| F-18 | CLM-09 scope | Readiness matrix | Per-finding categories | Spec review |
| F-19 | Review provenance | Provenance record | Limitation recorded; hashes | N/A |

## Regression obligations inherited

Every F-finding above becomes a regression obligation for any future
revision: the correction must remain present and the linked evidence must
remain green.
