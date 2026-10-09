# MSVE Design Review v0.5

**Reviewer:** Muse (self-review — NOT independent) · **Status:** DRAFT
**Scope:** `MSVE_DESIGN_SPEC_v0.5.md`, `MSVE_CAPABILITY_MATRIX_v0.5.md`,
`MSVE_ACCEPTANCE_PLAN_v0.5.md`, `MSVE_VISUALISATION_PLAN_v0.5.md`
**Work order:** MUSE WORK ORDER 0.4 (narrow correction pass addressing the seven
v0.4 blockers + the mathematical issue)
**Decision requested:** owner review; NOT a freeze recommendation from this review.

## 1. Method (what was actually checked)

This review changed method after four consecutive rounds in which
document-level "complete / PASS" claims were refuted by the documents'
own text. No claim below is marked as established unless the checking
procedure is named. Three mechanical procedures were run against the
actual v0.5 text:

- **M1 — nonterminal closure:** a script extracts all EBNF productions from
  §B.3, strips quoted literals, character classes and comments, and reports
  any referenced nonterminal with no defining production. (Catches the
  defect-01 class: undefined symbols.)
- **M2 — keyword/literal cross-check:** every quoted literal in the
  productions must be a declared §B.2 keyword, a type literal, or an
  operator/punctuation symbol; every declared keyword must appear as a
  literal. (Catches dropped or phantom keywords.)
- **M3 — section-reference resolution:** every `§X.N` reference across the
  four documents must resolve to an existing section header.
- **M4 — per-token example derivation:** the two most complex examples
  (selector check, validator check) derived token-by-token against the
  lexical rules and productions, with typing rules applied at each step.
  The remaining examples were checked for header/goal/verification/limits
  conformance.

**Not checked:** no parser was implemented, so M1–M4 do not constitute a
machine parse of the examples; the L1 proof sketches (U1–U4, V1–V2) are
proposed methods, not established proofs; no implementation exists, so
no conformance claim is made. (M3 flags two intentional mentions in §3
below of the historical misnumbered references §B.13/§B.14, explicitly
marked there as nonexistent.)

## 2. Defect ledger (v0.4 → v0.5)

| # | v0.4 defect (verified in v0.4 text) | v0.5 correction | Check |
|---|---|---|---|
| 01 | `Esc` referenced, undefined; no Int/Real/Binary64 literal syntax; unary-minus typing undefined | `Esc` defined (JSON escapes); `RealLit` added (exact decimals); `Nat` digits; Int via unary minus with typing table (Nat→Int, Int→Int, Real→Real, Binary64→Binary64-IEEE); Binary64 literals explicitly restricted (computation/external only) | M1 passes (47 defined, 55 referenced, 0 undefined); M4 applied to `-`-using and literal-using examples |
| 02 | `compare-models` had no model type; `output` typing vacuous | `CompareGoal` now carries `TypeExpr`; example: `goal compare-models M satisfying [two_vals] under xproj`; §B.5a ties `output` and projection paths to it | M4: example derives; projection path `output.x` resolves against `M` |
| 03 | No `RawInput`/validation-result type; invalid inputs fuzzed against selector contract | `type RawInput = String`; validator `Impl(RawInput -> Option<CandidateSet>)`; `validator_contract` formalized with `parses_as_valid` builtin (§B.4 rule 10, App. 2 §A2.9); acceptance plan §2/§6 route invalid inputs to the validator only | M4: validator example derives; `check` invocation rule (§B.5) type-matches |
| 04 | Empty corpus → vacuous HOLDS | §B.5b: HOLDS requires non-empty corpus; empty → INCONCLUSIVE(NO_TEST_CORPUS); `cases: 0` → INVALID_INPUT(degenerate-fuzz-config); §B.12 ex.14 records the rule | Adversarial case A4 (below) |
| 05 | §B.7 kernel-proof demand vs §E.5 recomputation eligibility | Goal-specific admission: `prove`+level-a→kernel-checked; `derive`+level-a→kernel-checked **or** independent-recompute; solver/test goals+level-a→assurance-level-unavailable; new `derive-level-a` example demonstrates the recompute route | M4: derive-level-a derives and passes the goal-specific static rule |
| 06 | Encodings incomplete; Real unexplained in hashed artifacts | §G.2 complete: records (sorted keys), lists, sets (sorted by canonical bytes), options, bools, strings, impl handles, blobs by hash; Real→INVALID_INPUT(real-not-encodable) at the canonicalizer with the explicit rationale and conversion requirement | Matrix E3 row updated; no example violates the profile |
| 07 | Schema types referenced, undefined | §E.1 defines ErrorCode (closed catalog), SemanticResult (Option), ReasonCode (+NO_TEST_CORPUS), SolverObs, VerificationRecord, EvidenceBundle (+ArtifactRef, ExternalEvidence), PartialResult (with presence validation), Discrepancy (with status-transition rule) | M3: all §E.1 type references resolve; no undefined type names remain |
| M | "Finite checklist case analysis" as validator universality proof | Withdrawn. Acceptance plan §4 states the L1 method as structural coverage of the full String domain (case split on parse outcome + checklist branching exhaustiveness) and keeps the three claims separate: (a) abstract model correct, (b) implementation conforms, (c) bounded tests found no failures in cases tested | Prose verified against the three-claim separation; (a)/(b)/(c) never conflated in §4–§6 |

