# Report B — Design Evidence — Specification (Part 3/3)

**Work Order:** 0.8.2 · **Source file:** `six-docs/MSVE_DESIGN_SPEC_v0.8.md` (DIRECT ARTEFACT, sha256 `377e106ef2b00db6…`)

Complete original text, unmodified. Part 3 of 3 (continued). END.

---


AdmissionError := closed per §B.9 (27 codes; is_admission_error).
UnsupportedReason := closed per §B.9 (3 codes; is_unsupported_reason).
ValidationError := closed per §B.13a (12 codes; is_validation_error).
PackagingError := String; is_packaging_error covers exactly
  {output-not-encodable, canonicalization-failure} (D-030); the
  `": <detail>"` suffix convention of §B.9 applies (base code checked
  before `": "`).

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

**Normative shortfall rule.**
```
shortfall = (required == LEVEL_A && achieved != LEVEL_A)
         || (required == LEVEL_B && achieved == NONE)
```
Invariants: `achieved == LEVEL_A` ⇒ `KERNEL_PROOF ∈ bases ∨ INDEPENDENT_RECOMPUTE ∈ bases`;
`achieved == LEVEL_B` ⇒ `bases` non-empty; `required == NONE` ⇒ `shortfall = false`.

### E.2 Semantic results per goal type

- `derive` → DERIVED_VALUE {value_ref, derivation_ref} | INCONCLUSIVE {reason}.
- `construct` → ARTIFACT_CONSTRUCTED {artifact_ref} | NO_SOLUTION {} | INCONCLUSIVE.
- `prove` → PROVED {proof_artifact} | DISPROVED {refutation_ref} | INCONCLUSIVE.
- `check` → HOLDS {} | VIOLATED {witness_ref} | INCONCLUSIVE (incl. NO_TEST_CORPUS).
- `compare-models` → UNIQUE_UNDER_PROJECTION {projection} |
  UNDERDETERMINED {witnesses_ref} | CONTRADICTION {} | INCONCLUSIVE.

### E.3 INCONCLUSIVE reason codes

SOLVER_UNKNOWN; PROCEDURE_INCOMPLETE; RESOURCE_EXHAUSTED;
EXECUTION_INTERRUPTED; ASSURANCE_REQUIREMENT_UNMET (shortfall recorded);
NO_TEST_CORPUS (never a vacuous HOLDS).

### E.4 Solver observation vs semantic conclusion vs assurance

The solver's report (`SolverObs`) is data. The semantic conclusion
(`SemanticResult`) is a judgment under the assurance policy. The assurance
triple records what was requested, on what bases, what was achieved, and the
computed shortfall.
- UNSAT observation with Level A required and only solver backing available →
  `solver_observation = {UNSAT,…}`, `semantic_result = Some(INCONCLUSIVE
  {ASSURANCE_REQUIREMENT_UNMET})`, `shortfall = true`. MSVE reports what the
  solver said and declines the stronger claim.
- A Level B conclusion (incl. CONTRADICTION from a solver) may be reported
  only with explicit `level-b accepted` in the frozen spec (§E.7 inv. 12);
  the record shows `achieved = LEVEL_B` with the corresponding basis.

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

### E.7 Cross-field invariants (exhaustive; D-022)

1. `admission ∈ {INVALID_INPUT, UNSUPPORTED}` ⇒ `execution = NOT_STARTED` ∧
   `semantic_result = None` ∧ `verification_summary = NOT_RUN` ∧
   `assurance_bases = []` ∧ `achieved = NONE`.
2. `execution ∈ {NOT_STARTED, RUNNING}` ⇒ `semantic_result = None`.
3. `semantic_result = Some(HOLDS {})` ⇒ the check corpus was non-empty.
4. `verification_summary = CHECKER_DIVERGENCE` ⇒ `discrepancies` contains an
   entry with `status = OPEN`.
5. `assurance_shortfall = true` ⇔ the §E.1 shortfall rule holds; ⇒
   `shortfall_description = Some(_)`.
