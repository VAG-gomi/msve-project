# Reviewer A — Independent Invariant Formalization (Work Order 0.8.4, Phase B)

**Source:** `~/workspace/msve-design/work-order-0.8.3-candidate/MSVE_DESIGN_SPEC_v0.8.md`
**Source SHA-256:** `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003` (verified before reading)
**Date:** 2026-10-09
**Method:** derived solely from the candidate text above; no other formalization consulted.

Notation: constraints are over a single `ResultRecord` value `r` unless a quantifier says otherwise. `Resolves(h, L)` is defined once in §0 and reused.

---

## 0. Typed model

### 0.1 Primitive and alias types

- `String`, `Bool`, `Nat` — as in §B.
- `Hash := String` constrained to exactly 64 characters in `[0-9a-f]` (SHA-256, lowercase hex).
- `SemVer`, `CheckerID` — opaque (string-like identifiers; no constraints stated).
- `Option<T> := None | Some(v: T)`.
- `AdmissionError := String` (closed by `is_admission_error`, §B.9: 27 base codes).
- `UnsupportedReason := String` (closed by `is_unsupported_reason`, §B.9: 3 base codes).
- `ValidationError := String` (closed by `is_validation_error`, §B.13a: 12 base codes).
- `PackagingError := String` (closed by `is_packaging_error`: base codes `output-not-encodable`, `canonicalization-failure`).

### 0.2 String operations used by the invariants

- `base_code: String → String` (§B.9, F-01): `base_code(e)` is the prefix of `e` before the first occurrence of `": "` (colon + exactly one space); if `e` contains no `": "`, `base_code(e) = e`. Total on `String`.
- Closure predicates (each tests `base_code(e)`, never `e` directly):
  - `is_admission_error(e) = ⋁_{c ∈ C_adm} (base_code(e) = c)`, `|C_adm| = 27`.
  - `is_unsupported_reason(e) = ⋁_{c ∈ C_uns} (base_code(e) = c)`, `|C_uns| = 3`.
  - `is_validation_error(e) = ⋁_{c ∈ C_val} (base_code(e) = c)`, `|C_val| = 12`.
  - `is_packaging_error(e) = (base_code(e) = "output-not-encodable") ∨ (base_code(e) = "canonicalization-failure")`.

### 0.3 Record model

```
Admission      := ACCEPTED
               | INVALID_INPUT(reason: AdmissionError)
               | UNSUPPORTED(reason: UnsupportedReason)

Execution      := NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED
               | INTERNAL_ERROR(reason: String)

Packaging      := PACKAGING_OK | PACKAGING_FAILED(reason: PackagingError)

SemanticResult := DERIVED_VALUE { value_ref: Option<Hash>, derivation_ref: Hash }
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

ReasonCode     := SOLVER_UNKNOWN | PROCEDURE_INCOMPLETE | RESOURCE_EXHAUSTED
               | EXECUTION_INTERRUPTED | ASSURANCE_REQUIREMENT_UNMET | NO_TEST_CORPUS

SolverObs      := { outcome: SAT | UNSAT | UNKNOWN, tool: String,
                    version: SemVer, config: String, provenance_ref: Hash,
                    certificate_ref: Option<Hash> }

AssuranceBasis := KERNEL_PROOF | INDEPENDENT_RECOMPUTE | SOLVER_BACKED | TEST_BACKED

VerificationRecord := { property: String, artifact: String,
  spec_version: SemVer, method: String, checker: CheckerID,
  result: PASS | FAIL | INCONCLUSIVE, reason: Option<String>,
  assurance_boundary: String, inputs_ref: Hash,
  source_item: String, required: Bool }

ArtifactRef    := { sha256: Hash, bytes: Nat, media: String, description: String }

ExternalEvidence := { experiment_id: String, method: String,
  data_ref: Hash, recorded_at: String }

EvidenceBundle := { derivation_records: [ArtifactRef],
  proof_artifacts: [ArtifactRef], witnesses: [ArtifactRef],
  constructed_artifacts: [ArtifactRef], verification_inputs_ref: Hash,
  external_evidence_records: [ExternalEvidence] }

PartialResult  := { description: String, semantic_fragment: SemanticResult,
  provenance_ref: Hash, labelled_partial: true }

Discrepancy    := { property: String, involved_records: [Nat],
  description: String, required_follow_up: String,
  status: OPEN | RESOLVED }

ResultRecord   := {
  admission: Admission,
  execution: Execution,
  output_packaging: Packaging,
  semantic_result: Option<SemanticResult>,
  solver_observation: Option<SolverObs>,
  assurance_required: NONE | LEVEL_A | LEVEL_B,
  assurance_bases: [AssuranceBasis],
  assurance_achieved: NONE | LEVEL_A | LEVEL_B,
  assurance_shortfall: Bool,
  shortfall_description: Option<String>,
  verification_records: [VerificationRecord],
  verification_summary: NOT_RUN | PASS | FAIL | INCONCLUSIVE | CHECKER_DIVERGENCE,
  evidence: EvidenceBundle,
  partial_results: [PartialResult],
  discrepancies: [Discrepancy] }
```

