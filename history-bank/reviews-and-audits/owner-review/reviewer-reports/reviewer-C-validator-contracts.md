All checks complete. Here is my independent audit report.

---

# Sub-agent C Report: Validator and Result-Contract Audit (MSVE v0.8)

**Role:** Independent adversarial reviewer — validator, error model, result schema.
**Sources verified directly:** `MSVE_DESIGN_SPEC_v0.8.md` (§B.7, §B.9, §B.11, §B.13/§B.13a, §E.1–E.9, §G.2), `m8/corpus/v08/v08-ex5.msve`, M8 runs I executed myself. I did not rely on any prior summaries.

## Task 6 (M8 run) — done first, so its limits frame everything else

**Command:** `cd /home/hatch/workspace/msve-design && python3 -m m8.cli check m8/corpus/v08/v08-ex5.msve`
**Result:** `M8: PASS` (exit 0). `python3 -m m8.cli spec-examples` → 6/6 valid examples pass; 5/5 invalid examples rejected with the marked categories (syntax, type, name-resolution, admission, lexical).

**What M8 establishes:** the validator example parses under the D-025 record-construction production; every identifier resolves; every expression type-checks — including `{ accepted: false, candidates: none, error: some(e) }` against `ValidationOutcome`, the `case`/`let`/`if` branches, and all builtin applications.

**What M8 does NOT establish** (and no one should claim it does): (a) that the contract's Boolean *logic* is correct — M8 only checks it has type `Bool`; (b) that the D-028 counterexample is rejected — that is semantic evaluation, not type-checking; (c) that `decode_candidates` implements the §B.13 table (D-012, explicitly conditional); (d) that `validate`'s error priority is the *intended* one; (e) that the contract is an adequate test oracle. My hand-derivation below covers (a) for the D-028 case and the invariant's both directions — that is what my derivation adds over M8.

## Task 1 — Validator contract logic (D-028): CONFIRMED FIXED, with full derivation

**(a)** D-028 (was B-03). **(b)** `MSVE_DESIGN_SPEC_v0.8.md` §B.11, `validator_contract` definition.

**(c) Counterexample derivation, step by step.** Substitute `d = { ok: false, candidates: [c], error: some("malformed-json") }`, `out = rejected("malformed-json")` into the contract body:

1. `d.ok` → `false`.
2. First conjunct `d.ok ==> ((!(is_some(d.error))) /\ (out == validate(d.candidates)))`: antecedent `false` → implication `true` (classical `==>`, §B.4 rule 5). Vacuous.
3. Second conjunct `(!(d.ok)) ==> (...)`: `!(false)` = `true` → consequent must hold.
4. Consequent, three conjuncts:
   - `is_some(d.error)` = `is_some(some("malformed-json"))` → **true**;
   - `len(d.candidates) == 0` = `len([c]) == 0` = `1 == 0` → **false**;
   - `case d.error of some(e) -> (is_validation_error(e) /\ (out == rejected(e))) | none -> false` → `e = "malformed-json"`: `true /\ (rejected("malformed-json") == rejected("malformed-json"))` → **true**.
5. Conjunction: `true /\ false /\ true` = **false** → `true ==> false` = **false**.
6. Whole contract: `true /\ false` = **false**.

**(d) Expected:** contract rejects the non-conforming decoder outcome. **Actual:** contract = `false` → rejected. ✓ The v0.8 fix holds. (For comparison I re-derived the v0.7 form without the `len` conjunct: it evaluates to `true` — confirming both the original bug and that the added conjunct is load-bearing.)

**Both invariant directions verified:** true branch enforces `ok=true ⇒ error=none` via `(!(is_some(d.error)))`; false branch enforces `ok=false ⇒ error=some(e) ∧ is_validation_error(e) ∧ candidates=[]` via the three conjuncts. I also verified the true branch on `d={ok:true, candidates:[c₁], error:none}`, `out=accept([c₁])` → `true`, and confirmed the contract is a tight oracle: any implementation whose output differs from the abstract decode→validate pipeline on any input fails the contract, because `out` is pinned to `validate(d.candidates)` / `rejected(e)` by structural equality (order-sensitive lists, exact record fields).

**(e) Root cause of v0.7 failure:** the false branch checked the error's presence and validity but never the candidate list — now repaired.

**(g) Regression case:** the derivation above, plus the true-branch case; both should be preserved as semantic (non-M8) regression cases — M8's corpus contains no D-028 case, correctly, since M8 cannot evaluate contract semantics. The acceptance plan lists it as a proposed L3 case.

**(h) Does NOT establish:** that the abstract `decode_candidates` implements the §B.13 table (D-012 — a stated assumption, correctly disclosed); that `validate`'s priority (empty → invalid-uci → duplicate-uci) is the *intended* order — it is defined only by the `define` itself, which is deterministic and affects only which code is reported, never accept/reject, so this is a design choice, not a defect.

