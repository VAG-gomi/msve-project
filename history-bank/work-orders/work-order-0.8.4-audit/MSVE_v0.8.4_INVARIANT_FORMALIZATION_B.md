# Work Order 0.8.4, Phase B — Reviewer B: Independent Invariant Formalization (DRAFT)

**Source:** `~/workspace/msve-design/work-order-0.8.3-candidate/MSVE_DESIGN_SPEC_v0.8.md`
**Source SHA-256:** `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003` (verified 2026-10-09)
**Source byte size:** 83,036
**Method:** derived solely from the specification text above; no other formalization consulted.

**Notation.** `R` ranges over `ResultRecord`. Field access is `R.field`.
`is-tag(R.f)` is a tag test on a sum-typed field; pattern `Some(C {x = v, …})`
binds payload fields, `…` = remaining fields unconstrained. `→` is material
implication, `↔` biconditional. All variables are explicitly typed at first use
in each invariant. `String`, `Nat`, `Bool` are primitive; `Hash` is the
subtype of `String` of exactly 64 chars in `[0-9a-f]` (spec §E.1).

---

## 1. Typed model

### 1.1 Primitive and abstract operations

- `base_code: String → String` — F-01 normative: prefix of the argument before
  the first occurrence of `": "` (colon + exactly one space); the whole string
  if no `": "` occurs. Total.
- `is_admission_error: String → Bool` — §B.9 closure predicate; defined as a
  disjunction of `(base_code(e) == "<code>")` over the 27 listed codes.
- `is_unsupported_reason: String → Bool` — §B.9; disjunction over 3 codes,
  applied to `base_code(e)`.
- `is_validation_error: String → Bool` — §B.13a/§B.11; disjunction over 12
  codes, applied to `base_code(e)`.
- `is_packaging_error: String → Bool` — §E.1; `(base_code(e) == "output-not-encodable")
  ∨ (base_code(e) == "canonicalization-failure")`.
- `resolves(h: Hash, L: [ArtifactRef]): Bool ≜ ∃a: ArtifactRef. (a ∈ L ∧ a.sha256 = h)`.
  **Interpretation note:** the spec never defines "resolves"; this is the only
  coherent reading given `ArtifactRef.sha256: Hash`. Recorded as AMB-R1 in the
  ambiguity register.

### 1.2 Enumerations

- `AdmissionTag := ACCEPTED | INVALID_INPUT | UNSUPPORTED`
- `ExecutionTag := NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED | INTERNAL_ERROR`
- `PackagingTag := PACKAGING_OK | PACKAGING_FAILED`
- `AssuranceLevel := NONE | LEVEL_A | LEVEL_B`
- `AssuranceBasis := KERNEL_PROOF | INDEPENDENT_RECOMPUTE | SOLVER_BACKED | TEST_BACKED`
- `VerifResult := PASS | FAIL | INCONCLUSIVE`
- `Summary := NOT_RUN | PASS | FAIL | INCONCLUSIVE | CHECKER_DIVERGENCE`
- `ReasonCode := SOLVER_UNKNOWN | PROCEDURE_INCOMPLETE | RESOURCE_EXHAUSTED | EXECUTION_INTERRUPTED | ASSURANCE_REQUIREMENT_UNMET | NO_TEST_CORPUS`
- `SolverOutcome := SAT | UNSAT | UNKNOWN`
- `DiscStatus := OPEN | RESOLVED`

### 1.3 Record types (exact field names)

```
ResultRecord {
  admission:            ACCEPTED | INVALID_INPUT(reason: String) | UNSUPPORTED(reason: String),
  execution:           NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED | INTERNAL_ERROR(reason: String),
  output_packaging:    PACKAGING_OK | PACKAGING_FAILED(reason: String),
  semantic_result:     Option<SemanticResult>,
  solver_observation:   Option<SolverObs>,
  assurance_required:  AssuranceLevel,
  assurance_bases:     [AssuranceBasis],
  assurance_achieved:  AssuranceLevel,
  assurance_shortfall: Bool,
  shortfall_description: Option<String>,
  verification_records:  [VerificationRecord],
  verification_summary:  Summary,
  evidence:            EvidenceBundle,
  partial_results:     [PartialResult],
  discrepancies:       [Discrepancy] }
```
(Type aliases `AdmissionError`, `UnsupportedReason`, `ValidationError`,
`PackagingError` are all `String` refined by their closure predicates.)