6. `achieved = LEVEL_A` ⇒ `KERNEL_PROOF ∈ bases ∨ INDEPENDENT_RECOMPUTE ∈ bases`.
7. `achieved = LEVEL_B` ⇒ `bases ≠ []`.
8. `semantic_result = Some(VIOLATED {witness_ref})` ⇒ the witness artifact is
   in `evidence.witnesses`.
9. `semantic_result = Some(DERIVED_VALUE {value_ref, derivation_ref})` ⇒
   `derivation_ref` resolves in `evidence.derivation_records`; `value_ref`
   per invariant 15. (NEW-C5: the v0.8 draft said "the evidence bundle"
   without naming a list.)
10. `execution = INTERNAL_ERROR` ⇒ `reason` is recorded; if the failure
    occurred at packaging (`reason` starts with `output-not-encodable`),
    the established `semantic_result` is still recorded (D-019: a valid
    result with an unserializable output is never INVALID_INPUT).
11. `solver_observation = Some({outcome: UNSAT, …})` ∧ `required = LEVEL_A`
    ∧ `achieved ≠ LEVEL_A` ⇒ `semantic_result =
    Some(INCONCLUSIVE {ASSURANCE_REQUIREMENT_UNMET})`.
12. `achieved = LEVEL_B` ⇒ the frozen spec contains `assurance: level-b accepted`.
13. `partial_results ≠ []` ⇒ `execution ∈ {TIMEOUT, INTERRUPTED}`.
14. Every `VerificationRecord` with `result = FAIL` ∧ `required = true` ⇒
    `verification_summary ∈ {FAIL, CHECKER_DIVERGENCE}` (D-033: evaluated
    from the recorded `source_item`/`required` fields).
15. (D-030) `output_packaging = PACKAGING_OK` ∧ `semantic_result =
    Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = Some(h)` ∧ `h`
    resolves to a canonicalized value artifact in
    `evidence.constructed_artifacts`. (NEW-C5: named list; the v0.8 draft
    said "the evidence bundle".)
    `output_packaging = PACKAGING_FAILED(_)` ⇒ `value_ref = None`. A NaN
    or function value therefore yields `PACKAGING_FAILED(output-not-encodable)`
    with the semantic result preserved — never INVALID_INPUT.
15b. (D-030, NEW-B7) Joint packaging/execution state:
    `output_packaging = PACKAGING_FAILED(r)` ⇔ `execution =
    INTERNAL_ERROR` with a reason whose base code is `r`'s base code.
    `output_packaging = PACKAGING_OK` ⇒ `execution` is not
    `INTERNAL_ERROR` with an `output-not-encodable`/`canonicalization-failure`
    reason.
16. (D-030) `semantic_result = Some(ARTIFACT_CONSTRUCTED {artifact_ref})`    ⇒ `artifact_ref = Some(h)` resolves in
    `evidence.constructed_artifacts`, or `artifact_ref = None` iff
    `output_packaging = PACKAGING_FAILED(_)`.
17. (D-030) `semantic_result = Some(PROVED {proof_artifact})` ⇒ the hash
    resolves in `evidence.proof_artifacts`.
18. (D-030) `semantic_result = Some(DISPROVED {refutation_ref})` ⇒ the
    hash resolves in `evidence.derivation_records`.
19. (D-030) `semantic_result = Some(UNDERDETERMINED {witnesses_ref})` ⇒
    the hash resolves in `evidence.witnesses`.
20. (D-030) `semantic_result = Some(HOLDS {})` ⇒ some `VerificationRecord`
    has `result = PASS` for the check property with `inputs_ref` resolving
    in the evidence bundle.
21. (D-030) `semantic_result = Some(NO_SOLUTION {})` ⇒
    `solver_observation = Some(_)` ∨ a search record in
    `evidence.derivation_records`.