### 0.4 Defined predicates

- `Resolves(h: Hash, L: [ArtifactRef]) := ∃ a ∈ L. a.sha256 = h`.
  ("resolves in <list>" / "the hash resolves in <list>" / "the witness artifact is in <list>".)
- `ShortfallRule(r) := (r.assurance_required = LEVEL_A ∧ r.assurance_achieved ≠ LEVEL_A) ∨ (r.assurance_required = LEVEL_B ∧ r.assurance_achieved = NONE)`.
- `PackBase := {output-not-encodable, canonicalization-failure}` (the `is_packaging_error` base codes).

### 0.5 Auxiliary constraints from §E.1 / §E.6 (not E.7-numbered, needed for a joint model)

- (S0) `r.assurance_shortfall = true ⇔ ShortfallRule(r)`.
- (S1) `r.assurance_required = NONE ⇒ r.assurance_shortfall = false`.
- (S2) `∀ vr ∈ r.verification_records.` field types as in §0.3 (no cross-field content).
- (E6) Verification aggregation (§E.6): summary precedence CHECKER_DIVERGENCE > FAIL > INCONCLUSIVE > PASS; `r.verification_records = [] ⇒ r.verification_summary = NOT_RUN`. (The full precedence function is stated as a rule, not as E.7 invariants; I do not formalize the argmax computation beyond the empty case, which is explicit.)

---

## 1. Invariant-by-invariant formalization

### Invariant 1

**Source text:** "`admission ∈ {INVALID_INPUT, UNSUPPORTED}` ⇒ `execution = NOT_STARTED` ∧ `semantic_result = None` ∧ `verification_summary = NOT_RUN` ∧ `assurance_bases = []` ∧ `assurance_achieved = NONE`."

**Formal:**
```
∀ r: ResultRecord.
  (r.admission = INVALID_INPUT(_) ∨ r.admission = UNSUPPORTED(_))
  ⟹ (r.execution = NOT_STARTED
     ∧ r.semantic_result = None
     ∧ r.verification_summary = NOT_RUN
     ∧ r.assurance_bases = []
     ∧ r.assurance_achieved = NONE)
```
Note: `INVALID_INPUT(_)` / `UNSUPPORTED(_)` match any `reason` payload. `assurance_required`, `assurance_shortfall`, `shortfall_description`, `output_packaging`, `solver_observation`, `evidence`, `partial_results`, `discrepancies` are unconstrained by this invariant.

### Invariant 1b

**Source text:** "`admission = INVALID_INPUT(reason)` ⇒ `is_admission_error(reason) = true`; `admission = UNSUPPORTED(reason)` ⇒ `is_unsupported_reason(reason) = true` (with `base_code` applied per §B.9, so detailed values such as `"unbound-identifier: foo"` satisfy the predicates)."

**Formal:**
```
∀ r: ResultRecord. ∀ s: String.
  ((r.admission = INVALID_INPUT(s) ⟹ is_admission_error(s) = true)
   ∧ (r.admission = UNSUPPORTED(s) ⟹ is_unsupported_reason(s) = true))
```
where `is_admission_error`, `is_unsupported_reason` are the §B.9 disjunctions over `base_code` (§0.2). The prose about M8 not evaluating the predicates is a meta-claim about evidence, not a constraint; it does not affect the formalization.

