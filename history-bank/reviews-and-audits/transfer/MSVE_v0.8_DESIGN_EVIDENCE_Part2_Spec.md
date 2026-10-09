# Report B — Design Evidence — Specification (Part 2/3)

**Work Order:** 0.8.2 · **Source file:** `six-docs/MSVE_DESIGN_SPEC_v0.8.md` (DIRECT ARTEFACT, sha256 `377e106ef2b00db6…`)

Complete original text, unmodified. Part 2 of 3 (continued). CONTINUED in next part.

---


### B.7 Verification policy, assurance syntax, duplicates (D-021, D-024)

```
AssuranceReq := "assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")
```

- At most one `assurance:` item; default when absent: `none` (recorded).
- **Goal-specific admission:**
  - `prove` + `level-a required` → requires `proof: kernel-checked by <id> required`.
  - `derive` + `level-a required` → requires `proof: kernel-checked … required`
    **or** `recompute: by <id> required`.
  - `construct` / `compare-models` / `check` + `level-a required` →
    INVALID_INPUT(assurance-level-unavailable).
  - `level-a required` with `proof: none` and `recompute: none` (or absent)
    and no eligible alternative → INVALID_INPUT(conflicting-assurance-requirements).
- `level-b accepted` records explicit acceptance of solver-backed or test-backed
  conclusions with labelling (§E.4). A Level B conclusion may be reported
  **only** when the frozen spec contains this item (§E.7 invariant 12).
- **D-021 separation.** `proof:` carries formal proof evidence only
  (`kernel-checked`). Independent recomputation is a **separate verification
  item** (`recompute:`), not a kind of proof — the grammar keeps the
  categories distinct even though the assurance policy admits recomputation
  as Level A evidence for exact-arithmetic derivations (§D.6).
- **D-024 duplicate rule (normative).** Two verification items are duplicates
  iff they have the same item kind **and** the same method: two `proof:`
  items with the same mode; two `recompute:` items with the same mode; two
  `test: differential …` items; two `test: property-fuzz …` items; two
  `assurance:` items. Checker-ID differences do not distinguish.
  `test: differential …` + `test: property-fuzz …` are **not** duplicates
  (different methods) — the §B.11 selector example is legal. Duplicates →
  INVALID_INPUT(duplicate-verification-item).
- **D-031 duplicates vs conflicts (normative).** A *duplicate* repeats the
  same requirement; a *conflict* declares two incompatible requirements
  for the same kind. They are different errors:
  - `proof:`: at most one item. `proof: none` + `proof: kernel-checked …` →
    INVALID_INPUT(conflicting-verification-requirements). Two
    `kernel-checked` with different checkers → conflicting; with the same
    checker → duplicate-verification-item.
  - `recompute:`: at most one item; same none/active and active/active
    rules as `proof:`.
  - `test:`: several items allowed **iff** their methods differ
    (`none` | `differential` | `property-fuzz`). Same method twice →
    duplicate-verification-item. `test: none` together with any active
    test → conflicting-verification-requirements.
  - `assurance:`: at most one item. `assurance: none` + an active level →
    conflicting-verification-requirements. Two different active levels →
    conflicting-verification-requirements.
  - **Qualifier default:** an omitted `required`/`optional` qualifier
    means `required`. (M8 applies this default.)
- Required-but-unrunnable → shortfall handling (§E.1); optional-but-unrunnable →
  recorded as skipped.

### B.8 Resource limits

`timeout` mandatory (missing → INVALID_INPUT(missing-mandatory-timeout)); range
1s…24h (outside → INVALID_INPUT(timeout-out-of-range)). `steps: 0` →
INVALID_INPUT(degenerate-resource-limit). `cases: 0` in a fuzz config →
INVALID_INPUT(degenerate-fuzz-config). `memory`/`steps` optional, combinable.

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

### B.10 Natural-language handling (hard rule)

NL drafts candidates under human supervision. Unreviewed NL-extracted
assumptions NEVER enter executable specifications. Review artifacts only.

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
### B.12 Invalid examples

Admission-level rejections (prose list; codes per the §B.9 three-type model):

1. Natural-language paragraph → INVALID_INPUT(not-a-formal-specification).
2. `goal compare-models M satisfying [two_vals]` (no `under`) →
   INVALID_INPUT(missing-required-projection).
3. `goal prove P assuming [ghost_asm]` →
   INVALID_INPUT(unbound-assumption-reference: ghost_asm).
4. No `limits` → INVALID_INPUT(missing-mandatory-timeout).
5. Two `define foo` → INVALID_INPUT(duplicate-definition: foo).
6. `require r: output.zzz == 1` → INVALID_INPUT(type-mismatch…).
7. `define output: Nat = 3` → INVALID_INPUT(reserved-context-name: output).
8. `define accepted: …` → INVALID_INPUT(reserved-keyword-misuse: accepted):
   definition names must not be reserved keywords (M8 found this in v0.7).
9. `assurance: level-a required` on `compare-models` →
   INVALID_INPUT(assurance-level-unavailable).