22. (D-030) `semantic_result = Some(CONTRADICTION {})` ⇒
    `solver_observation = Some({outcome: UNSAT, …})` ∨ a proof artifact in
    `evidence.proof_artifacts`.
23. (D-022, NEW-C4) `semantic_result = Some(UNIQUE_UNDER_PROJECTION
    {projection})` ⇒ `solver_observation = Some({outcome: UNSAT, …})`
    recording the completed second-model query under that projection ∨ a
    derivation record in `evidence.derivation_records` witnessing it.
    An evidence-free uniqueness claim violates this invariant.
    (NEW-C4: the v0.8 draft left this alternative without an evidence link.)

### E.8 External evidence (three-way split)

- **Evidence recorded:** the experiment, method and data reference ingested
  with provenance (`ExternalEvidence`).
- **Record integrity:** hashes / signatures vs the trusted reference.
- **External scientific assessment:** MSVE asserts nothing about the truth of
  external evidence; that assessment lives outside MSVE.

### E.9 Anti-conflation hard rules

1. A solver observation is never a semantic conclusion by itself.
2. A test result is never a universal claim.
3. Recorded evidence is never truth-certified evidence.
4. A shortfall is never silently absorbed: it is computed and, when true,
   described.
5. Two independent checkers disagreeing is DIVERGENCE, never averaged away.

---

## F. Trust base

Orchestration over established components; no new solver in v0. Parser/validator
(MSVE-owned): syntax/typing/mandatory fields — not semantics. Abstract decoder
(§B.13): the table is the contract; any implementation's parser conforms only
via an L2 method. SymPy (pinned): computed / independently checkable /
trusted-tool output. Z3 (pinned): decidable-fragment satisfiability; re-checked
witnesses; `unknown` preserved. Lean kernel (pinned): proof-term acceptance
relative to formal statement/definitions/imports/axioms. Independent checker
(per case): L3 agreement; recompute checker: §D.6. Provenance recorder: identity
+ integrity-vs-reference. "Trusted" = relied upon within the documented boundary
only.

---

## G. Provenance, canonicalisation, maturity

### G.1 Separated provenance claims

Content identity / integrity vs trusted reference / authenticity (v0: signed
release tags; key management bounded implementation decision) / correctness
(verification only). **"tamper-evident relative to a trusted reference"** —
never "tamper-proof".

### G.2 Canonical encoding profile `msve-canonical-3` (D-017, D-018, D-019)

Deterministic; versioned; **no bare JSON values** — every value is a typed
object with an explicit `$type` tag. `msve-canonical-2` (v0.6) is superseded
before any use: its binary64 rule admitted non-unique forms (D-017).
`msve-canonical-1` remains superseded (D-004). Old hashes are never
reinterpreted under new rules.

**Type tags:**

- **nat:** `{"$type":"nat","value":"12345"}` — no sign, no leading zeros.
- **int:** `{"$type":"int","value":"-12345"}` — optional `-`; `-0`→`"0"`.
- **rat (D-027 — rational text grammar):** `{"$type":"rat","value":"<text>"}`
  where `<text> := "-"? Nat "/" Nat` with: no leading zeros on either part
  (`07/3` forbidden); denominator > 0 (`1/0` forbidden); `gcd(num, den) = 1`
  (lowest terms; `6/4` forbidden); zero is exactly `0/1` (no `-0/1`).
  The same normal form is used under the `real` tag.
- **real (D-019):** `{"$type":"real","value":"<text>"}` — **exact rational
  payload** in the `<text>` normal form above under the `Real` tag. In v0,
  `Real` denotes exact rational values (no v0 operation constructs
  irrationals); therefore **every v0 `Real` is encodable**. The tag
  preserves type identity and reserves the future true-real extension
  (Appendix 3).
