# MSVE Regression Ledger v0.8

**Status:** DURABLE PROJECT DOCUMENT — carried forward by every successor version
**Version:** 0.8 · **Work order:** MSVE Work Order 0.8 (D-025–D-033; B-01–B-05 areas)

## Purpose and rules

This ledger is the correction loop's memory. Every entry preserves a known
defect so that no successor version can silently reintroduce it, rename it
away, or declare it fixed without the stated evidence. This revision is
fully self-contained: the recurrence-prevention rule and the release-gate
sequence are reproduced inline (not by reference).

This revision:
- carries D-001–D-024 with updated version histories;
- reopens the areas affected by the v0.7 forensic findings B-01–B-05 and
  records their v0.8 corrections;
- adds D-025–D-033 with original counterexamples, root causes, invariants,
  regression cases, and evidence;
- records two genuine v0.7 example defects found by M8 during construction.

**Recurrence-prevention rule (binding on future versions):**
1. Every successor version inherits this ledger and its regression cases.
2. A defect may not be removed without an auditable reason; marked resolved
   because prose was added; silently renamed, downgraded or reclassified;
   considered corrected without checking its original counterexample;
   reintroduced in another section or document; or declared verified merely
   because the specification describes an unrun test.
3. Unresolved defects stay visible; the release gate stays closed where they
   affect correctness, safety of conclusions, or acceptance criteria.
4. New defects are added with a counterexample, root cause and prospective
   regression check — never hidden for being absent from the inherited list.

**Evidence-status vocabulary:** NOT_CHECKED · SPECIFICATION_REVIEW ·
MECHANICAL_DOCUMENT_CHECK · IMPLEMENTATION_CONFORMANCE · EXECUTED_TEST ·
FORMAL_PROOF · INCONCLUSIVE.

## Mandatory release-gate sequence (future versions)

1. **Intake** — ingest the previous ledger, unresolved decisions, accepted
   limitations, regression cases.
2. **Classification** — syntax / type-system / logical contradiction /
   schema gap / evidence overclaim / implementation / cross-document.
3. **Root-cause analysis** — why did validation let it survive; not just
   where it appeared.
4. **Invariant formation** — convert each failure into a checkable statement.
5. **Targeted correction** — smallest normative change resolving the root cause.
6. **Adversarial challenge** — reproduce the original failure; hunt the same
   defect under different names, syntax, values, locations, status combos.
7. **Regression check** — inherited cases pass only when the revised
   normative semantics entail the required outcome.
8. **Cross-document reconciliation** — design, review, matrix, acceptance,
   visualisation, ledger agree.
9. **Evidence and limitations** — record what was examined, by which method;
   paper reasoning ≠ automated checking ≠ executed tests.
10. **Release decision** — READY_FOR_OWNER_REVIEW / BLOCKED / INCONCLUSIVE
    (none of which is owner approval, freeze, or implementation authorisation).

---

## D-001 – D-003 (validator; v0.6 corrections stand, v0.7 strengthens)

**D-001** — three-stage pipeline (§B.11/§B.13); v0.7 adds the `DecodeOutcome`
invariant and the `is_error_code` conjunct to the contract. Status: corrected
at spec level (SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK).
**D-002** — extensional-equality binding unchanged. Status: corrected at spec
level. **D-003** — closed codes via `is_error_code` predicate + closure rule
(§B.13a); D-020 below records the v0.6 gap. Status: corrected at spec level.

## D-004 (REOPENED by v0.6 review → corrected v0.7)

- **v0.6 failure:** list/set collision fixed, but the review's wider audit is
  accepted: the v0.6 profile still lacked function-value and signature-aware
  `Impl` rules.
- **v0.7 correction:** `msve-canonical-3`; function values explicitly not
  encodable (named packaging failure); `Impl` carries its signature;
  ±infinity encodable; NaN not encodable.
- **Invariant:** every `TypeExpr` kind has either an exact encoding rule or
  an explicit not-encodable rule with a named reason.
- **Regression case:** `{"$type":"impl","sig":"(nat)->nat","value":"x"}` vs
  same descriptor with `sig":"(int)->int"` → different bytes; a function
  value → packaging failure, not silent omission.