### Invariant 2

**Source text:** "`execution ∈ {NOT_STARTED, RUNNING}` ⇒ `semantic_result = None`."

**Formal:**
```
∀ r: ResultRecord.
  (r.execution = NOT_STARTED ∨ r.execution = RUNNING)
  ⟹ r.semantic_result = None
```

### Invariant 3

**Source text:** "`semantic_result = Some(HOLDS {})` ⇒ the check corpus was non-empty."

**Formal:** AMBIGUITY — see A-01 in the ambiguity register. "The check corpus" is not a field of `ResultRecord` or of any type in §0.3. Candidate partial formalization with an external parameter:
```
∀ r: ResultRecord. ∀ C: CheckCorpus.
  (r.semantic_result = Some(HOLDS {}) ∧ CorpusUsed(r, C)) ⟹ C ≠ ∅
```
but neither `CheckCorpus` nor `CorpusUsed` is defined anywhere in the candidate. No record-only constraint can be written without inventing them.

### Invariant 4

**Source text:** "`verification_summary = CHECKER_DIVERGENCE` ⇒ `discrepancies` contains an entry with `status = OPEN`."

**Formal:**
```
∀ r: ResultRecord.
  r.verification_summary = CHECKER_DIVERGENCE
  ⟹ ∃ d ∈ r.discrepancies. d.status = OPEN
```

### Invariant 5

**Source text:** "`assurance_shortfall = true` ⇔ the §E.1 shortfall rule holds; ⇒ `shortfall_description = Some(_)`."

**Formal:**
```
∀ r: ResultRecord.
  ((r.assurance_shortfall = true ⟺ ShortfallRule(r))
   ∧ (r.assurance_shortfall = true ⟹ ∃ s: String. r.shortfall_description = Some(s)))
```
Note: when `assurance_shortfall = false`, `shortfall_description` is unconstrained (may be `Some` or `None`). Combined with (S0)/(S1), `assurance_required = NONE` forces `assurance_shortfall = false`.

### Invariant 6

**Source text:** "`assurance_achieved = LEVEL_A` ⇒ `KERNEL_PROOF ∈ assurance_bases ∨ INDEPENDENT_RECOMPUTE ∈ assurance_bases`."

**Formal:**
```
∀ r: ResultRecord.
  r.assurance_achieved = LEVEL_A
  ⟹ (KERNEL_PROOF ∈ r.assurance_bases ∨ INDEPENDENT_RECOMPUTE ∈ r.assurance_bases)
```
(Identical to the §E.1 sentence; no conflict.)

### Invariant 7

**Source text:** "`assurance_achieved = LEVEL_B` ⇒ `assurance_bases ≠ []`."

**Formal:**
```
∀ r: ResultRecord.
  r.assurance_achieved = LEVEL_B ⟹ r.assurance_bases ≠ []
```

### Invariant 8

**Source text:** "`semantic_result = Some(VIOLATED {witness_ref})` ⇒ the witness artifact is in `evidence.witnesses`."

**Formal:**
```
∀ r: ResultRecord. ∀ w: Hash.
  r.semantic_result = Some(VIOLATED { witness_ref = w })
  ⟹ Resolves(w, r.evidence.witnesses)
```

### Invariant 9

**Source text:** "`semantic_result = Some(DERIVED_VALUE {value_ref, derivation_ref})` ⇒ `derivation_ref` resolves in `evidence.derivation_records`; `value_ref` per invariant 15."

**Formal:**
```
∀ r: ResultRecord. ∀ v: Option<Hash>. ∀ d: Hash.
  r.semantic_result = Some(DERIVED_VALUE { value_ref = v, derivation_ref = d })
  ⟹ Resolves(d, r.evidence.derivation_records)
```
(`value_ref` is deferred to invariant 15 exactly as the source states; no additional constraint here.)

### Invariant 10