```
SemanticResult :=
    DERIVED_VALUE { value_ref: Option<Hash>, derivation_ref: Hash }
  | ARTIFACT_CONSTRUCTED { artifact_ref: Option<Hash> }
  | NO_SOLUTION {}
  | PROVED { proof_artifact: Hash }
  | DISPROVED { refutation_ref: Hash }
  | HOLDS {}
  | VIOLATED { witness_ref: Hash }
  | UNIQUE_UNDER_PROJECTION { projection: String }
  | UNDERDETERMINED { witnesses_ref: Hash }
  | CONTRADICTION {}
  | INCONCLUSIVE { reason: ReasonCode }

SolverObs := { outcome: SolverOutcome, tool: String, version: String,
               config: String, provenance_ref: Hash,
               certificate_ref: Option<Hash> }

VerificationRecord := { property: String, artifact: String,
  spec_version: String, method: String, checker: String,
  result: VerifResult, reason: Option<String>, assurance_boundary: String,
  inputs_ref: Hash, source_item: String, required: Bool }

EvidenceBundle := { derivation_records: [ArtifactRef],
  proof_artifacts: [ArtifactRef], witnesses: [ArtifactRef],
  constructed_artifacts: [ArtifactRef], verification_inputs_ref: Hash,
  external_evidence_records: [ExternalEvidence] }

ArtifactRef := { sha256: Hash, bytes: Nat, media: String, description: String }

PartialResult := { description: String, semantic_fragment: SemanticResult,
  provenance_ref: Hash, labelled_partial: Bool }
```
Note: the schema declares `labelled_partial: true` (constant). Formalized as
the field with the constraint `∀p: PartialResult. p.labelled_partial = true`.

```
Discrepancy := { property: String, involved_records: [Nat],
  description: String, required_follow_up: String, status: DiscStatus }
```
Temporal rule (not a cross-field invariant; recorded for completeness):
`status` may transition `OPEN → RESOLVED` only with a recorded resolution.

### 1.4 Background definitions used by invariants

- Shortfall rule (§E.1):
  `shortfall-rule(R) ≜ (R.assurance_required = LEVEL_A ∧ R.assurance_achieved ≠ LEVEL_A)
   ∨ (R.assurance_required = LEVEL_B ∧ R.assurance_achieved = NONE)`.
- §E.1 also states: `assurance_achieved = LEVEL_A ⇒ KERNEL_PROOF ∈ assurance_bases
  ∨ INDEPENDENT_RECOMPUTE ∈ assurance_bases`;
  `assurance_achieved = LEVEL_B ⇒ assurance_bases` non-empty;
  `assurance_required = NONE ⇒ assurance_shortfall = false`.
  The first two duplicate invariants 6–7; the third is entailed by invariant 5's
  biconditional (neither disjunct can hold when `assurance_required = NONE`).
- §E.6 aggregation precedence (background, not numbered):
  `CHECKER_DIVERGENCE > FAIL > INCONCLUSIVE > PASS`; no records → `NOT_RUN`;
  a PASS/FAIL split on the same property → `CHECKER_DIVERGENCE` with both
  records preserved and a `Discrepancy` with `status = OPEN`.

---

## 2. Invariant-by-invariant formalization

### Invariant 1

**Source text:** "`admission ∈ {INVALID_INPUT, UNSUPPORTED}` ⇒ `execution = NOT_STARTED` ∧ `semantic_result = None` ∧ `verification_summary = NOT_RUN` ∧ `assurance_bases = []` ∧ `assurance_achieved = NONE`."

**Formal:**
```
∀R: ResultRecord.
  (tag(R.admission) ∈ {INVALID_INPUT, UNSUPPORTED})
  → (R.execution = NOT_STARTED
     ∧ R.semantic_result = None
     ∧ R.verification_summary = NOT_RUN
     ∧ R.assurance_bases = []
     ∧ R.assurance_achieved = NONE)
```
`tag(R.admission)` is the constructor tag, ignoring the `reason` payload.

### Invariant 1b (F-06)

**Source text:** "`admission = INVALID_INPUT(reason)` ⇒ `is_admission_error(reason) = true`; `admission = UNSUPPORTED(reason)` ⇒ `is_unsupported_reason(reason) = true` (with `base_code` applied per §B.9, so detailed values such as `"unbound-identifier: foo"` satisfy the predicates). … this invariant is the record-boundary check."

