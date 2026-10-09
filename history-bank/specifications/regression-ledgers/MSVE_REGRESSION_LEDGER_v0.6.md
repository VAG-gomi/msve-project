# MSVE Regression Ledger v0.6

**Status:** DURABLE PROJECT DOCUMENT — carried forward by every successor version
**Version:** 0.6 · **Work order:** MUSE WORK ORDER 0.6

## Purpose and rules

This ledger is the correction loop's memory. Every entry preserves a known
defect so that no successor version can silently reintroduce it, rename it
away, or declare it fixed without the stated evidence.

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

## Inherited defects D-001 – D-015

### D-001: Validator contract logically inconsistent

- **Original observation (v0.5 §B.11):** The contract required
  `is_some(out) ==> (is_wellformed(unwrap(out)) /\ parses_as_valid(raw))`
  and `!is_some(out) ==> !parses_as_valid(raw)`, where `parses_as_valid`
  checked JSON shape only. For `raw = "[]"` (vacuously shape-valid but
  semantically empty), `None` violates the second clause; `Some(B)` satisfies
  the first only by fabrication. No correct output exists — the contract is
  unsatisfiable for correct behaviour. Same for duplicate-UCIs arrays.
- **Root cause:** A Boolean shape predicate was used as a substitute for a
  parse relation; structural validity and semantic validity were conflated
  in one predicate, and the contract's two clauses partitioned the world on
  the wrong predicate.
- **Invariant:** The validator contract must separate (1) raw input,
  (2) syntax parsing, (3) structural decoding, (4) semantic validation,
  (5) a typed outcome — and must be satisfiable by exactly the correct
  behaviour for every input in the domain.
- **Regression case:** `raw = "[]"` → expected `ValidationOutcome{
  accepted=false, candidates=none, error=some("empty-candidate-set")}`.
  `raw = "[{...},{...}]"` with duplicate UCIs → `error=some("duplicate-uci")`.
- **Expected result:** `validator_contract("[]", out)` holds iff `out` is the
  empty-set rejection; no fabrication path satisfies the contract.
- **Affected documents:** design spec §B.11/§B.13/App.2, acceptance plan,
  visualisation Diagram 3.
- **Verification method:** SPECIFICATION_REVIEW of the three-stage pipeline +
  MECHANICAL_DOCUMENT_CHECK (contract derives; no `parses_as_valid` remains).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
  No implementation exists; no EXECUTED_TEST.
- **Residual limitation:** Correctness of the *abstract* contract only; L2
  parser conformance is a separate, unperformed check.
- **Version history:** introduced v0.4 (`parses_as_valid` Boolean);
  corrected v0.6 (three-stage pipeline).

### D-002: Accepted validator output not bound to the input

- **Original observation:** v0.5's contract permitted `Some(B)` for any
  well-formed `B` unrelated to `raw` — fabrication, omission, alteration
  and reordering all satisfied the predicate.
- **Root cause:** The contract constrained the output's *properties* but
  never its *relation* to the input; extensional equality with a reference
  pipeline was missing.
- **Invariant:** An accepted outcome must equal the decoded-and-validated
  input exactly: same candidates, same order, no additions/removals/changes.
- **Regression case:** `raw` = valid 2-candidate array; implementation
  returns the candidates in swapped order, or a third fabricated candidate →
  expected: `validator_contract` evaluates to false (VIOLATED with witness).
- **Expected result:** `out == validate(decode_candidates(raw).candidates)`
  is the contract; any deviation fails it.
- **Affected documents:** design spec §B.11/App.2, acceptance plan §8.
- **Verification method:** SPECIFICATION_REVIEW.
- **Evidence status:** SPECIFICATION_REVIEW. No implementation; no EXECUTED_TEST.
- **Residual limitation:** Abstract-contract level only.
- **Version history:** introduced v0.4; corrected v0.6.

### D-003: Validation errors not representable

- **Original observation:** `Option<CandidateSet>` cannot name defects;
  `None` conflates malformed JSON, missing fields, wrong types, duplicate
  UCIs, non-finite scores.
- **Root cause:** The outcome type was chosen for convenience (`Option` was
  already in the language) rather than derived from the contract's
  requirements (deterministic defect reporting).
- **Invariant:** Every rejection carries a deterministic error code from a
  closed, documented enumeration; detection priority is fixed and total.
- **Regression case:** each §B.13 table row → its exact code; e.g. rank
  `"x"` (valid JSON, wrong type) → `invalid-field-type`; unquoted keys →
  `malformed-json` (D-013).