- **Evidence status:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (M7-style: every TypeExpr kind audited).
- **Version history:** D-004 opened v0.6-work-order; partial v0.6;
  reopened by forensic review; corrected v0.7.

## D-005 (REOPENED → corrected v0.7)

- **v0.6 failure:** binary64 "normalized hexfloat" admitted
  `0x1.0000000000000p+1` and `0x2.0000000000000p+0` for 2.0 (and two
  subnormal forms; leading-zero exponents).
- **v0.7 correction:** exact grammar — leading digit exactly `1` for
  normals with `-1022 ≤ Exp ≤ 1023`, one subnormal form (`0x0.` + 13 digits
  + `p-1074`), exponents without leading zeros, zero exactly
  `0x0.0000000000000p+0`; uniqueness argued per class.
  (The M6 collision-construction check caught a draft-stage hole: the first
  v0.7 draft omitted the exponent-range bound, admitting
  `0x1.0000000000000p-1074` for the min subnormal — fixed before delivery.)
- **Invariant:** one canonical form per supported value; the old collision
  pair is rejected/distinguished under the new rules.
- **Regression case:** `0x2.0000000000000p+0` → not canonical (rejected);
  `0x1.0000000000000p+1` → canonical for 2.0.
- **Evidence status:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (M6: collision-construction attempt + round-trip script).
- **Version history:** opened v0.6-work-order; partial v0.6; reopened;
  corrected v0.7 (`msve-canonical-3`).

## D-006, D-007, D-008 (v0.6 corrections stand)

Unchanged; version histories extended to v0.7 (no regressions found).

## D-009 (REOPENED → corrected v0.7)

- **v0.6 failure:** `to_rat_exact(1.0/3.0) = None` although 1/3 is exactly a
  `Rat` — the name overpromised; and unserializable valid results had no
  proper outcome.
- **v0.7 correction:** `Real` carries exact rational payloads
  (`{"$type":"real","value":"1/3"}`); `to_rat: Real -> Rat` is total;
  `real-not-encodable` removed; packaging failures get
  `INTERNAL_ERROR(output-not-encodable: …)` with the semantic result
  preserved — never INVALID_INPUT (§E.7 inv. 10).
- **Invariant:** every v0 `Real` is encodable; conversion is total and exact;
  a valid result that cannot be packaged is a packaging failure, not an
  input error.
- **Regression case:** `derive 1.0/3.0` → packages as
  `{"$type":"real","value":"1/3"}`; `to_rat(1.0/3.0)` = `1/3 : Rat`.
- **Evidence status:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Version history:** opened v0.6-work-order; partial v0.6; reopened;
  corrected v0.7.

## D-010 – D-013 (v0.6 corrections stand)

Unchanged; histories extended. (D-010's vocabulary now also feeds the
`recompute:` separation.)

## D-014 (REOPENED → corrected v0.7)

- **v0.6 failure:** `proof: independent-recompute` kept recomputation under
  the `proof:` field while §D.6 denied it is a proof.
- **v0.7 correction:** `recompute:` is a separate `VerifItem`; `proof:`
  carries kernel-checked proof only; admission and basis-derivation rules
  updated; §B.12 ex.18 rejects the old syntax.
- **Invariant:** syntactic categories match evidential categories; the
  assurance policy's admission of recomputation as Level A evidence for
  exact derivations is stated separately from proof semantics.
- **Regression case:** `proof: independent-recompute by x/1.0.0` → syntax
  error; `recompute: by x/1.0.0` + `assurance: level-a required` on derive
  → admitted.
- **Evidence status:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Version history:** opened v0.6-work-order; partial v0.6; reopened;
  corrected v0.7.

## D-015 (REOPENED → corrected v0.7)

- **v0.6 failure:** `ErrorCode = String` alias called "closed"; payload-less
  `SemanticResult` tags; §E.7 "illustrative"; missing field definitions.
- **v0.7 correction:** `is_error_code` closure predicate + contract
  conjunct; payload-carrying `SemanticResult` alternatives with binding
  rules; exhaustive §E.7 (14 invariants); `Discrepancy.involved_records`
  = 0-based indices into `verification_records`;
  `ExternalEvidence.recorded_at` = `YYYY-MM-DDTHH:MM:SSZ`; Level B ⇒
  explicit spec acceptance (inv. 12).