- **f64 (D-017, D-026 — exact unique grammar):**
  `{"$type":"f64","value":"<form>"}` where `<form>` is:
  `"-"? "0x" Sig "." Frac13 "p" ("+0" | ("+"|"-") [1-9][0-9]*)`, with
  `Sig ∈ {"0","1"}`, `Frac13` exactly thirteen lowercase hex digits
  (D-026: the exponent is exactly `+0` or sign + nonzero digits — `-0`
  is not a spelling; `0x1.0000000000000p-0` is rejected, `p+0` is the
  unique form), and:
  - all fourteen hex digits zero → exactly `0x0.0000000000000p+0`
    (+0.0; −0.0 normalizes here; no sign);
  - `Sig = "1"` (normal): `Exp` must satisfy `-1022 ≤ Exp ≤ 1023`;
    value = ±`1.Frac13`₁₆ × 2^`Exp`. (The lower bound keeps normal forms
    disjoint from subnormal values; the upper bound keeps them finite —
    larger magnitudes are ±infinity, encoded separately.)
  - `Sig = "0"`, `Frac13 ≠ 0` (subnormal): exponent must be exactly `-1074`;
    value = ±`M` × 2^−1074 where `M` is the 13-digit hex integer;
  - sign `-` iff the value is negative.
  **Uniqueness:** every finite nonzero binary64 is either normal — unique
  `(Frac13, Exp)` since the normalized significand in [1,2) carries exactly
  52 bits = 13 hex digits — or subnormal — unique `M`; zero is unique.
  The v0.6 counterexamples are rejected: `0x2.0000000000000p+0` (leading
  digit must be `1` for normals), `0x1.0000000000000p-1074` (subnormals use
  the `0.` form with `p-1074`), `p+01` (no leading zeros). The v0.7
  survivor is rejected: `0x1.0000000000000p-0` (D-026: `-0` is not an
  exponent spelling; the unique form is `p+0`).
- **f64 non-finite (D-018):** `{"$type":"f64","value":"inf"}` /
  `{"$type":"f64","value":"-inf"}`. **NaN is not encodable** (payloads are
  implementation-defined; NaN ≠ NaN breaks value identity) — a NaN reaching
  packaging is a packaging failure (§E.7 inv. 10).
- **real (D-019):** `{"$type":"real","value":"-7/3"}` — **exact rational
  payload** (reduced fraction, same normal form as `rat`) under the `Real`
  tag. In v0, `Real` denotes exact rational values (no v0 operation
  constructs irrationals); therefore **every v0 `Real` is encodable**.
  The tag preserves type identity and reserves the future true-real
  extension (Appendix 3).
- **bool:** `{"$type":"bool","value":true}` / `false`.
- **string (D-027 — deterministic escaping):**
  `{"$type":"string","value":"…"}` where the JSON string is NFC-normalized
  UTF-8 and escaped by exactly this policy:
  - `"` → `\"`, `\` → `\\`, backspace → `\b`, form feed → `\f`,
    newline → `\n`, carriage return → `\r`, tab → `\t`;
  - any other codepoint < U+0020 or U+007F–U+009F → `\uXXXX` with exactly
    4 **lowercase** hex digits (`\u001a`, never `\u001A`);
  - a `\uXXXX` escape is never used where a short escape exists
    (`\u000a` is forbidden; `\n` is required);
  - printable ASCII (U+0020–U+007E except `"` and `\`) is never escaped;
  - `/` is not escaped.
  Equal strings therefore have equal bytes; `\u001A` vs `\u001a` cannot
  both occur.
- **list:** `{"$type":"list","of":"<t>","items":[...]}` — order preserved.
- **set:** `{"$type":"set","of":"<t>","items":[...]}` — sorted by canonical
  bytes; a set value with duplicates has no canonical form.
- **option:** `{"$type":"option","of":"<t>","some":true,"value":<canonical>}`
  / `{"$type":"option","of":"<t>","some":false}`.
- **record:** `{"$type":"record","fields":{…}}` — keys sorted bytewise;
  field values canonically encoded (aliases transparent).