- **Expected result:** `decode_candidates` returns the table's code for
  every listed condition; `validate` returns the if-chain's code.
- **Affected documents:** design spec §B.11/§B.13, result schema (unchanged —
  outcome is a value, not a record field), acceptance plan.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (all codes defined; all referenced).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No implementation to test the mapping.
- **Version history:** introduced v0.4; corrected v0.6.

### D-004: Canonical encoding not type-injective

- **Original observation:** v0.5 encoded lists and sets identically as JSON
  arrays: `[1]` and `{1}` both → `[{"$type":"nat","value":"1"}]`,
  contradicting the claimed injectivity. Same for `none: Option<Nat>` vs
  `none: Option<String>`.
- **Root cause:** Injectivity was asserted from examples rather than argued
  from the encoding rules; composite kinds lacked distinguishing tags.
- **Invariant:** Distinct (type, value) pairs → distinct byte strings, argued
  by structural induction over the tag rules, with collision counterexamples
  from the previous profile recorded.
- **Regression case:** list `[1]` → `{"$type":"list","of":"nat","items":[...]}`;
  set `{1}` → `{"$type":"set","of":"nat","items":[...]}` — different bytes.
  `none:Option<Nat>` vs `none:Option<String>` — differ in the `of` tag.
- **Expected result:** v0.6 encodings differ; the v0.5 collision pair is
  documented in §G.2 as the reason for `msve-canonical-2`.
- **Affected documents:** design spec §G.2, matrix E3, acceptance plan.
- **Verification method:** SPECIFICATION_REVIEW (induction argument) +
  MECHANICAL_DOCUMENT_CHECK (every TypeExpr kind has a tag rule).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** The induction is a paper argument, not a
  machine-checked proof.
- **Version history:** introduced v0.2 (profile); collision present v0.5;
  corrected v0.6 (`msve-canonical-2`).

### D-005: Canonical vocabulary incomplete (`Hash`/`Hex`/binary64)

- **Original observation:** `Hash`/`Hex` used as schema types, undefined;
  binary64 "normalized hexfloat" underspecified.
- **Root cause:** Schema types were introduced by use rather than by
  definition; precision was deferred with the word "normalized".
- **Invariant:** Every referenced type has a definition, allowed
  representation, validation rule and canonical encoding (schema-closure).
- **Regression case:** `Hash` = exactly 64 `[0-9a-f]` chars; `0x1.0p+0`
  (short hexfloat) is not canonical — must be `0x1.0000000000000p+0`;
  `-0.0` must encode as `0x0.0000000000000p+0`.
- **Expected result:** §E.1 defines `Hash`; §G.2 gives the exact f64 grammar
  with the zero/subnormal rules.
- **Affected documents:** design spec §E.1/§G.2, matrix E3.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** Paper-level exactness; no encoder implementation.
- **Version history:** introduced v0.4 (schema); corrected v0.6.

### D-006: Quantifier scope underspecified

- **Original observation:** `forall c in cs :: P /\ Q` admitted two readings;
  v0.5's "greedy bodies" prose note was fragile disambiguation outside the
  grammar.
- **Root cause:** Binding extent was treated as a parsing footnote instead
  of a grammar rule.
- **Invariant:** Quantifier scope is determined by the grammar alone; no
  well-formed expression has two parses.
- **Regression case:** `forall c in cs :: (P /\ Q)` derives (one parse);
  `forall c in cs :: P /\ Q` is a syntax error (§B.12 ex.15); nested
  quantifiers in §B.11 derive with explicit parens.
- **Expected result:** all §B.11 examples derive under the parenthesized
  production; the bare form is rejected.
- **Affected documents:** design spec §B.2/§B.3/§B.11/§B.12.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (grammar production + example re-derivation).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No parser implementation to confirm rejection.
- **Version history:** present since v0.1; prose patch v0.5; grammar rule v0.6.

### D-007: Signed integers and mixed arithmetic incoherent

- **Original observation:** v0.5 made `-3 : Int` (unary minus on `Nat`) while
  forbidding mixed arithmetic, so the ordinary `-3 + 2` was ill-typed.
- **Root cause:** Two rules designed independently (no-implicit-promotion;
  unary-minus typing) with no joint consideration of mixed expressions.
- **Invariant:** One explicit, exact Nat→Int embedding governs all mixed
  Nat/Int arithmetic; every other type combination is a type error; division
  semantics (exact-or-error) is stated.