- **Invariant:** schema closure is checkable: every referenced type defined,
  every field's optionality stated, every cross-field rule written.
- **Regression case:** `DERIVED_VALUE` without `value_ref` is ill-formed;
  `shortfall=true` with `shortfall_description=none` violates inv. 5.
- **Evidence status:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Version history:** opened v0.6-work-order; partial v0.6; reopened;
  corrected v0.7.

---

## New defects D-016 – D-024

### D-016: Incomplete language primitives

- **Original observation (v0.6 §B.11):** `validator_contract` calls
  `is_some(d.error)`, but `is_some` is absent from the §B.4 builtin list —
  unbound identifier; the contract is not well-typed. `range` typed but
  semantics undefined; record/option/list equality mentioned but not defined
  recursively.
- **Root cause:** Builtins were listed from memory of use, not audited
  against examples; "structural equality" was assumed self-explanatory.
- **Invariant:** M5 — every identifier in every normative example resolves
  (builtin list, definition, bound variable, keyword, or field access).
- **Regression case:** the v0.6 contract text → `is_some` unresolvable;
  v0.7 adds it; `range(3) = [0,1,2]` is now normative.
- **Expected result:** §B.4 rules 3 (equality) and 11 (builtins, incl.
  `is_some`, `range` semantics).
- **Affected documents:** design spec §B.4/§B.11.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (M5 identifier audit).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No type-checker implementation.
- **Version history:** introduced v0.6; corrected v0.7.

### D-017: Binary64 canonicalisation not unique

- **Original observation:** `0x1.0000000000000p+1` vs `0x2.0000000000000p+0`
  (both 2.0); `0x0.0000000000001p-1022` vs `0x1.0000000000000p-1074`
  (both min subnormal); `p+01` allowed.
- **Root cause:** The uniqueness claim was asserted, not proved — the
  induction step (leading digit must be exactly 1) was never attempted.
- **Invariant:** M6 — every uniqueness claim is challenged by explicit
  collision construction before acceptance.
- **Regression case:** the two pairs above → exactly one form each under
  §G.2; the rejected forms are named.
- **Expected result:** §G.2 exact grammar + per-class uniqueness argument.
- **Affected documents:** design spec §G.2, matrix E3, acceptance plan §6.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (M6 round-trip/collision script).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** Paper induction, not machine-checked.
- **Version history:** introduced v0.6 (`msve-canonical-2`); corrected v0.7
  (`msve-canonical-3`).

### D-018: Incomplete canonical type coverage

- **Original observation:** function types in `TypeExpr` with no encoding
  rule; `Impl` without signature; non-finite computed values (1.0/0.0 → ∞)
  with no packaging rule.
- **Root cause:** The encoding profile was built from the value types in
  examples, not from the `TypeExpr` grammar.
- **Invariant:** M7-style — every `TypeExpr` kind has an encoding rule or
  an explicit not-encodable rule.
- **Regression case:** `Impl("d", (Nat)->Nat)` vs `Impl("d", (Int)->Int)` →
  different bytes; a function value → `output-not-encodable` packaging
  failure; `1.0/0.0` → `{"$type":"f64","value":"inf"}`; NaN → packaging
  failure.
- **Expected result:** §G.2 rules as written.
- **Affected documents:** design spec §G.2/§E.7, matrix E3.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No encoder implementation.
- **Version history:** introduced v0.6; corrected v0.7.

### D-019: Real/Rat inconsistency

- **Original observation:** `to_rat_exact(1.0/3.0) = None` despite 1/3 being
  exactly a `Rat`; no proper outcome for valid-but-unserializable results.
- **Root cause:** "Exact conversion" was defined as "finite-decimal
  conversion"; the status model had only INVALID_INPUT for packaging
  problems.
- **Invariant:** conversion total and exact over the v0 domain; packaging
  failures are never input errors.
- **Regression case:** `derive 1.0/3.0` → `{"$type":"real","value":"1/3"}`;
  NaN output → INTERNAL_ERROR(output-not-encodable) with semantic result
  preserved.