**Formal:**
```
∀R: ResultRecord. ∀reason: String.
  ((R.admission = INVALID_INPUT(reason) → is_admission_error(reason) = true)
   ∧ (R.admission = UNSUPPORTED(reason) → is_unsupported_reason(reason) = true))
```
The parenthetical about `base_code` is explanatory: the predicates' §B.9
definitions already apply `base_code`. No additional constraint is needed beyond
invoking the predicates.

### Invariant 2

**Source text:** "`execution ∈ {NOT_STARTED, RUNNING}` ⇒ `semantic_result = None`."

**Formal:**
```
∀R: ResultRecord.
  (tag(R.execution) ∈ {NOT_STARTED, RUNNING} → R.semantic_result = None)
```

### Invariant 3

**Source text:** "`semantic_result = Some(HOLDS {})` ⇒ the check corpus was non-empty."

**Formal:** AMBIGUITY — see AMB-3. No field of `ResultRecord` (or any type it
references) names "the check corpus". Candidate partial rendering (NOT adopted):
`∀R. (R.semantic_result = Some(HOLDS {}) → ∃v ∈ R.verification_records. true)`
would merely require a record to exist, which invents semantics. The rule as
written cannot be translated without inventing the corpus's identity.

### Invariant 4

**Source text:** "`verification_summary = CHECKER_DIVERGENCE` ⇒ `discrepancies` contains an entry with `status = OPEN`."

**Formal:**
```
∀R: ResultRecord.
  (R.verification_summary = CHECKER_DIVERGENCE
   → ∃d: Discrepancy. (d ∈ R.discrepancies ∧ d.status = OPEN))
```

### Invariant 5

**Source text:** "`assurance_shortfall = true` ⇔ the §E.1 shortfall rule holds; ⇒ `shortfall_description = Some(_)`."

**Formal:**
```
∀R: ResultRecord.
  ((R.assurance_shortfall = true ↔ shortfall-rule(R))
   ∧ (R.assurance_shortfall = true → ∃s: String. R.shortfall_description = Some(s)))
```
with `shortfall-rule` as defined in §1.4. Note: the §E.1 side-statement
`assurance_required = NONE ⇒ assurance_shortfall = false` is entailed by the
biconditional and adds no independent constraint.

### Invariant 6

**Source text:** "`assurance_achieved = LEVEL_A` ⇒ `KERNEL_PROOF ∈ assurance_bases ∨ INDEPENDENT_RECOMPUTE ∈ assurance_bases`."

**Formal:**
```
∀R: ResultRecord.
  (R.assurance_achieved = LEVEL_A
   → (KERNEL_PROOF ∈ R.assurance_bases ∨ INDEPENDENT_RECOMPUTE ∈ R.assurance_bases))
```

### Invariant 7

**Source text:** "`assurance_achieved = LEVEL_B` ⇒ `assurance_bases ≠ []`."

**Formal:**
```
∀R: ResultRecord.
  (R.assurance_achieved = LEVEL_B → R.assurance_bases ≠ [])
```

### Invariant 8

**Source text:** "`semantic_result = Some(VIOLATED {witness_ref})` ⇒ the witness artifact is in `evidence.witnesses`."

**Formal:**
```
∀R: ResultRecord. ∀w: Hash.
  (R.semantic_result = Some(VIOLATED {witness_ref = w})
   → resolves(w, R.evidence.witnesses))
```

### Invariant 9

**Source text:** "`semantic_result = Some(DERIVED_VALUE {value_ref, derivation_ref})` ⇒ `derivation_ref` resolves in `evidence.derivation_records`; `value_ref` per invariant 15. (NEW-C5: the v0.8 draft said "the evidence bundle" without naming a list.)"

**Formal:**
```
∀R: ResultRecord. ∀v: Option<Hash>. ∀d: Hash.
  (R.semantic_result = Some(DERIVED_VALUE {value_ref = v, derivation_ref = d})
   → resolves(d, R.evidence.derivation_records))
```
The "`value_ref` per invariant 15" clause is a cross-reference, not an
independent constraint; `v` is additionally constrained by invariant 15
(formalized below). No double-counting.

### Invariant 10

