# MSVE v0.8.3 Cross-Document Matrix

**Work Order:** 0.8.3 · **Date:** 2026-10-09

Each finding mapped to normative location, correction, affected companion
documents, regression case or review method, actual evidence, and residual
limitation.

| Finding | Normative location | Correction | Companion docs touched | Regression / method | Evidence | Residual limitation |
|---|---|---|---|---|---|---|
| F-01 | §B.9 | `base_code` op + predicates | Matrix (none), M8 | `f01-base-code.msve` | EXECUTED_TEST (types) | Predicate *semantics* not executed |
| F-02 | §E.1/E.7 | `assurance_*` paths | Acceptance plan, Visualisation plan | Grep sweep | MECHANICAL | None known |
| F-03 | §B.4b | Exact intervals | — | Derivation | SPECIFICATION_REVIEW | Owner should check derivation |
| F-04 | §B.4 r.11 | `is_nan` builtin | M8 | `f04-is-nan-typed.msve` | EXECUTED_TEST (types) | NaN *semantics* not executed |
| F-05 | §B.4 r.8 | List-only domains | — | Text inspection | SPECIFICATION_REVIEW | None known |
| F-06 | §E.7 inv 1b | Boundary invariant | — | Text inspection | SPECIFICATION_REVIEW | Not machine-checked |
| F-07 | §E.7 inv 20 | Equality rule | — | Text inspection | SPECIFICATION_REVIEW | None known |
| F-08 | Spec summary | 27 / 3 | — | Count vs §B.9 | MECHANICAL | None known |
| F-09 | Spec/review/matrix | 46 / 48 | Review, Matrix | Manifest + CLI | EXECUTED_TEST (48/48) | CLI selection logic assumed |
| F-10 | Acc plan §9, Diag 2 | Inv-15b alignment | Acceptance plan, Visualisation plan | Text inspection | SPECIFICATION_REVIEW | Sufficiency of 15b unproven |
| F-11 | Review table | `Atom` wording | Design review | Grammar inspection | MECHANICAL | None known |
| F-12 | §G.2 | Type-name grammar | M8 | `test_canonical` | EXECUTED_TEST | None known |
| F-13 | §B.4b | Scope paragraph | — | Text inspection | SPECIFICATION_REVIEW | None known |
| F-14 | §G.2 | Escape rules | M8 | `test_canonical` | EXECUTED_TEST | NFC handling assumed from v0.8 |
| F-15 | §G.2 | Blob lowercase | M8 | `test_canonical` | EXECUTED_TEST | None known |
| F-16 | §E.7 | Bindings | — | Text inspection | SPECIFICATION_REVIEW | Joint satisfiability unproven |
| F-17 | Matrix | Totals | Readiness matrix | Recompute | MECHANICAL | None known |
| F-18 | Matrix | CLM-09 split | Readiness matrix | Text inspection | SPECIFICATION_REVIEW | None known |
| F-19 | Provenance | Limitation record | Provenance file | Hashing | MECHANICAL | Historical gap unfillable |

**Key:** EXECUTED_TEST = M8 ran green; MECHANICAL = grep/count/hash;
SPECIFICATION_REVIEW = human-readable reasoning, not machine-checked.