- **impl (D-018):** `{"$type":"impl","sig":"<canonical type name>",
  "value":"<external descriptor>"}` — the signature distinguishes
  same-descriptor implementations of different types.
- **function values (D-018):** **not encodable in v0** — named `FunDef`s are
  definitions, not first-class values; a function-typed value reaching the
  canonicalizer is a packaging failure (`output-not-encodable`).
- **hash:** `{"$type":"hash","value":"<64 lowercase hex>"}`.
- **blob:** `{"$type":"blob","sha256":"<64 hex>","bytes":<nat>}`.

Canonical type names `<t>` (D-027 — exact grammar, no whitespace anywhere):
`nat | int | real | rat | f64 | bool | string | hash`
`list<` t `>`, `set<` t `>`, `option<` t `>`,
`record{` f `:` t (`,` f `:` t)* `}` with fields sorted bytewise by field
name, `impl(` t `->` t `)`, function types `(` t (`,` t)* `)->` t.
Field names are raw idents. (NEW-B3: the v0.8 draft showed spaced forms
like `impl(nat -> nat)` alongside "no whitespace" — the spaceless form is
normative.)

**Injectivity argument.** By structural induction on (type, value): the
`$type` tag distinguishes kinds (`list`≠`set`, `f64` finite vs `inf`);
`of`/`fields`/`sig` distinguish types within kinds; value strings are
canonical per type (unique binary64 grammar, reduced fractions, sorted
keys/items, deterministic string escapes). Distinct (type, value) pairs
→ distinct bytes. v0.6 counterexamples now rejected or distinguished as
shown above; the v0.7 `p-0` survivor is rejected.

**Envelope (D-027 — exact).** Every canonical value is a JSON object whose
first field is exactly `"$type"`, followed by the remaining fields in the
order listed for that tag above (`value`; `of`,`items`; `of`,`some`,`value`;
`fields`; `sig`,`value`; `sha256`,`bytes`). No other fields; no missing
fields (`option` with `some:false` omits `value`). UTF-8; no insignificant
whitespace; the deterministic string escaping above. Digest: SHA-256 over
exact bytes. Profile id recorded per package.

**Packaging failure (D-019 status model, NEW-B7).** A value with no canonical
form (NaN, function value) reaching packaging is **not** INVALID_INPUT —
the input specification was valid. It is reported jointly as
`output_packaging = PACKAGING_FAILED(output-not-encodable: <type>)` **and**
`execution = INTERNAL_ERROR` with reason `output-not-encodable: <type>`,
the established `semantic_result` still recorded (§E.7 inv. 10, inv. 15b).
The `": <detail>"` suffix convention of §B.9 applies to `PackagingError`
codes (`is_packaging_error` checks the base code before `": "`).
(NEW-B7: the v0.8 draft described the event in two places with no rule
relating the two fields.)

### G.3 Result package contents

Result record (§E.1) + spec identity/version/hash; canonicalized input hashes;
exact tool/solver/checker versions + configuration; derivation records,
witnesses, proof artifacts; test inputs, seeds, fuzz conditions; output hashes;
human-reviewed assumption set; failure records and unresolved issues;
supersession records. Failures preserved; re-verification after changes;
superseded, never deleted.

### G.4 Unified maturity vocabulary

1. Designed · 2. Implemented · 3. Functionally verified · 4. Formally verified
(or N/A with recorded reason) · 5. Integrated and reproducible ·
6. Independently reproduced · 7. Released. Sequential 1–3, 5; 4 may be N/A;
6 requires 5; 7 requires all applicable prior stages.

### G.5 Version transition policy

Profile changes → version bump; both hashes recorded during transition; old
hashes never reinterpreted under new rules.

---

## H. Governance

Project owner: approves/revises/rejects design; freezes specs; authorizes repo
creation (after freeze), implementation (separate authorization), release on
evidence. MSVE separate track from research projects and àfi_adaptive. Tool use
grants no modification rights. Genesis rule: the frozen design spec is the
repository's genesis commit — and it must be self-contained (D-011).

