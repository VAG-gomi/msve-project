# MSVE Capability Matrix v0.8

**Status:** DRAFT FOR REVIEW · **Version:** 0.8
**Supersedes:** `MSVE_CAPABILITY_MATRIX_v0.7.md` (historical draft)
**Normative companion:** `MSVE_DESIGN_SPEC_v0.8.md`

Scale: Designed → Implemented → Functionally verified → Formally verified →
Integrated → Independently reproduced. "N/A (reason)" marks a stage that does
not apply. No stage is claimed without the evidence named in §D.6.

## v0 target capabilities (all Designed unless noted)

| ID | Capability | v0.8 status | Evidence / note |
|---|---|---|---|
| C1 | Formal input language (§B) | Designed | Grammar generated from `m8/grammar.py`; M8 parses + type-checks all §B.11 examples |
| C2 | Record construction (D-025) | Designed | New `Atom` production; R13 typing; M8 corpus cases |
| C3 | Binary64 canonical uniqueness (D-017/D-026) | Designed | `msve-canonical-3`; M8 canonical tests; 2000-value round-trip |
| C4 | Binary64 operational semantics (D-032) | Designed | §B.4b table; replaces the "IEEE 754" hand-wave |
| C5 | Exact Real/Rat (D-019) | Designed | Exact rational payloads; total `to_rat` |
| C6 | Three-stage validator (D-001/D-028) | Designed | Decode → validate → contract; D-028 conjunct enforced |
| C7 | Closed error model (D-029) | Designed | ValidationError / AdmissionError / UnsupportedReason |
| C8 | Result schema + packaging (D-030) | Designed | `output_packaging`; invariants 15–22 |
| C9 | Verification-item rules (D-031) | Designed | Cardinality + conflict rules; Qualifier default |
| C10 | Assurance levels L1/L2/L3 | Designed | §D.1; three claims separated |
| C11 | M8 audit tool (new) | Implemented | Lexer/parser/resolver/type-checker; 36-case corpus; see `m8/README.md` |

## Explicitly out of scope for v0

MSVE engine implementation; solver integration; chess experiments;
performance prediction; objective invention; arbitrary discovery;
inferred historical data; NL direct execution.

*End of MSVE_CAPABILITY_MATRIX_v0.8.md (draft for review).*