**Minor observation (not a defect):** the contract's false branch accepts all 12 `is_validation_error` codes, while the §B.13 table's failure rows define only 9 decode codes (the other 3 are validate-stage). A decoder emitting `ok=false`/`"empty-candidate-set"` would satisfy the contract. This slack is behaviorally invisible — `out` is identical either way — so I record it as an observation, not a finding.

## Task 2 — Three-type error model (D-029): partition coherent; closure only partially formalized

**Confirmed:** every result-schema field uses the right type (`admission` → `AdmissionError`/`UnsupportedReason`; validator contract → `ValidationError` only); all §B.12 invalid examples use codes from the correct domain (I checked all 16 against the §B.9 lists); the two `is_validation_error` definitions (§B.13a and §B.11) are byte-identical with exactly the 12 codes (verified mechanically).

**(a) NEW-C1 — D-029 residual: `is_admission_error` / `is_unsupported_reason` never formally defined.** **(b)** §B.9. **(c)** N/A (absence). **(d) Expected:** per §B.9's own text, "Each is `String` with a normative closure predicate (a disjunction over string literals, as in §B.13a)." **Actual:** no `define is_admission_error` or `define is_unsupported_reason` exists anywhere in the spec (grep confirms). Only `is_validation_error` is formalized. The 27+3 codes exist as prose lists only, so the closure claim for two of the three types is not mechanically checkable and M8 cannot enforce it. **(e) Root cause:** the formalization was done for the validator's type but not carried through. **(f)** Write both predicates as `define` disjunctions mirroring §B.13a, including the `": <detail>"` base-code rule. **(g)** M8 corpus case: an `INVALID_INPUT` with a non-listed code must be rejected by the predicate. **(h) Does NOT establish** that any *listed* code is wrong — the lists themselves look complete against §B.12.

**(a) NEW-C2 — D-029 residual: execution failures are a fourth, unclosed domain.** **(b)** §E.1 `execution: ... | INTERNAL_ERROR(reason: String)`; §B.4 rule 2. **(d) Expected:** D-029 requires "which domain each error belongs to and the exact allowed values" for "execution failures" too. **Actual:** `reason: String` is unbounded. §B.4 rule 2 promises `inexact-division` and `division-by-zero` as `INTERNAL_ERROR` reasons — real promised outcomes with no closed code. **(f)** Either a closed `ExecutionError` type with predicate, or an explicit normative statement that internal-error reasons are intentionally open with the known reasons enumerated. **(g)** A record with `INTERNAL_ERROR("division-by-zero")` should be classifiable. **(h) Does NOT establish** that any current use is wrong — only that the domain's allowed values are unspecified.

## Task 3 — Result packaging (D-030): two material findings

**(a) NEW-C3 — D-030 residual: `execution` vs `output_packaging` have no consistency rule.** **(b)** §E.1 schema; §E.7 inv. 10, 15; §G.2 "Packaging failure (D-019 status model)". **(c) Counterexample — a record satisfying ALL 22 invariants that is semantically incoherent:**
`execution = INTERNAL_ERROR("output-not-encodable: Binary64")`, `output_packaging = PACKAGING_OK`, `semantic_result = Some(DERIVED_VALUE { value_ref: Some(h), derivation_ref: h2 })`, with `h` present in `evidence.derivation_records`, everything else well-formed.
Check: inv. 15's antecedent needs `PACKAGING_OK ∧ DERIVED_VALUE ⇒ value_ref = Some(_)` ✓; inv. 10 fires (`INTERNAL_ERROR`, reason recorded, starts with `output-not-encodable`, semantic result recorded) ✓; invs. 1–9, 11–14, 16–22 all vacuous or satisfied ✓. Yet the record simultaneously claims packaging failed (`output-not-encodable`) and packaging is OK with a value hash. Two further variants — `COMPLETED` + `PACKAGING_FAILED` + `value_ref=None`, and `INTERNAL_ERROR(…)` + `PACKAGING_FAILED` + `value_ref=None` — also satisfy all invariants. **Three mutually inconsistent recordings of the same NaN event are all conforming.** **(d) Expected:** one unambiguous status model. **Actual:** §G.2 says a NaN "is reported as `execution: INTERNAL_ERROR`", inv. 15 says it "yields `PACKAGING_FAILED(output-not-encodable)`", and no invariant relates the two fields. **(e) Root cause:** v0.8 added `output_packaging` as a separate field without reconciling it with the v0.7-era `INTERNAL_ERROR(output-not-encodable)` rule. **(f)** Add an invariant, e.g. `execution = INTERNAL_ERROR(r) ∧ r starts with "output-not-encodable" ⟺ output_packaging = PACKAGING_FAILED(_)`, and state which field is authoritative. **(g)** The three variant records above: exactly one must be conforming after the fix. **(h) Does NOT establish** that the `Option<Hash>` discipline itself is wrong — inv. 15/16's `PACKAGING_OK⇒Some` / `PACKAGING_FAILED⇒None` logic is sound, which I verified.

