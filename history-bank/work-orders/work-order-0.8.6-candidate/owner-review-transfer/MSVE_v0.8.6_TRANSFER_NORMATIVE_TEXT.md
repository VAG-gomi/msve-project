# MSVE v0.8.6 Transfer — Report A: Exact Normative Excerpts

**Source:** `~/workspace/msve-design/work-order-0.8.6-candidate/MSVE_DESIGN_SPEC_v0.8.md`
**Purpose:** verbatim transcription for owner review of F-20/F-21.
All excerpts below are copied exactly; line numbers refer to the source file.
No typos or ambiguities were repaired. (One noted below.)

---

## A1. §E.6a Assurance-evidence linkage definitions (F-21) — lines 1232–1267

### E.6a Assurance-evidence linkage definitions (F-21)

An assurance basis recorded in `assurance_bases` is a claim, not evidence.
The following definitions make that claim auditable. They constrain the
existing `VerificationRecord` fields; no new field is introduced.

- **Proof basis (`source_item = "proof"`).** A verification record with
  `source_item = "proof"` and `result = PASS` substantiates a
  `KERNEL_PROOF` basis only if its `artifact` field contains exactly the
  64-character lowercase hexadecimal sha256 of the proof artifact, and
  that hash resolves in `evidence.proof_artifacts`
  (`∃ a ∈ evidence.proof_artifacts: a.sha256 = vr.artifact`).
- **Recomputation basis (`source_item = "recompute"`).** A verification
  record with `source_item = "recompute"` and `result = PASS`
  substantiates an `INDEPENDENT_RECOMPUTE` basis only if:
  (i) `vr.checker` identifies the checker that performed the independent
  recomputation (normative: this checker must be independent of the
  primary derivation producer; independence is attested by the producer
  and recorded via the checker ID for audit — it is not mechanically
  derivable from the record, which carries no primary-producer field);
  (ii) `vr.artifact` contains exactly the 64-character hash identifying
  the primary result compared — for `DERIVED_VALUE{value_ref = Some(h),
  …}` the value hash `h`, else the `derivation_ref` hash;
  (iii) `vr.inputs_ref` is the hash of the inputs the recomputation ran
  on (equal to `evidence.verification_inputs_ref` per F-07, as
  recomputation is a verification activity);
  (iv) `vr.result = PASS` normatively means the recomputation produced a
  value exactly equal to the primary result (§D.6: agreement is exact
  equality of derived values).
- **Solver basis.** `SOLVER_BACKED` is substantiated by the presence of a
  `solver_observation` (any outcome: the observation underlies the
  conclusion; its evidential weight follows §D.6).
- **Test basis.** `TEST_BACKED` is substantiated by a verification record
  with `source_item ∈ {"test:differential", "test:property-fuzz"}` and
  `result = PASS`.


---

## A2. New invariants 24–28 (F-21) — lines 1359–1398

24. (F-21) `∀ r: ResultRecord. (r.assurance_achieved = LEVEL_A) ⇒ (r.semantic_result = Some(sr) ∧ sr ≠ INCONCLUSIVE{_})`
    for some `sr: SemanticResult`. In prose: achieved Level A requires an
    actual, non-inconclusive semantic result. This preserves the valid
    shortfall case: Level A required, Level B achieved, and
    `INCONCLUSIVE{ASSURANCE_REQUIREMENT_UNMET}` (invariant 11) has
    `assurance_achieved = LEVEL_B`, so this invariant does not apply.
25. (F-21) `∀ r: ResultRecord. ((r.assurance_achieved = LEVEL_A ∧ KERNEL_PROOF ∈ r.assurance_bases)
    ⇒ ∃ vr ∈ r.verification_records: (vr.source_item = "proof" ∧ vr.result = PASS
    ∧ ∃ a ∈ r.evidence.proof_artifacts: a.sha256 = vr.artifact))`.
    In prose: a claimed `KERNEL_PROOF` basis for achieved Level A must be
    substantiated by a passing proof verification record whose `artifact`
    is the proof artifact's hash resolving in `evidence.proof_artifacts`
    (per §E.6a). A record that merely names `KERNEL_PROOF` without this
    evidence violates this invariant. Consistency: such a record also
    constrains `verification_summary` via invariants 4 and 14 and the §E.6
    precedence (a PASS proof record with no worse record ⇒ summary PASS).