**Source text:** "`execution = INTERNAL_ERROR(r)` ⇒ the `reason` field `r` is recorded; if the failure occurred at packaging (`base_code(r) = output-not-encodable`), the established `semantic_result` is still recorded (D-019: a valid result with an unserializable output is never INVALID_INPUT)."

**Formal:**
```
∀ r: ResultRecord. ∀ s: String.
  r.execution = INTERNAL_ERROR(s)
  ⟹ ((base_code(s) = "output-not-encodable" ⟹ r.semantic_result ≠ None)
      ∧ r.admission ≠ INVALID_INPUT(_))
```
Notes:
- "the `reason` field `r` is recorded" is vacuous as a constraint (the reason is carried by the `INTERNAL_ERROR` constructor itself); the substantive content is the two conjuncts above.
- "the established `semantic_result` is still recorded" is rendered as `semantic_result ≠ None` — the minimal faithful reading; the source does not say *which* result, only that one is present rather than the record collapsing to `INVALID_INPUT`. See A-02.
- The D-019 parenthetical ("never INVALID_INPUT") is rendered as `r.admission ≠ INVALID_INPUT(_)`; note this also follows from invariant 1's contrapositive given `execution = INTERNAL_ERROR ≠ NOT_STARTED`, so it is redundant but harmless.

### Invariant 11

**Source text:** "`solver_observation = Some({outcome: UNSAT, …})` ∧ `assurance_required = LEVEL_A` ∧ `assurance_achieved ≠ LEVEL_A` ⇒ `semantic_result = Some(INCONCLUSIVE {ASSURANCE_REQUIREMENT_UNMET})`."

**Formal:**
```
∀ r: ResultRecord. ∀ o: SolverObs.
  (r.solver_observation = Some(o) ∧ o.outcome = UNSAT
   ∧ r.assurance_required = LEVEL_A ∧ r.assurance_achieved ≠ LEVEL_A)
  ⟹ r.semantic_result = Some(INCONCLUSIVE { reason = ASSURANCE_REQUIREMENT_UNMET })
```
(`{outcome: UNSAT, …}` is a record pattern matching on the `outcome` field; remaining fields unconstrained.)

### Invariant 12

**Source text:** "`assurance_achieved = LEVEL_B` ⇒ the frozen spec contains `assurance: level-b accepted`."

**Formal:** AMBIGUITY — see A-03. "The frozen spec" is an external document, not a field of the record. Candidate with external parameter:
```
∀ r: ResultRecord. ∀ F: FrozenSpec.
  (r.assurance_achieved = LEVEL_B ∧ FrozenSpecOf(r, F))
  ⟹ Contains(F, "assurance: level-b accepted")
```
Neither `FrozenSpec`, `FrozenSpecOf`, nor `Contains` is defined in the candidate. No record-only constraint is expressible.

### Invariant 13

**Source text:** "`partial_results ≠ []` ⇒ `execution ∈ {TIMEOUT, INTERRUPTED}`."

**Formal:**
```
∀ r: ResultRecord.
  r.partial_results ≠ [] ⟹ (r.execution = TIMEOUT ∨ r.execution = INTERRUPTED)
```
(Converse not stated: `TIMEOUT`/`INTERRUPTED` with empty `partial_results` is permitted by this invariant. The `PartialResult` schema comment says "present only when execution ∈ {TIMEOUT, INTERRUPTED}", which is exactly this direction.)

### Invariant 14

**Source text:** "Every `VerificationRecord` with `result = FAIL` ∧ `required = true` ⇒ `verification_summary ∈ {FAIL, CHECKER_DIVERGENCE}` (D-033: evaluated from the recorded `source_item`/`required` fields)."

**Formal:**
```
∀ r: ResultRecord.
  (∃ vr ∈ r.verification_records. (vr.result = FAIL ∧ vr.required = true))
  ⟹ (r.verification_summary = FAIL ∨ r.verification_summary = CHECKER_DIVERGENCE)
```
(`required` here is `VerificationRecord.required: Bool`, explicitly scoped by the quantifier; no clash with assurance fields.)

### Invariant 15

**Source text:** "`output_packaging = PACKAGING_OK` ∧ `semantic_result = Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = Some(h)` ∧ `h` resolves to a canonicalized value artifact in `evidence.constructed_artifacts`. … `output_packaging = PACKAGING_FAILED(_)` ∧ `semantic_result = Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = None`."

