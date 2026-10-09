# MSVE v0.8.7 Transfer — Report A: Exact Normative Text

**Source:** `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/MSVE_DESIGN_SPEC_v0.8.md`
**Full SHA-256:** `48707955c81c4731e8533fa5135de2001388fd11461e2b0cef5a518730c4080e`
**Method:** verbatim programmatic extraction. Commentary is marked [COMMENTARY].

---

## A1. Claim-key definition — lines 1240–1253

- **Claim linkage.** A verification record substantiates a basis for a
  result `r` only if its `property` field identifies the claim of
  `r.semantic_result`. The claim key is defined as:
  - `Some(DERIVED_VALUE{value_ref = Some(h), …})` → `h`;
  - `Some(DERIVED_VALUE{value_ref = None, derivation_ref = d})` → `d`;
  - `Some(PROVED{proof_artifact = h})` → `h`;
  - `Some(ARTIFACT_CONSTRUCTED{artifact_ref = Some(h)})` → `h`;
  - `Some(DISPROVED{refutation_ref = h})` → `h`;
  - `Some(UNDERDETERMINED{witnesses_ref = h})` → `h`.
  - `Some(VIOLATED{witness_ref = h})` → `h`;
  `None` and `Some(INCONCLUSIVE{…})` have no provable claim; no basis
  substantiation applies to them. (F-23: a correctly classified but
  unrelated record — one whose `property` does not equal the claim key —
  does not substantiate the basis.)

[COMMENTARY: R1-1 (blocking) — no claim key is defined for `HOLDS`,
`NO_SOLUTION`, `CONTRADICTION`, or `UNIQUE_UNDER_PROJECTION`.]

---

## A2. Verification-record substantiation per basis — lines 1254–1291

- **Hash form.** `is_sha256_hex(s)` ≜ `s` is exactly 64 characters, each
  `0`–`9` or `a`–`f`. Proof and recomputation artifacts must satisfy this.
- **Proof basis (`source_item = "proof"`).** A verification record with
  `source_item = "proof"` and `result = PASS` substantiates a
  `KERNEL_PROOF` basis only if:
  (i) `vr.method = "kernel-checked"` (D-021: the proof method);
  (ii) `vr.property` equals the claim key of the result's semantic result;
  (iii) `vr.artifact` satisfies `is_sha256_hex` and equals the sha256 of
  an entry in `evidence.proof_artifacts`;
  (iv) `vr.checker` identifies the checking kernel (the specific
  authorization of a checker ID is attested, not in the record schema).
- **Recomputation basis (`source_item = "recompute"`).** A verification
  record with `source_item = "recompute"` and `result = PASS`
  substantiates an `INDEPENDENT_RECOMPUTE` basis only if:
  (i) `vr.property` equals the claim key of the result's semantic result;
  (ii) `vr.checker` identifies the independent checker (normative: this
  checker must be independent of the primary derivation producer;
  independence is attested by the producer and recorded via the checker
  ID for audit — it is not mechanically derivable from the record, which
  carries no primary-producer field) (F-24);
  (iii) `vr.artifact` satisfies `is_sha256_hex` and identifies the primary
  result compared — for `DERIVED_VALUE{value_ref = Some(h), …}` the value
  hash `h`, else the `derivation_ref` hash;
  (iv) `vr.inputs_ref` equals `evidence.verification_inputs_ref`;
  (v) `vr.result = PASS` normatively means the recomputation produced a
  value exactly equal to the primary result (§D.6).
- **Solver basis.** `SOLVER_BACKED` is substantiated by a present
  `solver_observation`. The observation is a field of the `ResultRecord`
  and is therefore structurally the observation for this result; its
  outcome must be consistent with the semantic conclusion per invariants
  4, 11, and 22. (F-23: a solver observation cannot be "unrelated" — it
  is part of the record — but an inconsistent outcome violates the
  outcome invariants.)
- **Test basis.** `TEST_BACKED` is substantiated by a verification record
  with `source_item ∈ {"test:differential", "test:property-fuzz"}`,
  `result = PASS`, and `vr.property` equal to the claim key of the
  result's semantic result. (F-23: a passing test for a different
  property does not substantiate the basis.)

---

## A3. Revised invariants 24–28 — lines 1384–1426

24. (F-21) `∀ r: ResultRecord. (r.assurance_achieved = LEVEL_A) ⇒ ∃ sr: SemanticResult. (r.semantic_result = Some(sr) ∧ sr ≠ INCONCLUSIVE{_})`
    for some `sr: SemanticResult`. In prose: achieved Level A requires an
    actual, non-inconclusive semantic result. This preserves the valid
    shortfall case: Level A required, Level B achieved, and
    `INCONCLUSIVE{ASSURANCE_REQUIREMENT_UNMET}` (invariant 11) has
    `assurance_achieved = LEVEL_B`, so this invariant does not apply.
