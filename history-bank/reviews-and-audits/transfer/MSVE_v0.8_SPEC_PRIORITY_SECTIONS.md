# MSVE v0.8 — Priority Spec Sections for Final-State Verification

**Source:** `six-docs/MSVE_DESIGN_SPEC_v0.8.md` (sha256 `377e106ef2b00db6…`), verbatim extracts. Prepared 2026-10-09 under owner direction to test claimed corrections against the as-built record.

## Final-state verification notes (checked 2026-10-09 against this file)

- **NEW-B1** (exact underflow/overflow thresholds): PRESENT — see §B.4b extract (`|r| ≥ 2^1024 − 2^970`; `|r| < 2^-1075` → ±0; `|r| = 2^-1075` → ±0 ties-to-even; `2^-1075 < |r| < 2^-1074` → min subnormal).
- **NEW-B5** (NaN predicates): PRESENT — §B.4 rule 3 extract (comparisons false except `!=`; ordering false).
- **NEW-B6** (Real/Rat div-by-zero): PRESENT — §B.4 rule 2 (`division-by-zero` execution error).
- **NEW-C1** (`is_admission_error`, `is_unsupported_reason` defines): PRESENT — §B.9 extract (lines 593, 621). This resolves the C-vs-D chronology: Reviewer C inspected a state where the defines were absent (real finding at the time); the defines were added as the NEW-C1 correction; the final spec contains them. Reviewer reports do not record the spec hash inspected, so the interleaving cannot be cryptographically anchored — this is a stated limitation.
- **NEW-B7 / NEW-C3** (joint packaging/execution invariant 15b): PRESENT — §E.7 extract (inv. 15b, line 1208).
- **NEW-C4** (UNIQUE_UNDER_PROJECTION invariant 23): PRESENT — §E.7 extract (inv. 23, line 1232).
- **D-028** (`len(d.candidates) == 0` conjunct): PRESENT — §B.11 contract extract (line 366).
- **NEW-D1** (stale v0.7 normative links): FIXED — the only remaining `v0.7.md` mention is the historical `Supersedes:` line; no normative references to v0.7 companion documents remain.
- **NEW-D2** (ledger D-025 misdescription): ledger now reads 'bare-brace record literal as an `Atom`' with a NEW-D2 self-correction note.
- **NEW-D3** (Diagram 3 stale contract): visualisation plan line 69 now shows `is_validation_error(e)` + `len(candidates)==0`; line 146 states the retired v0.7 `is_error_code` predicate must not appear.


## §B.4b Binary64 operational semantics (spec lines 423–472)

### B.4b Binary64 operational semantics (D-032)

The v0.7 text cited "IEEE 754" as a substitute for semantics; that was
insufficient (it is false for `0.0/0.0`, which yields NaN, not ±infinity).
The v0.8 subset is specified operationally here. This is the semantics
MSVE reasons about; an implementation must conform to exactly this.

- **Rounding:** every arithmetic operation rounds its exact mathematical
  result to the nearest binary64 value, ties to even (round-to-nearest,
  ties-to-even). This applies to `+`, `-`, `*`, `/`.
- **NaN propagation:** if any operand is NaN, the result is NaN (for
  `+`, `-`, `*`, `/`, and unary `-`).
- **Infinities:**
  - `(+inf) + (+inf) = +inf`; `(-inf) + (-inf) = -inf`;
    `(+inf) + (-inf) = NaN`; `(-inf) + (+inf) = NaN`.
  - `(+inf) - (-inf) = +inf`; `(-inf) - (+inf) = -inf`;
    `(+inf) - (+inf) = NaN`; `(-inf) - (-inf) = NaN`.
  - Finite `x`: `x + (+inf) = +inf`; `x + (-inf) = -inf`;
    `x - (+inf) = -inf`; `x - (-inf) = +inf`.
    `(+inf) - x = +inf`; `(-inf) - x = -inf` for finite `x`.
  - `(+inf) * (+inf) = +inf`, `(+inf) * (-inf) = -inf`,
    `(-inf) * (-inf) = +inf` (signs multiply normally).
  - `0 * (±inf) = NaN`; `(±inf) * 0 = NaN`.
  - Finite nonzero `x / (±inf) = ±0` (sign rules); `0 / (±inf) = ±0`;
    `(±inf) / (±inf) = NaN`;
    `(±inf) / 0 = ±inf` (sign rules); `(±inf) / finite-nonzero = ±inf`.
