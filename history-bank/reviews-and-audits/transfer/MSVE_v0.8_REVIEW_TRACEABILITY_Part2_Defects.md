# Report D — Defect Traceability D-001–D-033 and 24 Findings (Part 2/6)

**Work Order:** 0.8.2 · **Source:** `owner-review/MSVE_v0.8_DEFECT_TRACEABILITY.md` (DIRECT ARTEFACT — transcribed verbatim from the ZIP).

Includes the C3/B7 duplicate relationship as recorded.

---

# MSVE v0.8 Defect and Regression Traceability

**Work Order:** 0.8.1 · **Date:** 2026-10-09
**Source of record:** `MSVE_REGRESSION_LEDGER_v0.8.md` (full entries).
This table is an index; the ledger holds the original counterexamples,
root causes, and histories. Historical v0.7 statuses are preserved, not overwritten.

Evidence labels: EXECUTED_TEST · SPECIFICATION_REVIEW ·
MECHANICAL_DOCUMENT_CHECK. "Counterexample re-checked" = the defect's
original counterexample was exercised against the v0.8 correction.

## D-001 – D-033

| ID | Failure mode | Disposition (v0.8) | Normative location | Regression test | Expected / actual | Evidence | Limitation | Re-checked |
|---|---|---|---|---|---|---|---|---|
| D-001 | Validator contract inconsistent (`[]` case) | Corrected (v0.6, stands) | §B.11 | `v08-ex5.msve` via spec-examples | pass / pass | EXECUTED_TEST | Syntax/types only | Yes (spec-examples) |
| D-002 | Validator accepted malformed as valid | Corrected (v0.6, stands) | §B.11/B.13 | `inv-*` corpus | reject / reject | EXECUTED_TEST | — | Yes |
| D-003 | Single ErrorCode model | REOPENED by B-04 → superseded by D-029 | §B.9 | `is_validation_error` et al. | closed / closed | EXECUTED_TEST | — | Yes |
| D-004 | Canonical-form invariant incomplete | REOPENED by B-02 → re-corrected D-026/D-027 | §G.2 | test_canonical.py | unique / unique | EXECUTED_TEST | Bounded | Yes |
| D-005 | (canonical; reopened v0.6→v0.7) | REOPENED by B-02 → D-026/D-027 | §G.2 | test_canonical.py | — / — | EXECUTED_TEST | Bounded | Yes |
| D-006–D-008 | (v0.6 corrections stand) | Stand | various | corpus | — / — | EXECUTED_TEST | — | Via suite |
| D-009 | (reopened → corrected v0.7) | Stands | spec | corpus | — / — | EXECUTED_TEST | — | Via suite |
| D-010–D-013 | (v0.6 corrections stand) | Stand | various | corpus | — / — | EXECUTED_TEST | — | Via suite |
| D-014 | (reopened → corrected v0.7) | Stands | spec | corpus | — / — | EXECUTED_TEST | — | Via suite |
| D-015 | Admission codes in single ErrorCode | REOPENED by B-04 → D-029 | §B.9 | `is_admission_error` define | closed / closed | EXECUTED_TEST | Define parsed only | Yes |
| D-016 | Incomplete language primitives | Corrected (v0.7, stands) | §B | spec-examples | pass / pass | EXECUTED_TEST | — | Yes |
| D-017 | Binary64 canonicalisation not unique | REOPENED by B-02 → D-026 | §G.2 | test_canonical.py; B sweep | unique / unique | EXECUTED_TEST | Sweep not preserved | Yes |
| D-018 | Incomplete canonical type coverage | Corrected (v0.7, stands) | §G.2 | check_envelope | covered / covered | EXECUTED_TEST | — | Yes |
| D-019 | Real/Rat inconsistency | Corrected (v0.7, stands) | §B.4/§G.2 | rational tests | exact / exact | EXECUTED_TEST | — | Yes |
| D-020 | Non-closed validation types | REOPENED by B-03/B-04 → D-028+D-029 | §B.13a/§B.9 | predicate defines | closed / closed | EXECUTED_TEST | — | Yes |
| D-021 | Evidence-category syntax mismatch | Corrected (v0.7, stands) | §B.7 | corpus | — / — | EXECUTED_TEST | — | Via suite |
| D-022 | Result-schema gaps | REOPENED by B-05 → D-030 (+NEW-C4 inv.23) | §E | invariants 15–23 | linked / linked | SPECIFICATION_REVIEW | No execution | Paper |
| D-023 | Incomplete visualisation document | Corrected (v0.8 plan has 7 diagrams) | Visualisation plan | D's count (7 mermaid blocks) | 7 / 7 | MECHANICAL_DOCUMENT_CHECK | — | Yes |
| D-024 | Verification-item ambiguity | Corrected (v0.7, stands; D-031 extends) | §B.7 | corpus verif-* | — / — | EXECUTED_TEST | — | Yes |
| D-025 | Record construction absent (B-01) | Corrected v0.8 | §B.3 Atom; R13 | spec-examples 6/6; B-01 negative control | parse / parse | EXECUTED_TEST | Types only | Yes |
| D-026 | Exponent `-0` admitted (B-02) | Corrected v0.8 | §G.2; lexer | `f64-neg-zero-exp.msve` → lexical | reject / reject | EXECUTED_TEST | — | Yes |
| D-027 | Escapes/rationals/envelopes underspecified (B-02) | Corrected v0.8 | §G.2 | test_canonical.py | deterministic / deterministic | EXECUTED_TEST | Bounded | Yes |
| D-028 | Failed decode + candidates satisfied contract (B-03) | Corrected v0.8 | §B.11 contract | C's hand-derivation; acceptance §8.4 | contract false / false | SPECIFICATION_REVIEW | Not machine-checked | Yes (derived) |
| D-029 | Single ErrorCode (B-04) | Corrected v0.8 | §B.9 (3 types) | predicate defines; corpus | partitioned / partitioned | EXECUTED_TEST | Defines parsed only | Yes |
| D-030 | Packaging/schema incoherence (B-05) | Corrected v0.8 (+NEW-B7 inv.15b) | §E/§G.2 | invariants 15,15b,16 | joint / joint | SPECIFICATION_REVIEW | No execution | Paper |
| D-031 | Duplicate/conflict ambiguity | Corrected v0.8 | §B.7 | corpus verif-* (D-031 cases) | enforced / enforced | EXECUTED_TEST | — | Yes |
| D-032 | "IEEE 754" by reference | Corrected v0.8 (+NEW-B1 thresholds) | §B.4b | table rows (proposed L3) | stated / stated | SPECIFICATION_REVIEW | Not executed | Paper |
| D-033 | VerificationRecord linkage | Corrected v0.8 | §E.7 inv.14 | C's worked example | evaluable / evaluable | SPECIFICATION_REVIEW | — | Yes (example) |