**Source text:** "`execution = INTERNAL_ERROR(r)` ⇒ the `reason` field `r` is recorded; if the failure occurred at packaging (`base_code(r) = output-not-encodable`), the established `semantic_result` is still recorded (D-019: a valid result with an unserializable output is never INVALID_INPUT)."

**Formal:**
```
∀R: ResultRecord. ∀r: String.
  (R.execution = INTERNAL_ERROR(r)
   → (base_code(r) = "output-not-encodable" → R.semantic_result ≠ None))
```
Notes:
- "the `reason` field `r` is recorded" is vacuous as a constraint: `r` is a
  payload of the record's own `execution` field, hence present by construction.
  It is formalized as `true` (no constraint).
- "the established `semantic_result` is still recorded" is rendered as
  `R.semantic_result ≠ None` (i.e. `Some(_)`), since "recorded" for an
  `Option<SemanticResult>` field means non-`None`.
- The D-019 parenthetical ("never INVALID_INPUT") restates the admission
  typing, already covered by invariant 1b; no new constraint.
- **Gap noted:** the "occurred at packaging" condition is operationalized only
  for `base_code(r) = "output-not-encodable"`. An `INTERNAL_ERROR` with
  `base_code(r) = "canonicalization-failure"` is also a packaging failure per
  §G.2/invariant 15b, but this invariant's consequent does not cover it.
  See AMB-10.

### Invariant 11

**Source text:** "`solver_observation = Some({outcome: UNSAT, …})` ∧ `assurance_required = LEVEL_A` ∧ `assurance_achieved ≠ LEVEL_A` ⇒ `semantic_result = Some(INCONCLUSIVE {ASSURANCE_REQUIREMENT_UNMET})`."

**Formal:**
```
∀R: ResultRecord. ∀o: SolverObs.
  ((R.solver_observation = Some(o) ∧ o.outcome = UNSAT
    ∧ R.assurance_required = LEVEL_A ∧ R.assurance_achieved ≠ LEVEL_A)
   → R.semantic_result = Some(INCONCLUSIVE {reason = ASSURANCE_REQUIREMENT_UNMET}))
```
`…` = remaining `SolverObs` fields unconstrained.

### Invariant 12

**Source text:** "`assurance_achieved = LEVEL_B` ⇒ the frozen spec contains `assurance: level-b accepted`."

**Formal:** AMBIGUITY — see AMB-12. "The frozen spec" is not a field of
`ResultRecord` nor of any referenced type. The consequent cannot be evaluated
against the record model. This is a constraint relating the record to an
external artifact (the frozen specification text), not a cross-field
constraint within the schema.

### Invariant 13

**Source text:** "`partial_results ≠ []` ⇒ `execution ∈ {TIMEOUT, INTERRUPTED}`."

