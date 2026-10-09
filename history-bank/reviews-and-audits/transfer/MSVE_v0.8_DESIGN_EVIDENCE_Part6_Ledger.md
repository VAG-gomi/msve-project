# Report B — Design Evidence — Regression Ledger (Part 2/2)

**Work Order:** 0.8.2 · **Source file:** `six-docs/MSVE_REGRESSION_LEDGER_v0.8.md` (DIRECT ARTEFACT, sha256 `e04a05e68e92ce54…`)

Complete original text, unmodified. Part 2 of 2 (continued). END.

---


---

## New defects found during v0.7 drafting

One: the M6 collision-construction check caught an incomplete v0.7 fix —
the first draft's binary64 grammar omitted the exponent-range bound,
admitting `0x1.0000000000000p-1074` for the minimum subnormal alongside the
canonical `0x0.0000000000001p-1074`. Fixed before delivery (`-1022 ≤ Exp ≤
1023` for normals); recorded here per the loop's honesty rule. This is the
strengthened method working as intended: the claim was challenged by
construction, not by re-reading.

---

## v0.8 status of D-001 – D-024

All v0.6/v0.7 corrections stand unless noted. The v0.7 forensic findings
B-01–B-05 reopened these areas; v0.8 corrections are recorded under D-025–
D-033 and in the §B/§E/§G prose they cite:

- **D-003** (REOPENED by B-04 → superseded): the single-`ErrorCode` model is
  retired; replaced by the D-029 three-type model. D-003's original
  counterexample (contract conjunct wording) is re-checked under D-029.
- **D-004, D-005** (REOPENED by B-02): the canonical-form invariants were
  incomplete (exponent `-0`, escapes, rationals unspecified). Re-corrected
  under D-026/D-027; the v0.7 M6 check did not catch `-0` because the
  regex was copied from the spec prose rather than generated from a
  single rule. Root-cause lesson: generate the checker from the same
  rule text as the spec, or check the rule independently.
- **D-015** (REOPENED by B-04): the AdmissionError reason codes now live
  under the three-type model (D-029).
- **D-017** (REOPENED by B-02 → corrected under D-026): the exponent `-0`
  survivor; the unique form is `p+0`.
- **D-020** (REOPENED by B-03/B-04): the `ErrorCode` closure is superseded
  by D-028 (decoder invariant) + D-029 (three closed types).
- **D-022** (REOPENED by B-05 → corrected under D-030): packaging,
  `Option<Hash>` refs, payload→evidence links.
- **D-023**: the v0.8 visualisation plan reproduces all seven Mermaid
  sources (no "retained by reference" claims). Stands corrected.
- D-001, D-002, D-006–D-014, D-016, D-018, D-019, D-021, D-024:
  corrections stand; regression cases retained.

## New defects D-025 – D-033 (v0.8; from the v0.7 forensic review B-01–B-05)

### D-025: Record construction absent from the formal language

- **Original observation (B-01, v0.7 §B.11):** The §B.11 examples contain
  record literals (`Candidate{uci:…, rank:…}`, `ValidationOutcome`, …) but
  the grammar has no `record_literal` production. `m8 --check` fails the
  validator example at `32:3` ("expected expression, found '{'"). The prose
  says "record construction … from §B.3"; §B.3 has no such production.
- **Root cause:** Examples were written in an intended surface syntax
  before the grammar covered it; the "verified by hand-derivation" claim
  (AGENTS.md) was not mechanically performed.
- **Invariant:** Every syntactic form in a normative example is generated
  by the grammar (`spec-examples` gate).
- **Correction (v0.8):** bare-brace record literal as an `Atom`
  alternative (`"{" (Ident ":" Expr ("," Ident ":" Expr)*)? "}"`),
  R13 record-construction typing (exhaustive, typed, no-duplicates),
  `expect_field_name` policy (reserved keywords allowed as field names),
  M8 corpus cases. (NEW-D2: an earlier draft of this entry described a
  `TypeName`-prefixed form and a `Ctor` token — neither was built; the
  as-built form is bare braces.)
- **Regression:** M8 §B.11 suite (all six examples parse + type-check);
  B-01 negative control (record-literal branch disabled → exact v0.7
  failure reproduced).
- **Evidence:** EXECUTED_TEST (M8 suite) · **Limitation:** M8 checks
  syntax/types, not contract satisfiability.

### D-026: Exponent `-0` admitted in binary64 canonical form

- **Original observation (B-02):** v0.7 §G.2 allowed `("-"|"+") Exp`;
  `0x1.0000000000000p-0` and `p+0` are distinct spellings of the same
  value. The M6 v0.7 check missed it (regex copied from prose).