- **Regression case:** `-3 + 2 : Int` = `-1` ✓; `1.5 + 2` → type error
  (§B.12 ex.17); `7 / 2` on Nats → execution error `inexact-division`.
- **Expected result:** §B.4 rule 2/2a as written.
- **Affected documents:** design spec §B.4/§B.12, matrix C1–C2.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No type-checker implementation.
- **Version history:** introduced v0.4 (rule 2a); corrected v0.6.

### D-008: Raw JSON number conversion undefined

- **Original observation:** v0.5 never said what `1e400`, `1.5` (as rank),
  `-0`, duplicate keys or trailing data mean at the decode boundary.
- **Root cause:** The parsing primitive was axiomatized as a Boolean,
  hiding all conversion decisions.
- **Invariant:** The §B.13 table fixes every listed condition with
  deterministic priority; JSON-syntax validity and per-type value validity
  are distinguished.
- **Regression case:** `[{"uci":"a","rank":1.5,"score":0.5}]` → `invalid-rank`;
  `[{"uci":"a","rank":1,"score":1e400}]` → `invalid-score`;
  `{"uci":"a","rank":1,"score":0.5} trailing` → `malformed-json`;
  `[{"uci":"a","rank":1,"rank":2,"score":0.5}]` → `duplicate-key`.
- **Expected result:** table rows 1–10 of §B.13.
- **Affected documents:** design spec §B.13, acceptance plan §6/§8.
- **Verification method:** SPECIFICATION_REVIEW.
- **Evidence status:** SPECIFICATION_REVIEW. Decoder is specified, not built.
- **Residual limitation:** L1 claims conditional on the table (D-012).
- **Version history:** introduced v0.4; corrected v0.6.

### D-009: `Real` vs hashed artifacts unresolved

- **Original observation:** v0.5 excluded `Real` from hashed artifacts but
  left the "explicit conversion to rational" operationally undefined, and
  `Rat` was not even a language type.
- **Root cause:** The exclusion was a boundary drawn without a mechanism
  for crossing it.
- **Invariant:** v0 `Real` denotes exact rationals; the finitely-decimal
  subset is exactly encodable; the rest is refused at packaging with a named
  reason; `to_rat_exact` is the defined crossing mechanism; `Rat` is a type.
- **Regression case:** `derive 1.0/3.0` → value not finitely decimal →
  packaging → INVALID_INPUT(real-not-encodable); `to_rat_exact(3.14)` →
  `Some(157/50)`.
- **Expected result:** §B.4 rule 11, §G.2 real encoding rule.
- **Affected documents:** design spec §B.4/§G.2/C, matrix C1–C2/E3.
- **Verification method:** SPECIFICATION_REVIEW.
- **Evidence status:** SPECIFICATION_REVIEW.
- **Residual limitation:** True reals remain out of scope (App.3).
- **Version history:** introduced v0.4; partial v0.5; corrected v0.6.

### D-010: Assurance vocabulary incomplete

- **Original observation:** `assurance_achieved` had `LEVEL_B_SOLVER_BACKED`
  but no test-backed value; shortfall computation implicit.
- **Root cause:** The schema was extended by example (solver case) rather
  than from the evidence taxonomy.
- **Invariant:** required / bases / achieved are separate; shortfall is
  computed by the normative rule; every permitted evidence path (§D.6) is
  representable.
- **Regression case:** test-backed check with `level-b accepted`, tests pass
  → `required=LEVEL_B, bases=[TEST_BACKED], achieved=LEVEL_B,
  shortfall=false`. Solver UNSAT + `level-a required` → `achieved=NONE`(or B
  if accepted), `shortfall=true`, description names the gap.
- **Expected result:** §E.1 schema + shortfall rule.
- **Affected documents:** design spec §E.1/§E.4, matrix E1, visualisation.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No records produced (no execution).
- **Version history:** introduced v0.2; corrected v0.6.

### D-011: Specification not self-contained

- **Original observation:** v0.5 said "§A.2–A.5 unchanged from v0.4" and
  "§E.2–E.9 retained" — a genesis commit cannot depend on historical drafts.
- **Root cause:** Incremental drafting treated the previous version as
  shared context.
- **Invariant:** v0.6 reproduces every normative definition; the only
  backward references are explicit supersession notes, never normative
  dependencies.
- **Regression case:** a reader with only the v0.6 package can state the
  admission rules, the schema, and the assurance policy.
