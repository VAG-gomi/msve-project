# MSVE Design Specification v0.3

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.2.md` (retained as historical draft)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MUSE WORK ORDER 0.2 · **Review authority:** Project owner
**Version:** 0.3 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

Change summary: v0.3 is a controlled correction pass over v0.2 (see
`MSVE_DESIGN_REVIEW_v0.3.md` for the section-by-section ledger). Structural work
preserved: orthogonal result fields, exact projection-relative comparison,
L1/L2/L3 assurance, SAT/UNSAT boundaries, bounded provenance claims, disposition
vs maturity separation. Corrected: the selector ordering (explicit comparator),
the complete formal language (§B rewritten), UNSAT observation vs conclusion
semantics, the validator/selector separation, the generator domain, the
result-record schema, the canonical encoding profile, and the unified maturity
vocabulary.

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*: domain-agnostic within the formal scope
defined by the input language (§B) and the capability matrix
(`MSVE_CAPABILITY_MATRIX_v0.3.md`). Any problem outside the declared scope is
UNSUPPORTED (admission status), not attempted.

### A.2 Intended users and responsibilities

- **Specification authors** (humans): write, review, and freeze formal specifications.
- **MSVE (the engine)**: parses, validates, constructs, checks, and records — never
  invents premises, never executes unreviewed natural language.
- **Reviewers** (humans): approve specifications, adjudicate discrepancies, authorize
  capability changes.

### A.3 The three judgments (non-eliminable)

1. **Domain judgment** — objectives, axioms, definitions. Lives with the author; MSVE exposes it.
2. **Construction judgment** — choices the specification does not determine. MSVE reports
   alternatives or UNDERDETERMINED; never silently prefers one.
3. **Empirical uncertainty** — real-world behaviour. Only real-implementation evidence
   under appropriate experimental design addresses this. MSVE never derives it.

### A.4 "All-rounder" — normative definition

> "All-rounder within declared scope S, capability matrix version X.Y."

The capability matrix is normative. Every public use carries scope and version
qualifiers. The unified maturity ladder (§G.4, §J) defines what each stage requires.

### A.5 Explicit non-goals

MSVE will not infer missing historical data (FORBIDDEN); will not predict
real-world performance from formal correctness (OUT OF SCOPE); will not invent
objective functions; will not replace the empirical research process.

---

## B. Formal input language (complete v0 definition)

### B.1 Design rules

1. Minimal, machine-readable; natural language never drives execution (§B.12).
2. Every specification carries identity and version; frozen specifications are
   immutable content-hashed baselines.
3. This section is the **complete normative syntax**. §B.13 gives a valid example
   for every goal form; §B.14 gives invalid examples with exact rejection reasons.
   The grammar accepts all of §B.13 and rejects all of §B.14.

### B.2 Lexical rules

```
Ident     := [A-Za-z_][A-Za-z0-9_]*        # identifiers
String    := '"' ( [^"\\\u0000-\u001F] | Esc )* '"'   # JSON string escaping
Nat       := [0-9]+
SemVer    := Nat "." Nat "." Nat
Duration  := Nat ("ms" | "s" | "min" | "h")
MemSize   := Nat ("B" | "KB" | "MB" | "GB")
CheckerID := Ident "/" SemVer               # e.g. indie-ref-impl/0.3.0
```

Keywords (reserved, not usable as identifiers): `spec version scope authors type
define axiom assume constraints require forbid projection goal derive construct
satisfying prove assuming check of compare-models under verification proof test
none kernel-checked by differential property-fuzz required optional limits
timeout memory steps record all external context input output true false if then
else forall exists in as`.

Whitespace separates tokens; newlines are insignificant except inside strings.
`;` terminates items inside braced blocks. Comments: `//` to end of line.

### B.3 Grammar (EBNF — complete)

```
Specification  := Header Body
Header         := "spec" Ident "version" SemVer "scope" Ident
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

ConstraintGroup:= "constraints" Ident "{" Constraint (";" Constraint)* "}"
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

Verification   := "verification" "{" VerifItem (";" VerifItem)* "}"
VerifItem      := ProofReq | TestReq
ProofReq       := "proof" ":" ("none" | "kernel-checked" "by" CheckerID Qualifier)
TestReq        := "test" ":" ("none"
                   | "differential" "by" CheckerID Qualifier
                   | "property-fuzz" FuzzConfig Qualifier)
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
                | "Option" "<" TypeExpr ">" | ImplType | Ident
ImplType       := "Impl" "(" TypeExpr "->" TypeExpr ")"

Expr           := OrExpr
OrExpr         := AndExpr ("\\/" AndExpr)*
AndExpr        := ImplExpr ("/\\" ImplExpr)*
ImplExpr       := CmpExpr ("==>" CmpExpr)?
CmpExpr        := AddExpr (("==" | "!=" | "<" | "<=" | ">" | ">=") AddExpr)?
AddExpr        := MulExpr (("+" | "-") MulExpr)*
MulExpr        := Unary (("*" | "/") Unary)*
Unary          := ("!" | "-")? Primary
Primary        := Literal | Ident | Ident "(" (Expr ("," Expr)*)? ")"
                | Expr "." Ident | Expr "[" Expr "]"
                | "if" Proposition "then" Expr "else" Expr
                | "forall" Ident "in" Domain "::" Proposition
                | "exists" Ident "in" Domain "::" Proposition
                | "(" Expr ")"
Domain         := Expr | TypeExpr
Literal        := String | Nat | "true" | "false"
Proposition    := Expr        # required type: Bool
Predicate      := Expr        # required type: Bool
```

### B.4 Type system and type-checking rules

Base types: `String Nat Int Real Binary64 Bool`. Records `{f: T, …}`,
lists `[T]`, sets `Set<T>`, options `Option<T>`, `Impl(A -> B)`.

Rules (checked at parse; violation → INVALID_INPUT(type-mismatch …)):

1. Every `Expr` has a unique type; literals: strings→`String`, digits→`Nat`,
   `true/false`→`Bool`.
2. Arithmetic `+ - * /`: operands share one numeric type (`Nat Int Real Binary64`);
   **no implicit promotion** — mixed types are a type error. `/` on `Nat`/`Int` is
   exact division only where divisible (otherwise INVALID_INPUT at evaluation or
   a solver constraint; documented per operation).
3. Comparisons `== !=`: same type required. Ordering `< <= > >=`: ordered types
   only (`Nat Int Real Binary64 String`).
4. `String` ordering: **bytewise lexicographic over the UTF-8 encoding**
   (§B.4a). `==` on records: structural equality.
5. `\/ /\ ==> !`: `Bool` operands. `if`: condition `Bool`, branches same type.
6. Quantifiers: `forall x in D :: P` / `exists x in D :: P` — `D` is a collection
   expression (`[T]`, `Set<T>`) or a type name (denoting its extension; may be
   infinite — decidability is a separate, solver-level concern); `P: Bool` with
   `x` bound.
7. Field access `e.f`: `e` a record with field `f`. Index `e[i]`: `e` a list,
   `i: Nat`.
8. Function application: argument types match parameter types exactly.
9. `Option<T>`: constructors `some(e: T)`, `none`; builtins `is_some: Option<T>->Bool`.
10. Builtins: `len: [T]->Nat`; `is_finite: Binary64->Bool`; `external` introduces
    an opaque `Impl` handle (no operations except being named by `check` goals).

**B.4a String order.** The contract defines string comparison as bytewise
lexicographic comparison of UTF-8 encodings. For the selector's UCI alphabet
(ASCII), this coincides with ASCII byte order. Producers must supply
NFC-normalized UTF-8; the parser does not normalize.

### B.5 Name resolution

- One flat namespace per specification for: type aliases, value/function
  definitions, axioms, assumptions, constraint groups, projections, external handles.
- Duplicate definition of a name → INVALID_INPUT(duplicate-definition: name).
- Every identifier reference must resolve to a declaration in scope;
  otherwise → INVALID_INPUT(unbound-identifier: name).
- `assuming [a₁, …]`: each must name an `assume` or `axiom` declaration;
  otherwise → INVALID_INPUT(unbound-assumption-reference: name).
- Constraint-group references in goals must name `constraints` groups;
  projection references must name `projection` declarations; a
  `projection-path` must resolve against the model context, else
  INVALID_INPUT(projection-path-unresolvable: path).
- A `compare-models` goal without an `under` clause is
  INVALID_INPUT(missing-required-projection) — the engine must not guess the
  intended projection.
- In `check f of h`: `f` must be a defined function of type `(In, Out) -> Bool`;
  `h` must have type `Impl(In -> Out)` with matching `In`/`Out`.
- In constraint groups used by `construct`/`compare-models`, `output` is a
  reserved identifier bound to the object under construction (typed by the goal's
  target type).

### B.6 Assumptions: declaration, reference, and roles

Named assumptions close the v0.2 gap (`assume` created no referenceable entity):

- `assume name: P` declares a named premise. `prove … assuming [name, …]`
  resolves each name; the proved proposition is established **relative to** that
  assumption context, which is recorded in the result.
- Semantic roles (not interchangeable):
  - **`assume`**: taken as given; tracked in the assumption set; never checked
    by the engine; adequacy is a human freeze-gate judgment.
  - **`require`**: must hold of the constructed/checked/found object; checked;
    violation → VIOLATED / NO_SOLUTION / constraint failure as applicable.
  - **`forbid`**: must not hold; checked symmetrically.
  - **`prove`**: the proposition the engine is asked to establish (relative to
    assumptions). A PROVED result names the exact proposition and its assumption
    context.

### B.7 Verification-policy syntax

- Proof and test requirements are syntactically separate (`proof:` vs `test:` items).
- Multiple checkers/methods permitted as separate items.
- Duplicate identical items → INVALID_INPUT(duplicate-verification-item).
- `proof: none` together with `proof: kernel-checked …` →
  INVALID_INPUT(conflicting-verification-requirements). Same for `test:`.
- Qualifier `required` (default) vs `optional`: a `required` method that cannot
  run → the run reports INCONCLUSIVE or a shortfall; an `optional` method that
  cannot run is skipped and recorded as skipped.
- CheckerIDs are `name/version`; the version pins the checker for provenance.

### B.8 Resource limits

- `timeout` **mandatory**; missing → INVALID_INPUT(missing-mandatory-timeout).
- Type `Duration`; legal range **1s … 24h**; outside →
  INVALID_INPUT(timeout-out-of-range). `0s`/negative impossible lexically; a
  `steps: 0` → INVALID_INPUT(degenerate-resource-limit).
- `memory`, `steps` optional, combinable with `timeout`; each independently validated.

### B.9 Admission and error catalog

INVALID_INPUT reasons (exact strings): `not-a-formal-specification`,
`missing-header-field`, `duplicate-header-field`, `syntax-error`,
`unbound-identifier: <name>`, `duplicate-definition: <name>`,
`type-mismatch: expected <T>, found <U>`, `missing-required-projection`,
`unbound-assumption-reference: <name>`, `missing-mandatory-timeout`,
`timeout-out-of-range`, `degenerate-resource-limit`,
`duplicate-verification-item`, `conflicting-verification-requirements`,
`missing-goal`, `projection-path-unresolvable: <path>`.
UNSUPPORTED reasons: `scope-not-supported`, `construct-not-decidable-for-proof`.

### B.10 Natural-language handling (hard rule)

NL drafts candidate specifications under human supervision. **An unreviewed
assumption extracted from an NL draft must NEVER appear in an executable
specification** — not even labelled. It may live only in review artifacts as a
proposal. Execution requires explicit human incorporation into the frozen formal
specification.

### B.11 Valid examples (one per goal form; all parse under §B.3)

**derive:**
```
spec tiny-derive
version 0.3.0
scope exact-arithmetic
authors ["example"]
goal derive (2 * 21) + 1
verification { proof: none; }
limits { timeout: 10s; }
record: all
```

**construct:**
```
spec tiny-construct
version 0.3.0
scope finite-search
authors ["example"]
type Pair = { x: Nat, y: Nat }
constraints positive {
  require px: output.x > 0;
  require py: output.y > 0;
}
goal construct Pair satisfying [positive]
verification { proof: none; test: none; }
limits { timeout: 10s; }
record: all
```

**prove:**
```
spec tiny-prove
version 0.3.0
scope kernel-proofs
authors ["example"]
axiom add_zero: forall n in Nat :: n + 0 == n
goal prove forall n in Nat :: n + 0 == n assuming [add_zero]
verification { proof: kernel-checked by lean-kernel/4.9.0 required; }
limits { timeout: 60s; }
record: all
```

**check** (selector — the normative example; contract in Appendix 2):
```
spec selector-contract
version 0.3.0
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
  (forall c in cs :: len(c.uci) > 0) /\
  (forall c in cs :: forall d in cs :: ((c.uci == d.uci) ==> (c == d))) /\
  (forall c in cs :: is_finite(c.score))

define contract_holds(candidates: CandidateSet, output: Candidate): Bool =
  is_wellformed(candidates) /\
  (exists c in candidates :: output.uci == c.uci) /\
  (forall c in candidates :: prefers(output, c) \/ (output == c))

define selector_impl: Impl(CandidateSet -> Candidate) = external("selector-impl/0.3.0")
define indie_ref_impl: Impl(CandidateSet -> Candidate) = external("independent-ref-impl/0.3.0")

goal check contract_holds of selector_impl

verification {
  proof: none;
  test: differential by indie-ref-impl/0.3.0 required;
  test: property-fuzz { seeds: [1, 2, 3], cases: 10000 } required;
}
limits { timeout: 300s; memory: 2GB; }
record: all
```

**compare-models:**
```
spec tiny-models
version 0.3.0
scope finite-constraint-models
authors ["example"]
type M = { x: Nat }
constraints two_vals {
  require xv: (output.x == 1) \/ (output.x == 2);
}
projection xproj = [output.x]
goal compare-models satisfying [two_vals] under xproj
verification { proof: none; test: none; }
limits { timeout: 10s; }
record: all
```

### B.12 Invalid examples (each rejected with the exact reason)

1. A natural-language paragraph ("select the best move please") →
   INVALID_INPUT(not-a-formal-specification).
2. `goal compare-models satisfying [two_vals]` with no `under` →
   INVALID_INPUT(missing-required-projection).
3. `goal prove P assuming [ghost_asm]` → INVALID_INPUT(unbound-assumption-reference: ghost_asm).
4. Specification without `limits` → INVALID_INPUT(missing-mandatory-timeout).
5. Two `define foo` declarations → INVALID_INPUT(duplicate-definition: foo).
6. `require r: output.zzz == 1` where `zzz` is not a field →
   INVALID_INPUT(type-mismatch: expected field of Candidate, found zzz).
7. `limits { timeout: 0s; }` → INVALID_INPUT(degenerate-resource-limit).
8. `goal check contract_holds of missing_impl` →
   INVALID_INPUT(unbound-identifier: missing_impl).

---

## C. Supported problem classes

The capability matrix (`MSVE_CAPABILITY_MATRIX_v0.3.md`) is normative. v0 target
dispositions (all at maturity DESIGN_ONLY):

Exact integer/rational arithmetic — Supported. Symbolic computation (SymPy-backed)
— Supported within §F.4 limits. Finite constraint systems, decidable fragments
(e.g. QF_LIA) — Supported. General/nonlinear SMT — Restricted (unknown →
INCONCLUSIVE(SOLVER_UNKNOWN)). Model construction/witnesses — Supported where
the solver provides models. Uniqueness checking — Supported via §D within
decidable fragments. Proof checking (Lean kernel) — Supported; formalization is
human-reviewed. Implementation-contract assurance — L1/L2/L3 (§D.1). Code
generation — Restricted to the v0 generator class (§D.7). Inferring missing
historical data — FORBIDDEN. Predicting real-world performance — OUT OF SCOPE.
Inventing objective functions — OUT OF SCOPE.

---

## D. Assurance levels, uniqueness, and generation scope

### D.1 Three assurance levels

- **L1 — Mathematical model.** Properties of the abstract algorithm under explicit
  assumptions (proof or sound procedure).
- **L2 — Implementation conformance.** Named method (checked refinement,
  translation validation, static analysis, or documented limited method) linking
  model to code. L1 alone establishes nothing about code.
- **L3 — Tested behaviour.** Regression, differential, property-based, fuzzing —
  bounded to executed inputs.

Where v0 provides no method for a promised guarantee: narrow the guarantee, mark
RESTRICTED, or label FUTURE.

### D.2 Uniqueness decision procedure (per supported class)

1. Satisfiability → else CONTRADICTION (assurance per §F.5).
2. Declared projection (absent → INVALID_INPUT).
3. Second-model query: assert ⋁ᵢ(πᵢ(m₂) ≠ πᵢ(m₁)) with exact inequality on
   canonical forms; re-solve. Second model → UNDERDETERMINED with witnesses.
4. UNIQUE_UNDER_PROJECTION only if the query is UNSAT **and** the procedure is
   complete for the class; record procedure, guarantees, and assurance achieved.
5. Otherwise INCONCLUSIVE with reason code; uniqueness not established.

### D.3 Exact distinctness

Projection equality is exact over canonical forms (transitive by construction):
selection projection compares UCI strings exactly; probability-output projection
compares canonicalized binary64 sequences bitwise; no tolerance-based
equivalence. A future tolerance-based witness comparison must be specified
separately and never described as the projection equality.

### D.4 Uniqueness-restoring assumptions

v0 tests only user-supplied or declared-finite-family candidate assumptions and
reports which restore uniqueness. Mathematically sufficient ≠ empirically
justified; only the human author may assert the latter.

### D.5 The v0 generator class (Correction E)

v0.2's "pure total functions over finite enumerable domains" is corrected: as
stated it **excludes the selector** (String inputs; unbounded class of finite
lists). v0.3 adopts the parametric-template approach:

**v0 generator class:** template-based generation for total functions defined by
structural recursion over finite lists/collections, where:
- element types come from the permitted set (base types, records/lists/sets/options thereof);
- the template is fixed, reviewed, and frozen;
- recursion is structural (termination by construction);
- operation contracts (e.g., the comparator's total-order obligations) are proof
  obligations on the specification author, discharged at L1;
- generation = template instantiation; output re-checked against the contract (L2).

The design distinguishes, explicitly:
- a **finite collection** passed to one execution;
- a **finite input domain** containing all allowed inputs;
- an **unbounded class of finite collections** (the selector's input class).

The template handles the third via structural recursion, not enumeration. One
property never establishes the others.

**Scope note:** the first selector vertical slice proceeds as a
contract-verification case; code generation is **out of scope** for it (acceptance
plan states this explicitly). Any wider generator capability is FUTURE unless its
design and guarantees are established.

---

## E. Result-record schema (complete, Correction F)

### E.1 Rationale

v0.2 defined five fields but later referenced an `assurance` field outside the
schema, used one `verification` outcome for multiple checks, and had no typed
place for solver observations or partial results. v0.3 defines one authoritative
typed schema below. Fields not applicable to a goal type or lifecycle state are
marked inapplicable (not filled with dummy values).

### E.2 Schema

```
ResultRecord {
  admission: ACCEPTED | INVALID_INPUT(reason: ErrorCode) | UNSUPPORTED(reason: ErrorCode),
  execution: NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED
             | INTERNAL_ERROR(reason: String),
  semantic_result: SemanticResult,          # §E.3, per goal type
  solver_observation: Option<SolverObs>,    # §E.5; None when inapplicable
  assurance_required: NONE | LEVEL_A | LEVEL_B,      # from frozen Verification policy
  assurance_achieved: NONE | LEVEL_A | LEVEL_B_SOLVER_BACKED,
  assurance_shortfall: Bool,                # true iff required > achieved
  shortfall_description: Option<String>,
  verification_records: [VerificationRecord],  # §E.7, per property
  verification_summary: NOT_RUN | PASS | FAIL | INCONCLUSIVE | CHECKER_DIVERGENCE,
  evidence: EvidenceBundle,                 # §G.3
  partial_results: [PartialResult],          # established before timeout/interruption
  discrepancies: [Discrepancy],              # unresolved; each names required follow-up
}
SolverObs {
  outcome: SAT | UNSAT | UNKNOWN,
  tool: String, version: SemVer, config: String, provenance_ref: Hash,
  certificate_ref: Option<Hash>,   # Level A artifact where available
}
VerificationRecord {
  property: String,            # obligation identifier
  artifact: String,            # what was checked (impl id + version)
  spec_version: SemVer,
  method: String,              # e.g. differential-testing, kernel-check
  checker: CheckerID,
  result: PASS | FAIL | INCONCLUSIVE,
  reason: Option<String>,
  assurance_boundary: String,  # what the method does/does not establish
  inputs_ref: Hash,            # test inputs / proof artifact reference
}
```

Mandatory/optional/inapplicable:
- `solver_observation`: mandatory for solver-backed goals (construct/compare-models
  via SMT); inapplicable for pure `derive`/`prove` and for runs rejected at admission.
- `verification_records`: may be empty → `verification_summary` = NOT_RUN.
- `partial_results`: only when execution ∈ {TIMEOUT, INTERRUPTED} and something
  was independently established; otherwise empty.
- `assurance_required`: NONE when the Verification policy requires no assurance
  beyond execution (still recorded, not omitted).

### E.3 Semantic results per goal type

`derive`: DERIVED_VALUE · INCONCLUSIVE(reason).
`construct`: ARTIFACT_CONSTRUCTED · NO_SOLUTION · INCONCLUSIVE(reason).
`prove`: PROVED · DISPROVED · INCONCLUSIVE(reason).
`check`: HOLDS · VIOLATED (counterexample witness) · INCONCLUSIVE(reason).
`compare-models`: UNIQUE_UNDER_PROJECTION · UNDERDETERMINED (witnesses) ·
CONTRADICTION · INCONCLUSIVE(reason).

### E.4 INCONCLUSIVE reason codes

SOLVER_UNKNOWN · PROCEDURE_INCOMPLETE · RESOURCE_EXHAUSTED ·
EXECUTION_INTERRUPTED · ASSURANCE_REQUIREMENT_UNMET. Each has a distinct
evidential meaning; they are never merged.

### E.5 Solver observations vs conclusions (Correction C)

Three distinct things, never conflated:
- **Solver observation**: SAT / UNSAT / UNKNOWN as returned by the procedure,
  with tool identity, version, configuration, provenance (§E.2 SolverObs).
- **Semantic result**: the conclusion MSVE is justified in reporting under the
  requested assurance policy.
- **Assurance achieved**: the method and trust boundary actually supporting it.

**UNSAT rule.** If the solver reports UNSAT:
- assurance_required = LEVEL_A and only Level B available →
  `semantic_result` = INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET);
  `assurance_shortfall` = true; the solver observation and Level B evidence are
  preserved with provenance. The requested contradiction is **refused**, not lowered.
- assurance_required = LEVEL_B (explicitly accepted in the frozen spec) →
  `semantic_result` = CONTRADICTION with `assurance_achieved` =
  LEVEL_B_SOLVER_BACKED, clearly attached. The two cases are not equivalent.
- Unsatisfiable cores remain diagnostic evidence only — never an independently
  checked proof of unsatisfiability.

### E.6 v0 assurance policy (Correction C — Level A eligibility)

No invented certificates. v0 eligibility:
- **Level A eligible**: `prove` goals discharged by Lean kernel (artifact: kernel-checked
  proof term; independent check: kernel re-run); `derive` goals with exact arithmetic
  re-checked by an independent recomputation.
- **Level A for SMT UNSAT: FUTURE.** v0 establishes no independently checkable
  certificate pipeline for SMT unsatisfiability; do not claim solver proof output
  as a standard certificate. In v0, UNSAT-dependent conclusions
  (CONTRADICTION, UNIQUE_UNDER_PROJECTION via unsat second-model query) are
  Level B unless the request accepts it; a Level A demand yields
  INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET) by the refusal rule.
- Unsupported/unverified certificate formats are unavailable for Level A — stated,
  not silently used.

### E.7 Per-property verification and aggregation

Verification records are individually attributable (§E.2). The summary is computed
by a fixed rule and never hides an individual outcome:
1. No records → NOT_RUN.
2. Any record FAIL → FAIL.
3. Conflicting results on the same property from different checkers →
   CHECKER_DIVERGENCE (records preserved).
4. Any record INCONCLUSIVE (and none of the above) → INCONCLUSIVE.
5. Otherwise → PASS.

### E.8 Legal combinations (schema examples, not executed tests)

- Invalid input: admission=INVALID_INPUT(syntax-error), execution=NOT_STARTED,
  verification_summary=NOT_RUN.
- Unsupported: admission=UNSUPPORTED(scope-not-supported), execution=NOT_STARTED.
- Constructed, unverified: execution=COMPLETED,
  semantic_result=ARTIFACT_CONSTRUCTED, verification_summary=NOT_RUN.
- Completed but inconclusive: execution=COMPLETED,
  semantic_result=INCONCLUSIVE(SOLVER_UNKNOWN).
- Timeout after witness: execution=TIMEOUT, partial_results=[re-checked model
  m₁, labelled partial], semantic_result=INCONCLUSIVE(RESOURCE_EXHAUSTED).
- Level B UNSAT, Level A required: solver_observation={UNSAT,…},
  semantic_result=INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET),
  assurance_shortfall=true.
- Checker disagreement: two VerificationRecords on one property (PASS, FAIL) →
  verification_summary=CHECKER_DIVERGENCE; discrepancy recorded with follow-up.
- Split properties: records [PASS, FAIL] → summary FAIL; the PASS is preserved,
  not hidden.
- External evidence: evidence.external_evidence_records=[…],
  semantic_result per goal; no scientific conclusion asserted by MSVE (§E.9).

### E.9 External experimental evidence

Three-way split (retained): EVIDENCE_RECORDED (ingest with provenance; MSVE
asserts nothing about truth) / RECORD_INTEGRITY assessment (PASS/FAIL on the
record's integrity) / EXTERNAL_ASSESSMENT (who concluded what, on what basis —
never promoted by MSVE into a confirmed result).

### E.10 Anti-conflation rules (hard)

Solver `unknown`/interruption/timeout never reported as CONTRADICTION or
UNDERDETERMINED. Finite test suites never establish universal properties.
ARTIFACT_CONSTRUCTED ≠ verified. Verified ≠ experimentally successful.
COMPLETED ≠ PASS. Failed runs and spec changes remain distinguishable from
successes.

---

## F. Trust base and verification architecture

### F.1 Architecture

spec text → [Parser/Validator] → admission → [Review & freeze gate] →
[Dispatcher] → SymPy / Z3 / Lean / Independent checker → [Provenance recorder] →
result record + evidence bundle. Orchestration over established components; no
new solver in v0.

### F.2 Component table

Parser/validator (MSVE-owned): syntax/typing/mandatory fields; not semantics.
SymPy (pinned): see §F.3. Z3 (pinned): satisfiability in decidable fragments;
model witnesses (re-checked); `unknown` preserved. Lean kernel (pinned):
proof-term acceptance relative to formal statement/definitions/imports/axioms.
Independent checker (per case): behavioural agreement on tested inputs (L3).
Provenance recorder (MSVE-owned): content identity + integrity vs reference (§G);
not origin without the authenticity mechanism; not correctness.

### F.3 Symbolic computation

Computed (library produced the value; version+inputs recorded) /
independently checkable (re-verified by an independent path, e.g. substitution;
check run and recorded) / trusted-tool output (no v0 independent check;
labelled as relying on the pinned library within the trust boundary — never
described as formally verified derivation).

### F.4 SAT assurance

Witnesses re-checked against the canonical spec independently of the solver;
checker + version recorded; model and input hashes preserved.

### F.5 "Trusted" boundary

Relied upon without re-verification only within the documented boundary. Z3
models are checked, not trusted. The kernel is trusted for proof-term acceptance,
not formalization adequacy.

---

## G. Provenance, canonicalisation, maturity

### G.1 Separated provenance claims

1. **Content identity** — SHA-256 over the canonical form (§G.2); recomputable.
2. **Integrity relative to a trusted reference** — comparison against an
   independently preserved manifest/anchor reveals substitution.
3. **Authenticity** — origin claims only via the defined mechanism (v0:
   project-owner signed release tags, verified out-of-band; operational key
   management is a bounded implementation decision — §G.5).
4. **Correctness** — only via verification procedures, never via hashing.

Accurate claim: **"tamper-evident relative to a trusted reference"** — never
"tamper-proof".

### G.2 Canonical encoding profile `msve-canonical-1` (Correction G)

One deterministic profile; no alternatives within a version:

- **Envelope:** canonical JSON — UTF-8, object keys sorted bytewise by UTF-8
  encoding, no insignificant whitespace.
- **Strings:** JSON string escaping (minimal escapes; control characters as
  `\uXXXX`). Producers must supply NFC-normalized UTF-8; the canonicalizer does
  not normalize (non-conforming input → INVALID_INPUT at admission).
- **No bare JSON numbers.** Every numeric value is a typed object — this
  eliminates the string-vs-number ambiguity class entirely:
  - Integer: `{"$type":"int","value":"-12345"}` — decimal, optional leading `-`,
    no leading zeros, no `+`.
  - Rational: `{"$type":"rat","value":"-7/3"}` — lowest terms, positive denominator.
  - Binary64: `{"$type":"f64","value":"0x1.921fb54442d18p+1"}` — C99-style hexfloat,
    lowercase, normalized (`0x1.` + exactly 13 hex digits + `p` + signed decimal
    exponent without leading zeros); −0.0 → `"0x0.0000000000000p+0"`.
- **Signed zero:** normalized to +0.0 before encoding.
- **Non-finite values:** not encodable; rejected where prohibited (admission).
- **Type safety:** `{"$type":"int","value":"12"}` ≠ `"12"` ≠ `12` — different
  types never collide through serialization.
- **Digest:** SHA-256 over the exact UTF-8 bytes of the canonical form.
- **Versioning:** profile identifier `msve-canonical-1` recorded in every package.

### G.3 Result package contents

The result record (§E.2) plus: spec identity/version/hash; canonicalized input
hashes; exact tool/solver/checker versions + configuration; derivation records,
witnesses, proof artifacts; test inputs, seeds, fuzz conditions; output hashes;
human-reviewed assumption set; failure records and unresolved issues;
supersession records. Failed attempts and revisions preserved; re-verification
required after spec/tool changes; prior results superseded, not deleted.

### G.4 Unified maturity vocabulary (Correction H)

One shared ladder used identically in §J, the matrix, the acceptance plan, the
review, and diagrams:

1. **Designed** — contract written; failure behaviour specified; in the matrix.
2. **Implemented** — exists with documented interface; versioned.
3. **Functionally verified** — acceptance suite (normal, boundary,
   expected-failure) green and recorded.
4. **Formally verified** — kernel-checked proof or sound procedure + artifacts;
   or **N/A with recorded reason** (e.g., "no universal claim made") — never
   misleadingly labelled.
5. **Integrated and reproducible** — composes with declared components; versions
   pinned; re-runs reproduce (bit-for-bit modulo declared non-determinism).
6. **Independently reproduced** — separate party/machine reproduces from the
   package alone. (Distinct from 5: integration is about composition; 6 about
   independent confirmation.)
7. **Released** — all declared matrix entries at claimed maturity; limitations
   documented; scope+version-qualified claims evidenced.

Stages 1–3 and 5 are sequential; 4 may be N/A (recorded); 6 requires 5; 7
requires all applicable prior stages. Evidence required per stage is defined by
the advancement criteria above; a claim advances only on that evidence.

### G.5 Version transition policy

Changing canonicalisation rules requires a profile version bump
(`msve-canonical-2`, …). During transition, hashes under both profiles are
recorded; old hashes are never silently reinterpreted under new rules. The
authenticity mechanism's operational details (key management, rotation) are
bounded implementation decisions; no stronger origin claim than the defined
mechanism permits.

---

## H. Governance and capability authorisation

Authority: project owner approves/revises/rejects the design; freezes specs;
authorizes repository creation (after design freeze), implementation (separate
explicit authorization), and release declaration on evidence. MSVE is a separate
capability track from research projects and from àfi_adaptive. Tool use against
a separately authorized task grants no modification rights (read-only unless the
task's authorization says otherwise). Repository genesis rule: the reviewed,
frozen design specification is the genesis commit.

---

## I. Acceptance plan summary

Normative: `MSVE_ACCEPTANCE_PLAN_v0.3.md`. End-to-end conceptual steps:
(1) parse/validate the frozen spec; (2) produce and assess the abstract selector
and validator contracts; (3) establish L1 properties; (4) identify the actual L2
method per claim or mark unavailable; (5) run L3 checks if a later work order
permits execution; (6) emit the result record + evidence package under §E.2;
(7) assess what was established beyond the Order 7 panel. The vertical slice
remains proposed until separately authorized; code generation is out of scope
for it.

---

## J. Release gates (unified vocabulary)

| Gate | Criterion (uses §G.4 terms) |
|---|---|
| 1. Designed | Frozen spec (genesis commit); language, output contract, scope defined; reviewed |
| 2. Implemented | Every claimed operation exists with documented interface; no phantoms |
| 3. Functionally verified | Acceptance suite green: normal, boundary, expected-failure cases |
| 4. Formally verified (where applicable) | Kernel-checked proofs or sound procedures + artifacts; or N/A with reason |
| 5. Integrated and reproducible | Composes; versions pinned; re-runs reproduce |
| 6. Independently reproduced | Separate party/machine reproduces from the package |
| 7. Released | Matrix entries at claimed maturity; limitations documented; qualified claims evidenced |

**Completion rule:** no capability is complete merely because components exist.
Every advertised operation needs contract, acceptance tests, failure behaviour,
and evidence. Unsupported/unproven/untested capabilities stay explicitly
labelled; failed operations stay visible.

---

## Appendix 1. Glossary (v0.3)

- **Specification / frozen specification:** as v0.2.
- **Comparator:** the explicit preference relation for the selector (§App.2.2);
  not a maximizable key tuple.
- **Admission validator:** the object receiving serialized/structured input,
  checking form and types, establishing well-formedness or rejecting
  (separate contract from the abstract selector).
- **Abstract selector:** pure function on well-formed candidate sets.
- **Solver observation:** SAT/UNSAT/UNKNOWN as returned, with tool provenance —
  distinct from the semantic conclusion (§E.5).
- **Assurance required/achieved/shortfall:** the requested minimum, what was
  actually established, and whether they differ (§E.2).
- **Verification record:** per-property attributable check (§E.2); the summary
  is computed and never hides an individual outcome (§E.7).
- **Canonical profile `msve-canonical-1`:** the deterministic encoding of §G.2.
- **Maturity:** the seven-stage demonstrated-evidence ladder (§G.4), separate
  from target disposition.
- **EVIDENCE_RECORDED:** external evidence ingested with provenance; MSVE asserts
  nothing about its truth.

## Appendix 2. Formal selector contract v0.3 (Correction A)

*Normative for the acceptance plan. Proposed — to be frozen before any execution.*

**A2.1 Types.** `Candidate = { uci: String, rank: Nat, score: Binary64 }`;
`CandidateSet = [Candidate]`. Binary64: IEEE-754 binary64; −0.0 normalized to
+0.0; NaN/±∞ not representable in a well-formed candidate.

**A2.2 Comparator (replaces the v0.2 key tuple).** Define the strict preference
`prefers(a, b)`:
1. `a.score > b.score`, or
2. `a.score == b.score` and `a.rank < b.rank`, or
3. `a.score == b.score` and `a.rank == b.rank` and `a.uci < b.uci`
   (bytewise lexicographic over UTF-8; §B.4a).

`output` is the unique `prefers`-maximal element of the candidate set.
*Why not a key tuple:* maximizing `(score, −rank, uci)` selects the
lexicographically **greatest** UCI on ties — the v0.2 error. The three
preferences have mixed directions (max, min, min); no single maximization
encodes them without an order-reversing map on strings, which the contract does
not define. The explicit comparator is the unambiguous specification.

**A2.3 Uniqueness.** Each component order is a strict total order on its domain
(binary64 exact order on finite values; Nat; bytewise string order); their
lexicographic composition is a strict total order. With pairwise-distinct UCIs,
trichotomy holds for any two candidates; hence every non-empty well-formed
candidate set has exactly one maximal element. (L1 proof obligation.)

**A2.4 Membership.** `∃c ∈ C : output.uci = c.uci`.

**A2.5 Admission (validator contract).** The admission validator accepts a raw
input iff: the candidate set is non-empty; every `uci` is a non-empty ASCII
printable string without whitespace; UCIs are pairwise distinct; every `rank`
is a Nat; every `score` is finite. Otherwise it rejects, naming the defect.
Rejection of invalid inputs is a property of this validator object — not of the
abstract selector (Correction D).

**A2.6 Numeric semantics.** Scores compared as canonicalized binary64 with exact
comparison; equality = bitwise equality of canonical forms; no tolerance. Used
for ranking only — no calibration claim; no sum/normalization constraint unless
declared.

**A2.7 Determinism.** Selection is a pure function of the candidate set.

**A2.8 Historical comparison (corrected).** The comparator was checked against
the preserved Order 7 adapter source: higher probability, then lower
Stockfish rank, then lexicographically smaller UCI (`a.uci < b.uci ? -1 : …`),
with exact float equality for tie detection. **The corrected contract matches
the observed Order 7 behaviour**, including the 11 tie cases. The v0.2 claim of
"no mismatch" was unsound because the v0.2 formula itself was wrong; the
corrected statement is: the *implementation's* observed behaviour matches the
*corrected* contract. Edge-case rules beyond the historical record (non-finite
rejection, −0.0 normalization, duplicate-UCI rejection, empty-string rejection,
ASCII restriction) are new explicit contract proposals, not historical facts,
and are labelled as such.

## Appendix 3. Unresolved design decisions

1. Lean version + proof-carrying interface format (carried).
2. Full v0 problem-class catalog beyond the matrix (carried; matrix authoritative).
3. Per-class timeout/memory defaults (carried; set at implementation authorization).
4. Widening the v0 generator class beyond structural-recursion templates (new).
5. Signed-tag key management operations (bounded implementation decision).

*End of MSVE_DESIGN_SPEC_v0.3.md (draft for review — not frozen).*