26. (F-21) `∀ r: ResultRecord. ∀ v: Option<Hash>. ∀ d: Hash.
    ((r.assurance_achieved = LEVEL_A ∧ INDEPENDENT_RECOMPUTE ∈ r.assurance_bases
    ∧ r.semantic_result = Some(DERIVED_VALUE{value_ref = v, derivation_ref = d}))
    ⇒ ∃ vr ∈ r.verification_records: (vr.source_item = "recompute" ∧ vr.result = PASS
    ∧ vr.inputs_ref = r.evidence.verification_inputs_ref
    ∧ ((v = Some(h) ∧ vr.artifact = h) ∨ (v = None ∧ vr.artifact = d))))`.
    In prose: a claimed `INDEPENDENT_RECOMPUTE` basis for achieved Level A
    on a derived value must be substantiated by a passing recomputation
    verification record identifying the primary result compared
    (per §E.6a). `vr.result = PASS` normatively attests exact agreement
    (§D.6); checker independence is attested via `vr.checker` (§E.6a).
    A record that merely names `INDEPENDENT_RECOMPUTE` without this
    evidence violates this invariant.
27. (F-21) `∀ r: ResultRecord. ((r.assurance_achieved = LEVEL_B ∧ SOLVER_BACKED ∈ r.assurance_bases)
    ⇒ r.solver_observation = Some(_))`.
    In prose: a claimed `SOLVER_BACKED` basis for achieved Level B must be
    substantiated by a present solver observation.
28. (F-21) `∀ r: ResultRecord. ((r.assurance_achieved = LEVEL_B ∧ TEST_BACKED ∈ r.assurance_bases)
    ⇒ ∃ vr ∈ r.verification_records: ((vr.source_item = "test:differential" ∨ vr.source_item = "test:property-fuzz")
    ∧ vr.result = PASS))`.
    In prose: a claimed `TEST_BACKED` basis for achieved Level B must be
    substantiated by a passing differential or property-fuzz test
    verification record.


---

## A3. Revised invariant 10 (F-20) — lines 1296–1302

10. (F-20) `∀ r: ResultRecord. ∀ e: String. (r.execution = INTERNAL_ERROR(e) ∧ is_packaging_error(e)) ⇒ r.semantic_result ≠ None`.
    In prose: `execution = INTERNAL_ERROR(e)` ⇒ the `reason` field `e` is recorded; if the failure
    occurred at packaging (`is_packaging_error(e)`, i.e. `base_code(e) ∈ {output-not-encodable, canonicalization-failure}`),
    the established `semantic_result` is still recorded (D-019: a valid
    result with an unserializable output is never INVALID_INPUT).
    Temporal note: the static record establishes the result's presence and its evidence linkage;
    it cannot by itself prove the historical transition from pre-packaging to post-packaging state.

---

## A4. Invariant 15 — lines 1311–1321

15. (D-030) `output_packaging = PACKAGING_OK` ∧ `semantic_result =
    Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = Some(h)` ∧ `h`
    resolves to a canonicalized value artifact in
    `evidence.constructed_artifacts`. (NEW-C5: named list; the v0.8 draft
    said "the evidence bundle".)
    `output_packaging = PACKAGING_FAILED(_)` ∧ `semantic_result =
    Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = None`. (F-16: the
    previous wording left `value_ref` unbound outside the `DERIVED_VALUE`
    alternative.) A NaN or function value therefore yields
    `PACKAGING_FAILED(output-not-encodable)` with the semantic result
    preserved — never INVALID_INPUT.

---

## A5. Invariant 15b — lines 1322–1329

15b. (D-030, NEW-B7) Joint packaging/execution state:
    `output_packaging = PACKAGING_FAILED(r)` ⇔ `execution =
    INTERNAL_ERROR(e)` ∧ `base_code(e) = base_code(r)` (F-01: the reason's
    base code must equal the packaging reason's base code; details may
    differ).
    `output_packaging = PACKAGING_OK` ⇒ `execution` is not
    `INTERNAL_ERROR` with an `output-not-encodable`/`canonicalization-failure`
    base code.

---

## A6. Invariant 16 — lines 1330–1332

16. (D-030) `semantic_result = Some(ARTIFACT_CONSTRUCTED {artifact_ref})`    ⇒ `artifact_ref = Some(h)` resolves in
    `evidence.constructed_artifacts`, or `artifact_ref = None` iff
    `output_packaging = PACKAGING_FAILED(_)`.

---

## A7. Type definitions — §E.1 schema block, lines 1071–1176