25. (F-21, revised 0.8.7 for F-22/F-23) `∀ r: ResultRecord. (KERNEL_PROOF ∈ r.assurance_bases
    ⇒ ∃ vr ∈ r.verification_records: (vr.source_item = "proof" ∧ vr.result = PASS
    ∧ vr.method = "kernel-checked" ∧ vr.property = claim_key(r.semantic_result)
    ∧ is_sha256_hex(vr.artifact) ∧ vr.checker ≠ ""
    ∧ ∃ a ∈ r.evidence.proof_artifacts: a.sha256 = vr.artifact))`.
    In prose: any claimed `KERNEL_PROOF` basis — at any achieved level —
    must be substantiated by a passing kernel-checked proof verification
    record whose `property` is the result's claim key and whose `artifact`
    is the proof artifact's hash resolving in `evidence.proof_artifacts`
    (per §E.6a). A record that merely names the basis, uses a different
    method, or verifies a different property does not substantiate it.
26. (F-21, revised 0.8.7 for F-22/F-23) `∀ r: ResultRecord. (INDEPENDENT_RECOMPUTE ∈ r.assurance_bases
    ⇒ (∃ sr: SemanticResult. (r.semantic_result = Some(sr) ∧ sr = DERIVED_VALUE{…}))
    ∧ (∀ v: Option<Hash>. ∀ d: Hash.
    ((r.semantic_result = Some(DERIVED_VALUE{value_ref = v, derivation_ref = d}))
    ⇒ ∃ vr ∈ r.verification_records: (vr.source_item = "recompute" ∧ vr.result = PASS
    ∧ vr.property = claim_key(r.semantic_result) ∧ vr.checker ≠ ""
    ∧ vr.inputs_ref = r.evidence.verification_inputs_ref ∧ is_sha256_hex(vr.artifact)
    ∧ ((∃ h: Hash. (v = Some(h) ∧ vr.artifact = h)) ∨ (v = None ∧ vr.artifact = d))))))`.
    In prose: any claimed `INDEPENDENT_RECOMPUTE` basis requires a
    `DERIVED_VALUE` result (recomputation is the `derive`-goal path per
    §E.5; the basis is incompatible with other result types) and a passing
    recomputation record linked to the exact claim, checker, inputs, and
    primary result (per §E.6a). Checker independence is attested via
    `vr.checker`, not mechanically derived.
27. (F-21, revised 0.8.7 for F-22) `∀ r: ResultRecord. (SOLVER_BACKED ∈ r.assurance_bases
    ⇒ r.solver_observation = Some(_))`.
    In prose: any claimed `SOLVER_BACKED` basis — at any achieved level —
    must be substantiated by a present solver observation (structurally the
    observation for this result; outcome-consistency via invariants 4, 11, 22).
28. (F-21, revised 0.8.7 for F-22/F-23) `∀ r: ResultRecord. (TEST_BACKED ∈ r.assurance_bases
    ⇒ ∃ vr ∈ r.verification_records: ((vr.source_item = "test:differential" ∨ vr.source_item = "test:property-fuzz")
    ∧ vr.result = PASS ∧ vr.property = claim_key(r.semantic_result)))`.
    In prose: any claimed `TEST_BACKED` basis — at any achieved level —
    must be substantiated by a passing differential or property-fuzz test
    verification record whose `property` is the result's claim key.


---

## A4. Type definitions

### SolverObs — lines 1142–1144

SolverObs := { outcome: SAT | UNSAT | UNKNOWN, tool: String, version: SemVer,
               config: String, provenance_ref: Hash,
               certificate_ref: Option<Hash> }

### VerificationRecord — lines 1146–1152

VerificationRecord := { property: String, artifact: String, spec_version: SemVer,
  method: String, checker: CheckerID, result: PASS | FAIL | INCONCLUSIVE,
  reason: Option<String>, assurance_boundary: String, inputs_ref: Hash,
  source_item: String, required: Bool }
# source_item (D-033): identifies the originating verification item, e.g.
# "proof", "recompute", "test:differential", "test:property-fuzz",
# "assurance". required: the item's qualifier (default required, §B.7).

### EvidenceBundle / ArtifactRef — lines 1154–1158


EvidenceBundle := {
  derivation_records: [ArtifactRef], proof_artifacts: [ArtifactRef],
  witnesses: [ArtifactRef], constructed_artifacts: [ArtifactRef],
  verification_inputs_ref: Hash, external_evidence_records: [ExternalEvidence] }

### ResultRecord (schema) — lines 1072–1091

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

---

## A5. §E.4–§E.6a — lines 1201–1231

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

### E.6 Verification aggregation (divergence-first)

Per-property `VerificationRecord`s are never collapsed. Summary precedence:
CHECKER_DIVERGENCE > FAIL > INCONCLUSIVE > PASS; no records → NOT_RUN.
A PASS/FAIL split on the same property → CHECKER_DIVERGENCE with both records
preserved and a `Discrepancy{status: OPEN}` requiring follow-up.


---

## A6. provenance_ref references

`provenance_ref: Hash` appears in `SolverObs` (line 1143) and in a
`labelled_partial` record (line 1165). No normative definition of what
`provenance_ref` points to, how the target is represented, or whether
the relationship is machine-checkable was found in the specification.
[COMMENTARY: This is UNDEFINED OR UNDERCONSTRAINED — see Report B, Q-B.]

---

## A7. Coverage matrix

See `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/MSVE_v0.8.7_COVERAGE_MATRIX.md`
(SHA-256 `8a3a15cc1d0a19c5718f830e012d5af7155c7d2cace5d114401f793e1630062b`).
The matrix adjudicates that every basis in `assurance_bases` must be
substantiated at any level, and records unresolved limitations
(checker independence attested; payload-free variants per R1-1).