## 3. Defects found *during* this review (by M1–M3)

The mechanical checks earned their keep — three genuine defects in the v0.5
draft, all fixed before this review was written:

1. **Dropped keywords (M2):** the rewritten §B.2 keyword list omitted `seeds`,
   `cases`, `spec-hash`, `input-hash`, `tool-versions`, `witness`, `outputs`
   — all grammar literals. Restored.
2. **Misnumbered example references (M3):** §B.1 pointed to the nonexistent
   §B.13/§B.14 (historical misnumbering); the examples live at §B.11/§B.12.
   Corrected.
3. **Dangling §E.4 references (M3):** §E.4 is not a standalone header (it is
   inside the `E.2–E.9` range). Three references repointed to §E.2–E.9.
4. **Unspecified quantifier-body extent (M4):** greedy-body rule and the
   `==>`/`/\`/`\/` precedence chain added as parsing notes in §B.2.

## 4. Adversarial cases (re-run against v0.5)

- **A1 (undefined symbol):** every nonterminal in every production resolves —
  the v0.4 `Esc` counterexample is closed (M1).
- **A2 (typeless goal):** `compare-models` now requires a model type at the
  grammar level; a missing type is a syntax error, not a semantic gap.
- **A3 (wrong-object fuzzing):** acceptance §8.4 walks a malformed raw input
  through both contracts, showing the selector routing is now prohibited.
- **A4 (empty corpus):** `test: none` on a check goal → INCONCLUSIVE(NO_TEST_CORPUS)
  per §B.5b/§B.12-ex.14; `cases: 0` rejected at admission.
- **A5 (Level A contradiction):** derive-level-a passes the goal-specific
  rule; a `prove` goal with `proof: none` + `level-a required` still fails
  admission — the two rules are consistent, not contradictory.
- **A6 (unencodable artifact):** a `Real` value in a hashed artifact →
  INVALID_INPUT(real-not-encodable); the conversion requirement is in-spec.
- **A7 (undefined schema type):** no result-record field references an
  undefined type (M3 + manual pass over §E.1).
- **A8 (membership hole):** retained from v0.4 — whole-record `sel == c`
  rejects score-inflated records (acceptance §8.3).
- **A9 (binary64 -0.0):** `-0.0` literal impossible (no Binary64 literals);
  computed −0.0 normalized at the canonicalizer; `==` on canonical forms.
- **A10 (duplicate identical records):** position-sensitive distinctness
  rejects; the validator's pairwise rule agrees (A2.5 + §B.11 predicate).
- **A11 (assurance shortfall):** UNSAT with Level A required and only
  Level B available → INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET), shortfall
  recorded — the v0.2 self-contradiction stays closed.
- **A12 (timeout):** TIMEOUT + labelled partials; no silent completion.

## 5. Consistency gate — per-claim results

| Check | Method | Result |
|---|---|---|
| Nonterminal closure | M1 (script) | 47 defined / 55 referenced / 0 undefined |
| Keyword/literal agreement | M2 (script) | 95 literals; all accounted; 0 unused keywords |
| Section references | M3 (script) | All resolve (after the 3 fixes in §3) |
| Selector example derivation | M4 (manual, per-token) | Derives; typing rules applied |
| Validator example derivation | M4 (manual, per-token) | Derives; `==>` short-circuit noted for `unwrap` |
| Level A admission vs policy | Manual: §B.7 × §E.5 | Consistent (goal-specific) |
| Acceptance plan vs contracts | Manual: plan §2/§4–§6 × App. 2 | Invalid inputs routed to validator; three claims separate |
| Matrix vs spec | Manual: capability rows × §B/§E/§G | Aligned (E1 schema types, E3 encodings, P4 corpus rule) |
| Visualisation vs spec | Manual: diagrams × text | Diagram 2 (corpus rule), Diagram 3 (routing) match |

**Explicitly not established by this review:** machine-parseability of the
examples (no parser built); the L1 proof sketches; implementation
conformance (no implementation authorized); freeze-readiness as a
document-level claim — that verdict belongs to external review.

## 6. Residual risks

- Hand-derivation (M4) is weaker than a machine parse; a parser
  implementation remains the honest next verification step for the grammar.
- `parses_as_valid` is an axiomatized builtin; its L2 connection to a real
  parser is a named future obligation, not a closed item.
- The greedy-quantifier rule was added late (this review); examples were
  re-checked against it, but it deserves a second pair of eyes.

## 7. Verdict

The seven v0.4 blockers and the mathematical issue are addressed in the
v0.5 text, and the mechanical checks caught and fixed three further
defects during drafting. I do **not** claim v0.5 is complete or
freeze-ready — the "complete grammar / 12/12 PASS" failure mode of the
previous rounds is exactly what the per-claim method above is meant to
prevent. External review is still required before any freeze decision.
No repository, implementation, or experiment is authorized by this review.

*End of MSVE_DESIGN_REVIEW_v0.5.md (draft).*