```
ResultRecord {
  admission: ACCEPTED | INVALID_INPUT(reason: AdmissionError) | UNSUPPORTED(reason: UnsupportedReason),
  execution: NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED
             | INTERNAL_ERROR(reason: String),
  output_packaging: PACKAGING_OK | PACKAGING_FAILED(reason: PackagingError),
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
  discrepancies: [Discrepancy],
}

AdmissionError := closed per §B.9 (27 codes; is_admission_error).
UnsupportedReason := closed per §B.9 (3 codes; is_unsupported_reason).
ValidationError := closed per §B.13a (12 codes; is_validation_error).
PackagingError := String; closure is enforced by the predicate (F-01):
```define is_packaging_error(e: PackagingError): Bool =
  (base_code(e) == "output-not-encodable") \/
  (base_code(e) == "canonicalization-failure")```
which covers exactly {output-not-encodable, canonicalization-failure}
(D-030); the `": <detail>"` suffix convention of §B.9 applies (base code
checked before `": "`).

(NEW-C2) `INTERNAL_ERROR` reasons are an **intentionally open** domain:
they name implementation-level failures, which the specification cannot
close. The reasons specified normatively in v0.8 are:
`inexact-division` (§B.4 rule 2), `division-by-zero` (§B.4 rule 2, NEW-B6),
`output-not-encodable: <type>` (§G.2 packaging failure — joint with
`output_packaging` per inv. 15b), `canonicalization-failure: <detail>`
(§G.2). Any future specified reason must be added to this list; ad-hoc
reasons are permitted only for failures outside specified behavior and
must be recorded verbatim.

AssuranceBasis := KERNEL_PROOF | INDEPENDENT_RECOMPUTE | SOLVER_BACKED | TEST_BACKED
# Derivation: KERNEL_PROOF from `proof: kernel-checked …`;
# INDEPENDENT_RECOMPUTE from `recompute: by …`;
# SOLVER_BACKED when a solver observation underlies the conclusion;
# TEST_BACKED from differential/fuzz test items.

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
# Payload binding (D-022, D-030): each alternative carries the references
# that make it auditable. value_ref / artifact_ref are Option<Hash> because
# a computed value may have no canonical form (NaN, function values):
# PACKAGING_OK ⇒ Some(_); PACKAGING_FAILED ⇒ None (§E.7 inv. 15–16).
# derivation_ref points to the derivation record; witness_ref to the
# recorded counterexample witness. Payload-free tags (NO_SOLUTION, HOLDS,
# CONTRADICTION) are linked to their justifying evidence by §E.7
# invariants 20–22, not by new payloads.

ReasonCode := SOLVER_UNKNOWN | PROCEDURE_INCOMPLETE | RESOURCE_EXHAUSTED
            | EXECUTION_INTERRUPTED | ASSURANCE_REQUIREMENT_UNMET | NO_TEST_CORPUS

SolverObs := { outcome: SAT | UNSAT | UNKNOWN, tool: String, version: SemVer,
               config: String, provenance_ref: Hash,
               certificate_ref: Option<Hash> }

VerificationRecord := { property: String, artifact: String, spec_version: SemVer,
  method: String, checker: CheckerID, result: PASS | FAIL | INCONCLUSIVE,
  reason: Option<String>, assurance_boundary: String, inputs_ref: Hash,
  source_item: String, required: Bool }
# source_item (D-033): identifies the originating verification item, e.g.
# "proof", "recompute", "test:differential", "test:property-fuzz",
# "assurance". required: the item's qualifier (default required, §B.7).
# Invariant 14 is evaluated from these recorded fields.

EvidenceBundle := {
  derivation_records: [ArtifactRef], proof_artifacts: [ArtifactRef],
  witnesses: [ArtifactRef], constructed_artifacts: [ArtifactRef],
  verification_inputs_ref: Hash, external_evidence_records: [ExternalEvidence] }
ArtifactRef := { sha256: Hash, bytes: Nat, media: String, description: String }
ExternalEvidence := { experiment_id: String, method: String,
  data_ref: Hash, recorded_at: String }
# recorded_at: ISO 8601 UTC, exactly "YYYY-MM-DDTHH:MM:SSZ" (D-022).

PartialResult := { description: String, semantic_fragment: SemanticResult,
  provenance_ref: Hash, labelled_partial: true }
# Validation: present only when execution ∈ {TIMEOUT, INTERRUPTED}.

Discrepancy := { property: String, involved_records: [Nat],
  description: String, required_follow_up: String, status: OPEN | RESOLVED }
# involved_records: 0-based indices into this record's verification_records.
# status may move OPEN → RESOLVED only with a recorded resolution.
# (D-022 definitions.)

Hash := String of exactly 64 characters in [0-9a-f]  # SHA-256, lowercase hex
# Canonical encoding: {"$type":"hash","value":"<64 hex>"} (§G.2).
```