- **Division by zero (finite operands):**
  - `x / +0 = +inf` for finite `x > 0`; `= -inf` for finite `x < 0`.
  - `x / -0 = -inf` for finite `x > 0`; `= +inf` for finite `x < 0`.
  - **`0.0 / 0.0 = NaN`** (any zero signs); `±0 / ±0 = NaN`.
- **Overflow:** the exact result `r` overflows to ±infinity (sign of `r`)
  iff `|r| ≥ 2^1024 − 2^970` (the round-to-nearest-even threshold; values
  below it round to the maximum finite binary64 `0x1.fffffffffffffp+1023`).
- **Underflow:** let `r` be the exact nonzero result. `|r| < 2^-1075`
  rounds to ±0 (sign of `r`); `|r| = 2^-1075` rounds to ±0 (ties-to-even,
  zero being the even choice); `2^-1075 < |r| < 2^-1074` rounds to the
  minimum subnormal `±2^-1074`; magnitudes in `[2^-1074, 2^-1022)` round
  to subnormals. (NEW-B1: the v0.8 draft's "magnitude < 2^-1074 rounds
  to ±0" was false — e.g. `3/4 × 2^-1074` rounds to the min subnormal.)
- **Signed zero:** `+0 + +0 = +0`; `-0 + -0 = -0`; `+0 + -0 = +0`
  (round-to-nearest); `x + (-x) = +0` for finite `x` (including `x = ±0`
  with opposite signs); `(-0) * x` has the opposite sign of `(+0) * x`
  (sign rules: `(-0) * (+3.0) = -0`, `(-0) * (-3.0) = +0`).
- **Negation:** `-x` flips the sign bit, including `-(-0.0) = +0.0`,
  `-(+inf) = -inf`, `-NaN = NaN`.
- **Alignment with packaging:** `-0.0` produced by computation normalizes
  to `+0` at canonicalization (§G.2); NaN has no canonical form and
  triggers the packaging-failure outcome (§E.7 inv. 10), never
  INVALID_INPUT.


## §B.9 Admission and error model (spec lines 568–639)

### B.9 Admission and error model (D-029: three closed types)

The v0.7 single-`ErrorCode` model is retired: it could not name admission
and unsupported outcomes while claiming closure. v0.8 uses three closed
types. Each is `String` with a normative closure predicate (a disjunction
over string literals, as in §B.13a). A code may carry a detail suffix
`": <detail>"` (e.g. ``unbound-identifier: foo``); the predicate checks
the base code before `": "`, the detail is free text.

**`AdmissionError`** — reasons for `INVALID_INPUT` (admission failures).
`is_admission_error` covers exactly:
`not-a-formal-specification`, `missing-header-field`, `syntax-error`,
`unbound-identifier`, `duplicate-definition`, `reserved-context-name`,
`reserved-keyword-misuse`, `type-mismatch`, `arity-mismatch`,
`unknown-builtin`, `unsupported-quantifier-domain`,
`undefined-nonterminal`, `missing-required-projection`,
`projection-path-unresolvable`, `unbound-assumption-reference`,
`missing-mandatory-timeout`, `timeout-out-of-range`,
`degenerate-resource-limit`, `degenerate-fuzz-config`,
`duplicate-verification-item`, `conflicting-verification-requirements`,
`conflicting-assurance-requirements`, `assurance-level-unavailable`,
`missing-goal`, `string-not-normalized`, `memory-limit-exceeded`,
`unsupported-target`. (27 codes.)

```
define is_admission_error(e: AdmissionError): Bool =
  (e == "not-a-formal-specification") \/ (e == "missing-header-field") \/
  (e == "syntax-error") \/ (e == "unbound-identifier") \/
  (e == "duplicate-definition") \/ (e == "reserved-context-name") \/
  (e == "reserved-keyword-misuse") \/ (e == "type-mismatch") \/
  (e == "arity-mismatch") \/ (e == "unknown-builtin") \/
  (e == "unsupported-quantifier-domain") \/ (e == "undefined-nonterminal") \/
  (e == "missing-required-projection") \/
  (e == "projection-path-unresolvable") \/
  (e == "unbound-assumption-reference") \/
  (e == "missing-mandatory-timeout") \/ (e == "timeout-out-of-range") \/
  (e == "degenerate-resource-limit") \/ (e == "degenerate-fuzz-config") \/
  (e == "duplicate-verification-item") \/
  (e == "conflicting-verification-requirements") \/
  (e == "conflicting-assurance-requirements") \/
  (e == "assurance-level-unavailable") \/ (e == "missing-goal") \/
  (e == "string-not-normalized") \/ (e == "memory-limit-exceeded") \/
  (e == "unsupported-target")
```
(NEW-C1: the v0.8 draft stated the closure predicate normatively but
never wrote it; the 27 disjuncts above are exactly the prose list.)

**`UnsupportedReason`** — reasons for `UNSUPPORTED` (in-scope but not
supported in v0). `is_unsupported_reason` covers exactly:
`scope-not-supported`, `goal-not-supported`,
`construct-not-decidable-for-proof`. (3 codes.)

```
define is_unsupported_reason(e: UnsupportedReason): Bool =
  (e == "scope-not-supported") \/ (e == "goal-not-supported") \/
  (e == "construct-not-decidable-for-proof")
```
(NEW-C1: as above.)

**`ValidationError`** — decoder/validator failures (the §B.13 table +
`validate`). `is_validation_error` covers exactly the 12 codes of §B.13a:
`malformed-json`, `invalid-top-level`, `invalid-element`, `duplicate-key`,
`missing-field`, `unexpected-field`, `invalid-field-type`, `invalid-rank`,
`invalid-score`, `empty-candidate-set`, `invalid-uci`, `duplicate-uci`.

`ResultRecord.admission: ACCEPTED | INVALID_INPUT(reason: AdmissionError)
| UNSUPPORTED(reason: UnsupportedReason)`. The validator contract uses
`ValidationError` only. No field may carry a code from another domain —
M8's corpus and the §E.7 invariants enforce the partition
(`is_validation_error` in the validator contract; admission codes only in
`INVALID_INPUT`; unsupported codes only in `UNSUPPORTED`).


## §B.11 Valid examples (validator contract) (spec lines 645–815)

### B.11 Valid examples

Every example below passes M8 parse + name-resolution + type-check
(`python3 -m m8.cli spec-examples`). The record literals in the
validator example parse under the D-025 production; without it M8
reproduces the B-01 syntax failure (see `m8/runs/`).

**derive (recomputation as its own item, D-021):**
```
spec derive-level-a
version 0.8.0
scope exact-arithmetic
authors ["example"]
goal derive (2 * 21) + 1
verification { proof: none; recompute: by recompute-checker/1.0.0 required; assurance: level-a required; }
limits { timeout: 10s; }
record: all
```

**construct with output-bound constraints (§B.5a):**
```
spec tiny-construct
version 0.8.0
scope finite-search
authors ["example"]
type Pair = { x: Nat, y: Nat }
constraints positive {
  require px: output.x > 0;
  require py: output.y > 0;
}
goal construct Pair satisfying [positive]
verification { proof: none; test: none; assurance: none; }
limits { timeout: 10s; }
record: all
```

**prove with kernel-checked proof (Level A admission):**
```
spec tiny-prove
version 0.8.0
scope kernel-proofs
authors ["example"]
axiom add_zero: forall n in type Nat :: (n + 0 == n)
goal prove forall n in type Nat :: (n + 0 == n) assuming [add_zero]
verification { proof: kernel-checked by lean-kernel/4.9.0 required; assurance: level-a required; }
limits { timeout: 60s; }
record: all
```

**selector contract: three-stage validation, differential + property-fuzz (D-024):**
```
spec selector-contract
version 0.8.0
scope finite-total-order-selection
authors ["MSVE design team"]

type Candidate = { uci: String, rank: Nat, score: Binary64 }
type CandidateSet = [Candidate]
type RawInput = String

define prefers(a: Candidate, b: Candidate): Bool =
  (a.score > b.score) \/
  ((a.score == b.score) /\ (a.rank < b.rank)) \/
  ((a.score == b.score) /\ (a.rank == b.rank) /\ (a.uci < b.uci))

define is_wellformed(cs: CandidateSet): Bool =
  (len(cs) > 0) /\
  (forall c in cs :: ((c.uci != "") /\ is_ascii_printable(c.uci) /\ has_no_whitespace(c.uci))) /\
  (forall i in range(len(cs)) :: (forall j in range(len(cs)) :: (((i == j) \/ (cs[i].uci != cs[j].uci))))) /\
  (forall c in cs :: (is_finite(c.score)))

define contract_holds(candidates: CandidateSet, sel: Candidate): Bool =
  is_wellformed(candidates) /\
  (exists c in candidates :: (sel == c)) /\
  (forall c in candidates :: ((prefers(sel, c) \/ (sel == c))))

define selector_impl: Impl(CandidateSet -> Candidate) = external("selector-impl/0.8.0")
define indie_ref_impl: Impl(CandidateSet -> Candidate) = external("independent-ref-impl/0.8.0")

goal check contract_holds of selector_impl

verification {
  proof: none;
  test: differential by indie-ref-impl/0.8.0 required;
  test: property-fuzz { seeds: [1, 2, 3], cases: 10000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; memory: 2GB; }
record: all
```

**compare-models with projection:**
```
spec tiny-models
version 0.8.0
scope finite-constraint-models
authors ["example"]
type M = { x: Nat }
constraints two_vals {
  require xv: (output.x == 1) \/ (output.x == 2);
}
projection xproj = [output.x]
goal compare-models M satisfying [two_vals] under xproj
verification { proof: none; test: none; assurance: level-b accepted; }
limits { timeout: 10s; }
record: all
```

**validator contract (D-025 record literals; D-028 decoder-failure conjunct; D-029 ValidationError):**
```
spec validator-contract-check
version 0.8.0
scope input-validation
authors ["MSVE design team"]

type Candidate = { uci: String, rank: Nat, score: Binary64 }
type CandidateSet = [Candidate]
type RawInput = String
type ValidationError = String
type DecodeOutcome = { ok: Bool, candidates: [Candidate], error: Option<ValidationError> }
type ValidationOutcome = { accepted: Bool, candidates: Option<CandidateSet>, error: Option<ValidationError> }

define ERR_EMPTY_SET: ValidationError = "empty-candidate-set"
define ERR_INVALID_UCI: ValidationError = "invalid-uci"
define ERR_DUPLICATE_UCI: ValidationError = "duplicate-uci"

define is_validation_error(e: ValidationError): Bool =
  (e == "malformed-json") \/ (e == "invalid-top-level") \/
  (e == "invalid-element") \/ (e == "duplicate-key") \/
  (e == "missing-field") \/ (e == "unexpected-field") \/
  (e == "invalid-field-type") \/ (e == "invalid-rank") \/
  (e == "invalid-score") \/ (e == "empty-candidate-set") \/
  (e == "invalid-uci") \/ (e == "duplicate-uci")

define valid_uci(u: String): Bool =
  (u != "") /\ is_ascii_printable(u) /\ has_no_whitespace(u)

define has_dup_uci(cs: [Candidate]): Bool =
  exists i in range(len(cs)) :: (exists j in range(len(cs)) :: (((i != j) /\ (cs[i].uci == cs[j].uci))))

define rejected(e: ValidationError): ValidationOutcome =
  { accepted: false, candidates: none, error: some(e) }

define accept(cs: CandidateSet): ValidationOutcome =
  { accepted: true, candidates: some(cs), error: none }

define validate(cs: [Candidate]): ValidationOutcome =
  if len(cs) == 0 then rejected(ERR_EMPTY_SET)
  else if exists c in cs :: ((!(valid_uci(c.uci)))) then rejected(ERR_INVALID_UCI)
  else if has_dup_uci(cs) then rejected(ERR_DUPLICATE_UCI)
  else accept(cs)

define validator_contract(raw: RawInput, out: ValidationOutcome): Bool =
  let d = decode_candidates(raw) in
  ((d.ok ==> ((!(is_some(d.error))) /\ (out == validate(d.candidates)))) /\
  ((!(d.ok)) ==> (is_some(d.error) /\
    (len(d.candidates) == 0) /\
    (case d.error of some(e) -> ((is_validation_error(e)) /\ (out == rejected(e))) | none -> false))))

define validator_impl: Impl(RawInput -> ValidationOutcome) = external("validator-impl/0.8.0")

goal check validator_contract of validator_impl

verification {
  proof: none;
  test: property-fuzz { seeds: [7, 8], cases: 5000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; }
record: all
```

## §E.7 Cross-field invariants (spec lines 1169–1281)

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


## §G.2 Canonical encoding profile (spec lines 1282–1404)

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


## §B.4 rules 1–5 (NaN predicates, div-by-zero) (spec lines 255–310)

### B.4 Type system and type-checking rules

Base types: `String Nat Int Real Rat Binary64 Bool`. Records, lists, sets,
options, `Impl(A -> B)`, function types.

1. Every `Expr` has a unique type. Literals: strings→`String`; digits→`Nat`;
   `RealLit`→`Real` (exact decimal value); `HexFloat`→`Binary64` (the
   canonical spelling, §G.2); `true/false`→`Bool`;
   `"none"`→`Option<T>` (T from context, else type error).
2. **Arithmetic.** `+ - *`:
   - Same-type operands: `Nat`/`Int`/`Real`/`Rat`/`Binary64` with matching types.
   - **Mixed `Nat`/`Int`:** the one explicit exact embedding — the `Nat`
     operand is treated as `Int`; result `Int`. The only permitted
     cross-type arithmetic; all other mixed-type arithmetic → type error.
   - `/`: same-type operands; `Nat`/`Int` division is **exact division** —
     a non-exact quotient is an execution error (`INTERNAL_ERROR`, reason
     `inexact-division`); division by zero is an execution error
     (`division-by-zero`). `Real`/`Rat` division is exact rational division;
     division by a zero rational is an execution error (`division-by-zero`,
     NEW-B6 — the v0.8 draft left this case undefined).
     `Binary64` division follows the operational semantics of §B.4b
     (D-032) — in particular `0.0/0.0 → NaN`, not ±infinity.
   - **2a. Unary minus:** `-e` well-typed iff `e: Nat|Int|Real|Rat|Binary64`;
     result: `Nat→Int`, `Int→Int`, `Real→Real`, `Rat→Rat`,
     `Binary64→Binary64` (negation per §B.4b; canonicalization applies §G.2).
     `-5` denotes `Int(-5)`; `-3 + 2 : Int` denotes `-1`.
   - `!e` requires `Bool`.
3. **Equality (D-016).** `==`/`!=` require the same type; equality is
   structural, defined recursively:
   - base types: value equality (`Binary64`: equality of canonical forms,
     with the NaN exception below; `Real`/`Rat`: exact rational equality);
   - records: same fields, pairwise equal;
   - lists: same length, pairwise equal in order;
   - options: `none == none`; `some(a) == some(b)` iff `a == b`;
     `some(_) != none`;
   - sets: equality as sets (order-insensitive), defined via the canonical
     form. (NEW-A9: `Set` is reserved for future use in v0 — it has no
     introduction form in surface syntax and cannot be written in a v0
     `TypeExpr`. The equality rule and the canonical `set` envelope are
     retained for the future extension.)
   - `Impl` handles: equality of (descriptor, signature) pairs.
   Ordering `< <= > >=`: `Nat Int Real Rat Binary64 String`.
   **NaN predicates (NEW-B5):** NaN has no canonical form, so comparisons
   involving NaN follow IEEE-style rules explicitly: `NaN == x` and
   `x == NaN` are `false` (including `NaN == NaN`); `NaN != x` and
   `x != NaN` are `true`; `NaN < x`, `NaN <= x`, `NaN > x`, `NaN >= x`
   (and mirrored) are all `false`. `is_finite`/`is_nan` builtins let
   authors guard. (The v0.8 draft left these undefined.)
4. `String` ordering: bytewise lexicographic over UTF-8 (§B.4a).
5. Boolean connectives on `Bool`. `==>` is **classical implication**;
   its meaning never depends on evaluation order.
6. `if`: `Bool` condition, equal branch types. `let x = e1 in e2`: `e1: T1`,
   `e2: U` under `x: T1`; result `U`.
7. `case e of some(x) -> e1 | none -> e2`: `e: Option<T>`; `e1: U` under
   `x: T`; `e2: U`; result `U`. The total option eliminator.
   `some(e: T): Option<T>` (constructor syntax).