10. `assurance: level-a required` with `proof: none; recompute: none` on a
    `derive` goal → INVALID_INPUT(conflicting-assurance-requirements).
11. Non-NFC string in a hashed artifact → INVALID_INPUT(string-not-normalized).
12. `test: property-fuzz { seeds: [1], cases: 0 }` →
    INVALID_INPUT(degenerate-fuzz-config).
13. `goal check contract_holds of selector_impl` with `test: none` only →
    admission ACCEPTED; at execution, empty corpus →
    INCONCLUSIVE(NO_TEST_CORPUS) (never vacuous HOLDS).
14. Two `test: differential by …` items → INVALID_INPUT(duplicate-verification-item);
    but `test: differential …` + `test: property-fuzz …` is legal (D-024).
15. `proof: none` + `proof: kernel-checked …` →
    INVALID_INPUT(conflicting-verification-requirements) (D-031: conflict,
    not duplicate).
16. `proof: independent-recompute by x/1.0.0` → INVALID_INPUT(syntax-error):
    recomputation is a `recompute:` item, not a `proof:` alternative (D-021).

Machine-checkable invalid examples (each carries a `// INVALID: <category>`
marker; `python3 -m m8.cli spec-examples` verifies M8 rejects each with the
marked category):

**Bare quantifier body (D-005: parens mandatory):**
```
// INVALID: syntax
spec inv-bare-quant
version 0.8.0
scope m8-corpus
authors ["m8"]
define p : Bool = forall x in type Nat :: x >= 0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all
```

**Mixed Real + Nat (D-007: no embedding):**
```
// INVALID: type
spec inv-mixed-arith
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Real = 1.5 + 2
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all
```

**Unbound identifier (D-016):**
```
// INVALID: name-resolution
spec inv-unbound
version 0.8.0
scope m8-corpus
authors ["m8"]
define b : Bool = frobnicate(1)
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all
```

**proof: none + proof: kernel-checked (D-031: conflict):**
```
// INVALID: admission
spec inv-proof-conflict
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  proof: kernel-checked by lean-kernel/4.9.0 required;
}
limits { timeout: 10s; }
record: all
```

**Binary64 p-0 exponent (D-026):**
```
// INVALID: lexical
spec inv-f64-negzero
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Binary64 = 0x1.0000000000000p-0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all
```
## C. Supported problem classes

Matrix (`MSVE_CAPABILITY_MATRIX_v0.8.md`) normative. v0 targets (all Designed):
exact integer/rational arithmetic (D-007 model); SymPy-backed symbolic
computation within stated limits; decidable-fragment constraint solving;
restricted general SMT (unknown → INCONCLUSIVE(SOLVER_UNKNOWN)); model
construction/witnesses; uniqueness checking via §D; Lean-kernel proof checking
(formalization human-reviewed); L1/L2/L3 assurance (§D.1); generation restricted
to §D.5. `Real` denotes exact rationals in v0 with exact rational payloads
(§G.2); `Rat` is the lowest-terms rational type; `to_rat: Real -> Rat` is total.
FORBIDDEN: inferred historical data, NL direct execution, silent gap-filling,
unreviewed-spec execution. OUT OF SCOPE: performance prediction, objective
invention, arbitrary discovery.

---

## D. Assurance levels, uniqueness, generation, evidence taxonomy

### D.1 Three assurance levels

- **L1 — Mathematical model.** Abstract-algorithm properties by proof or sound
  procedure. For the validator: proved over the abstract decoder+validator
  covering the full `RawInput` domain by structural case analysis on the
  §B.13 table — conditional on the table's semantics (D-012).
- **L2 — Implementation conformance.** Named method per claim. L1 alone proves
  nothing about code. Three claims stay separate: (a) abstract model correct,
  (b) implementation conforms, (c) bounded tests found no failures in the
  cases tested; (c) never substitutes for (b).
- **L3 — Tested behaviour.** Corpus-bound per §B.5b (empty corpus →
  INCONCLUSIVE(NO_TEST_CORPUS)).

### D.2 Uniqueness decision procedure

Satisfiability → else CONTRADICTION (assurance §E.4). Declared projection on
the explicit model type (absent → INVALID_INPUT). Second-model query with exact
inequality on canonical forms; re-solve. Second model → UNDERDETERMINED with
witnesses. UNIQUE_UNDER_PROJECTION only if query UNSAT and procedure complete;
record procedure, guarantees, assurance (Level B in v0 for solver-backed
classes). Else INCONCLUSIVE with reason code.

### D.3–D.4

Exact projection equality (transitive); no tolerance equivalence.
Uniqueness-restoring assumptions: user-supplied or declared-finite-family only;
sufficient ≠ justified.

### D.5 v0 generator class

Structural-recursion templates over finite lists/collections; permitted element
types; fixed reviewed template; termination by construction; operation
contracts as L1 obligations; output re-checked (L2). Finite collection ≠ finite
domain ≠ unbounded class of finite collections. **Generation out of scope for
the first selector vertical slice.**

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

## E. Result-record schema (D-015, D-022: closed)

### E.1 Schema (authoritative)

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