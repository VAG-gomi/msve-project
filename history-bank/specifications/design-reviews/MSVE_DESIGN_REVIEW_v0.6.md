# MSVE Design Review v0.6

**Reviewer:** Muse, operating as the MSVE Specification Correction Loop
(self-review — NOT independent) · **Status:** DRAFT
**Scope:** the six-document v0.6 package (spec, review, matrix, acceptance
plan, visualisation plan, regression ledger)
**Work order:** MUSE WORK ORDER 0.6 · **Decision requested:** owner review;
this review does not freeze, accept, or authorize implementation.

**Evidence labels used** (per the work order): SPECIFICATION_REVIEW ·
MECHANICAL_DOCUMENT_CHECK · IMPLEMENTATION_CONFORMANCE · EXECUTED_TEST ·
FORMAL_PROOF · INCONCLUSIVE. No label is used unless the named check was
actually performed.

## 1. Inherited-defect coverage (D-001 – D-015)

| ID | Correction in v0.6 normative text | Evidence | Status |
|---|---|---|---|
| D-001 | Three-stage pipeline replaces the contradictory contract: decode (§B.13) → validate (§B.11) → `validator_contract` as extensional equality; `"[]"` → decode-ok + `validate` → `rejected("empty-candidate-set")` — satisfiable, no fabrication path | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (contract derives; `parses_as_valid` fully removed) | Corrected at spec level |
| D-002 | Accepted outcome must equal `validate(decode(raw).candidates)` — exact input binding | SPECIFICATION_REVIEW | Corrected at spec level |
| D-003 | `ValidationOutcome` with closed `ErrorCode` enumeration; deterministic priority (§B.13 table + `validate` if-chain) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-004 | `msve-canonical-2`: every type tagged (`list`≠`set`, `of` tags on options); induction argument; v0.5 collision pairs documented | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (every TypeExpr kind has a tag rule) | Corrected at spec level |
| D-005 | `Hash` defined (§E.1); exact binary64 grammar (§G.2) incl. zero/subnormal rules | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-006 | Quantifier bodies parenthesized in the grammar; bare form is a syntax error (§B.12 ex.15); all examples re-derived | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-007 | Unary minus + one exact Nat→Int embedding; `-3 + 2 : Int`; exact-division-or-error; `1.5 + 2` type error (§B.12 ex.17) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-008 | §B.13 conversion table (ranks, scores, overflow/underflow/−0, duplicate keys, trailing data) with deterministic priority | SPECIFICATION_REVIEW | Corrected at spec level |
| D-009 | `Real` = exact rationals in v0; finitely-decimal subset exactly encodable; `to_rat_exact`; `Rat` is a type; else `real-not-encodable` | SPECIFICATION_REVIEW | Corrected at spec level |
| D-010 | required / bases / achieved separated; normative shortfall rule; test-backed Level B representable | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-011 | Full §A, §E.2–E.9 reproduced; zero normative backward references (mechanically verified) | MECHANICAL_DOCUMENT_CHECK | Corrected |
| D-012 | §B.13 specifies the abstract decoder; L1 claims explicitly conditional; L2 conformance a named separate obligation | SPECIFICATION_REVIEW | Corrected at spec level |
| D-013 | Acceptance §8.4 uses valid JSON for the type-error case; malformed-JSON case separate | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected |
| D-014 | §D.6 evidence taxonomy; recomputation's evidential meaning stated, never called a proof; UNSAT refusal rule (§E.4) | SPECIFICATION_REVIEW | Corrected at spec level |
| D-015 | Schema closure: all types defined, optionality stated, cross-field invariants as rules (§E.1, §E.7) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |

**Correction-to-invariant mapping:** each row above preserves its ledger
invariant (ledger §D-001…D-015). No defect was renamed, merged away, or
downgraded: the fifteen identifiers and their original failure modes are
intact in `MSVE_REGRESSION_LEDGER_v0.6.md`.

## 2. Regression-case mapping

Every work-order §5 case group maps to a corrected normative rule:

- **Validator cases** (14): each §B.13 table row and `validate` branch is a
  case with an expected error code; binding probes (§8.4) target D-002.
- **Canonical cases** (10): list/set, nesting, field order, `none` across
  option types, int/rat reduction, f64 ±0/subnormals/spellings, non-encodable
  values — all decided by §G.2 rules.
- **Grammar/type cases** (8): bare quantifier (rejected), nested quantifiers
  (derive), escapes (lexical), `-3 + 2` / `1.5 + 2`, `Real` packaging,
  guarded `case`, `==>` classicality.
- **Assurance/schema cases** (9): UNSAT-without-certificate, failed
  certificate, recompute disagreement, bounded-corpus limits, empty corpus,
  unmet assurance, test-backed Level B, inconclusive-vs-negative,
  checker divergence — all representable per §E.1/§E.4/§E.6.

