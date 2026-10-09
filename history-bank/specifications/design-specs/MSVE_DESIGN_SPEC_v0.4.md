# MSVE Design Specification v0.4

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.3.md` (retained as historical draft)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MUSE WORK ORDER 0.3 (narrow correction pass) · **Review authority:** Project owner
**Version:** 0.4 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

Change summary: v0.4 repairs the six freeze-blocking defects found in the v0.3
review (see `MSVE_DESIGN_REVIEW_v0.4.md` for the ledger). Every defect below was
verified against the v0.3 text before correction:
1. The grammar rejected its own examples (hyphenated names, reserved `output`
   used as identifier, trailing semicolons, left recursion).
2. The membership predicate permitted fabricated scores on a real UCI; the
   well-formedness predicate admitted identical duplicates and omitted the
   ASCII/whitespace rules.
3. The assurance policy had no syntax despite the result schema depending on it.
4. The checker invocation rule and function types were never formalized.
5. The verification-summary aggregation contradicted its own example.
6. The canonical profile did not cover the language's numeric types.

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*: domain-agnostic within the formal scope
defined by the input language (§B) and the capability matrix
(`MSVE_CAPABILITY_MATRIX_v0.4.md`). Outside the declared scope: UNSUPPORTED, not attempted.

### A.2 Intended users and responsibilities

- **Specification authors** (humans): write, review, and freeze formal specifications.
- **MSVE (the engine)**: parses, validates, constructs, checks, and records — never
  invents premises, never executes unreviewed natural language.
- **Reviewers** (humans): approve specifications, adjudicate discrepancies, authorize
  capability changes.

### A.3 The three judgments (non-eliminable)

1. **Domain judgment** — objectives, axioms, definitions. With the author; MSVE exposes it.
2. **Construction judgment** — choices the specification does not determine. MSVE reports
   alternatives or UNDERDETERMINED; never silently prefers one.
3. **Empirical uncertainty** — real-world behaviour. Only real-implementation evidence
   addresses this. MSVE never derives it.

### A.4 "All-rounder" — normative definition

> "All-rounder within declared scope S, capability matrix version X.Y."

The capability matrix is normative. Every public use carries scope and version
qualifiers. The unified maturity ladder (§G.4, §J) defines each stage.

### A.5 Explicit non-goals

No inferred historical data (FORBIDDEN); no performance prediction from formal
correctness (OUT OF SCOPE); no invented objective functions; no replacement of
the empirical research process.

---

## B. Formal input language (complete v0 definition, corrected)

### B.1 Design rules

1. Minimal, machine-readable; natural language never drives execution (§B.12).
2. Specifications carry identity and version; frozen specifications are immutable
   content-hashed baselines.
3. This section is the **complete normative syntax**. §B.13 gives a valid example
   for every goal form; §B.14 gives invalid examples with exact rejection reasons.
   Each example in §B.13 was derived against the §B.3 productions token by token
   (derivation notes in the review); each §B.14 example fails for the stated reason.

### B.2 Lexical rules

```
Ident     := [A-Za-z_][A-Za-z0-9_]*        # program identifiers
Slug      := [A-Za-z0-9_]+(-[A-Za-z0-9_]+)* # spec names, scopes, checker names (hyphens allowed)
String    := '"' ( [^"\\\u0000-\u001F] | Esc )* '"'   # JSON string escaping
Nat       := [0-9]+
SemVer    := Nat "." Nat "." Nat
Duration  := Nat ("ms" | "s" | "min" | "h")
MemSize   := Nat ("B" | "KB" | "MB" | "GB")
CheckerID := Slug "/" SemVer               # e.g. indie-ref-impl/0.4.0
```

Hyphens are permitted in `Slug` (spec names, scopes, checker names) but **not**
in `Ident`. This avoids lexing ambiguity with the `-` operator (`a-b` would
otherwise be ambiguous). Program identifiers never contain hyphens.

Keywords (reserved, not usable as identifiers): `spec version scope authors type
define axiom assume constraints require forbid projection goal derive construct
satisfying prove assuming check of compare-models under verification proof test
none kernel-checked by differential property-fuzz required optional assurance
level-a level-b accepted limits timeout memory steps record all external true
false if then else forall exists in type`.

`output` is **not** a keyword. It is a special context variable (§B.5a): usable
exactly where the binding rules allow, and not declarable by the user.

Whitespace separates tokens; newlines insignificant except in strings. `;`
terminates items; blocks tolerate a trailing `;` (§B.3). Comments: `//` to end
of line.

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
CompareGoal    := "compare-models" "satisfying" "[" Ident ("," Ident)* "]"
                  ("under" Ident)?

Verification   := "verification" "{" (";" | VerifItem ";")* "}"
VerifItem      := ProofReq | TestReq | AssuranceReq
ProofReq       := "proof" ":" ("none" | "kernel-checked" "by" CheckerID Qualifier)
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
OrExpr         := AndExpr ("\\/" AndExpr)*
AndExpr        := ImplExpr ("/\\" ImplExpr)*
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
Literal        := String | Nat | "true" | "false" | "none"
Proposition    := Expr        # required type: Bool
Predicate      := Expr        # required type: Bool
```

Notes on the v0.3 defects repaired here:
- `Slug` covers hyphenated names; `Ident` unchanged (no minus ambiguity).
- Blocks use `(";" | Item ";")*`: trailing semicolons accepted, empty blocks accepted.
- `Postfix` replaces the left-recursive `Primary → Expr` cycle: field access and
  indexing are iterative suffixes on `Atom`.
- `Domain` requires the `type` marker for type extensions, removing the
  `forall n in Nat` ambiguity (expression vs type).
- `Literal` includes `"none"` (was reserved but unproducible).
- Function types are expressible: `(CandidateSet, Candidate) -> Bool`.
- `CompareGoal`'s `under` is optional; absence is a semantic admission error
  (§B.5), not a syntax accident.

### B.4 Type system and type-checking rules

Base types: `String Nat Int Real Binary64 Bool`. Records, lists, sets, options,
`Impl(A -> B)`, function types `(A, …) -> R`.

1. Every `Expr` has a unique type. Literals: strings→`String`, digits→`Nat`,
   `true/false`→`Bool`, `"none"`→`Option<T>` (T from context; error if uninferred).
2. Arithmetic `+ - * /`: operands share one numeric type; **no implicit promotion**.
3. `== !=`: same type. Ordering `< <= > >=`: ordered types
   (`Nat Int Real Binary64 String`).
4. `String` ordering: bytewise lexicographic over UTF-8 (§B.4a).
5. `==` on records: structural equality. On `Binary64`: bitwise equality of
   canonical forms (see §G.2; −0.0 normalized).
6. Boolean connectives on `Bool`. `if`: `Bool` condition, equal branch types.
7. Quantifiers: domain is `type T` (extension of T, possibly infinite —
   decidability is solver-level) or a collection expression; body `Bool`.
8. `e.f`: record field. `e[i]`: list index, `i: Nat`. Chained freely via Postfix.
9. Application: argument types match exactly. `some(e: T): Option<T>`;
   `is_some: Option<T> -> Bool`.
10. Builtins: `len: [T] -> Nat`; `range: Nat -> [Nat]` (0..n−1);
    `is_finite: Binary64 -> Bool`; `is_ascii_printable: String -> Bool`;
    `has_no_whitespace: String -> Bool`.
11. `external("…")` introduces an opaque `Impl` handle; usable only as a `check`
    goal target.

**B.4a String order.** Bytewise lexicographic over UTF-8. Producers must supply
NFC-normalized UTF-8; non-normalized input → INVALID_INPUT(string-not-normalized)
at admission. The parser never silently normalizes.

### B.5 Name resolution and special variables

- Flat namespace per specification: type aliases, definitions, axioms,
  assumptions, constraint groups, projections, external handles. Duplicates →
  INVALID_INPUT(duplicate-definition: name). Unresolved references →
  INVALID_INPUT(unbound-identifier: name).
- `assuming […]`: each name must resolve to an `assume`/`axiom` declaration.
- Constraint-group references must name `constraints` groups; projection
  references must name `projection` declarations; projection paths resolve
  against the model context.
- `check f of h`: `f` must be a defined function of type `(In, Out) -> Bool`;
  `h` must have type `Impl(In -> Out)` with identical `In`/`Out`.

**B.5a Special variable `output`.** In constraint groups referenced by
`construct`/`compare-models` goals, and in projection paths of `compare-models`
goals, `output` is bound to the object (resp. model) under consideration, typed
by the goal's target type. `output` is not declarable:
`define output …` → INVALID_INPUT(reserved-context-name). It is not a keyword
and has no meaning outside these positions.

**B.5b Check-goal invocation rule (defect 04).** For `goal check f of h` with
`f: (In, Out) -> Bool`, `h: Impl(In -> Out)`: the engine determines the input
corpus from the Verification test policy — `differential` uses the paired
differential corpus; `property-fuzz` uses the generated corpus (`cases` count,
`seeds`). For each input `i`: `o = invoke(h, i)`; evaluate `f(i, o)`.
`semantic_result` = HOLDS iff every evaluation is true; the first `(i, o)`
with `f(i,o) = false` is the counterexample witness for VIOLATED.
Test-based checking is **bounded to the corpus** (L3). Universal claims about
implementations are not established by `check` goals; they require L2 methods
(spec §D.1). The corpus actually used is recorded in the evidence bundle.

### B.6 Assumptions: roles

- **`assume name: P`**: premise, taken as given, tracked in the assumption set,
  never checked by the engine; adequacy is a human freeze-gate judgment.
- **`require`**: must hold of the constructed/checked/found object; checked.
- **`forbid`**: must not hold; checked symmetrically.
- **`prove`**: the proposition to establish relative to the `assuming` context.
  A PROVED result names the exact proposition and its assumption context.

### B.7 Verification policy and assurance syntax (defect 03)

```
VerifItem := ProofReq | TestReq | AssuranceReq
AssuranceReq := "assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")
```

- At most one `assurance:` item; duplicates → INVALID_INPUT(duplicate-verification-item).
- Absent → default `none` (no assurance beyond execution; recorded, not silent).
- `level-a required` demands kernel-checked proof (or independent recomputation
  for `derive`). Static checks at admission:
  - `level-a required` without `proof: kernel-checked by <id> required` →
    INVALID_INPUT(conflicting-assurance-requirements).
  - `level-a required` on a solver-backed goal (`construct`/`compare-models`
    via SMT) → INVALID_INPUT(assurance-level-unavailable): v0 policy (§E.6)
    establishes no Level A certificate pipeline for SMT UNSAT.
- `level-b accepted` records explicit acceptance of solver-backed or test-backed
  conclusions with labelling (§E.5). This is the syntax §E.5's rule depends on:
  a Level B contradiction may be reported **only** when the frozen spec contains
  `assurance: level-b accepted`.
- Proof/test items keep the required/optional qualifier; required-but-unrunnable
  → shortfall handling (§E.5); optional-but-unrunnable → recorded as skipped.

### B.8 Resource limits

`timeout` mandatory; missing → INVALID_INPUT(missing-mandatory-timeout). Legal
range 1s…24h; outside → INVALID_INPUT(timeout-out-of-range). `steps: 0` →
INVALID_INPUT(degenerate-resource-limit). `memory`/`steps` optional, combinable.

### B.9 Admission and error catalog

INVALID_INPUT reasons: `not-a-formal-specification`, `missing-header-field`,
`syntax-error`, `unbound-identifier: <name>`, `duplicate-definition: <name>`,
`reserved-context-name: <name>`, `type-mismatch: expected <T>, found <U>`,
`missing-required-projection`, `unbound-assumption-reference: <name>`,
`missing-mandatory-timeout`, `timeout-out-of-range`, `degenerate-resource-limit`,
`duplicate-verification-item`, `conflicting-verification-requirements`,
`conflicting-assurance-requirements`, `assurance-level-unavailable`,
`missing-goal`, `projection-path-unresolvable: <path>`,
`string-not-normalized`.
UNSUPPORTED reasons: `scope-not-supported`, `construct-not-decidable-for-proof`.

### B.10 Natural-language handling (hard rule)

NL drafts candidates under human supervision. Unreviewed NL-extracted
assumptions NEVER enter executable specifications — not even labelled. They may
live only in review artifacts as proposals.

### B.11 Valid examples (one per goal form; derived against §B.3)

**derive:**
```
spec tiny-derive
version 0.4.0
scope exact-arithmetic
authors ["example"]
goal derive (2 * 21) + 1
verification { proof: none; assurance: none; }
limits { timeout: 10s; }
record: all
```

**construct:**
```
spec tiny-construct
version 0.4.0
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
version 0.4.0
scope kernel-proofs
authors ["example"]
axiom add_zero: forall n in type Nat :: n + 0 == n
goal prove forall n in type Nat :: n + 0 == n assuming [add_zero]
verification { proof: kernel-checked by lean-kernel/4.9.0 required; assurance: level-a required; }
limits { timeout: 60s; }
record: all
```

**check** (selector — normative example; contract in Appendix 2):
```
spec selector-contract
version 0.4.0
scope finite-total-order-selection
authors ["MSVE design team"]

type Candidate = { uci: String, rank: Nat, score: Binary64 }
type CandidateSet = [Candidate]

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

define selector_impl: Impl(CandidateSet -> Candidate) = external("selector-impl/0.4.0")
define indie_ref_impl: Impl(CandidateSet -> Candidate) = external("independent-ref-impl/0.4.0")

goal check contract_holds of selector_impl

verification {
  proof: none;
  test: differential by indie-ref-impl/0.4.0 required;
  test: property-fuzz { seeds: [1, 2, 3], cases: 10000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; memory: 2GB; }
record: all
```

**compare-models:**
```
spec tiny-models
version 0.4.0
scope finite-constraint-models
authors ["example"]
type M = { x: Nat }
constraints two_vals {
  require xv: (output.x == 1) \/ (output.x == 2);
}
projection xproj = [output.x]
goal compare-models satisfying [two_vals] under xproj
verification { proof: none; test: none; assurance: level-b accepted; }
limits { timeout: 10s; }
record: all
```

### B.12 Invalid examples (each rejected with the exact reason)

1. A natural-language paragraph → INVALID_INPUT(not-a-formal-specification).
2. `goal compare-models satisfying [two_vals]` with no `under` →
   INVALID_INPUT(missing-required-projection).
3. `goal prove P assuming [ghost_asm]` →
   INVALID_INPUT(unbound-assumption-reference: ghost_asm).
4. Specification without `limits` → INVALID_INPUT(missing-mandatory-timeout).
5. Two `define foo` declarations → INVALID_INPUT(duplicate-definition: foo).
6. `require r: output.zzz == 1` (no such field) → INVALID_INPUT(type-mismatch…).
7. `limits { timeout: 10s; steps: 0; }` → INVALID_INPUT(degenerate-resource-limit).
   (`timeout: 0s` → INVALID_INPUT(timeout-out-of-range) per the 1s…24h rule.)
8. `goal check contract_holds of missing_impl` →
   INVALID_INPUT(unbound-identifier: missing_impl).
9. `define output: Nat = 3` → INVALID_INPUT(reserved-context-name: output).
10. `assurance: level-a required` on a `compare-models` goal →
    INVALID_INPUT(assurance-level-unavailable) — v0 establishes no Level A
    pipeline for SMT-backed goals.
11. `assurance: level-a required` with `proof: none` →
    INVALID_INPUT(conflicting-assurance-requirements).
12. Non-NFC string literal in a hashed artifact → INVALID_INPUT(string-not-normalized).

---

## C. Supported problem classes

Capability matrix (`MSVE_CAPABILITY_MATRIX_v0.4.md`) normative. v0 targets (all
maturity: Designed): exact integer/rational arithmetic; SymPy-backed symbolic
computation within §F.3 limits; decidable-fragment constraint solving (e.g.
QF_LIA); restricted general SMT (unknown → INCONCLUSIVE(SOLVER_UNKNOWN)); model
construction/witnesses where the solver provides models; uniqueness checking via
§D within decidable fragments; Lean-kernel proof checking (formalization
human-reviewed); L1/L2/L3 implementation-contract assurance (§D.1); code
generation restricted to §D.5; FORBIDDEN: inferring missing historical data,
NL direct execution, silent gap-filling, executing unreviewed specs; OUT OF
SCOPE: performance prediction, objective invention, arbitrary discovery.

---

## D. Assurance levels, uniqueness, generation

### D.1 Three assurance levels

- **L1 — Mathematical model.** Abstract-algorithm properties by proof or sound procedure.
- **L2 — Implementation conformance.** Named method per claim (checked refinement,
  translation validation, static analysis, documented limited method). L1 alone
  proves nothing about code.
- **L3 — Tested behaviour.** Regression, differential, property-based, fuzzing —
  bounded to executed inputs. `check` goals are L3 by §B.5b (corpus-bound).

### D.2 Uniqueness decision procedure

Satisfiability → else CONTRADICTION (assurance §F.5/§E.5). Declared projection
(absent → INVALID_INPUT). Second-model query ⋁ᵢ(πᵢ(m₂) ≠ πᵢ(m₁)) with exact
inequality on canonical forms; re-solve. Second model → UNDERDETERMINED with
witnesses. UNIQUE_UNDER_PROJECTION only if query UNSAT **and** procedure complete
for the class; record procedure, guarantees, assurance achieved (Level B in v0
for solver-backed classes). Else INCONCLUSIVE with reason code.

### D.3 Exact distinctness

Projection equality exact over canonical forms (transitive). No tolerance-based
equivalence; any future tolerance comparison specified separately, never as the
projection equality.

### D.4 Uniqueness-restoring assumptions

v0 tests only user-supplied or declared-finite-family candidates; reports which
restore uniqueness. Sufficient ≠ justified; only the human author asserts
empirical justification.

### D.5 v0 generator class

Template-based generation for total functions defined by structural recursion
over finite lists/collections: permitted element types (base types and
records/lists/sets/options thereof); fixed, reviewed, frozen template;
structural recursion (termination by construction); operation contracts
(e.g., comparator total-order obligations) as L1 proof obligations on the author;
output re-checked against the contract (L2). Distinguished: finite collection
per execution ≠ finite input domain ≠ unbounded class of finite collections —
the template handles the third via recursion, never enumeration. **Code
generation is out of scope for the first selector vertical slice.**

---

## E. Result-record schema

### E.1 Schema (authoritative)

```
ResultRecord {
  admission: ACCEPTED | INVALID_INPUT(reason: ErrorCode) | UNSUPPORTED(reason: ErrorCode),
  execution: NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED
             | INTERNAL_ERROR(reason: String),
  semantic_result: Option<SemanticResult>,  # None when admission != ACCEPTED
                                            # or execution == NOT_STARTED
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
```

`semantic_result` is `Option`: invalid-input examples correctly state there is
*no* semantic result — the field is absent (None), not filled with a dummy.

### E.2 Semantic results per goal type

`derive`: DERIVED_VALUE · INCONCLUSIVE(reason). `construct`:
ARTIFACT_CONSTRUCTED · NO_SOLUTION · INCONCLUSIVE(reason). `prove`: PROVED ·
DISPROVED · INCONCLUSIVE(reason). `check`: HOLDS · VIOLATED (counterexample) ·
INCONCLUSIVE(reason). `compare-models`: UNIQUE_UNDER_PROJECTION ·
UNDERDETERMINED (witnesses) · CONTRADICTION · INCONCLUSIVE(reason).

### E.3 INCONCLUSIVE reason codes

SOLVER_UNKNOWN · PROCEDURE_INCOMPLETE · RESOURCE_EXHAUSTED ·
EXECUTION_INTERRUPTED · ASSURANCE_REQUIREMENT_UNMET. Never merged.

### E.4 Solver observations vs conclusions

Observation (SAT/UNSAT/UNKNOWN + tool provenance) ≠ semantic conclusion ≠
assurance achieved. **UNSAT rule:** LEVEL_A required but only Level B available →
INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET), shortfall true, observation and Level
B evidence preserved — the contradiction is refused, not lowered. LEVEL_B
explicitly accepted (`assurance: level-b accepted` in the frozen spec) →
CONTRADICTION with LEVEL_B_SOLVER_BACKED clearly attached. Unsat cores remain
diagnostic only.

### E.5 v0 assurance policy

Level A eligible: `prove` goals via Lean kernel (artifact: kernel-checked term);
`derive` goals via independent recomputation. **SMT-UNSAT Level A: FUTURE** — v0
establishes no independently checkable certificate pipeline; no solver proof
output is claimed as a standard certificate. Unsupported/unverified certificate
formats are unavailable for Level A, stated not silently used.

### E.6 Per-property verification and aggregation (corrected, defect 05)

Records individually attributable (property, artifact, spec version, method,
checker + version, result, reason, assurance boundary, inputs ref). Summary by
fixed precedence — **divergence first**, because an untrustworthy check dominates
a definitive outcome:
1. No records → NOT_RUN.
2. Conflicting results on the same property from different checkers →
   CHECKER_DIVERGENCE (records preserved).
3. Any record FAIL → FAIL.
4. Any record INCONCLUSIVE (and none above) → INCONCLUSIVE.
5. Otherwise → PASS.

The summary never deletes per-property records; a package with one FAIL and one
DIVERGENCE reports DIVERGENCE as summary while both records (and both facts)
remain in the package.

### E.7 Legal combinations (schema examples, not executed tests)

Invalid input: admission=INVALID_INPUT(syntax-error), execution=NOT_STARTED,
semantic_result=None, verification_summary=NOT_RUN. Unsupported: admission=
UNSUPPORTED(scope-not-supported). Constructed unverified: execution=COMPLETED,
semantic_result=Some(ARTIFACT_CONSTRUCTED), verification_summary=NOT_RUN.
Completed inconclusive: INCONCLUSIVE(SOLVER_UNKNOWN). Timeout after witness:
execution=TIMEOUT, partial_results=[m₁ labelled partial],
semantic_result=Some(INCONCLUSIVE(RESOURCE_EXHAUSTED)). Level B UNSAT, Level A
required: solver_observation={UNSAT,…}, semantic_result=
Some(INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET)), shortfall=true. Checker
disagreement: records (PASS, FAIL) same property → summary CHECKER_DIVERGENCE +
discrepancy with follow-up. Split properties: records [PASS, FAIL] different
properties → summary FAIL (rule 3). External evidence: evidence bundle carries
records; no scientific conclusion asserted.

### E.8 External experimental evidence

EVIDENCE_RECORDED (ingest + provenance; MSVE asserts nothing) /
RECORD_INTEGRITY assessment (PASS/FAIL on the record) / EXTERNAL_ASSESSMENT
(who concluded what, on what basis — never promoted by MSVE).

### E.9 Anti-conflation rules (hard)

Solver unknown/interruption/timeout never → CONTRADICTION/UNDERDETERMINED.
Finite suites never prove universal properties. ARTIFACT_CONSTRUCTED ≠ verified.
COMPLETED ≠ PASS. Failures and spec changes stay distinguishable from successes.

---

## F. Trust base

Orchestration over established components; no new solver in v0. Parser/validator
(MSVE-owned): syntax/typing/mandatory fields — not semantics. SymPy (pinned):
computed / independently checkable / trusted-tool output (§F.3, v0.3 retained).
Z3 (pinned): decidable-fragment satisfiability; re-checked model witnesses;
`unknown` preserved. Lean kernel (pinned): proof-term acceptance relative to
formal statement/definitions/imports/axioms. Independent checker (per case): L3
behavioural agreement. Provenance recorder: identity + integrity-vs-reference;
not origin without the authenticity mechanism; not correctness. "Trusted" =
relied upon without re-verification within the documented boundary. SAT
assurance: witnesses re-checked against the canonical spec; checker + version
recorded.

---

## G. Provenance, canonicalisation, maturity

### G.1 Separated provenance claims

Content identity (SHA-256 over canonical form) / integrity relative to a trusted
reference / authenticity (v0: project-owner signed release tags; key management
a bounded implementation decision) / correctness (verification procedures only).
Accurate claim: **"tamper-evident relative to a trusted reference"** — never
"tamper-proof".

### G.2 Canonical encoding profile `msve-canonical-1` (corrected, defect 06)

Deterministic; versioned; no bare JSON numbers — every numeric value is a typed
object, so JSON strings, JSON numbers, and typed values can never collide:

- **nat:** `{"$type":"nat","value":"12345"}` — decimal, no sign, no leading zeros.
- **int:** `{"$type":"int","value":"-12345"}` — decimal, optional leading `-`, no
  leading zeros; integer `-0` normalized to `"0"` (canonicalizer rule; not an error).
- **rat:** `{"$type":"rat","value":"-7/3"}` — lowest terms, positive denominator.
- **f64:** `{"$type":"f64","value":"-0x1.921fb54442d18p+1"}` — C99-style hexfloat,
  lowercase, normalized (`0x1.` + exactly 13 hex digits for nonzero finite values),
  optional leading `-` for negative values; exponent signed decimal, no leading
  zeros; −0.0 → `"0x0.0000000000000p+0"` (unsigned).
- **Real:** not encodable in general — **excluded from hashed artifacts**.
  A specification requiring a real value in a hashed artifact must convert it
  explicitly (e.g., to `rat`); the canonicalizer rejects bare `Real` with
  INVALID_INPUT(real-not-encodable). This restriction is explicit, not silent.

Injectivity: distinct (type, value) pairs map to distinct byte strings —
different `$type` tags never collide; within a type the value string is
canonical (normalization rules above). Equal typed values always produce
identical bytes within profile `msve-canonical-1`.

Envelope: canonical JSON — UTF-8, keys sorted bytewise, no insignificant
whitespace, minimal string escaping, NFC-normalized input (else
INVALID_INPUT(string-not-normalized) at admission). Digest: SHA-256 over the
exact UTF-8 bytes.

### G.3 Result package contents

Result record (§E.1) + spec identity/version/hash; canonicalized input hashes;
exact tool/solver/checker versions + configuration; derivation records,
witnesses, proof artifacts; test inputs, seeds, fuzz conditions; output hashes;
human-reviewed assumption set; failure records and unresolved issues;
supersession records. Failed attempts preserved; re-verification after
spec/tool changes; prior results superseded, never deleted.

### G.4 Unified maturity vocabulary

1. Designed · 2. Implemented · 3. Functionally verified · 4. Formally verified
(or N/A with recorded reason — never misleadingly labelled) · 5. Integrated and
reproducible · 6. Independently reproduced (distinct from 5: composition vs
independent confirmation) · 7. Released. Stages 1–3, 5 sequential; 4 may be N/A
(recorded); 6 requires 5; 7 requires all applicable prior stages. Used
identically in §J, the matrix, the acceptance plan, the review, and diagrams.

### G.5 Version transition policy

Profile changes require a version bump (`msve-canonical-2`, …); both hashes
recorded during transition; old hashes never reinterpreted under new rules.

---

## H. Governance

Project owner: approves/revises/rejects design; freezes specs; authorizes repo
creation (after freeze), implementation (separate authorization), release
declaration on evidence. MSVE is a separate capability track from research
projects and àfi_adaptive. Tool use grants no modification rights (read-only
unless authorized). Genesis rule: the reviewed, frozen design specification is
the repository's genesis commit.

---

## I. Acceptance plan summary

Normative: `MSVE_ACCEPTANCE_PLAN_v0.4.md`. End-to-end: (1) parse/validate frozen
spec; (2) assess selector + validator contracts; (3) establish L1; (4) identify
L2 method per claim or mark unavailable; (5) run L3 if later authorized;
(6) emit §E.1 result record + evidence package; (7) assess marginal value vs the
Order 7 panel. Vertical slice proposed until separately authorized; generation
out of scope.

---

## J. Release gates (unified vocabulary)

1. Designed — frozen spec (genesis commit); language, output contract, scope defined; reviewed.
2. Implemented — every claimed operation exists with documented interface.
3. Functionally verified — acceptance suite green: normal, boundary, expected-failure.
4. Formally verified (where applicable) — kernel-checked proofs or sound procedures + artifacts; or N/A with reason.
5. Integrated and reproducible — composes; versions pinned; re-runs reproduce.
6. Independently reproduced — separate party/machine reproduces from the package.
7. Released — matrix entries at claimed maturity; limitations documented; qualified claims evidenced.

**Completion rule:** no capability complete merely because components exist.
Advertised operations need contract, tests, failure behaviour, evidence.
Unsupported/unproven/untested stay labelled; failures stay visible.

---

## Appendix 1. Glossary (v0.4)

- **Slug:** hyphen-permitting name token for spec names, scopes, checker names
  (program identifiers never contain hyphens).
- **Special variable `output`:** context-bound identifier in constraint groups
  and projection paths (§B.5a); not declarable, not a keyword.
- **Comparator `prefers`:** explicit mixed-direction preference relation (App. 2).
- **Admission validator:** object checking raw input form/types/well-formedness
  (separate contract from the abstract selector).
- **Solver observation:** SAT/UNSAT/UNKNOWN + tool provenance (§E.1).
- **Assurance required/achieved/shortfall** (§E.1, §B.7).
- **Verification record / summary** (§E.6): per-property records; computed summary
  with divergence-first precedence.
- **Canonical profile `msve-canonical-1`** (§G.2).
- **Maturity:** seven-stage ladder (§G.4), separate from target disposition.

## Appendix 2. Formal selector contract v0.4

*Normative for the acceptance plan. Proposed — frozen before any execution.*

**A2.1 Types.** `Candidate = { uci: String, rank: Nat, score: Binary64 }`;
`CandidateSet = [Candidate]`. Binary64: −0.0→+0.0; NaN/±∞ not representable in
well-formed candidates.

**A2.2 Comparator.** `prefers(a, b)`:
1. `a.score > b.score`, or 2. equal scores and `a.rank < b.rank`, or
3. equal scores, equal ranks, and `a.uci < b.uci` (bytewise UTF-8).
`output` = unique `prefers`-maximal element. (No key tuple: mixed directions
cannot be encoded in one maximization — the v0.2 error.)

**A2.3 Uniqueness.** Component strict total orders compose lexicographically to
a strict total order; pairwise-distinct UCIs give trichotomy; every non-empty
well-formed set has exactly one maximal element. (L1.)

**A2.4 Membership (corrected, defect 02).** `∃c ∈ C : output == c` —
whole-record structural equality. The v0.3 UCI-only formulation is withdrawn:
it permitted a fabricated score/rank on a genuine UCI.

**A2.5 Admission (validator contract).** Accept raw input iff: set non-empty;
every `uci` non-empty, ASCII printable, whitespace-free; UCIs pairwise distinct
**including identical duplicate records** (position-sensitive: `i≠j ⇒
cs[i].uci ≠ cs[j].uci`); every `rank`: Nat; every `score` finite. Else reject,
naming the defect. Invalid-input rejection is this validator's property, proved
over its finite checklist (L1) — not the abstract selector's.

**A2.6 Numeric semantics.** Canonicalized binary64, exact comparison, no
tolerance; ranking use only, no calibration claim.

**A2.7 Determinism.** Pure function of the candidate set.

**A2.8 Historical comparison.** Corrected contract matches the preserved Order 7
adapter (higher probability, lower rank, smaller UCI; exact float tie
detection). Edge-case rules beyond the record (non-finite rejection, −0.0
normalization, duplicate/empty/non-ASCII UCI rejection) are new contract
proposals, not historical facts.

## Appendix 3. Unresolved design decisions

Lean version + proof-carrying interface; full problem-class catalog; per-class
resource defaults; generator-class widening; signed-tag key management.

*End of MSVE_DESIGN_SPEC_v0.4.md (draft for review — not frozen).*