**Formal:**
```
∀ r: ResultRecord. ∀ v: Option<Hash>. ∀ d: Hash.
  r.semantic_result = Some(DERIVED_VALUE { value_ref = v, derivation_ref = d })
  ⟹ ( (r.output_packaging = PACKAGING_OK
       ⟹ ∃ h: Hash. (v = Some(h) ∧ Resolves(h, r.evidence.constructed_artifacts)))
      ∧ (r.output_packaging = PACKAGING_FAILED(_)
         ⟹ v = None) )
```
Notes:
- The trailing prose ("A NaN or function value therefore yields … never INVALID_INPUT") is explanatory; the `never INVALID_INPUT` part is already covered by invariant 10 / invariant 1.
- "resolves to a canonicalized value artifact" — "canonicalized" adds no checkable condition beyond `Resolves` (there is no `is_canonicalized` field on `ArtifactRef`); rendered as `Resolves`. See A-04.
- No constraint is stated for `DERIVED_VALUE` when `output_packaging` is neither `PACKAGING_OK` nor `PACKAGING_FAILED`, but the `Packaging` type is exhaustive over exactly those two constructors, so the case split is complete.

### Invariant 15b

**Source text:** "`output_packaging = PACKAGING_FAILED(r)` ⇔ `execution = INTERNAL_ERROR(e)` ∧ `base_code(e) = base_code(r)` (F-01: the reason's base code must equal the packaging reason's base code; details may differ). `output_packaging = PACKAGING_OK` ⇒ `execution` is not `INTERNAL_ERROR` with an `output-not-encodable`/`canonicalization-failure` base code."

**Formal:**
```
∀ r: ResultRecord. ∀ p: PackagingError.
  r.output_packaging = PACKAGING_FAILED(p)
  ⟹ ∃ e: String. (r.execution = INTERNAL_ERROR(e)
                   ∧ base_code(e) = base_code(p))
```
plus
```
∀ r: ResultRecord.
  r.output_packaging = PACKAGING_OK
  ⟹ ¬∃ e: String. (r.execution = INTERNAL_ERROR(e)
                    ∧ base_code(e) ∈ PackBase)
```
**The ⟸ direction of the stated biconditional is AMBIGUOUS — see A-05.** As written, "`PACKAGING_FAILED(r)` ⇔ `execution = INTERNAL_ERROR(e)` ∧ …" leaves `r` unbound on the ⟸ side and, read literally over all `INTERNAL_ERROR`s, contradicts NEW-C2's open reason domain (`inexact-division`, `division-by-zero` are specified `INTERNAL_ERROR` reasons that must not force `PACKAGING_FAILED`). The coherent restricted reading is:
```
∀ r: ResultRecord. ∀ e: String.
  (r.execution = INTERNAL_ERROR(e) ∧ base_code(e) ∈ PackBase)
  ⟹ ∃ p: PackagingError. (r.output_packaging = PACKAGING_FAILED(p)
                           ∧ base_code(p) = base_code(e))
```
I adopt the ⟹ direction exactly as stated, the second paragraph exactly as stated, and record the ⟸ direction as ambiguous between the literal (inconsistent with NEW-C2) and restricted (consistent) readings.

### Invariant 16

**Source text:** "`semantic_result = Some(ARTIFACT_CONSTRUCTED {artifact_ref})` ⇒ `artifact_ref = Some(h)` resolves in `evidence.constructed_artifacts`, or `artifact_ref = None` iff `output_packaging = PACKAGING_FAILED(_)`."

**Formal:**
```
∀ r: ResultRecord. ∀ a: Option<Hash>.
  r.semantic_result = Some(ARTIFACT_CONSTRUCTED { artifact_ref = a })
  ⟹ ( (a = Some(h) ⟹ Resolves(h, r.evidence.constructed_artifacts))
      ∧ (a = None ⟺ r.output_packaging = PACKAGING_FAILED(_)) )
```
Note: the `⟺` makes `PACKAGING_FAILED ⟹ artifact_ref = None` and `PACKAGING_OK ⟹ artifact_ref = Some(h)` (with `h` resolving) jointly. The first disjunct's "`artifact_ref = Some(h)` resolves" is read as the conditional shown (it cannot be an unconditional assertion since the `None` case is explicitly allowed).