These are **specification-level cases** (the work order's required honesty):
no case is claimed as an executed test.

## 3. Adversarial challenge (gate 6) — performed

1. *Can a valid raw input still be rejected under an impossible condition?*
   `"[]"` now flows decode-ok → `validate` → named rejection: satisfiable. ✓
2. *Can an invalid input be accepted via an unrelated output?* The contract
   requires extensional equality with the reference pipeline. ✓
3. *Can two typed values share canonical bytes?* The v0.5 collision pairs
   differ under canonical-2; the induction argument covers the type grammar. ✓
4. *Two parses from one expression?* Quantifier parens are grammatical;
   precedence chain is total. ✓
5. *Example type-checking vs the rules?* The validator contract and both
   check examples were derived per-token against the v0.6 grammar and typing
   rules. ✓
6. *A result the schema can't represent?* Test-backed Level B, shortfall,
   divergence, interruption, partials — all representable; §E.7 guards
   combinations. ✓
7. *Assurance exceeding evidence?* The shortfall rule is computed; bases are
   recorded; §D.6 caps each method. ✓
8. *Cross-document incompatibility?* §5 below. ✓
9. *Defect omitted from the ledger?* All fifteen carried; §1 maps each. ✓
10. *What would falsify the corrections?* A counterexample input whose
    required outcome the normative rules don't entail — none found in the
    challenge pass; the ledger records the cases for future falsification. ✓

Draft-stage catches (fixed before delivery, per the loop's honesty rule):
the EBNF fence-extraction bug in the checker (prose words flagged as
nonterminals — checker fixed, not the spec); the `\/` vs `\\/` operator
literal mismatch (spec fixed); seven dropped keywords from the v0.5 rewrite
(spec fixed). The v0.6 checker now reads only fenced EBNF blocks.

## 4. Evidence obtained vs not obtained

**Obtained:**
- MECHANICAL_DOCUMENT_CHECK: M1 nonterminal closure (47 defined / 55
  referenced / 0 undefined); M2 keyword–literal agreement (100 literals,
  0 unaccounted, 0 unused keywords); M3 section-reference resolution (all
  resolve across 6 documents); no `parses_as_valid`/`unwrap` remnants; no
  normative backward references.
- SPECIFICATION_REVIEW: per-token derivation of the validator contract,
  selector contract, and quantifier examples under the v0.6 grammar and
  typing rules; the 10 adversarial questions above; schema-closure audit.

**Not obtained (disclosed):**
- No parser, type-checker, decoder, or canonicalizer implementation exists
  (out of scope) → no IMPLEMENTATION_CONFORMANCE, no EXECUTED_TEST.
- L1 proof sketches (U1–U4, V1–V3) are proposed methods, not FORMAL_PROOFs.
- L2 conformance methods are proposed, not executed.
- The canonical injectivity argument is a paper induction, not machine-checked.
- No OWNER_DECISION_REQUIRED arose: all choices (Real=exact rationals,
  Nat→Int embedding, required quantifier parens, canonical-2 supersession)
  were resolved within the work order's mandate and are recorded with
  rationale; none was silently settled against the owner's known positions.

## 5. Cross-document consistency report

- **Spec ↔ ledger:** all 15 defects' corrections present in normative text;
  invariants match.
- **Spec ↔ matrix:** C1/C2 (arithmetic model), E1 (schema closure), E3
  (canonical-2), P4 (decoder-conditional L1) aligned; no capability claimed
  beyond what the language/schema/evidence model supports.
- **Spec ↔ acceptance plan:** contracts (§B.11/§B.13/App.2) match the plan's
  oracles; regression cases map to ledger entries; entry conditions intact.
- **Spec ↔ visualisation:** Diagram 3 shows the three-stage pipeline and
  typed outcome; Diagram 4's assurance note shows required/bases/achieved
  + computed shortfall — no single-badge assurance implied.
- **Terminology/version:** v0.6 / `0.6.0` / `msve-canonical-2` used
  consistently; `msve-canonical-1` mentioned only as superseded.

## 6. Release-gate decision

**READY_FOR_OWNER_REVIEW.**

Reasons: no known release-blocking regression remains among D-001–D-015 —
each has a corrected normative rule, an invariant, regression cases, and
specification-level plus mechanical evidence as listed in §1. All required
specification-level checks were evaluated; the §4 disclosures state exactly
what was not checked. Unresolved matters (no implementation, unproved L1
sketches, paper-only injectivity argument) are disclosed, not hidden.

This status is **not** owner approval, acceptance, freeze, or implementation
authorisation. It means the package is fit for the owner's review.

*End of MSVE_DESIGN_REVIEW_v0.6.md (draft).*