---

## A8. §D.6 Evidence taxonomy — lines 1046–1064

### D.6 Evidence taxonomy

| Method | Establishes | Assumes | Does NOT establish |
|---|---|---|---|
| Kernel-checked proof | The proposition follows from the stated assumptions in the kernel's logic | Formalization adequacy (human); kernel soundness | Truth of the assumptions; adequacy of the formalization |
| Independent recomputation | A second, independent implementation produced the same derived value | Checker independence (separation); determinism of the derivation | A formal proof of the claim; absence of shared-specification bugs |
| Solver observation (SAT/UNSAT/UNKNOWN) | The solver reported this outcome under the recorded configuration | Solver soundness within the declared fragment | A proof (UNSAT alone is not a proof); correctness outside the fragment |
| Differential test | Primary and reference agree on the tested corpus | Reference independence; corpus relevance | Universal correctness |
| Property fuzz | No counterexample in the generated cases | Generator coverage; oracle correctness | Universal correctness |
| Bounded test | The stated property held for the executed cases | Corpus adequacy | Anything about untested cases |

**Independent recomputation is not a formal proof term** (D-021). The grammar
keeps it syntactically separate (`recompute:` vs `proof:`). For `derive`
goals it is admissible Level A evidence *for the exact-arithmetic derivation
class* because the derivation is deterministic, the recompute checker is
independent, and the comparison is exact equality of derived values. What
remains assumed — no shared misreading of the specification — is recorded in
the evidence bundle, never silently upgraded.


---

## A9. §E.4 and §E.5 — lines 1201–1224

### E.4 Solver observation vs semantic conclusion vs assurance

The solver's report (`SolverObs`) is data. The semantic conclusion
(`SemanticResult`) is a judgment under the assurance policy. The assurance
triple records what was requested, on what bases, what was achieved, and the
computed shortfall.
- UNSAT observation with Level A required and only solver backing available →
  `solver_observation = {UNSAT,…}`, `semantic_result = Some(INCONCLUSIVE
  {ASSURANCE_REQUIREMENT_UNMET})`, `assurance_shortfall = true`. MSVE reports what the
  solver said and declines the stronger claim.
- A Level B conclusion (incl. CONTRADICTION from a solver) may be reported
  only with explicit `level-b accepted` in the frozen spec (§E.7 inv. 12);
  the record shows `assurance_achieved = LEVEL_B` with the corresponding basis.

### E.5 Level A policy (v0)

- `prove` goals: kernel-checked proof only.
- `derive` goals (exact arithmetic): kernel-checked proof OR independent
  recomputation with agreement (evidential meaning: §D.6).
- SMT-UNSAT Level A: FUTURE — no invented certificates; unsat cores are
  diagnostic (observation, not proof).
- Solver- or test-backed goals: no Level A pipeline in v0 (admission rejects
  `level-a required`).


---

## A10. Helper definitions

### `is_packaging_error` — lines 1093–1099

ValidationError := closed per §B.13a (12 codes; is_validation_error).
PackagingError := String; closure is enforced by the predicate (F-01):
```define is_packaging_error(e: PackagingError): Bool =
  (base_code(e) == "output-not-encodable") \/
  (base_code(e) == "canonicalization-failure")```
which covers exactly {output-not-encodable, canonicalization-failure}
(D-030); the `": <detail>"` suffix convention of §B.9 applies (base code

### `base_code` — lines 619–627

**`base_code: String -> String`** (F-01: normative detail-separator
operation; also listed in the §B.4 rule 11 builtin inventory). For any
string `e`, `base_code(e)` is the prefix of `e` before the first occurrence
of `": "` (colon followed by exactly one space); if `e` contains no `": "`,
`base_code(e) = e`. The remainder after the first `": "` is the *detail*:
free text, which may be empty and may itself contain further `": "`
sequences. The operation is total on `String`. A code may carry a detail
suffix `": <detail>"` (e.g. `unbound-identifier: foo`); every closure
predicate below tests `base_code(e)`, never `e` directly.

---

## Recorded note (not a repair)

Line 1330 in the source contains irregular spacing in
"`{artifact_ref})`    ⇒" (four spaces before ⇒). Transcribed verbatim;
not repaired.
