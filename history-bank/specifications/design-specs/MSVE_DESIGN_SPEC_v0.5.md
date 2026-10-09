# MSVE Design Specification v0.5

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.4.md` (retained as historical draft)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MUSE WORK ORDER 0.4 (narrow correction pass) · **Review authority:** Project owner
**Version:** 0.5 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

Change summary: v0.5 repairs the seven freeze-blocking defects found in the v0.4
review (see `MSVE_DESIGN_REVIEW_v0.5.md`). Each was verified against the v0.4 text
before correction:
1. `Esc` undefined; no `Int`/`Real`/`Binary64` literal syntax; unary-minus typing
   undefined under no-implicit-promotion.
2. `compare-models` had no model type; `output`'s typing rule was vacuous for it.
3. No `RawInput` or validation-result type; invalid inputs were fuzzed against
   the selector contract instead of the validator.
4. Empty test corpora could yield vacuous HOLDS.
5. Level A admission contradicted the derivation policy (kernel-proof demand vs
   independent-recomputation eligibility).
6. Canonical profile missed sets/options/records/bools/strings as first-class
   encodings; `Real`'s place in hashed artifacts unexplained.
7. `EvidenceBundle`, `PartialResult`, `Discrepancy`, `ErrorCode`,
   `SemanticResult` referenced but not structurally defined.
Plus the mathematical correction: validator universality claims separated into
three claims (abstract correctness / implementation conformance / bounded tests).

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*: domain-agnostic within the formal scope
defined by the input language (§B) and the capability matrix
(`MSVE_CAPABILITY_MATRIX_v0.5.md`). Outside the declared scope: UNSUPPORTED.

### A.2–A.5

Intended users, the three non-eliminable judgments, the scope-qualified
"all-rounder" definition, and the explicit non-goals are unchanged from v0.4
(§A.2–§A.5). The capability matrix remains normative for the "all-rounder" claim.

---

## B. Formal input language (complete v0 definition, corrected)

### B.1 Design rules

1. Minimal, machine-readable; natural language never drives execution (§B.12).
2. Specifications carry identity and version; frozen specifications are immutable
   content-hashed baselines.
3. This section is the **complete normative syntax**. §B.11 gives valid examples;
   §B.12 gives invalid examples with exact rejection reasons. The review records
   the mechanical checks performed (nonterminal closure, per-token derivation).

### B.2 Lexical rules

```
Ident     := [A-Za-z_][A-Za-z0-9_]*
Slug      := [A-Za-z0-9_]+(-[A-Za-z0-9_]+)*
String    := '"' ( [^"\\\u0000-\u001F] | Esc )* '"'
Esc       := "\\" ( "\"" | "\\" | "/" | "b" | "f" | "n" | "r" | "t"
                   | "u" Hex Hex Hex Hex )
Hex       := [0-9a-fA-F]
Nat       := [0-9]+
RealLit   := Nat "." Nat                       # exact decimal, e.g. 3.14
SemVer    := Nat "." Nat "." Nat
Duration  := Nat ("ms" | "s" | "min" | "h")
MemSize   := Nat ("B" | "KB" | "MB" | "GB")
CheckerID := Slug "/" SemVer
```

Notes (defect 01):
- `Esc` is now defined (JSON string escapes, as above).
- Numeric literals: `Nat` (digits), `RealLit` (exact decimal). There are **no**
  `Int` or `Binary64` literals in v0 — negative integers arise from unary minus
  (§B.4 rule 2a); `Binary64` values arise from computation or external inputs.
  This restriction is explicit, not an oversight.
- Hyphens only in `Slug` (spec/scope/checker names); `Ident` unchanged.

Keywords (reserved): `spec version scope authors type define axiom assume
constraints require forbid projection goal derive construct satisfying prove
assuming check of compare-models under verification proof test none
kernel-checked independent-recompute by differential property-fuzz seeds cases
required optional assurance level-a level-b accepted limits timeout memory
steps record all external spec-hash input-hash tool-versions witness outputs
true false if then else forall exists in type`.

`output` is not a keyword; it is a special context variable (§B.5a).

Whitespace insignificant except in strings. Blocks tolerate trailing `;` (§B.3).
Comments: `//` to end of line.

**Parsing notes.** Quantifier bodies (`forall`/`exists`) extend greedily to the
enclosing delimiter (closing parenthesis, `;`, or block end). `==>` binds
tighter than `/\`, which binds tighter than `\/` (see the Expr chain);
parentheses override.

### B.3 Grammar (EBNF — complete, non-left-recursive)

```
Specification  := Header Body
Header         := "spec" Slug "version" SemVer "scope" Slug
                  "authors" "[" (String ("," String)*)? "]"
Body           := Definition* ConstraintGroup* Projection* Goal
                  Verification ResourceLimits ProvenanceReq

Definition     := TypeAlias | ValueDef | FunDef | AxiomDecl | AssumptionDecl | ExternalDecl
TypeAlias      := "type" Ident "=" TypeExpr
ValueDef       := "define" Ident ":" TypeExpr "=" Expr
FunDef         := "define" Ident "(" Params ")" ":" TypeExpr "=" Expr
Params         := (Ident ":" TypeExpr ("," Ident ":" TypeExpr)*)?
AxiomDecl      := "axiom" Ident ":" Proposition
AssumptionDecl := "assume" Ident ":" Proposition
ExternalDecl   := "define" Ident ":" ImplType "=" "external" "(" String ")"

ConstraintGroup:= "constraints" Ident "{" (";" | Constraint ";")* "}"
Constraint     := "require" Ident ":" Predicate | "forbid" Ident ":" Predicate

Projection     := "projection" Ident "=" "[" ProjPath ("," ProjPath)* "]"
ProjPath       := Ident ("." Ident)*

Goal           := "goal" (DeriveGoal | ConstructGoal | ProveGoal | CheckGoal | CompareGoal)
DeriveGoal     := "derive" Expr
ConstructGoal  := "construct" TypeExpr "satisfying" "[" Ident ("," Ident)* "]"
ProveGoal      := "prove" Proposition "assuming" "[" Ident ("," Ident)* "]"
CheckGoal      := "check" Ident "of" Ident
CompareGoal    := "compare-models" TypeExpr "satisfying" "[" Ident ("," Ident)* "]"
                  ("under" Ident)?

Verification   := "verification" "{" (";" | VerifItem ";")* "}"
VerifItem      := ProofReq | TestReq | AssuranceReq
ProofReq       := "proof" ":" ("none"
                   | "kernel-checked" "by" CheckerID Qualifier
                   | "independent-recompute" "by" CheckerID Qualifier)
TestReq        := "test" ":" ("none"
                   | "differential" "by" CheckerID Qualifier
                   | "property-fuzz" FuzzConfig Qualifier)
AssuranceReq   := "assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")
Qualifier      := ("required" | "optional")?            # default: required
FuzzConfig     := "{" "seeds" ":" "[" Nat ("," Nat)* "]" ","
                  "cases" ":" Nat "}"

ResourceLimits := "limits" "{" "timeout" ":" Duration ";"
                   ("memory" ":" MemSize ";")? ("steps" ":" Nat ";")? "}"
ProvenanceReq  := "record" ":" ("all" | "[" ProvItem ("," ProvItem)* "]")
ProvItem       := "spec-hash" | "input-hash" | "tool-versions" | "witness" | "outputs"

TypeExpr       := "String" | "Nat" | "Int" | "Real" | "Binary64" | "Bool"
                | "{" (Ident ":" TypeExpr ("," Ident ":" TypeExpr)*)? "}"
                | "[" TypeExpr "]" | "Set" "<" TypeExpr ">"
                | "Option" "<" TypeExpr ">" | ImplType
                | "(" (TypeExpr ("," TypeExpr)*)? ")" "->" TypeExpr
                | Ident
ImplType       := "Impl" "(" TypeExpr "->" TypeExpr ")"

Expr           := OrExpr
OrExpr         := AndExpr ("\/" AndExpr)*
AndExpr        := ImplExpr ("/\" ImplExpr)*
ImplExpr       := CmpExpr ("==>" CmpExpr)?
CmpExpr        := AddExpr (("==" | "!=" | "<" | "<=" | ">" | ">=") AddExpr)?
AddExpr        := MulExpr (("+" | "-") MulExpr)*
MulExpr        := Unary (("*" | "/") Unary)*
Unary          := ("!" | "-")? Postfix
Postfix        := Atom ("." Ident | "[" Expr "]")*
Atom           := Literal | Ident | Ident "(" (Expr ("," Expr)*)? ")"
                | "(" Expr ")"
                | "if" Proposition "then" Expr "else" Expr
                | "forall" Ident "in" Domain "::" Proposition
                | "exists" Ident "in" Domain "::" Proposition
Domain         := "type" TypeExpr | Expr
Literal        := String | Nat | RealLit | "true" | "false" | "none"
Proposition    := Expr        # required type: Bool
Predicate      := Expr        # required type: Bool
```

### B.4 Type system and type-checking rules

Base types: `String Nat Int Real Binary64 Bool`. Records, lists, sets, options,
`Impl(A -> B)`, function types.

1. Every `Expr` has a unique type. Literals: strings→`String`; digits→`Nat`;
   `RealLit`→`Real` (exact decimal value); `true/false`→`Bool`;
   `"none"`→`Option<T>` (T from context, else type error).
2. Arithmetic `+ - * /`: operands share one numeric type; **no implicit promotion**.
   **2a. Unary minus (defect 01):** `-e` is well-typed iff `e: Nat|Int|Real|Binary64`;
   result type: `Nat→Int`, `Int→Int`, `Real→Real`, `Binary64→Binary64`
   (IEEE negation; artifact canonicalization then applies §G.2 normalization).
   `-` on other types → type error. `!e` requires `Bool`.
3. `== !=`: same type. Ordering `< <= > >=`: `Nat Int Real Binary64 String`.
4. `String` ordering: bytewise lexicographic over UTF-8 (§B.4a).
5. `==` on records: structural equality. On `Binary64`: bitwise equality of
   canonical forms.
6. Boolean connectives on `Bool`. `if`: `Bool` condition, equal branch types.
7. Quantifiers: domain is `type T` (extension, possibly infinite) or a collection
   expression; body `Bool`.
8. `e.f`: record field; `e[i]`: list index (`i: Nat`); chained via Postfix.
9. Application: exact argument-type match. `some(e: T): Option<T>`;
   `is_some: Option<T> -> Bool`; `unwrap: Option<T> -> T` (partial — contracts
   use it only under an `is_some` guard; harness evaluates `==>` with
   short-circuit semantics).
10. Builtins: `len: [T]->Nat`; `range: Nat->[Nat]`; `is_finite: Binary64->Bool`;
    `is_ascii_printable: String->Bool`; `has_no_whitespace: String->Bool`;
    `parses_as_valid: RawInput->Bool` (semantics: Appendix 2 §A2.9 — true iff the
    raw string is a JSON array of candidate objects with correctly typed fields).
11. `external("…")`: opaque `Impl` handle; only usable as a `check` target.

**B.4a String order.** Bytewise lexicographic over UTF-8. NFC-normalized input
required; non-normalized → INVALID_INPUT(string-not-normalized) at admission.
The parser never silently normalizes.

### B.5 Name resolution and special variables

- Flat namespace per specification (types, definitions, axioms, assumptions,
  constraint groups, projections, external handles). Duplicates →
  INVALID_INPUT(duplicate-definition: name). Unresolved →
  INVALID_INPUT(unbound-identifier: name).
- `assuming […]`: names must resolve to `assume`/`axiom` declarations.
- Constraint-group references must name `constraints` groups; projection
  references must name `projection` declarations; projection paths resolve
  against the goal's model type (§B.5a).
- `check f of h`: `f: (In, Out) -> Bool`; `h: Impl(In -> Out)`; types must match.

**B.5a Special variable `output` (defect 02).** In constraint groups referenced
by `construct` goals, `output` is bound to the object under construction, typed
by the goal's explicit target type. In `compare-models` goals, `output` is bound
to the model, typed by the goal's explicit model type (§B.3 `CompareGoal` now
carries `TypeExpr`), and projection paths type-check against that type.
`define output …` → INVALID_INPUT(reserved-context-name). No other positions
bind `output`.

**B.5b Check-goal invocation rule.** For `goal check f of h`,
`f: (In, Out) -> Bool`, `h: Impl(In -> Out)`: the engine determines the input
corpus from the Verification test policy (`differential`: the paired corpus;
`property-fuzz`: the generated corpus of `cases` inputs under `seeds`). For
each input `i`: `o = invoke(h, i)`; evaluate `f(i, o)`. HOLDS iff the corpus is
**non-empty** and every evaluation is true; the first failing `(i, o)` is the
counterexample witness for VIOLATED. An empty effective corpus (no test items,
or all `test: none`) → INCONCLUSIVE(NO_TEST_CORPUS) — never vacuous HOLDS.
Test-based checking is corpus-bound (L3); universal implementation claims need
L2 methods (§D.1).

### B.6 Assumption roles

- **`assume name: P`**: premise; tracked; never checked; adequacy is human judgment.
- **`require`**: must hold of the object; checked.
- **`forbid`**: must not hold; checked.
- **`prove`**: proposition to establish relative to the `assuming` context; PROVED
  names proposition + context.

### B.7 Verification policy and assurance syntax

```
AssuranceReq := "assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")
```

- At most one `assurance:` item; default when absent: `none` (recorded).
- **Goal-specific admission (defect 05):**
  - `prove` + `level-a required` → requires `proof: kernel-checked by <id> required`.
  - `derive` + `level-a required` → requires `proof: kernel-checked … required`
    **or** `proof: independent-recompute by <id> required` (the recomputation
    checker independently re-derives; agreement is the Level A evidence).
  - `construct` / `compare-models` / `check` + `level-a required` →
    INVALID_INPUT(assurance-level-unavailable) — v0 establishes no Level A
    pipeline for solver- or test-backed goals.
  - `level-a required` with `proof: none` and no eligible alternative →
    INVALID_INPUT(conflicting-assurance-requirements).
- `level-b accepted` records explicit acceptance of solver-backed or test-backed
  conclusions with labelling (§E.2–E.9). A Level B contradiction may be reported
  **only** when the frozen spec contains this item.
- Required-but-unrunnable → shortfall handling; optional-but-unrunnable →
  recorded as skipped.

### B.8 Resource limits

`timeout` mandatory (missing → INVALID_INPUT(missing-mandatory-timeout)); range
1s…24h (outside → INVALID_INPUT(timeout-out-of-range)). `steps: 0` →
INVALID_INPUT(degenerate-resource-limit). `cases: 0` in a fuzz config →
INVALID_INPUT(degenerate-fuzz-config). `memory`/`steps` optional, combinable.

### B.9 Admission and error catalog

INVALID_INPUT: `not-a-formal-specification`, `missing-header-field`,
`syntax-error`, `unbound-identifier: <name>`, `duplicate-definition: <name>`,
`reserved-context-name: <name>`, `type-mismatch: expected <T>, found <U>`,
`missing-required-projection`, `unbound-assumption-reference: <name>`,
`missing-mandatory-timeout`, `timeout-out-of-range`, `degenerate-resource-limit`,
`degenerate-fuzz-config`, `duplicate-verification-item`,
`conflicting-verification-requirements`, `conflicting-assurance-requirements`,
`assurance-level-unavailable`, `missing-goal`,
`projection-path-unresolvable: <path>`, `string-not-normalized`,
`real-not-encodable`.
UNSUPPORTED: `scope-not-supported`, `construct-not-decidable-for-proof`.

### B.10 Natural-language handling (hard rule)

NL drafts candidates under human supervision. Unreviewed NL-extracted
assumptions NEVER enter executable specifications. Review artifacts only.

### B.11 Valid examples

**derive** (independent recomputation demonstrating defect 05's fix):
```
spec derive-level-a
version 0.5.0
scope exact-arithmetic
authors ["example"]
goal derive (2 * 21) + 1
verification { proof: independent-recompute by recompute-checker/1.0.0 required; assurance: level-a required; }
limits { timeout: 10s; }
record: all
```

**construct:**
```
spec tiny-construct
version 0.5.0
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

**prove:**
```
spec tiny-prove
version 0.5.0
scope kernel-proofs
authors ["example"]
axiom add_zero: forall n in type Nat :: n + 0 == n
goal prove forall n in type Nat :: n + 0 == n assuming [add_zero]
verification { proof: kernel-checked by lean-kernel/4.9.0 required; assurance: level-a required; }
limits { timeout: 60s; }
record: all
```

**check** (selector; contract in Appendix 2):
```
spec selector-contract
version 0.5.0
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
  (forall c in cs :: (len(c.uci) > 0) /\ is_ascii_printable(c.uci) /\ has_no_whitespace(c.uci)) /\
  (forall i in range(len(cs)) :: forall j in range(len(cs)) ::
    ((i == j) \/ (cs[i].uci != cs[j].uci))) /\
  (forall c in cs :: is_finite(c.score))

define contract_holds(candidates: CandidateSet, sel: Candidate): Bool =
  is_wellformed(candidates) /\
  (exists c in candidates :: sel == c) /\
  (forall c in candidates :: prefers(sel, c) \/ (sel == c))

define selector_impl: Impl(CandidateSet -> Candidate) = external("selector-impl/0.5.0")
define indie_ref_impl: Impl(CandidateSet -> Candidate) = external("independent-ref-impl/0.5.0")

goal check contract_holds of selector_impl

verification {
  proof: none;
  test: differential by indie-ref-impl/0.5.0 required;
  test: property-fuzz { seeds: [1, 2, 3], cases: 10000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; memory: 2GB; }
record: all
```

**compare-models** (defect 02: explicit model type):
```
spec tiny-models
version 0.5.0
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

**validator check** (defect 03: RawInput and validation-result types):
```
spec validator-contract-check
version 0.5.0
scope input-validation
authors ["MSVE design team"]

type Candidate = { uci: String, rank: Nat, score: Binary64 }
type CandidateSet = [Candidate]
type RawInput = String

define is_wellformed(cs: CandidateSet): Bool =
  (len(cs) > 0) /\
  (forall c in cs :: (len(c.uci) > 0) /\ is_ascii_printable(c.uci) /\ has_no_whitespace(c.uci)) /\
  (forall i in range(len(cs)) :: forall j in range(len(cs)) ::
    ((i == j) \/ (cs[i].uci != cs[j].uci))) /\
  (forall c in cs :: is_finite(c.score))

define validator_contract(raw: RawInput, out: Option<CandidateSet>): Bool =
  ((is_some(out) ==> (is_wellformed(unwrap(out)) /\ parses_as_valid(raw))) /\
  ((!is_some(out)) ==> !parses_as_valid(raw)))

define validator_impl: Impl(RawInput -> Option<CandidateSet>) = external("validator-impl/0.5.0")

goal check validator_contract of validator_impl

verification {
  proof: none;
  test: property-fuzz { seeds: [7, 8], cases: 5000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; }
record: all
```
(`parses_as_valid`: builtin, §B.4 rule 10; `==>` short-circuits, so `unwrap`
is never evaluated on `none`.)

### B.12 Invalid examples

1. Natural-language paragraph → INVALID_INPUT(not-a-formal-specification).
2. `goal compare-models M satisfying [two_vals]` (no `under`) →
   INVALID_INPUT(missing-required-projection).
3. `goal prove P assuming [ghost_asm]` →
   INVALID_INPUT(unbound-assumption-reference: ghost_asm).
4. No `limits` → INVALID_INPUT(missing-mandatory-timeout).
5. Two `define foo` → INVALID_INPUT(duplicate-definition: foo).
6. `require r: output.zzz == 1` → INVALID_INPUT(type-mismatch…).
7. `limits { timeout: 10s; steps: 0; }` → INVALID_INPUT(degenerate-resource-limit).
8. `goal check contract_holds of missing_impl` → INVALID_INPUT(unbound-identifier).
9. `define output: Nat = 3` → INVALID_INPUT(reserved-context-name: output).
10. `assurance: level-a required` on `compare-models` →
    INVALID_INPUT(assurance-level-unavailable).
11. `assurance: level-a required` with `proof: none` on a `prove` goal →
    INVALID_INPUT(conflicting-assurance-requirements).
12. Non-NFC string in a hashed artifact → INVALID_INPUT(string-not-normalized).
13. `test: property-fuzz { seeds: [1], cases: 0 }` →
    INVALID_INPUT(degenerate-fuzz-config).
14. `goal check contract_holds of selector_impl` with `test: none` only →
    admission ACCEPTED; at execution, empty corpus →
    INCONCLUSIVE(NO_TEST_CORPUS) (never vacuous HOLDS).

---

## C. Supported problem classes

Matrix (`MSVE_CAPABILITY_MATRIX_v0.5.md`) normative. v0 targets (all Designed):
exact integer/rational arithmetic; SymPy-backed symbolic computation within
stated limits; decidable-fragment constraint solving; restricted general SMT
(unknown → INCONCLUSIVE(SOLVER_UNKNOWN)); model construction/witnesses;
uniqueness checking via §D; Lean-kernel proof checking (formalization
human-reviewed); L1/L2/L3 assurance (§D.1); generation restricted to §D.5.
FORBIDDEN: inferred historical data, NL direct execution, silent gap-filling,
unreviewed-spec execution. OUT OF SCOPE: performance prediction, objective
invention, arbitrary discovery.

---

## D. Assurance levels, uniqueness, generation

### D.1 Three assurance levels

- **L1 — Mathematical model.** Abstract-algorithm properties by proof or sound
  procedure. For the validator: the L1 claim is proved over the abstract
  validator model covering the **full** RawInput domain (see acceptance plan —
  structural case analysis on the validation algorithm, never enumeration).
- **L2 — Implementation conformance.** Named method per claim. L1 alone proves
  nothing about code. The three claims — (a) abstract model correct, (b)
  implementation conforms, (c) bounded tests found no failures — stay separate;
  (c) never substitutes for (b).
- **L3 — Tested behaviour.** Corpus-bound per §B.5b (differential/property-fuzz
  corpora; empty corpus → INCONCLUSIVE(NO_TEST_CORPUS)).

### D.2 Uniqueness decision procedure

Satisfiability → else CONTRADICTION (assurance §E.2–E.9). Declared projection on
the explicit model type (absent → INVALID_INPUT). Second-model query with exact
inequality on canonical forms; re-solve. Second model → UNDERDETERMINED with
witnesses. UNIQUE_UNDER_PROJECTION only if query UNSAT and procedure complete;
record procedure, guarantees, assurance (Level B in v0 for solver-backed
classes). Else INCONCLUSIVE with reason code. For the observation-vs-conclusion
distinction see §E.2–E.9 (solver observation, semantic result, assurance policy).

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

---

## E. Result-record schema (defect 07: fully defined)

### E.1 Schema (authoritative)

```
ResultRecord {
  admission: ACCEPTED | INVALID_INPUT(reason: ErrorCode) | UNSUPPORTED(reason: ErrorCode),
  execution: NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED
             | INTERNAL_ERROR(reason: String),
  semantic_result: Option<SemanticResult>,
  solver_observation: Option<SolverObs>,
  assurance_required: NONE | LEVEL_A | LEVEL_B,
  assurance_achieved: NONE | LEVEL_A | LEVEL_B_SOLVER_BACKED,
  assurance_shortfall: Bool,
  shortfall_description: Option<String>,
  verification_records: [VerificationRecord],
  verification_summary: NOT_RUN | PASS | FAIL | INCONCLUSIVE | CHECKER_DIVERGENCE,
  evidence: EvidenceBundle,
  partial_results: [PartialResult],
  discrepancies: [Discrepancy],
}

ErrorCode := one of the §B.9 catalog strings (closed enumeration).

SemanticResult :=
    DERIVED_VALUE | ARTIFACT_CONSTRUCTED | NO_SOLUTION
  | PROVED | DISPROVED | HOLDS | VIOLATED | UNIQUE_UNDER_PROJECTION
  | UNDERDETERMINED | CONTRADICTION
  | INCONCLUSIVE(reason: ReasonCode)

ReasonCode := SOLVER_UNKNOWN | PROCEDURE_INCOMPLETE | RESOURCE_EXHAUSTED
            | EXECUTION_INTERRUPTED | ASSURANCE_REQUIREMENT_UNMET | NO_TEST_CORPUS

SolverObs := { outcome: SAT | UNSAT | UNKNOWN, tool: String, version: SemVer,
               config: String, provenance_ref: Hash,
               certificate_ref: Option<Hash> }

VerificationRecord := { property: String, artifact: String, spec_version: SemVer,
  method: String, checker: CheckerID, result: PASS | FAIL | INCONCLUSIVE,
  reason: Option<String>, assurance_boundary: String, inputs_ref: Hash }

EvidenceBundle := {
  derivation_records: [ArtifactRef], proof_artifacts: [ArtifactRef],
  witnesses: [ArtifactRef], constructed_artifacts: [ArtifactRef],
  verification_inputs_ref: Hash, external_evidence_records: [ExternalEvidence] }
ArtifactRef := { sha256: Hex, bytes: Nat, media: String, description: String }
ExternalEvidence := { experiment_id: String, method: String,
  data_ref: Hash, recorded_at: String }

PartialResult := { description: String, semantic_fragment: SemanticResult,
  provenance_ref: Hash, labelled_partial: true }
# Validation: present only when execution ∈ {TIMEOUT, INTERRUPTED}.

Discrepancy := { property: String, involved_records: [Nat],
  description: String, required_follow_up: String, status: OPEN | RESOLVED }
# Validation: status may move OPEN → RESOLVED only with a recorded resolution.
```

### E.2–E.9

Semantic results per goal type; INCONCLUSIVE reason codes (now six, incl.
NO_TEST_CORPUS); solver-observation vs conclusion vs assurance (§E.2–E.9: UNSAT rule
with refusal; Level B only on explicit `level-b accepted`); v0 Level A policy
(prove→kernel, derive→kernel-or-recompute; SMT-UNSAT Level A FUTURE);
divergence-first aggregation (DIVERGENCE > FAIL > INCONCLUSIVE > PASS; empty →
NOT_RUN; records always preserved); legal combinations; external-evidence
three-way split; anti-conflation hard rules — all retained from v0.4 with the
§E.1 types above as the single normative reference.

---

## F. Trust base

Orchestration over established components; no new solver in v0. Parser/validator
(MSVE-owned): syntax/typing/mandatory fields — not semantics. SymPy (pinned):
computed / independently checkable / trusted-tool output. Z3 (pinned):
decidable-fragment satisfiability; re-checked witnesses; `unknown` preserved.
Lean kernel (pinned): proof-term acceptance relative to formal
statement/definitions/imports/axioms. Independent checker (per case): L3
agreement. Provenance recorder: identity + integrity-vs-reference. "Trusted" =
relied upon within the documented boundary only.

---

## G. Provenance, canonicalisation, maturity

### G.1 Separated provenance claims

Content identity / integrity vs trusted reference / authenticity (v0: signed
release tags; key management bounded implementation decision) / correctness
(verification only). **"tamper-evident relative to a trusted reference"** —
never "tamper-proof".

### G.2 Canonical encoding profile `msve-canonical-1` (defect 06: complete)

Deterministic; versioned; **no bare JSON numbers** — every numeric value is a
typed object:

- **nat:** `{"$type":"nat","value":"12345"}` — no sign, no leading zeros.
- **int:** `{"$type":"int","value":"-12345"}` — optional `-`; `-0`→`"0"`.
- **rat:** `{"$type":"rat","value":"-7/3"}` — lowest terms, positive denominator.
- **f64:** `{"$type":"f64","value":"-0x1.921fb54442d18p+1"}` — lowercase hexfloat,
  normalized, optional leading `-`; −0.0 → `"0x0.0000000000000p+0"`.
- **Real:** **excluded from hashed artifacts.** A `Real` value reaching the
  canonicalizer → INVALID_INPUT(real-not-encodable). Rationale: arbitrary
  reals have no finite exact encoding. A specification needing a real-valued
  result in a hashed artifact must convert explicitly (e.g., to `rat` where
  exact, declared in the spec); the conversion itself is part of the reviewed
  specification. `Real` remains supported for computation (derive goals); only
  its presence in *hashed* artifacts is refused.

Composite and scalar encodings (all deterministic):
- **Records:** JSON objects, keys sorted bytewise by UTF-8.
- **Lists:** JSON arrays, order preserved.
- **Sets:** JSON arrays sorted by the UTF-8 bytes of each element's canonical form.
- **Options:** `{"$type":"some","value":<canonical>}` / `{"$type":"none"}`.
- **Booleans:** JSON `true`/`false`. **Strings:** JSON strings (NFC-validated).
- **Impl handles:** `{"$type":"impl","value":"<external descriptor>"}`.
- **Type aliases:** transparent (encoded by expansion).
- **Artifacts/blobs:** referenced by `{"$type":"blob","sha256":"<hex>","bytes":<nat>}`;
  bytes carried alongside, linked by the hash.

Injectivity: distinct (type, value) pairs → distinct byte strings (`$type` tags
never collide; value strings canonical per type above). Equal typed values →
identical bytes within the profile version.

Envelope: UTF-8; no insignificant whitespace; minimal string escaping.
Digest: SHA-256 over exact bytes. Profile id recorded per package.

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
repository's genesis commit.

---

## I. Acceptance plan summary

Normative: `MSVE_ACCEPTANCE_PLAN_v0.5.md`. End-to-end: parse/validate frozen
spec; assess selector + validator contracts; establish L1 (three claims kept
separate); identify L2 method per claim or mark unavailable; run L3 if
authorized (invalid inputs routed to the validator contract, never the selector
contract); emit §E.1 result record + evidence package; assess marginal value vs
the Order 7 panel. Slice proposed until separately authorized; generation out
of scope.

---

## J. Release gates (unified vocabulary)

1. Designed · 2. Implemented · 3. Functionally verified · 4. Formally verified
(where applicable; or N/A with reason) · 5. Integrated and reproducible ·
6. Independently reproduced · 7. Released. **Completion rule:** no capability
complete merely because components exist; advertised operations need contract,
tests, failure behaviour, evidence; failures stay visible.

---

## Appendix 1. Glossary (v0.5)

- **Slug / special variable `output` / comparator / admission validator /
  abstract selector** — as defined in §B.
- **RawInput** — the validator's input type (`String`: serialized candidate set).
- **Solver observation / assurance triple / verification record+summary /
  canonical profile `msve-canonical-1` / maturity** — §E–§G.
- **EVIDENCE_RECORDED** — external evidence ingested with provenance; MSVE
  asserts nothing about its truth.

## Appendix 2. Formal selector contract v0.5

*Normative for the acceptance plan. Proposed — frozen before any execution.*

**A2.1 Types.** `Candidate`, `CandidateSet`, `RawInput = String` as in §B.11.
Binary64: −0.0→+0.0; NaN/±∞ excluded from well-formed candidates.

**A2.2 Comparator.** `prefers(a, b)`: higher score; equal scores → lower rank;
equal scores+ranks → smaller UCI (bytewise UTF-8). Output = unique maximal
element. (No key tuple.)

**A2.3 Uniqueness.** Strict total order ⇒ unique maximum for non-empty
well-formed sets. (L1.)

**A2.4 Membership.** `∃c ∈ C : output == c` (whole-record structural equality).

**A2.5 Admission (validator contract).** Accept iff: non-empty set; UCIs
non-empty ASCII-printable whitespace-free; UCIs pairwise distinct
(position-sensitive); ranks Nat; scores finite. Else reject naming the defect.

**A2.6 Numeric semantics.** Canonicalized binary64, exact comparison, no
tolerance; ranking use only.

**A2.7 Determinism.** Pure function of the candidate set.

**A2.8 Historical comparison.** Matches the preserved Order 7 adapter; edge-case
rules are new proposals, not historical facts.

**A2.9 Raw-input serialization (defect 03).** `RawInput` is a JSON array; each
element an object with exactly the fields `uci` (string), `rank` (number),
`score` (number). `parses_as_valid(raw)` (builtin, §B.4 rule 10) is true iff the
raw string satisfies this shape. The validator contract (§B.11):
accept (`Some(cs)`) iff `parses_as_valid(raw)` and `is_wellformed(cs)` for the
parsed set; reject (`None`) otherwise. The parsing relation is axiomatized by
the builtin's definition; L2 conformance must connect the implementation's
parser to it.

## Appendix 3. Unresolved design decisions

Lean version + proof-carrying interface; full problem-class catalog; per-class
resource defaults; generator-class widening; signed-tag key management.

*End of MSVE_DESIGN_SPEC_v0.5.md (draft for review — not frozen).*