### Invariant 17

**Source text:** "`semantic_result = Some(PROVED {proof_artifact})` ⇒ the hash resolves in `evidence.proof_artifacts`."

**Formal:**
```
∀ r: ResultRecord. ∀ h: Hash.
  r.semantic_result = Some(PROVED { proof_artifact = h })
  ⟹ Resolves(h, r.evidence.proof_artifacts)
```

### Invariant 18

**Source text:** "`semantic_result = Some(DISPROVED {refutation_ref})` ⇒ the hash resolves in `evidence.derivation_records`."

**Formal:**
```
∀ r: ResultRecord. ∀ h: Hash.
  r.semantic_result = Some(DISPROVED { refutation_ref = h })
  ⟹ Resolves(h, r.evidence.derivation_records)
```

### Invariant 19

**Source text:** "`semantic_result = Some(UNDERDETERMINED {witnesses_ref})` ⇒ the hash resolves in `evidence.witnesses`."

**Formal:**
```
∀ r: ResultRecord. ∀ h: Hash.
  r.semantic_result = Some(UNDERDETERMINED { witnesses_ref = h })
  ⟹ Resolves(h, r.evidence.witnesses)
```

### Invariant 20

**Source text:** "`semantic_result = Some(HOLDS {})` ⇒ some `VerificationRecord` has `result = PASS` for the check property with `inputs_ref = evidence.verification_inputs_ref`."

**Formal:**
```
∀ r: ResultRecord.
  r.semantic_result = Some(HOLDS {})
  ⟹ ∃ vr ∈ r.verification_records.
        (vr.result = PASS ∧ vr.inputs_ref = r.evidence.verification_inputs_ref)
```
AMBIGUITY — see A-06: "for the check property" is not rendered. There is no field identifying *which* property is "the check property" of a `check` goal; `VerificationRecord.property: String` exists but the source does not say the PASS record's `property` must equal any particular value. The existential above is the maximal faithful rendering; strengthening it (e.g. requiring a specific `property` value) would invent semantics.

### Invariant 21

**Source text:** "`semantic_result = Some(NO_SOLUTION {})` ⇒ `solver_observation = Some(_)` ∨ a search record in `evidence.derivation_records`."

**Formal:**
```
∀ r: ResultRecord.
  r.semantic_result = Some(NO_SOLUTION {})
  ⟹ ( (∃ o: SolverObs. r.solver_observation = Some(o))
      ∨ (∃ a ∈ r.evidence.derivation_records. IsSearchRecord(a)) )
```
AMBIGUITY — see A-07: `IsSearchRecord` is not defined. `ArtifactRef` has no kind/tag field distinguishing search records from other derivation records, so the second disjunct cannot be evaluated without inventing a discriminator.

### Invariant 22

**Source text:** "`semantic_result = Some(CONTRADICTION {})` ⇒ `solver_observation = Some({outcome: UNSAT, …})` ∨ a proof artifact in `evidence.proof_artifacts`."

**Formal:**
```
∀ r: ResultRecord.
  r.semantic_result = Some(CONTRADICTION {})
  ⟹ ( (∃ o: SolverObs. (r.solver_observation = Some(o) ∧ o.outcome = UNSAT))
      ∨ (∃ a ∈ r.evidence.proof_artifacts. true) )
```
The second disjunct ("a proof artifact in `evidence.proof_artifacts`") is rendered as non-emptiness of the list; any member qualifies since no further condition is stated.

### Invariant 23

**Source text:** "`semantic_result = Some(UNIQUE_UNDER_PROJECTION {projection})` ⇒ `solver_observation = Some({outcome: UNSAT, …})` recording the completed second-model query under that projection ∨ a derivation record in `evidence.derivation_records` witnessing it. An evidence-free uniqueness claim violates this invariant."