- **Correction (v0.8):** Exponent is exactly `+0` or sign + nonzero
  digits; `-0` is not a spelling. `msve-canonical-3` §G.2.
- **Regression:** `canonical_test.go`-style corpus: `p-0` rejected,
  `p+0` accepted; 2000-value round-trip (M8 `test_canonical.py`).
- **Evidence:** EXECUTED_TEST · **Limitation:** bounded corpus; the
  injectivity argument is a proof sketch (structural induction), not a
  machine-checked proof.

### D-027: Canonical form underspecified (escapes, rationals, envelopes)

- **Original observation (B-02):** "minimal string escaping" allows
  `\u001A` vs `\u001a`; rational text grammar absent; envelope field
  order, type-name formatting, UTF-8/NFC handling unstated.
- **Correction (v0.8):** Deterministic escape policy (short escapes
  preferred, lowercase `\uXXXX`, `/` unescaped); rational normal form
  (`-`? Nat `/` Nat, lowest terms, `0/1` zero); exact envelope field
  orders; canonical type-name grammar; UTF-8 required, NFC required for
  strings.
- **Regression:** M8 `test_canonical.py` escape/rational/envelope cases.
- **Evidence:** EXECUTED_TEST · **Limitation:** as D-026.

### D-028: Decoder failure with non-empty candidates satisfies the contract

- **Original observation (B-03):** v0.7 `validator_contract` checked only
  `is_validation_error(e)` on the false branch. A decoder returning
  `{ok:false, candidates:[c], error:some("malformed-json")}` with
  `out=rejected("malformed-json")` satisfies it — violating the
  `DecodeOutcome` invariant that failed decode yields no candidates.
- **Correction (v0.8):** Contract false branch: `is_validation_error(e)
  && len(d.candidates) == 0`. Decoder §B.13 table rows for malformed
  inputs now state `candidates = []` explicitly.
- **Regression:** Acceptance plan §8.4 D-028 case; M8 type-checks the
  contract (the logical content is hand-verified, not machine-checked —
  stated as SPECIFICATION_REVIEW).
- **Evidence:** SPECIFICATION_REVIEW (contract logic) + EXECUTED_TEST
  (M8 parses the contract) · **Limitation:** no automated
  satisfiability check of the contract formula.

### D-029: Single `ErrorCode` cannot name admission failures

- **Original observation (B-04):** `INVALID_INPUT(duplicate-definition)`
  is an admission-time failure, but the v0.7 model funnels it through
  the validation `ErrorCode`. The three domains (validation / admission /
  unsupported) were conflated.
- **Correction (v0.8):** Three closed types: `ValidationError`,
  `AdmissionError`, `UnsupportedReason`; every result-schema field
  typed by domain; `§B.9` states the domain each field belongs to.
- **Regression:** M8 type-checks all §B.11 examples under the new
  model; admission examples in corpus.
- **Evidence:** EXECUTED_TEST (M8) + SPECIFICATION_REVIEW (domain
  assignment).

### D-030: Result schema cannot link payloads to evidence (packaging)

- **Original observation (B-05):** v0.7 schema had no way to record
  that a computed value was packaged, or to keep the semantic result
  when packaging fails (NaN, function values).
- **Correction (v0.8):** `output_packaging` field; `Option<Hash>` refs
  for payload/evidence; invariants 15–22; PACKAGING_FAILED status that
  preserves the semantic result.
- **Regression:** Acceptance plan §8 D-030 cases; schema invariant
  checks (SPECIFICATION_REVIEW).
- **Evidence:** SPECIFICATION_REVIEW · **Limitation:** no executed
  packaging tests (no implementation exists).

### D-031: Verification-item duplicate/conflict rules ambiguous

- **Original observation (B-01-adjacent, v0.7 §B.7):** The D-024
  correction left duplicate vs conflicting verification items
  under-specified (same claim twice vs contradictory claims).
- **Correction (v0.8):** Explicit duplicate/conflict admission rules;
  Qualifier default stated.
- **Regression:** M8 admission corpus cases.
- **Evidence:** EXECUTED_TEST (M8 corpus) + SPECIFICATION_REVIEW.

### D-032: Binary64 arithmetic was "IEEE 754" by reference only

- **Original observation:** §B.4b said "IEEE 754" without stating which
  operations, rounding, or exceptional cases.
- **Correction (v0.8):** Full §B.4b operational semantics: exact
  operations table, NaN/inf/signed-zero rules, overflow/underflow,
  comparison, `to_rat` totality.
- **Regression:** §B.4b table rows as test vectors (proposed;
  EXECUTED_TEST only when an implementation exists).