- **Expected result:** full §A, §E.2–E.9 in the v0.6 spec.
- **Affected documents:** design spec (all sections).
- **Verification method:** MECHANICAL_DOCUMENT_CHECK (no "retained from" /
  "unchanged from" normative references remain).
- **Evidence status:** MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** —
- **Version history:** introduced v0.2; corrected v0.6.

### D-012: Parser assumptions exceed formalisation

- **Original observation:** L1 validator claims over the full `String`
  domain rested on the one-line `parses_as_valid` axiom.
- **Root cause:** The abstraction boundary was drawn to make the proof easy
  rather than to match the implementation's obligations.
- **Invariant:** The abstract decoder is specified (§B.13 table); L1 claims
  are explicitly conditional on it; implementation conformance is a named,
  separate, unperformed L2 obligation.
- **Regression case:** acceptance plan §4–§5 state the conditional and the
  L2 method (or its marked unavailability).
- **Expected result:** three-claim separation with the decoder boundary named.
- **Affected documents:** design spec §B.13/§D.1/§F, acceptance plan.
- **Verification method:** SPECIFICATION_REVIEW.
- **Evidence status:** SPECIFICATION_REVIEW.
- **Residual limitation:** The L2 method itself is proposed, not executed.
- **Version history:** introduced v0.4; corrected v0.6.

### D-013: Misleading malformed-input example

- **Original observation:** acceptance v0.5 §8.4 used
  `"[{uci:\"e2e4\",rank:\"x\",score:0.5}]"` — unquoted keys are invalid JSON,
  so the case tested malformed JSON, not a mistyped rank.
- **Root cause:** Example written from memory of the intent, not derived
  from the JSON grammar.
- **Invariant:** Every regression example is syntactically valid for the
  layer it targets; malformed-JSON, wrong-type, and semantic-violation
  cases are separate.
- **Regression case:** `[{"uci":"e2e4","rank":"x","score":0.5}]` →
  `invalid-field-type`; `[{uci:"e2e4",...}]` → `malformed-json`.
- **Expected result:** acceptance plan v0.6 §8.4 uses the corrected forms.
- **Affected documents:** acceptance plan.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK.
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** —
- **Version history:** introduced v0.5; corrected v0.6.

### D-014: Evidence and verification boundaries unclear

- **Original observation:** `independent-recompute` sat under `proof:` with
  no stated evidential meaning; solver UNSAT risked being read as proof.
- **Root cause:** Method names were treated as self-explanatory.
- **Invariant:** §D.6 table states per method what is established, assumed,
  and not established; recomputation is never called a formal proof.
- **Regression case:** UNSAT + level-a required + solver-only →
  INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET) (§E.4); recompute agreement on
  a derive goal → LEVEL_A with basis INDEPENDENT_RECOMPUTE and the §D.6
  assumptions recorded.
- **Expected result:** §D.6, §E.4, §E.5 as written.
- **Affected documents:** design spec §B.7/§D.6/§E.4/§E.5, matrix P1–P4.
- **Verification method:** SPECIFICATION_REVIEW.
- **Evidence status:** SPECIFICATION_REVIEW.
- **Residual limitation:** Separation requirements for the recompute checker
  are stated in the acceptance plan, not yet instantiated.
- **Version history:** present since v0.2; corrected v0.6.

### D-015: Result schema not closed

- **Original observation:** Major record names present, but `Hash`/`Hex`,
  enums, optionality rules and cross-field invariants incomplete.
- **Root cause:** Schema grown by accretion across versions.
- **Invariant:** Full dependency closure: every referenced type defined;
  every field's optionality stated; every cross-field invariant written as
  a rule (§E.1 invariants, §E.7).
- **Regression case:** an `INCONCLUSIVE` record with `shortfall=true` but
  `shortfall_description=none` violates the §E.7 combination rules.
- **Expected result:** §E.1 (all types) + §E.7 as written.
- **Affected documents:** design spec §E, matrix E1.
- **Verification method:** SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK
  (M3-style reference closure over §E).
- **Evidence status:** SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK.
- **Residual limitation:** No records instantiated by execution.
- **Version history:** present since v0.2; corrected v0.6.

---

## New defects found during v0.6 drafting

(none — the v0.6 mechanical checks caught two draft-stage issues before
delivery: a `\/` vs `\\/` operator-literal mismatch between grammar and
examples, and seven dropped keywords; both fixed in-draft and recorded in
the design review. No new normative defects were discovered.)

*End of MSVE_REGRESSION_LEDGER_v0.6.md — to be carried forward by v0.7+.*