**Formal:**
```
∀ r: ResultRecord. ∀ p: String.
  r.semantic_result = Some(UNIQUE_UNDER_PROJECTION { projection = p })
  ⟹ ( (∃ o: SolverObs. (r.solver_observation = Some(o) ∧ o.outcome = UNSAT))
      ∨ (∃ a ∈ r.evidence.derivation_records. WitnessesSecondModelQuery(a, p)) )
```
AMBIGUITY — see A-08: neither "recording the completed second-model query under that projection" (first disjunct — the `SolverObs` has no projection or query-completeness field) nor "witnessing it" (second disjunct — `ArtifactRef` carries no such relation) is checkable from the schema. The "evidence-free uniqueness claim violates" sentence confirms the intent (at least one disjunct must hold with genuine content), but the schema provides no field on which to test genuineness. Maximal faithful rendering keeps the disjunction over bare existence; anything stronger invents semantics.

---

## Ambiguity register

**A-01 (Invariant 3).** "The check corpus was non-empty" refers to an object outside the record. No `CheckCorpus` type, no field linking a record to the corpus used. Not formalizable as a record constraint without inventing both.

**A-02 (Invariant 10).** "The established `semantic_result` is still recorded" rendered as `semantic_result ≠ None`. The source does not define which result counts as "established"; the minimal reading is presence. A stronger reading (equality with the pre-packaging result) would require a temporal model the spec does not provide.

**A-03 (Invariant 12).** "The frozen spec contains `assurance: level-b accepted`" references an external document. No `FrozenSpec` parameter or `Contains` predicate is defined. Not formalizable at the record level.

**A-04 (Invariant 15).** "Resolves to a canonicalized value artifact" — "canonicalized" has no corresponding field or predicate on `ArtifactRef`; rendered as bare `Resolves`. If canonicalization of the artifact bytes is intended as an additional check, the spec does not state how a checker would perform it from the record.

**A-05 (Invariant 15b, ⟸ direction).** The biconditional as written is ill-formed on the ⟸ side (`r` unbound) and, read literally, contradicts NEW-C2: specified non-packaging `INTERNAL_ERROR` reasons (`inexact-division`, `division-by-zero`) would force `PACKAGING_FAILED`. Two readings: (i) literal — inconsistent with NEW-C2, likely not intended; (ii) restricted to packaging base codes — consistent with the second paragraph of 15b and with NEW-C2. Owner decision required on which reading is normative. I formalize the ⟹ direction and the second paragraph exactly, and the restricted ⟸ as the coherent candidate.

**A-06 (Invariant 20).** "For the check property" is unrendered: no field identifies the property whose PASS is required. The existential over any PASS record is the maximal faithful constraint.

**A-07 (Invariant 21).** "A search record" has no discriminator in `ArtifactRef`. The disjunct is not evaluable without inventing one.

**A-08 (Invariant 23).** Neither disjunct's qualifier ("recording the completed second-model query under that projection", "witnessing it") corresponds to any schema field. The invariant as written mandates non-emptiness of the cited evidence locations, but cannot test that the evidence is *about* the projection.

## Variable-binding notes

- All pattern variables (`value_ref`, `derivation_ref`, `witness_ref`, `proof_artifact`, `refutation_ref`, `witnesses_ref`, `artifact_ref`, `projection`, `reason`/`r`/`e`/`s`/`p`/`h`/`d`/`v`/`a`/`o`/`vr`) are bound by an explicit pattern match or quantifier in each formalization above.
- Invariant 14's `required` is `VerificationRecord.required: Bool`, scoped by the record quantifier — no clash with assurance fields.
- Invariant 15's `value_ref` is bound only inside the `DERIVED_VALUE` pattern (per the F-16 correction); the formalization above respects that scope.
- `PackBase` is derived from the `is_packaging_error` definition (F-01), not invented.

## What this formalization does and does not establish

- Establishes: a precise, per-invariant logical reading of §E.7 with explicit types, scopes, and eight marked ambiguities.
- Does not establish: that this reading matches any other reviewer's reading (that comparison is Phase B's next step); that the formalization is a complete model of the prose (A-01, A-03, A-07, A-08 mark where the prose outruns the schema); or anything about the specification's satisfiability (Phase D's task).