---

## I. Acceptance plan summary

Normative: `MSVE_ACCEPTANCE_PLAN_v0.8.md`. End-to-end: parse/validate frozen
spec; assess selector + validator contracts; establish L1 (three claims
separate; decoder-conditional); identify L2 method per claim or mark
unavailable; run L3 if authorized (corpora per §6; ledger regression cases);
emit §E.1 result record + evidence package; assess marginal value vs the Order
7 panel. Slice proposed until separately authorized; generation out of scope.

---

## J. Release gates (unified vocabulary)

1. Designed · 2. Implemented · 3. Functionally verified · 4. Formally verified
(where applicable; or N/A with reason) · 5. Integrated and reproducible ·
6. Independently reproduced · 7. Released. **Completion rule:** no capability
complete merely because components exist; advertised operations need contract,
tests, failure behaviour, evidence; failures stay visible.

---

## Appendix 1. Glossary (v0.8)

- **Slug / special variable `output` / comparator / abstract selector /
  abstract decoder** — §B.
- **RawInput / DecodeOutcome / ValidationOutcome / ValidationError /
  AdmissionError / UnsupportedReason** — §B.9, §B.11, §B.13, §B.13a.
  (The v0.7 single `ErrorCode` is retired, D-029.)
- **Solver observation / assurance required+bases+achieved+shortfall /
  verification record+summary / canonical profile `msve-canonical-3` /
  maturity** — §E–§G.
- **EVIDENCE_RECORDED** — external evidence ingested with provenance; MSVE
  asserts nothing about its truth.

## Appendix 2. Formal contracts v0.8

*Normative for the acceptance plan. Proposed — frozen before any execution.*

**A2.1 Selector types.** `Candidate`, `CandidateSet`, `RawInput = String` as in
§B.11. Binary64: −0.0→+0.0 at the canonical boundary; NaN/±∞ excluded from
well-formed candidates (decode rejects non-finite scores).

**A2.2 Comparator.** `prefers(a, b)`: higher score; equal scores → lower rank;
equal scores+ranks → smaller UCI (bytewise UTF-8). Output = unique maximal
element.

**A2.3 Uniqueness.** Strict total order ⇒ unique maximum for non-empty
well-formed sets. (L1.)

**A2.4 Membership.** `∃c ∈ C : (output == c)` (whole-record structural equality,
§B.4 rule 3).

**A2.5 Validator pipeline.** Three stages:
1. **Decode** (`decode_candidates`, §B.13): raw string → `DecodeOutcome`
   (typed candidates or a named closed error code; deterministic priority;
   `DecodeOutcome` invariant).
2. **Validate** (`validate`, §B.11): decoded candidates → `ValidationOutcome`
   (non-empty, uci shape, duplicate ucis; fixed priority).
3. **Contract** (`validator_contract`, §B.11): implementation outcome must
   equal `rejected(e)` with `is_validation_error(e)` **and**
   `len(d.candidates) == 0` on decode failure (D-028), else
   `validate(decoded)` — accepted data exactly equals decoded input.

**A2.6 Numeric semantics.** Canonicalized binary64, exact comparison, no
tolerance; ranking use only. Mixed Nat/Int via the exact embedding (§B.4
rule 2). `Real` = exact rationals; `to_rat` total.

**A2.7 Determinism.** Selector: pure function of the candidate set. Validator:
pure function of the raw input.

**A2.8 Historical comparison.** Matches the preserved Order 7 adapter for the
selector; validator edge-case rules are new proposals, not historical facts.

## Appendix 3. Unresolved design decisions

Lean version + proof-carrying interface; full problem-class catalog; per-class
resource defaults; generator-class widening; signed-tag key management;
whether `Real` should eventually denote true reals (v0: exact rationals with
exact payloads — the tag reserves the extension).

*End of MSVE_DESIGN_SPEC_v0.8.md (draft for review — not frozen).*