- **Expected result:** §B.4 rule 11 (`to_rat`), §G.2 real rule, §E.7 inv. 10.
- **Affected documents:** design spec §B.4/§B.9/§E.7/§G.2/C, matrix C2/E3.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** True reals remain future work (App.3).
- **Version history:** opened as D-009 (v0.6-work-order); the v0.6 correction
  was insufficient; corrected v0.7 (kept under D-009's history; D-019 is the
  forensic finding's tracking ID — both point here).

### D-020: Non-closed validation types

- **Original observation:** `ErrorCode = String` called a closed enumeration;
  `DecodeOutcome` admittable as `{ok:true, error:some(e)}`.
- **Root cause:** Closure claimed by listing, not by rule.
- **Invariant:** M7 — closed types have a membership predicate; contradictory
  states are either unrepresentable or contract-violating by construction.
- **Regression case:** `is_error_code("bogus") = false`; a decoder returning
  `{ok:true, error:some("malformed-json")}` fails `validator_contract`.
- **Expected result:** §B.13a + contract conjunct + `DecodeOutcome` invariant.
- **Affected documents:** design spec §B.11/§B.13/§E.1.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (M7: disjuncts = table codes).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No implementation to violate it.
- **Version history:** introduced v0.6; corrected v0.7.

### D-021: Evidence-category mismatch (syntax)

- **Original observation:** `proof: independent-recompute` conflates
  categories the §D.6 table distinguishes.
- **Root cause:** Grammar edited for policy convenience, not category hygiene.
- **Invariant:** syntactic categories match evidential categories.
- **Regression case:** §B.12 ex.18.
- **Expected result:** `RecomputeReq` production; updated B.7 rules; example
  uses `recompute:`.
- **Affected documents:** design spec §B.2/§B.3/§B.7/§B.11/§B.12/§D.6/§E.1,
  acceptance plan, matrix P4.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** —
- **Version history:** introduced v0.4 (`proof:` alternative); corrected v0.7.

### D-022: Result-schema gaps

- **Original observation:** payload-less tags; "illustrative" invariants;
  undefined `involved_records` / `recorded_at`; missing Level-B-acceptance
  invariant.
- **Root cause:** Schema grown by accretion; invariants stated as examples.
- **Invariant:** every tag carries its audit payload; invariants exhaustive
  and checkable.
- **Regression case:** §E.7 inv. 1–14, each with a violating instance.
- **Expected result:** §E.1–§E.7 as written.
- **Affected documents:** design spec §E, matrix E1, visualisation Diagram 4
  note.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No records instantiated by execution.
- **Version history:** introduced v0.2; partial v0.6; corrected v0.7.

### D-023: Incomplete visualisation document

- **Original observation:** v0.6 visualisation plan reproduced only Diagram
  3's source; Diagrams 1, 2, 4–7 "retained" by reference — unauditable.
- **Root cause:** D-011 applied to the spec but not to the package.
- **Invariant:** every normative diagram's source is reproduced in the
  document that claims it.
- **Regression case:** v0.7 visualisation plan contains all seven Mermaid
  sources.
- **Expected result:** `MSVE_VISUALISATION_PLAN_v0.7.md`.
- **Affected documents:** visualisation plan.
- **Verification method:** MECHANICAL_DOCUMENT_CHECK (seven fenced sources
  present).
- **Evidence status:** MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** —
- **Version history:** introduced v0.5; corrected v0.7.

### D-024: Verification-item ambiguity

- **Original observation:** `duplicate-verification-item` undefined while
  the selector example carries two `test:` items.
- **Root cause:** The error was named before its condition was defined.
- **Invariant:** every admission error has a decidable condition stated
  where the error is listed.
- **Regression case:** two `test: differential …` → duplicate; `test:
  differential …` + `test: property-fuzz …` → legal (§B.12 ex.17).
- **Expected result:** §B.7 D-024 rule.
- **Affected documents:** design spec §B.7/§B.9/§B.12, acceptance plan.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** —
- **Version history:** introduced v0.2 (error name); corrected v0.7.

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