**(a) NEW-C4 — D-022/B-05 residual: `UNIQUE_UNDER_PROJECTION` has no E.7 invariant.** **(b)** §E.7. **(c)** `semantic_result = Some(UNIQUE_UNDER_PROJECTION { projection: "xproj" })` with empty `verification_records`, no `solver_observation`, and `verification_summary = NOT_RUN` satisfies every invariant. **(d) Expected:** per B-05's demand, every result alternative needs an evidence link. **Actual:** I checked mechanically — all 10 other `SemanticResult` alternatives are mentioned in E.7; `UNIQUE_UNDER_PROJECTION` is the only one absent. It can be claimed with zero supporting evidence. **(f)** Add an invariant tying it to the §D.2 procedure record (e.g. a solver observation or derivation record showing the second-model query was UNSAT). **(g)** The evidence-free record above must violate the new invariant. **(h) Does NOT establish** that the §D.2 procedure is wrong — only that its execution leaves no checkable trace in the record.

**Confirmed sound:** invs. 17–22 give precise, enforceable payload→evidence-list links (`proof_artifacts`, `derivation_records`, `witnesses`); invs. 20–22 make the payload-free tags (`HOLDS`, `NO_SOLUTION`, `CONTRADICTION`) auditable without new payloads — the B-05 complaint is substantially addressed.

**Observation:** inv. 9 and inv. 15 say "resolves in the evidence bundle" without naming a list (contrast inv. 17's precise "resolves in `evidence.proof_artifacts`") — and `EvidenceBundle` has no value-artifact list, so a `DERIVED_VALUE`'s `value_ref` has no designated home. This vagueness is what lets my NEW-C3 construction's `Some(h)` "resolve." Propose naming the target list (e.g. `constructed_artifacts` or a new `value_artifacts` list).

## Task 4 — VerificationRecord linkage (D-033): CONFIRMED sufficient

`source_item: String` + `required: Bool` make inv. 14 mechanically evaluable: for each record with `result=FAIL ∧ required=true`, check `verification_summary ∈ {FAIL, CHECKER_DIVERGENCE}`. Example: `[{property:"validator_contract", method:"property-fuzz", checker:"fuzz/1.0", result:FAIL, source_item:"test:property-fuzz", required:true, …}]` with `verification_summary=PASS` violates inv. 14; with `FAIL` satisfies it. The fields are present, typed, and the invariant references exactly them. ✓

**Observations (not defects):** `source_item`/`method` are free Strings — the record can't be validated against the originating spec's verification block, but the record doesn't contain the spec, so that's out of scope. E.6's precedence (`FAIL` dominates regardless of `required`) gives a failed *optional* item the power to fail the summary, while §B.7's "optional-but-unrunnable → recorded as skipped" has no schema representation (no `SKIPPED` status anywhere).

## Task 5 — Assurance rules, duplicates vs conflicts (D-031): CONFIRMED, tested against M8

I ran four concrete cases through M8 (all behaved per §B.7):
- `proof: none` + `proof: kernel-checked …` → `conflicting-verification-requirements` ✓
- `test: none` + `test: differential …` → conflict ✓
- two `proof: kernel-checked` with different checkers → `conflicting` (not duplicate) ✓
- same `proof:` twice with different qualifiers (`required` vs `optional`) → `duplicate-verification-item` ✓ (consistent with the kind+method rule; mildly odd that qualifier difference doesn't make it a conflict, but it follows the stated rule)
- Omitted qualifier → M8 accepts (default `required` applied) ✓ — the default is stated in §B.7 and honored.

The `assurance:` rules (at most one; `none`+active → conflict; two active levels → conflict) are stated normatively; the duplicate/conflict distinction is now genuinely operational, not prose.

## Severity judgment for the lead

- **NEW-C3** (execution/output_packaging underdetermination) is the most serious: conforming records can be mutually contradictory about the same event. Recommend fixing before any gate opens.
- **NEW-C4** (`UNIQUE_UNDER_PROJECTION` evidence-free) is a real B-05/D-022 residual; recommend an invariant.
- **NEW-C1/NEW-C2** (prose-only closure predicates; unclosed internal-error reasons) mean D-029 is only partially formalized — the *lists* look right, but two of three predicates and the fourth domain aren't mechanically closed.
- **NEW-C5** (vague "resolves in the evidence bundle"; no value-artifact list) is minor but interacts with NEW-C3.

**What this audit does not establish:** M8's own correctness (I treated it as a tool, not a verified artifact); anything about L1/L2/L3 claims beyond the contract logic; whether the §B.13 table is implementable. All findings above are from the document text and my own derivations/runs.

**Files:** [MSVE_DESIGN_SPEC_v0.8.md](sandbox://workspace/msve-design/MSVE_DESIGN_SPEC_v0.8.md) · [v08-ex5.msve](sandbox://workspace/msve-design/m8/corpus/v08/v08-ex5.msve)