- **Evidence:** SPECIFICATION_REVIEW · **Limitation:** not executed.

### D-033: VerificationRecord linkage insufficient for invariant 14

- **Original observation:** Invariant 14 (verification aggregation)
  could not be evaluated from the recorded fields.
- **Correction (v0.8):** `source_item` and `required` fields added;
  aggregation executable from recorded fields.
- **Regression:** Invariant-14 worked example (SPECIFICATION_REVIEW).
- **Evidence:** SPECIFICATION_REVIEW.

## New defects found during v0.8 construction (M8)

1. **v0.7 selector example used list-only `len` on `String`** (`len(c.uci)`).
   Found by M8 type-checking; corrected to `c.uci != ""`. Recorded as a
   v0.7 example defect (not a new D-number; the examples were never
   mechanically checked).
2. **v0.7 validator example defined `accepted`, a reserved keyword.**
   Found by M8 name resolution; corrected to `accept`.
3. **M8 implementation defects (12, corrected during construction):**
   missing punctuation tokenization; `ProveGoal` parser-method mapping;
   hyphenated keywords split; resource-limit semicolons; `CheckError`
   calling convention; infinite recursion on unbound type variable;
   function-body checked against full function type; alias resolution
   before builtin unification; missing quantifier resolution in
   axioms/prove goals; reserved keywords as record field names; two
   incorrect corpus expectations. M8 is an audit tool under test, not an
   oracle — these are preserved in `m8/runs/2026-10-09-m8-build.md`.

## B-01 – B-05 → D-number mapping (v0.7 forensic findings)

| Finding | Maps to |
|---|---|
| B-01 (record literals) | D-025 |
| B-02 (canonical form) | D-026, D-027; reopens D-004, D-005, D-017 |
| B-03 (decoder invariant) | D-028; reopens D-020 |
| B-04 (error model) | D-029; reopens D-003, D-015, D-020 |
| B-05 (packaging/schema) | D-030; reopens D-022 |

## New defects found during v0.8 Phase-D review (Sub-agent B, 2026-10-09)

Sub-agent B (canonicalisation/numerical semantics) confirmed A1–A4
(binary64 uniqueness under collision attack, rational grammar, envelope,
packaging coherence) and found seven genuine defects. All conceded by
the lead; corrections applied:

- **NEW-B1 (§B.4b, D-032):** underflow/overflow boundary prose was false
  (`3/4 × 2^-1074` rounds to min subnormal, not ±0; overflow threshold
  is `2^1024 − 2^970`, not `2^1024`). Corrected with exact thresholds;
  added `(+inf) − finite` and `0/(±inf)` rows.
- **NEW-B2 (M8, D-027):** `check_string_canonical` accepted `\u00a0`,
  `\u20ac`, `\ud83d` — codepoints the spec requires as raw UTF-8 or
  rejects. Corrected: `\uXXXX` allowed only for < U+0020 / U+007F–U+009F;
  surrogates rejected; raw U+007F–U+009F must be escaped.
- **NEW-B3 (§G.2, D-027):** type-name productions showed spaces
  (`impl(nat -> nat)`) contradicting "no whitespace". Corrected to
  spaceless forms.
- **NEW-B4 (M8, D-027):** `check_envelope` validated field order only;
  `of`/`sig` and value spellings unchecked. Corrected: `check_typename`
  grammar + recursive value validation.
- **NEW-B5 (§B.4 rule 3, D-032):** NaN comparisons undefined (`x == x`
  for NaN). Corrected: IEEE-style predicate rules stated explicitly.
- **NEW-B6 (§B.4 rule 2):** `Real`/`Rat` division by zero undefined.
  Corrected: execution error `division-by-zero`.
- **NEW-B7 (§E.7/§G.2, D-030):** `output_packaging` and `execution`
  unconstrained jointly; `is_packaging_error` suffix rule unstated.
  Corrected: invariant 15b (biconditional); suffix convention stated.

Evidence: SPECIFICATION_REVIEW (spec corrections) + EXECUTED_TEST (M8
regression cases in `test_canonical.py`).

## New defects found during v0.8 Phase-D review (Sub-agent C, 2026-10-09)

Sub-agent C (validator/result-contract) confirmed D-028 with a full
hand-derivation (both contract branches; the v0.7 form without the
`len` conjunct re-derived to `true`, confirming the conjunct is
load-bearing), confirmed D-029's domain partition and D-031 via M8,
and confirmed D-033 sufficient. Found four defects (one duplicate):

