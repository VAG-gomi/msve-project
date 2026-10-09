# MSVE Design Specification v0.7

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.6.md` (retained as historical draft;
release gate: BLOCKED)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** v0.7 targeted correction pass (D-016–D-024; D-001–D-015 kept)
**Review authority:** Project owner · **Version:** 0.7 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

**Self-containment note.** This document reproduces every normative definition
needed to interpret v0.7. The v0.6 package is superseded, not depended upon.
Changes are recorded in `MSVE_REGRESSION_LEDGER_v0.7.md`.

**Change summary (v0.6 → v0.7).** Targeted corrections, architecture preserved:
- D-016: `is_some` added to builtins; `range` semantics defined; structural
  equality defined recursively over records/lists/options; identifier audit.
- D-017: binary64 canonical form made truly unique — leading digit exactly
  `1` for normals, one subnormal form (`p-1074`), no exponent leading zeros;
  `msve-canonical-3` supersedes canonical-2 (defective before any use).
- D-018: function values not encodable in v0 (named reason); `Impl` encoding
  carries its signature; ±infinity encodable; NaN not encodable.
- D-019: `Real` uses exact rational payloads under the `Real` tag — every v0
  `Real` is encodable; `to_rat: Real -> Rat` is total; unserializable valid
  results get a distinct packaging outcome, never INVALID_INPUT.
- D-020: `ErrorCode` genuinely closed via the `is_error_code` predicate +
  contract conjunct; `DecodeOutcome` invariant stated normatively.
- D-021: `recompute:` is its own verification item, separated from `proof:`.
- D-022: `SemanticResult` alternatives carry payloads; §E.7 invariants made
  exhaustive; `Discrepancy.involved_records` and `ExternalEvidence.recorded_at`
  defined; Level B ⇒ explicit spec acceptance invariant.
- D-023: (visualisation plan) all diagram sources reproduced.
- D-024: duplicate verification items defined precisely.

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*: domain-agnostic within the formal scope
defined by the input language (§B) and the capability matrix
(`MSVE_CAPABILITY_MATRIX_v0.7.md`). Outside the declared scope: UNSUPPORTED.

### A.2 Intended users

Users who need mathematical claims checked, constructed or evidenced with the
reasoning made explicit: researchers, engineers and reviewers who must defend
what was established, by which method, and what remains unknown.

### A.3 The three non-eliminable judgments

1. **Domain judgment** — what the mathematics means and whether the
   formalization is adequate (human, recorded as assumptions).
2. **Construction judgment** — which object, proof or computation to attempt
   (human or heuristic, recorded as the specification).
3. **Empirical uncertainty** — what the world does (recorded as external
   evidence, never upgraded by MSVE into proof).

### A.4 Scope-qualified "all-rounder"

"All-rounder within scope S, matrix vX.Y" requires every capability the matrix
marks SUPPORTED for S to reach maturity stage 7 (Released) with evidence. The
matrix is normative for this claim.

### A.5 Non-goals

MSVE does not: invent domain semantics; certify its own implementation;
predict real-world performance from formal correctness; execute unreviewed
specifications; or extend an experimental sequence merely because another step
is possible.

---

## B. Formal input language (complete v0.7 definition)

### B.1 Design rules

1. Minimal, machine-readable; natural language never drives execution (§B.12).
2. Specifications carry identity and version; frozen specifications are immutable
   content-hashed baselines.
3. This section is the **complete normative syntax**. §B.11 gives valid examples;
   §B.12 gives invalid examples with exact rejection reasons. Quantifier scope,
   `let`, `case` and constructor rules are in the grammar itself.

### B.2 Lexical rules

```
Ident     := [A-Za-z_][A-Za-z0-9_]*
Slug      := [A-Za-z0-9_]+(-[A-Za-z0-9_]+)*
String    := '"' ( [^"\\\u0000-\u001F] | Esc )* '"'
Esc       := "\\" ( "\"" | "\\" | "/" | "b" | "f" | "n" | "r" | "t"
                   | "u" Hex Hex Hex Hex )
Hex       := [0-9a-fA-F]
Nat       := [0-9]+
RealLit   := Nat "." Nat
SemVer    := Nat "." Nat "." Nat
Duration  := Nat ("ms" | "s" | "min" | "h")
MemSize   := Nat ("B" | "KB" | "MB" | "GB")
CheckerID := Slug "/" SemVer
```

Keywords (reserved): `spec version scope authors type define axiom assume
constraints require forbid projection goal derive construct satisfying prove
assuming check of compare-models under verification proof recompute test none
kernel-checked by differential property-fuzz seeds cases required optional
assurance level-a level-b accepted limits timeout memory steps record all
external spec-hash input-hash tool-versions witness outputs true false if
then else forall exists in let case of some type`.

`output` is not a keyword; it is a special context variable (§B.5a).
`independent-recompute` is removed as a `proof:` alternative (D-021); the
`recompute:` item replaces it.

Whitespace insignificant except in strings. Blocks tolerate trailing `;`.
Comments: `//` to end of line.

**Parsing notes.** Operator precedence, tightest first: unary (`!`, `-`);
multiplicative (`*`, `/`); additive (`+`, `-`); comparison; `==>`; `/\`; `\/`.
Parentheses override. `case` and `let` are in `Atom` and bind as written.

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
VerifItem      := ProofReq | RecomputeReq | TestReq | AssuranceReq
ProofReq       := "proof" ":" ("none" | "kernel-checked" "by" CheckerID Qualifier)
RecomputeReq   := "recompute" ":" ("none" | "by" CheckerID Qualifier)
TestReq        := "test" ":" ("none"
                   | "differential" "by" CheckerID Qualifier
                   | "property-fuzz" FuzzConfig Qualifier)
AssuranceReq   := "assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")
Qualifier      := ("required" | "optional")?
FuzzConfig     := "{" "seeds" ":" "[" Nat ("," Nat)* "]" ","
                  "cases" ":" Nat "}"

ResourceLimits := "limits" "{" "timeout" ":" Duration ";"
                   ("memory" ":" MemSize ";")? ("steps" ":" Nat ";")? "}"
ProvenanceReq  := "record" ":" ("all" | "[" ProvItem ("," ProvItem)* "]")
ProvItem       := "spec-hash" | "input-hash" | "tool-versions" | "witness" | "outputs"

TypeExpr       := "String" | "Nat" | "Int" | "Real" | "Rat" | "Binary64" | "Bool"
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
                | "let" Ident "=" Expr "in" Expr
                | "case" Expr "of" "some" "(" Ident ")" "->" Expr
                  "|" "none" "->" Expr
                | "some" "(" Expr ")"
                | "forall" Ident "in" Domain "::" "(" Proposition ")"
                | "exists" Ident "in" Domain "::" "(" Proposition ")"
Domain         := "type" TypeExpr | Expr
Literal        := String | Nat | RealLit | "true" | "false" | "none"
Proposition    := Expr        # required type: Bool
Predicate      := Expr        # required type: Bool
```

Quantifier bodies are parenthesized in the grammar itself; the bare form is a
syntax error.

### B.4 Type system and type-checking rules

Base types: `String Nat Int Real Rat Binary64 Bool`. Records, lists, sets,
options, `Impl(A -> B)`, function types.

1. Every `Expr` has a unique type. Literals: strings→`String`; digits→`Nat`;
   `RealLit`→`Real` (exact decimal value); `true/false`→`Bool`;
   `"none"`→`Option<T>` (T from context, else type error).
2. **Arithmetic.** `+ - *`:
   - Same-type operands: `Nat`/`Int`/`Real`/`Rat`/`Binary64` with matching types.
   - **Mixed `Nat`/`Int`:** the one explicit exact embedding — the `Nat`
     operand is treated as `Int`; result `Int`. The only permitted
     cross-type arithmetic; all other mixed-type arithmetic → type error.
   - `/`: same-type operands; `Nat`/`Int` division is **exact division** —
     a non-exact quotient is an execution error (`INTERNAL_ERROR`, reason
     `inexact-division`); division by zero is an execution error
     (`division-by-zero`). `Real`/`Rat` division is exact rational division.
     `Binary64` follows IEEE 754 (division by zero → ±infinity).
   - **2a. Unary minus:** `-e` well-typed iff `e: Nat|Int|Real|Rat|Binary64`;
     result: `Nat→Int`, `Int→Int`, `Real→Real`, `Rat→Rat`,
     `Binary64→Binary64` (IEEE negation; canonicalization applies §G.2).
     `-5` denotes `Int(-5)`; `-3 + 2 : Int` denotes `-1`.
   - `!e` requires `Bool`.
3. **Equality (D-016).** `==`/`!=` require the same type; equality is
   structural, defined recursively:
   - base types: value equality (`Binary64`: equality of canonical forms;
     `Real`/`Rat`: exact rational equality);
   - records: same fields, pairwise equal;
   - lists: same length, pairwise equal in order;
   - options: `none == none`; `some(a) == some(b)` iff `a == b`;
     `some(_) != none`;
   - sets: equality as sets (order-insensitive), defined via the canonical
     form;
   - `Impl` handles: equality of (descriptor, signature) pairs.
   Ordering `< <= > >=`: `Nat Int Real Rat Binary64 String`.
4. `String` ordering: bytewise lexicographic over UTF-8 (§B.4a).
5. Boolean connectives on `Bool`. `==>` is **classical implication**;
   its meaning never depends on evaluation order.
6. `if`: `Bool` condition, equal branch types. `let x = e1 in e2`: `e1: T1`,
   `e2: U` under `x: T1`; result `U`.
7. `case e of some(x) -> e1 | none -> e2`: `e: Option<T>`; `e1: U` under
   `x: T`; `e2: U`; result `U`. The total option eliminator.
   `some(e: T): Option<T>` (constructor syntax).
8. Quantifiers: domain is `type T` or a collection expression; the body is
   parenthesized (§B.3) and `Bool`.
9. `e.f`: record field; `e[i]`: list index (`i: Nat`; out of bounds is an
   execution error). Chained via Postfix.
10. Application: exact argument-type match.
11. Builtins (D-016: complete inventory — every builtin used in §B.11 is
    listed here):
    - `len: [T]->Nat` — list length.
    - `range: Nat->[Nat]` — `range(n) = [0, 1, …, n-1]`; `range(0) = []`.
    - `is_finite: Binary64->Bool` — false for ±infinity and NaN.
    - `is_ascii_printable: String->Bool`; `has_no_whitespace: String->Bool`.
    - `is_some: Option<T>->Bool` — true iff the value is `some(_)`.
    - `to_rat: Real -> Rat` — **total** (D-019): every v0 `Real` is an exact
      rational; returns it in lowest terms. (Replaces v0.6's `to_rat_exact`.)
    - `decode_candidates: RawInput -> DecodeOutcome` — the abstract decoding
      relation, specified normatively in §B.13.
12. `external("…")`: opaque `Impl` handle; only usable as a `check` target.

**B.4a String order.** Bytewise lexicographic over UTF-8. Input strings must
be NFC-normalized; non-normalized strings in hashed artifacts →
INVALID_INPUT(string-not-normalized) at admission. The parser never silently
normalizes.

### B.13 Abstract decoding relation

`decode_candidates` maps a raw string to a `DecodeOutcome`:

```
type RawInput = String
type DecodeOutcome = { ok: Bool, candidates: [Candidate], error: Option<ErrorCode> }
```

`Candidate = { uci: String, rank: Nat, score: Binary64 }`;
`ErrorCode = String` (closed per §B.13a). On every `ok=false` row,
`candidates` is `[]`.

**Normative invariant (D-020):** a `DecodeOutcome` with `ok=true` has
`error=none`; with `ok=false` has `error=some(e)` for an `is_error_code`
`e` and `candidates=[]`. The §B.11 contract's first clause makes any
violation fail the contract (the decoder is then faulty).

| # | Input condition | Outcome |
|---|---|---|
| 1 | Not well-formed JSON (RFC 8259), including trailing data | `ok=false`, `malformed-json` |
| 2 | Top-level is not an array | `ok=false`, `invalid-top-level` |
| 3 | Array element is not an object | `ok=false`, `invalid-element` |
| 4 | Object has duplicate keys | `ok=false`, `duplicate-key` |
| 5 | Object missing `uci`/`rank`/`score` (checked in that field order) | `ok=false`, `missing-field` |
| 6 | Object has another field | `ok=false`, `unexpected-field` |
| 7 | `uci` not a string, or `rank`/`score` not a JSON number | `ok=false`, `invalid-field-type` |
| 8 | `rank`: JSON number not denoting a non-negative integer | `ok=false`, `invalid-rank` |
| 9 | `score`: JSON number whose binary64 rounding overflows | `ok=false`, `invalid-score` |
| 10 | Otherwise | `ok=true`, `candidates` in array order, `error=none` |

Conversion rules: **rank** — valid iff the exact value is a non-negative
integer (`1e2`→`100`; `1.0`→`1`; `1.5`,`-1` invalid; `-0`→`0`; `1e400` valid,
`Nat` is arbitrary precision). **score** — round-to-nearest-ties-even of the
exact decimal value; overflow → invalid; underflow → subnormal/zero per IEEE
(accepted); `-0` accepted (normalizes to `+0.0` at §G.2). **uci** — exact JSON
string, content unchecked here (semantic stage).

**D-012 boundary.** L1 validator claims are conditional on this table; they
do not establish that any implementation's parser implements it (L2).

#### B.13a Closed error codes (D-020)

```
type ErrorCode = String
```

The twelve constants below are the **only** inhabitants. Closure is enforced
by the predicate (every use site is checked against it):

```
define is_error_code(e: ErrorCode): Bool =
  (e == "malformed-json") \/ (e == "invalid-top-level") \/
  (e == "invalid-element") \/ (e == "duplicate-key") \/
  (e == "missing-field") \/ (e == "unexpected-field") \/
  (e == "invalid-field-type") \/ (e == "invalid-rank") \/
  (e == "invalid-score") \/ (e == "empty-candidate-set") \/
  (e == "invalid-uci") \/ (e == "duplicate-uci")
```

**Closure rule (normative):** any `ErrorCode`-typed value with
`is_error_code(e) = false` is rejected — at contract evaluation (the
§B.11 contract conjoins `is_error_code` on produced errors) and at
packaging. Membership test (M7): the disjuncts above are exactly the
§B.13 table's codes — verified mechanically.

### B.5 Name resolution and special variables

- Flat namespace per specification (types, definitions, axioms, assumptions,
  constraint groups, projections, external handles, builtins per §B.4 rule 11).
  Duplicates → INVALID_INPUT(duplicate-definition: name). Unresolved →
  INVALID_INPUT(unbound-identifier: name).
- `assuming […]`: names must resolve to `assume`/`axiom` declarations.
- Constraint-group references must name `constraints` groups; projection
  references must name `projection` declarations; projection paths resolve
  against the goal's model type (§B.5a).
- `check f of h`: `f: (In, Out) -> Bool`; `h: Impl(In -> Out)`; types must match.

**B.5a Special variable `output`.** In constraint groups referenced by
`construct` goals, `output` is bound to the object under construction, typed
by the goal's explicit target type. In `compare-models` goals, `output` is
bound to the model, typed by the goal's explicit model type, and projection
paths type-check against that type.
`define output …` → INVALID_INPUT(reserved-context-name). No other positions
bind `output`.

**B.5b Check-goal invocation rule.** For `goal check f of h`,
`f: (In, Out) -> Bool`, `h: Impl(In -> Out)`: the engine determines the input
corpus from the Verification test policy. For each input `i`:
`o = invoke(h, i)`; evaluate `f(i, o)`. HOLDS iff the corpus is **non-empty**
and every evaluation is true; the first failing `(i, o)` is the witness for
VIOLATED. Empty corpus → INCONCLUSIVE(NO_TEST_CORPUS). Test-based checking is
corpus-bound (L3); universal implementation claims need L2 methods (§D.1).

### B.6 Assumption roles

- **`assume name: P`**: premise; tracked; never checked; adequacy is human judgment.
- **`require`**: must hold of the object; checked.
- **`forbid`**: must not hold; checked.
- **`prove`**: proposition to establish relative to the `assuming` context; PROVED
  names proposition + context.

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
  items; two `recompute:` items; two `test: differential …` items; two
  `test: property-fuzz …` items; two `assurance:` items. Checker-ID
  differences do not distinguish. `test: differential …` + `test:
  property-fuzz …` are **not** duplicates (different methods) — the §B.11
  selector example is legal. Duplicates →
  INVALID_INPUT(duplicate-verification-item).
- Required-but-unrunnable → shortfall handling (§E.1); optional-but-unrunnable →
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
`projection-path-unresolvable: <path>`, `string-not-normalized`.
(`real-not-encodable` removed: every v0 `Real` is encodable, D-019.)
UNSUPPORTED: `scope-not-supported`, `construct-not-decidable-for-proof`.

### B.10 Natural-language handling (hard rule)

NL drafts candidates under human supervision. Unreviewed NL-extracted
assumptions NEVER enter executable specifications. Review artifacts only.

### B.11 Valid examples

**derive** (recomputation as its own item, D-021):
```
spec derive-level-a
version 0.7.0
scope exact-arithmetic
authors ["example"]
goal derive (2 * 21) + 1
verification { proof: none; recompute: by recompute-checker/1.0.0 required; assurance: level-a required; }
limits { timeout: 10s; }
record: all
```

**construct:**
```
spec tiny-construct
version 0.7.0
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
version 0.7.0
scope kernel-proofs
authors ["example"]
axiom add_zero: forall n in type Nat :: (n + 0 == n)
goal prove forall n in type Nat :: (n + 0 == n) assuming [add_zero]
verification { proof: kernel-checked by lean-kernel/4.9.0 required; assurance: level-a required; }
limits { timeout: 60s; }
record: all
```

**check** (selector):
```
spec selector-contract
version 0.7.0
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
  (forall c in cs :: ((len(c.uci) > 0) /\ is_ascii_printable(c.uci) /\ has_no_whitespace(c.uci))) /\
  (forall i in range(len(cs)) :: (forall j in range(len(cs)) :: (((i == j) \/ (cs[i].uci != cs[j].uci))))) /\
  (forall c in cs :: (is_finite(c.score)))

define contract_holds(candidates: CandidateSet, sel: Candidate): Bool =
  is_wellformed(candidates) /\
  (exists c in candidates :: (sel == c)) /\
  (forall c in candidates :: ((prefers(sel, c) \/ (sel == c))))

define selector_impl: Impl(CandidateSet -> Candidate) = external("selector-impl/0.7.0")
define indie_ref_impl: Impl(CandidateSet -> Candidate) = external("independent-ref-impl/0.7.0")

goal check contract_holds of selector_impl

verification {
  proof: none;
  test: differential by indie-ref-impl/0.7.0 required;
  test: property-fuzz { seeds: [1, 2, 3], cases: 10000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; memory: 2GB; }
record: all
```

**compare-models:**
```
spec tiny-models
version 0.7.0
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

**validator check** (three-stage pipeline; D-020 closure conjunct):
```
spec validator-contract-check
version 0.7.0
scope input-validation
authors ["MSVE design team"]

type Candidate = { uci: String, rank: Nat, score: Binary64 }
type CandidateSet = [Candidate]
type RawInput = String
type ErrorCode = String
type DecodeOutcome = { ok: Bool, candidates: [Candidate], error: Option<ErrorCode> }
type ValidationOutcome = { accepted: Bool, candidates: Option<CandidateSet>, error: Option<ErrorCode> }

define ERR_EMPTY_SET: ErrorCode = "empty-candidate-set"
define ERR_INVALID_UCI: ErrorCode = "invalid-uci"
define ERR_DUPLICATE_UCI: ErrorCode = "duplicate-uci"

define is_error_code(e: ErrorCode): Bool =
  (e == "malformed-json") \/ (e == "invalid-top-level") \/
  (e == "invalid-element") \/ (e == "duplicate-key") \/
  (e == "missing-field") \/ (e == "unexpected-field") \/
  (e == "invalid-field-type") \/ (e == "invalid-rank") \/
  (e == "invalid-score") \/ (e == "empty-candidate-set") \/
  (e == "invalid-uci") \/ (e == "duplicate-uci")

define valid_uci(u: String): Bool =
  (len(u) > 0) /\ is_ascii_printable(u) /\ has_no_whitespace(u)

define has_dup_uci(cs: [Candidate]): Bool =
  exists i in range(len(cs)) :: (exists j in range(len(cs)) :: (((i != j) /\ (cs[i].uci == cs[j].uci))))

define rejected(e: ErrorCode): ValidationOutcome =
  { accepted: false, candidates: none, error: some(e) }

define accepted(cs: CandidateSet): ValidationOutcome =
  { accepted: true, candidates: some(cs), error: none }

define validate(cs: [Candidate]): ValidationOutcome =
  if len(cs) == 0 then rejected(ERR_EMPTY_SET)
  else if exists c in cs :: ((!(valid_uci(c.uci)))) then rejected(ERR_INVALID_UCI)
  else if has_dup_uci(cs) then rejected(ERR_DUPLICATE_UCI)
  else accepted(cs)

define validator_contract(raw: RawInput, out: ValidationOutcome): Bool =
  let d = decode_candidates(raw) in
  ((d.ok ==> ((!(is_some(d.error))) /\ (out == validate(d.candidates)))) /\
  ((!(d.ok)) ==> (is_some(d.error) /\
    (case d.error of some(e) -> ((is_error_code(e)) /\ (out == rejected(e))) | none -> false)))

define validator_impl: Impl(RawInput -> ValidationOutcome) = external("validator-impl/0.7.0")

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
11. `assurance: level-a required` with `proof: none; recompute: none` on a
    `derive` goal → INVALID_INPUT(conflicting-assurance-requirements).
12. Non-NFC string in a hashed artifact → INVALID_INPUT(string-not-normalized).
13. `test: property-fuzz { seeds: [1], cases: 0 }` →
    INVALID_INPUT(degenerate-fuzz-config).
14. `goal check contract_holds of selector_impl` with `test: none` only →
    admission ACCEPTED; at execution, empty corpus →
    INCONCLUSIVE(NO_TEST_CORPUS) (never vacuous HOLDS).
15. `forall c in cs :: P /\ Q` (bare quantifier body) → INVALID_INPUT(syntax-error).
16. `1.5 + 2` → INVALID_INPUT(type-mismatch): `Real + Nat` has no embedding rule.
17. Two `test: differential by …` items → INVALID_INPUT(duplicate-verification-item);
    but `test: differential …` + `test: property-fuzz …` is legal (D-024).
18. `proof: independent-recompute by x/1.0.0` → INVALID_INPUT(syntax-error):
    recomputation is a `recompute:` item, not a `proof:` alternative (D-021).

---

## C. Supported problem classes

Matrix (`MSVE_CAPABILITY_MATRIX_v0.7.md`) normative. v0 targets (all Designed):
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
  admission: ACCEPTED | INVALID_INPUT(reason: ErrorCode) | UNSUPPORTED(reason: ErrorCode),
  execution: NOT_STARTED | RUNNING | COMPLETED | TIMEOUT | INTERRUPTED
             | INTERNAL_ERROR(reason: String),
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

ErrorCode := closed enumeration per §B.13a (represented as String;
             is_error_code is the membership test).

AssuranceBasis := KERNEL_PROOF | INDEPENDENT_RECOMPUTE | SOLVER_BACKED | TEST_BACKED
# Derivation: KERNEL_PROOF from `proof: kernel-checked …`;
# INDEPENDENT_RECOMPUTE from `recompute: by …`;
# SOLVER_BACKED when a solver observation underlies the conclusion;
# TEST_BACKED from differential/fuzz test items.

SemanticResult :=
    DERIVED_VALUE { value_ref: Hash, derivation_ref: Hash }
  | ARTIFACT_CONSTRUCTED { artifact_ref: Hash }
  | NO_SOLUTION {}
  | PROVED { proof_artifact: Hash }
  | DISPROVED { refutation_ref: Hash }
  | HOLDS {}
  | VIOLATED { witness_ref: Hash }
  | UNIQUE_UNDER_PROJECTION { projection: String }
  | UNDERDETERMINED { witnesses_ref: Hash }
  | CONTRADICTION {}
  | INCONCLUSIVE { reason: ReasonCode }
# Payload binding (D-022): each alternative carries the references that make
# it auditable. value_ref points to the canonicalized value artifact;
# derivation_ref to the derivation record; witness_ref to the recorded
# counterexample witness. A payload-less tag never stands for a payload.

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
9. `semantic_result = Some(DERIVED_VALUE {value_ref, derivation_ref})` ⇒ both
   hashes resolve to artifacts in the evidence bundle.
10. `execution = INTERNAL_ERROR` ⇒ `reason` is recorded; if the failure
    occurred at packaging (`reason` starts with `output-not-encodable`),
    the established `semantic_result` is still recorded (D-019: a valid
    result with an unserializable output is never INVALID_INPUT).
11. `solver_observation = Some({outcome: UNSAT, …})` ∧ `required = LEVEL_A`
    ∧ `achieved ≠ LEVEL_A` ⇒ `semantic_result =
    Some(INCONCLUSIVE {ASSURANCE_REQUIREMENT_UNMET})`.
12. `achieved = LEVEL_B` ⇒ the frozen spec contains `assurance: level-b accepted`.
13. `partial_results ≠ []` ⇒ `execution ∈ {TIMEOUT, INTERRUPTED}`.
14. Every `VerificationRecord` with `result = FAIL` on a `required` item ⇒
    `verification_summary ∈ {FAIL, CHECKER_DIVERGENCE}`.

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
- **rat:** `{"$type":"rat","value":"-7/3"}` — lowest terms, positive denominator.
- **f64 (D-017 — exact unique grammar):**
  `{"$type":"f64","value":"<form>"}` where `<form>` is:
  `"-"? "0x" Sig "." Frac13 "p" ("+"|"-") Exp`, with `Sig ∈ {"0","1"}`,
  `Frac13` exactly thirteen lowercase hex digits, `Exp = "0" | [1-9][0-9]*`
  (no leading zeros), and:
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
  the `0.` form with `p-1074`), `p+01` (no leading zeros).
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
- **string:** `{"$type":"string","value":"…"}` — NFC-validated JSON string.
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

Canonical type names `<t>`: `nat int real rat f64 bool string hash`,
`list<…>`, `set<…>`, `option<…>`, `record{f:t,…}` (sorted), `impl`,
function types as written.

**Injectivity argument.** By structural induction on (type, value): the
`$type` tag distinguishes kinds (`list`≠`set`, `f64` finite vs `inf`);
`of`/`fields`/`sig` distinguish types within kinds; value strings are
canonical per type (unique binary64 grammar, reduced fractions, sorted
keys/items). Distinct (type, value) pairs → distinct bytes. v0.6
counterexamples now rejected or distinguished as shown above.

Envelope: UTF-8; no insignificant whitespace; minimal string escaping.
Digest: SHA-256 over exact bytes. Profile id recorded per package.

**Packaging failure (D-019 status model).** A value with no canonical form
(NaN, function value) reaching packaging is **not** INVALID_INPUT — the
input specification was valid. It is reported as
`execution: INTERNAL_ERROR` with reason `output-not-encodable: <type>`,
the established `semantic_result` still recorded (§E.7 inv. 10).

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

Normative: `MSVE_ACCEPTANCE_PLAN_v0.7.md`. End-to-end: parse/validate frozen
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

## Appendix 1. Glossary (v0.7)

- **Slug / special variable `output` / comparator / abstract selector /
  abstract decoder** — §B.
- **RawInput / DecodeOutcome / ValidationOutcome / ErrorCode** — §B.11, §B.13.
- **Solver observation / assurance required+bases+achieved+shortfall /
  verification record+summary / canonical profile `msve-canonical-3` /
  maturity** — §E–§G.
- **EVIDENCE_RECORDED** — external evidence ingested with provenance; MSVE
  asserts nothing about its truth.

## Appendix 2. Formal contracts v0.7

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
   equal `rejected(e)` with `is_error_code(e)` on decode failure, else
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

*End of MSVE_DESIGN_SPEC_v0.7.md (draft for review — not frozen).*
