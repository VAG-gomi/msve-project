# Report B — Design Evidence — Regression Ledger (Part 1/2)

**Work Order:** 0.8.2 · **Source file:** `six-docs/MSVE_REGRESSION_LEDGER_v0.8.md` (DIRECT ARTEFACT, sha256 `e04a05e68e92ce54…`)

Complete original text, unmodified. Part 1 of 2. CONTINUED in next part.

---

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