- **NEW-C1 (§B.9, D-029):** `is_admission_error` / `is_unsupported_reason`
  never formally defined — prose lists only. Corrected: both `define`
  disjunctions written (27 + 3 codes); M8-verified to parse/type-check.
- **NEW-C2 (§E.1, D-029):** `INTERNAL_ERROR(reason: String)` unbounded —
  a fourth unclosed domain. Corrected: normative statement that the
  domain is intentionally open, with the four specified reasons
  enumerated (`inexact-division`, `division-by-zero`,
  `output-not-encodable: <type>`, `canonicalization-failure: <detail>`).
- **NEW-C3 (§E.7/§G.2, D-030):** DUPLICATE of NEW-B7 (found independently
  by C; confirms the defect). Fixed by invariant 15b. C's three variant
  records: exactly one conforms after the fix.
- **NEW-C4 (§E.7, D-022):** `UNIQUE_UNDER_PROJECTION` had no evidence
  invariant. Corrected: invariant 23 ties it to a solver observation or
  derivation record.
- **NEW-C5 (observation, §E.7):** "resolves in the evidence bundle" vague;
  no value-artifact list named. Corrected: inv. 9 → `derivation_records`;
  inv. 15 → `constructed_artifacts`.

Evidence: SPECIFICATION_REVIEW + EXECUTED_TEST (predicate defines).

## New defects found during v0.8 Phase-D review (Sub-agent D, 2026-10-09)

Sub-agent D (cross-document) verified all M8 gates green, confirmed the
7-diagram visualisation plan, the B→D mapping, the D-028 acceptance case,
and the matrix claims. Found three copy-forward defects:

- **NEW-D1 (cross-document):** three normative links in the v0.8 spec
  pointed to v0.7 companion files. Corrected to v0.8 filenames.
- **NEW-D2 (ledger accuracy):** the D-025 correction line described a
  `TypeName`-prefixed record form and `Ctor` token that were never built.
  Corrected to the as-built bare-brace `Atom` alternative.
- **NEW-D3 (visualisation):** Diagram 3 and its image prompt showed the
  retired `is_error_code` contract, omitting the D-028 conjunct.
  Corrected to the v0.8 contract form.

Evidence: SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (greps).

## New defects found during v0.8 Phase-D review (Sub-agent A, 2026-10-09)

Sub-agent A (grammar/type-system) re-ran all M8 commands independently,
verified keyword agreement (62/62), reproduced the B-01 negative
control, and manually traced the §B.11 examples. Found 10 defects.
All conceded by the lead; corrections applied:

- **NEW-A1 (M8, §B.8):** `check_limits` was a stub; `timeout: 9999h`
  and `steps: 0` passed silently. Corrected: 1s…24h range + `steps: 0`
  rejection enforced.
- **NEW-A2 (M8, §B.7):** `level-a required` on construct/check/
  compare-models goals passed silently. Corrected: `else` branch emits
  `assurance-level-unavailable`.
- **NEW-A3 (M8, §B.5a):** projection paths never validated (a dangling
  comment claimed the check). Corrected: `check_proj_paths` walks paths
  against the model record type.
- **NEW-A4 (M8):** cyclic type aliases crashed with `ValueError`.
  Corrected: `CheckError(admission)` + definition-time cycle detection.
- **NEW-A5 (M8, §B.5):** unbound type names passed silently.
  Corrected: name-resolution error at the declaration.
- **NEW-A6 (M8, §B.5):** builtin shadowing (`define len: Nat = 3`)
  accepted. Corrected: `collect` rejects collisions with `BUILTINS`.
- **NEW-A7 (§B.2 lexical):** `HexFloat` `-?` created a maximal-munch
  ambiguity with binary minus. Corrected: `-?` removed from the token;
  negation is unary minus (spec §B.2 updated).
- **NEW-A8 (M8/§B.4):** function-typed locals could not be called.
  Corrected: `check_call` allows locals with `fn` type.
- **NEW-A9 (§B.3):** `Set<T>` had no introduction form. Corrected:
  removed from v0 surface `TypeExpr` (reserved for future use).
- **NEW-A10 (M8/§B.4):** `Option` accepted as a quantifier domain
  without defined semantics. Corrected: restricted to list/set.

Evidence: EXECUTED_TEST (10 new corpus cases; 46 total, 0 failures).

Agent A's bottom-line warning is accepted as a standing methodological
rule: "M8's *implemented* checks have run" — the unimplemented ones are
where the next B-01-class defect hides. The six gaps are now closed;
future rounds must re-audit M8's coverage against the normative text.

*End of MSVE_REGRESSION_LEDGER_v0.8.md — to be carried forward by v0.9+.*