**Formal:**
```
∀R: ResultRecord.
  (R.partial_results ≠ [] → tag(R.execution) ∈ {TIMEOUT, INTERRUPTED})
```
Consistent with the `PartialResult` schema comment ("present only when
execution ∈ {TIMEOUT, INTERRUPTED}").

### Invariant 14

**Source text:** "Every `VerificationRecord` with `result = FAIL` ∧ `required = true` ⇒ `verification_summary ∈ {FAIL, CHECKER_DIVERGENCE}` (D-033: evaluated from the recorded `source_item`/`required` fields)."

**Formal:**
```
∀R: ResultRecord. ∀v: VerificationRecord.
  ((v ∈ R.verification_records ∧ v.result = FAIL ∧ v.required = true)
   → R.verification_summary ∈ {FAIL, CHECKER_DIVERGENCE})
```
`required` here is `VerificationRecord.required: Bool`, correctly scoped by the
quantifier; no confusion with assurance fields. Consistent with §E.6
precedence (a required FAIL forces FAIL or DIVERGENCE, both ≥ FAIL).

### Invariant 15

**Source text:** "(D-030) `output_packaging = PACKAGING_OK` ∧ `semantic_result = Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = Some(h)` ∧ `h` resolves to a canonicalized value artifact in `evidence.constructed_artifacts`. (NEW-C5: named list; the v0.8 draft said "the evidence bundle".) `output_packaging = PACKAGING_FAILED(_)` ∧ `semantic_result = Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = None`. (F-16: the previous wording left `value_ref` unbound outside the `DERIVED_VALUE` alternative.) A NaN or function value therefore yields `PACKAGING_FAILED(output-not-encodable)` with the semantic result preserved — never INVALID_INPUT."

**Formal:**
```
∀R: ResultRecord. ∀v: Option<Hash>. ∀h: Hash.
  ((R.output_packaging = PACKAGING_OK
    ∧ R.semantic_result = Some(DERIVED_VALUE {value_ref = v, …})
    → (v = Some(h) ∧ resolves(h, R.evidence.constructed_artifacts)))
   ∧
   (R.output_packaging = PACKAGING_FAILED(_)
    ∧ R.semantic_result = Some(DERIVED_VALUE {value_ref = v, …})
    → v = None))
```
Notes:
- "resolves to a canonicalized value artifact": `ArtifactRef` carries no
  canonicalized flag; formalized as `resolves` (see AMB-R1). The
  "canonicalized" qualifier has no formal counterpart — see AMB-15.
- The NaN sentence is explanatory (an instance of the second implication),
  not an independent constraint.
- "never INVALID_INPUT" restates admission typing; no new constraint.

### Invariant 15b

**Source text:** "(D-030, NEW-B7) Joint packaging/execution state: `output_packaging = PACKAGING_FAILED(r)` ⇔ `execution = INTERNAL_ERROR(e)` ∧ `base_code(e) = base_code(r)` (F-01: the reason's base code must equal the packaging reason's base code; details may differ). `output_packaging = PACKAGING_OK` ⇒ `execution` is not `INTERNAL_ERROR` with an `output-not-encodable`/`canonicalization-failure` base code."

**Formal:**
```
∀R: ResultRecord. ∀r: String. ∀e: String.
  ((R.output_packaging = PACKAGING_FAILED(r)
    ↔ (R.execution = INTERNAL_ERROR(e) ∧ base_code(e) = base_code(r)))
   ∧
   (R.output_packaging = PACKAGING_OK
    → ¬∃e: String. (R.execution = INTERNAL_ERROR(e)
                    ∧ (base_code(e) = "output-not-encodable"
                       ∨ base_code(e) = "canonicalization-failure"))))
```
Note: the biconditional's left-to-right direction forces every packaging
failure to coincide with an `INTERNAL_ERROR`; right-to-left forces every
`INTERNAL_ERROR` whose reason base-matches the packaging reason to coincide
with `PACKAGING_FAILED`. An `INTERNAL_ERROR` with a *non-packaging* base code
(e.g. `division-by-zero`) is unconstrained by the biconditional — correctly so,
since then no `r` with matching base code exists on the packaging side.

### Invariant 16

**Source text:** "(D-030) `semantic_result = Some(ARTIFACT_CONSTRUCTED {artifact_ref})` ⇒ `artifact_ref = Some(h)` resolves in `evidence.constructed_artifacts`, or `artifact_ref = None` iff `output_packaging = PACKAGING_FAILED(_)`."

**Formal:**
```
∀R: ResultRecord. ∀a: Option<Hash>. ∀h: Hash.
  (R.semantic_result = Some(ARTIFACT_CONSTRUCTED {artifact_ref = a})
   → ((a = Some(h) ∧ resolves(h, R.evidence.constructed_artifacts))
      ∨ (a = None ↔ tag(R.output_packaging) = PACKAGING_FAILED)))
```
The "or" is read inclusively; the second disjunct's biconditional forces
`artifact_ref = None` exactly when packaging failed (for this alternative).
Combined with 15b, a `PACKAGING_FAILED` record with this alternative must
carry `artifact_ref = None`, and a `PACKAGING_OK` record must carry
`Some(h)` resolving in `constructed_artifacts`.

### Invariant 17

**Source text:** "(D-030) `semantic_result = Some(PROVED {proof_artifact})` ⇒ the hash resolves in `evidence.proof_artifacts`."

**Formal:**
```
∀R: ResultRecord. ∀h: Hash.
  (R.semantic_result = Some(PROVED {proof_artifact = h})
   → resolves(h, R.evidence.proof_artifacts))
```

### Invariant 18

**Source text:** "(D-030) `semantic_result = Some(DISPROVED {refutation_ref})` ⇒ the hash resolves in `evidence.derivation_records`."

**Formal:**
```
∀R: ResultRecord. ∀h: Hash.
  (R.semantic_result = Some(DISPROVED {refutation_ref = h})
   → resolves(h, R.evidence.derivation_records))
```

### Invariant 19

**Source text:** "(D-030) `semantic_result = Some(UNDERDETERMINED {witnesses_ref})` ⇒ the hash resolves in `evidence.witnesses`."

**Formal:**
```
∀R: ResultRecord. ∀h: Hash.
  (R.semantic_result = Some(UNDERDETERMINED {witnesses_ref = h})
   → resolves(h, R.evidence.witnesses))
```

### Invariant 20

**Source text:** "(D-030, F-07) `semantic_result = Some(HOLDS {})` ⇒ some `VerificationRecord` has `result = PASS` for the check property with `inputs_ref = evidence.verification_inputs_ref`. (F-07 resolution rule: the bundle exposes exactly one verification-inputs hash, so each record's `inputs_ref` must equal it; there is no separately addressable input collection. Valid: `inputs_ref` equal to the bundle's `verification_inputs_ref`. Invalid: any other hash — the record's inputs cannot be located.)"

**Formal:**
```
∀R: ResultRecord.
  (R.semantic_result = Some(HOLDS {})
   → ∃v: VerificationRecord.
       (v ∈ R.verification_records
        ∧ v.result = PASS
        ∧ v.inputs_ref = R.evidence.verification_inputs_ref))
```
AMBIGUITY — see AMB-20: "for the check property" cannot be formalized.
`ResultRecord` carries no goal or property field identifying *which* check the
`HOLDS` verdict concerns, so the existential cannot be restricted to the
relevant property without inventing one. The formalization above requires a
PASS record with matching `inputs_ref` but does not (and cannot, from the
schema) require it to be *about* the check in question.

### Invariant 21

**Source text:** "(D-030) `semantic_result = Some(NO_SOLUTION {})` ⇒ `solver_observation = Some(_)` ∨ a search record in `evidence.derivation_records`."

**Formal:**
```
∀R: ResultRecord.
  (R.semantic_result = Some(NO_SOLUTION {})
   → ((∃o: SolverObs. R.solver_observation = Some(o))
      ∨ (∃a: ArtifactRef. a ∈ R.evidence.derivation_records)))
```
AMBIGUITY — see AMB-21: "a search record" — `ArtifactRef` has no kind tag
distinguishing search records from other derivation records, so the second
disjunct is formalized as bare existence in the list. Any derivation record
satisfies it as written.

### Invariant 22

**Source text:** "(D-030) `semantic_result = Some(CONTRADICTION {})` ⇒ `solver_observation = Some({outcome: UNSAT, …})` ∨ a proof artifact in `evidence.proof_artifacts`."

**Formal:**
```
∀R: ResultRecord.
  (R.semantic_result = Some(CONTRADICTION {})
   → ((∃o: SolverObs. (R.solver_observation = Some(o) ∧ o.outcome = UNSAT))
      ∨ (∃a: ArtifactRef. a ∈ R.evidence.proof_artifacts)))
```

### Invariant 23

**Source text:** "(D-022, NEW-C4) `semantic_result = Some(UNIQUE_UNDER_PROJECTION {projection})` ⇒ `solver_observation = Some({outcome: UNSAT, …})` recording the completed second-model query under that projection ∨ a derivation record in `evidence.derivation_records` witnessing it. An evidence-free uniqueness claim violates this invariant. (NEW-C4: the v0.8 draft left this alternative without an evidence link.)"

**Formal:**
```
∀R: ResultRecord. ∀p: String.
  (R.semantic_result = Some(UNIQUE_UNDER_PROJECTION {projection = p})
   → ((∃o: SolverObs. R.solver_observation = Some(o) ∧ o.outcome = UNSAT)
      ∨ (∃a: ArtifactRef. a ∈ R.evidence.derivation_records)))
```
AMBIGUITY — see AMB-23: "recording the completed second-model query **under
that projection**" / "witnessing **it**" — neither `SolverObs` nor
`ArtifactRef` has fields capturing *which* projection a second-model query was
run under, nor any marker of "second-model query". The `UNSAT` outcome is
formalizable; the linkage to projection `p` is not. As formalized, any UNSAT
observation (or any derivation record) satisfies the invariant regardless of
projection. The final sentence ("an evidence-free uniqueness claim violates
this invariant") is entailed by the formalization and adds no constraint.

---

## 3. Ambiguity register

**AMB-R1 — "resolves in" undefined.** The spec uses "resolves in <list>"
throughout invariants 8, 9, 15–19 but never defines it. Formalized as
`∃a ∈ L. a.sha256 = h`. This is the only coherent reading, but a Z3 encoding
adopts it as an *interpretation*, not a quoted rule. If "resolves" were meant
to include e.g. content-integrity checks beyond hash presence, the
formalization would be weaker than intended.

**AMB-3 — Invariant 3 ("the check corpus was non-empty").** No corpus is named
by any field of `ResultRecord` or its referenced types. The rule cannot be
translated without inventing the corpus's identity. Any formalization would be
fabrication. **Status: unformalizable as written.**

**AMB-10 — Invariant 10 packaging condition is narrower than §G.2/15b.**
The "occurred at packaging" test is given only as
`base_code(r) = "output-not-encodable"`. A packaging failure with
`base_code(r) = "canonicalization-failure"` (also a packaging base code per
§E.1/§G.2) does not trigger this invariant's consequent. Either the
consequent was meant to cover both packaging base codes, or
canonicalization-failure packaging errors are exempt from the
"semantic_result still recorded" requirement — the text does not say.
Additionally, "the `reason` field `r` is recorded" is vacuous (r is a payload
of the record itself).

**AMB-12 — Invariant 12 references the frozen spec's text.** "The frozen spec
contains `assurance: level-b accepted`" is a constraint on an external
artifact, not on any record field. It cannot be evaluated within the record
model. **Status: unformalizable within the schema;** it belongs to a
cross-artifact check, not a cross-field invariant.

**AMB-15 — "canonicalized value artifact" (invariant 15).** `ArtifactRef` has
fields `sha256`, `bytes`, `media`, `description` — no canonicalization flag.
The qualifier cannot be checked formally; `resolves` is the formalizable
content.

**AMB-20 — Invariant 20 "for the check property".** `ResultRecord` has no goal
or property field, so the required PASS `VerificationRecord` cannot be tied to
the property the `HOLDS` verdict concerns. A record with `HOLDS {}` and a PASS
record about an unrelated property satisfies the formalization.

**AMB-21 — Invariant 21 "search record".** `ArtifactRef` has no kind
discriminator; any derivation record satisfies the second disjunct as written.

**AMB-23 — Invariant 23 projection linkage.** Neither disjunct can express
"the second-model query was run *under projection p*". The variable `p` is
bound by the pattern but does not occur in the consequent's formalizable
content — a vacuous binding, which is itself a formalization smell indicating
the natural-language rule demands more than the schema provides.

### Variable-binding notes (all invariants)

- Every pattern-bound variable (`r`, `e`, `h`, `w`, `v`, `d`, `a`, `o`, `p`)
  occurs in its invariant's consequent, **except** `p` in invariant 23 (see
  AMB-23).
- `required` in invariant 14 is `VerificationRecord.required: Bool`, correctly
  scoped by its quantifier — no clash with assurance fields.
- The `…` in `Some({outcome: UNSAT, …})` (invariants 11, 22, 23) leaves
  remaining `SolverObs` fields unconstrained; this is a deliberate
  formalization of the source's own ellipsis.
- Invariant 5's `Some(_)` is an existential over `String`; formalized as such.
- Invariant 16's inclusive "or" with the inner biconditional is the strongest
  coherent reading; an exclusive-or reading would additionally forbid the
  (impossible-in-practice) overlap and is not adopted.

### Suggested Z3 encoding notes (for Phase D; not part of the formalization)

- Model `ResultRecord` fields as algebraic datatypes; `String`/`Hash` as Z3
  `String` with a `base_code` uninterpreted function constrained by the F-01
  examples, or define `base_code` via `str.indexof`/`str.substr`.
- `is_admission_error` etc.: uninterpreted Boolean functions, or explicit
  disjunctions over the listed codes applied to `base_code(e)`.
- `resolves(h, L)`: membership of `h` in the list of `sha256` projections.
- Invariants 3 and 12 must be **excluded** from the encoded constraint set
  (unformalizable); 20, 21, 23 encoded in their weakened forms with the
  weakening explicitly logged as a soundness caveat.
- A SAT result then establishes: the *formalized fragment* is jointly
  satisfiable — not that the specification as written is satisfiable, since
  the unformalizable and weakened rules are outside the solver's view.