## Reviewer findings → corrections (24 unique)

| Finding | Reviewer | Correction | Regression case | Evidence status |
|---|---|---|---|---|
| NEW-A1 – A6 | A | M8 enforcement implemented (§B.5/7/8, paths, cycles, builtins) | 6 corpus cases | EXECUTED_TEST |
| NEW-A7 | A | HexFloat `-?` removed; unary minus (§B.2) | `f64-subtraction-no-spaces.msve` | EXECUTED_TEST |
| NEW-A8 | A | `check_call` allows fn-typed locals | `call-local-fn.msve` | EXECUTED_TEST |
| NEW-A9 | A | `Set` removed from v0 TypeExpr | §B.3 regenerated; parser rejects | EXECUTED_TEST |
| NEW-A10 | A | Quantifier domains restricted to list/set | `quant-option-domain.msve` | EXECUTED_TEST |
| NEW-B1 | B | §B.4b exact thresholds; 2 rows added | Proposed L3 vectors | SPECIFICATION_REVIEW |
| NEW-B2 | B | `check_string_canonical` codepoint ranges | test_canonical.py assertions | EXECUTED_TEST |
| NEW-B3 | B | Spaceless type-name grammar | `check_typename` tests | EXECUTED_TEST |
| NEW-B4 | B | `check_envelope` validates of/sig/values | test_canonical.py assertions | EXECUTED_TEST |
| NEW-B5 | B | NaN predicate semantics stated | — (spec text) | SPECIFICATION_REVIEW |
| NEW-B6 | B | Rat/Real div-by-zero → execution error | — (spec text) | SPECIFICATION_REVIEW |
| NEW-B7 | B | Invariant 15b (packaging/execution joint) | — (spec text) | SPECIFICATION_REVIEW |
| NEW-C1 | C | `is_admission_error`/`is_unsupported_reason` defines | M8 parse of defines | EXECUTED_TEST |
| NEW-C2 | C | INTERNAL_ERROR open-domain statement | — (spec text) | SPECIFICATION_REVIEW |
| NEW-C3 | C | **Duplicate of NEW-B7** (independently found) | See NEW-B7 | — |
| NEW-C4 | C | Invariant 23 (UNIQUE_UNDER_PROJECTION) | — (spec text) | SPECIFICATION_REVIEW |
| NEW-C5 | C | Inv. 9/15 name evidence lists | — (spec text) | SPECIFICATION_REVIEW |
| NEW-D1 | D | v0.7 normative links → v0.8 | grep regression | MECHANICAL_DOCUMENT_CHECK |
| NEW-D2 | D | Ledger D-025 corrected to as-built | — (ledger text) | SPECIFICATION_REVIEW |
| NEW-D3 | D | Diagram 3 → v0.8 contract | — (plan text) | SPECIFICATION_REVIEW |

**Count reconciliation:** 10 (A) + 7 (B) + 5 (C) + 3 (D) = 25 findings;
NEW-C3 duplicates NEW-B7 → **24 unique defects**. Each original finding
is preserved above; the duplicate relationship is documented, not merged.

## Outstanding limitations

- D-022, D-028, D-030, D-032, NEW-B1, NEW-B5, NEW-B6, NEW-B7, NEW-C2,
  NEW-C4, NEW-C5 are SPECIFICATION_REVIEW only — corrected in prose,
  not executed (no implementation exists).
- D-017/B sweep: the 2,998-value script was not preserved.
- No finding's fix received a second independent review.
