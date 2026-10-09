# MSVE Design Specification v0.6

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.5.md` (retained as historical draft)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MUSE WORK ORDER 0.6 (regression-gated correction pass)
**Review authority:** Project owner · **Version:** 0.6 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

**Self-containment note.** This document reproduces every normative definition
needed to interpret v0.6. It does not depend on v0.4 or v0.5 drafts; where a
rule changed, the v0.6 rule below is authoritative and the change is recorded in
`MSVE_REGRESSION_LEDGER_v0.6.md`.

**Change summary (v0.5 → v0.6).** All fifteen inherited defects D-001–D-015
addressed:
- Validator rebuilt as a three-stage pipeline (decode → validate → typed
  outcome) replacing the contradictory `parses_as_valid` Boolean and the
  reason-less `Option` (D-001, D-002, D-003, D-012, D-013).
- Canonical profile `msve-canonical-2`: every type explicitly tagged
  (list≠set injectivity restored), exact binary64 grammar, `Hash`/`Hex`
  defined, `Real` policy made operational (D-004, D-005, D-009).
- Grammar: quantifier bodies require parentheses (D-006); total `case`
  analysis replaces partial `unwrap`; `==>` is classical (D-014-implied E);
  `let` added; `some` is a constructor keyword.
- Type system: coherent signed-arithmetic model — unary minus plus one
  explicit exact Nat→Int embedding for mixed arithmetic; exact division
  semantics (D-007); full JSON→type conversion table for the decoder (D-008).
- Result schema closed: every referenced type defined; assurance split into
  required / bases / achieved with a normative shortfall rule (D-010, D-015).
- Evidence taxonomy: each method's establishment, assumptions and limits
  stated; independent recomputation given precise evidential meaning (D-014).
- All normative content reproduced in full (D-011).

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*: domain-agnostic within the formal scope
defined by the input language (§B) and the capability matrix
(`MSVE_CAPABILITY_MATRIX_v0.6.md`). Outside the declared scope: UNSUPPORTED.

### A.2 Intended users

Users who need mathematical claims checked, constructed or evidenced with the
reasoning made explicit: researchers, engineers and reviewers who must defend
what was established, by which method, and what remains unknown.

### A.3 The three non-eliminable judgments

No formal instrument eliminates three judgments; MSVE separates them instead:
1. **Domain judgment** — what the mathematics means and whether the
   formalization is adequate (human, recorded as assumptions).
2. **Construction judgment** — which object, proof or computation to attempt
   (human or heuristic, recorded as the specification).
3. **Empirical uncertainty** — what the world does (recorded as external
   evidence, never upgraded by MSVE into proof).

### A.4 Scope-qualified "all-rounder"

"All-rounder" is never a bare title. It is earned per scope and matrix version:
"all-rounder within scope S, matrix vX.Y" requires every capability the matrix
marks SUPPORTED for S to reach maturity stage 7 (Released) with evidence. The
matrix is normative for this claim.

### A.5 Non-goals

MSVE does not: invent domain semantics; certify its own implementation;
predict real-world performance from formal correctness; execute unreviewed
specifications; or extend an experimental sequence merely because another step
is possible.

---

## B. Formal input language (complete v0.6 definition)

### B.1 Design rules

1. Minimal, machine-readable; natural language never drives execution (§B.12).
2. Specifications carry identity and version; frozen specifications are immutable
   content-hashed baselines.
3. This section is the **complete normative syntax**. §B.11 gives valid examples;
   §B.12 gives invalid examples with exact rejection reasons. Quantifier scope,
   `let`, `case` and constructor rules are in the grammar itself — no
   disambiguation lives in prose alone.

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

Notes: `Esc` is the JSON escape set. Numeric literals: `Nat` (digits),
`RealLit` (exact decimals). There are no `Binary64` literals in v0 — values
arise from computation or external inputs. Signed integers are written with
unary minus (§B.4 rule 2a); `-5` denotes `Int(-5)`.

Keywords (reserved): `spec version scope authors type define axiom assume
constraints require forbid projection goal derive construct satisfying prove
assuming check of compare-models under verification proof test none
kernel-checked independent-recompute by differential property-fuzz seeds cases
required optional assurance level-a level-b accepted limits timeout memory
steps record all external spec-hash input-hash tool-versions witness outputs
true false if then else forall exists in let case of some type`.

`output` is not a keyword; it is a special context variable (§B.5a).
`some` is a constructor keyword (see §B.3); the old builtin function `some(e)`
is removed.

Whitespace insignificant except in strings. Blocks tolerate trailing `;`.
Comments: `//` to end of line.

**Parsing notes.** Operator precedence, tightest first: unary (`!`, `-`);
multiplicative (`*`, `/`); additive (`+`, `-`); comparison; `==>`; `/\`; `\/`
(see the Expr chain). Parentheses override. `case` and `let` are in `Atom`
and bind as written.

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

**D-006 resolution.** Quantifier bodies are parenthesized in the grammar
itself: `forall c in cs :: (P /\ Q)` is the only well-formed shape. The bare
form `forall c in cs :: P /\ Q` is a **syntax error**, not an ambiguous
reading. All examples in §B.11 use the parenthesized form.

### B.4 Type system and type-checking rules

Base types: `String Nat Int Real Rat Binary64 Bool`. Records, lists, sets,
options, `Impl(A -> B)`, function types.

1. Every `Expr` has a unique type. Literals: strings→`String`; digits→`Nat`;
   `RealLit`→`Real` (exact decimal value); `true/false`→`Bool`;
   `"none"`→`Option<T>` (T from context, else type error).
2. **Arithmetic (D-007).** `+ - *`:
   - Same-type operands: `Nat`/`Int`/`Real`/`Rat`/`Binary64` with matching types.
   - **Mixed `Nat`/`Int`:** exactly one explicit exact embedding applies —
     the `Nat` operand is treated as `Int` via the identity embedding
     (every `Nat` is an `Int`); result type `Int`. This is the *only*
     cross-type arithmetic permitted; it is exact and total, not a lossy
     promotion. All other mixed-type arithmetic → type error.
   - `/`: same-type operands; `Nat`/`Int` division is **exact division** —
     a non-exact quotient is an execution error (`INTERNAL_ERROR`,
     reason `inexact-division`); division by zero is an execution error
     (`division-by-zero`). `Real`/`Rat` division is exact. `Binary64`
     follows IEEE 754 (division by zero → ±infinity, which then fails
     any finiteness requirement).
   - **2a. Unary minus:** `-e` is well-typed iff `e: Nat|Int|Real|Rat|Binary64`;
     result: `Nat→Int`, `Int→Int`, `Real→Real`, `Rat→Rat`,
     `Binary64→Binary64` (IEEE negation; artifact canonicalization then
     applies §G.2 normalization). `-` on other types → type error.
     `-5` is unary minus applied to the `Nat` literal `5`, denoting
     `Int(-5)`; `-3 + 2` is well-typed (`Int + Nat` → `Int` by the
     embedding rule) denoting `-1`.
   - `!e` requires `Bool`.
3. `== !=`: same type (records: structural equality; `Binary64`: equality of
   canonical forms). Ordering `< <= > >=`: `Nat Int Real Rat Binary64 String`.
4. `String` ordering: bytewise lexicographic over UTF-8 (§B.4a).
5. Boolean connectives on `Bool`. `==>` is **classical implication**
   (equivalent to `!A \/ B`); its *meaning* never depends on evaluation
   order. (Checkers may evaluate lazily; that is an operational choice,
   not part of the semantics.)
6. `if`: `Bool` condition, equal branch types. `let x = e1 in e2`: `e1: T1`,
   `e2: U` under `x: T1`; result `U`.
7. `case e of some(x) -> e1 | none -> e2`: `e: Option<T>`; `e1: U` under
   `x: T`; `e2: U`; result `U`. This is the total option eliminator; the
   partial `unwrap` of v0.5 is removed. `some(e: T): Option<T>`.
8. Quantifiers: domain is `type T` (extension, possibly infinite) or a
   collection expression; the body is parenthesized (§B.3) and `Bool`.
9. `e.f`: record field; `e[i]`: list index (`i: Nat`; out of bounds is an
   execution error). Chained via Postfix.
10. Application: exact argument-type match.
11. Builtins:
    - `len: [T]->Nat`; `range: Nat->[Nat]`; `is_finite: Binary64->Bool`;
      `is_ascii_printable: String->Bool`; `has_no_whitespace: String->Bool`;
    - `to_rat_exact: Real -> Option<Rat>` — `Some(q)` iff the `Real` value
      has a finite decimal expansion (decidable: the value is rational
      `p/q` in lowest terms and `q`'s prime factors ⊆ {2,5}); else `None`.
      (§G.2 Real policy.)
    - `decode_candidates: RawInput -> DecodeOutcome` — the abstract decoding
      relation, specified normatively in §B.13. This replaces v0.5's
      `parses_as_valid` Boolean, which is removed.
12. `external("…")`: opaque `Impl` handle; only usable as a `check` target.

**B.4a String order.** Bytewise lexicographic over UTF-8. Input strings must
be NFC-normalized; non-normalized strings in hashed artifacts →
INVALID_INPUT(string-not-normalized) at admission. The parser never silently
normalizes.

### B.13 Abstract decoding relation (D-008, D-012)

`decode_candidates` maps a raw string to a `DecodeOutcome`:

```
type RawInput = String
type DecodeOutcome = { ok: Bool, candidates: [Candidate], error: Option<ErrorCode> }
```

where `Candidate = { uci: String, rank: Nat, score: Binary64 }` and
`ErrorCode = String` with the named constants below. On every `ok=false` row,
`candidates` is `[]`. The table is normative for the abstract decoder;
detection priority is top-to-bottom (first applicable row wins — deterministic):

| # | Input condition | Outcome |
|---|---|---|
| 1 | Not well-formed JSON (RFC 8259), including trailing data after the top-level value | `ok=false`, `ERR_MALFORMED_JSON` |
| 2 | Well-formed JSON but top-level is not an array | `ok=false`, `ERR_INVALID_TOP_LEVEL` |
| 3 | Array element is not an object | `ok=false`, `ERR_INVALID_ELEMENT` |
| 4 | Object has duplicate keys | `ok=false`, `ERR_DUPLICATE_KEY` |
| 5 | Object missing `uci`, `rank` or `score` (checked in that field order) | `ok=false`, `ERR_MISSING_FIELD` |
| 6 | Object has a field other than `uci`/`rank`/`score` | `ok=false`, `ERR_UNEXPECTED_FIELD` |
| 7 | `uci` is not a JSON string, or `rank`/`score` is not a JSON number | `ok=false`, `ERR_INVALID_FIELD_TYPE` |
| 8 | `rank` is a JSON number not denoting a non-negative integer (fractional part ≠ 0, e.g. `1.5`; negative, e.g. `-1`) | `ok=false`, `ERR_INVALID_RANK` |
| 9 | `score` is a JSON number whose binary64 rounding overflows (±infinity) | `ok=false`, `ERR_INVALID_SCORE` |
| 10 | Otherwise | `ok=true`, `candidates` in array order, `error=none` |

Conversion rules (rows 8–9):
- **rank:** a JSON number denotes a valid rank iff its exact value is a
  non-negative integer. `1e2` → `100`; `1.0` → `1`; `1.5` → invalid;
  `-0` → `0` (valid). `Nat` is arbitrary precision: `1e400` as a rank is
  a valid (enormous) integer — no overflow applies to `Nat`.
- **score:** the exact decimal value is rounded to binary64 with
  round-to-nearest, ties-to-even. Overflow → ±infinity → `ERR_INVALID_SCORE`.
  Underflow → subnormal or zero per IEEE 754 (accepted). `-0`/`-0.0` →
  negative zero, accepted; artifact canonicalization normalizes it to
  `+0.0` (§G.2). `1e400` → +infinity → `ERR_INVALID_SCORE`.
- **uci:** kept as the exact JSON string (content unchecked here — semantic
  validation in §B.11's `validate`).

**D-012 boundary.** L1 claims about the validator are conditional on this
table: they establish that the *abstract* decoder+validator contract is
correct. They do not establish that any implementation's parser implements
this table — that is an L2 conformance claim requiring its own method.

Error-code constants (`ErrorCode = String`):
```
ERR_MALFORMED_JSON  = "malformed-json"      ERR_INVALID_TOP_LEVEL = "invalid-top-level"
ERR_INVALID_ELEMENT = "invalid-element"     ERR_DUPLICATE_KEY     = "duplicate-key"
ERR_MISSING_FIELD   = "missing-field"       ERR_UNEXPECTED_FIELD  = "unexpected-field"
ERR_INVALID_FIELD_TYPE = "invalid-field-type"
ERR_INVALID_RANK    = "invalid-rank"        ERR_INVALID_SCORE     = "invalid-score"
ERR_EMPTY_SET       = "empty-candidate-set" ERR_INVALID_UCI       = "invalid-uci"
ERR_DUPLICATE_UCI   = "duplicate-uci"
```

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

**B.5a Special variable `output`.** In constraint groups referenced by
`construct` goals, `output` is bound to the object under construction, typed
by the goal's explicit target type. In `compare-models` goals, `output` is
bound to the model, typed by the goal's explicit model type, and projection
paths type-check against that type.
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
- **Goal-specific admission:**
  - `prove` + `level-a required` → requires `proof: kernel-checked by <id> required`.
  - `derive` + `level-a required` → requires `proof: kernel-checked … required`
    **or** `proof: independent-recompute by <id> required`.
  - `construct` / `compare-models` / `check` + `level-a required` →
    INVALID_INPUT(assurance-level-unavailable) — v0 establishes no Level A
    pipeline for solver- or test-backed goals.
  - `level-a required` with `proof: none` and no eligible alternative →
    INVALID_INPUT(conflicting-assurance-requirements).
- `level-b accepted` records explicit acceptance of solver-backed or test-backed
  conclusions with labelling (§E.4). A Level B contradiction may be reported
  **only** when the frozen spec contains this item.
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
`projection-path-unresolvable: <path>`, `string-not-normalized`,
`real-not-encodable`.
UNSUPPORTED: `scope-not-supported`, `construct-not-decidable-for-proof`.

### B.10 Natural-language handling (hard rule)

NL drafts candidates under human supervision. Unreviewed NL-extracted
assumptions NEVER enter executable specifications. Review artifacts only.

### B.11 Valid examples

**derive** (independent recomputation):
```
spec derive-level-a
version 0.6.0
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
version 0.6.0
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
version 0.6.0
scope kernel-proofs
authors ["example"]
axiom add_zero: forall n in type Nat :: (n + 0 == n)
goal prove forall n in type Nat :: (n + 0 == n) assuming [add_zero]
verification { proof: kernel-checked by lean-kernel/4.9.0 required; assurance: level-a required; }
limits { timeout: 60s; }
record: all
```

**check** (selector; contract in Appendix 2):
```
spec selector-contract
version 0.6.0
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

define selector_impl: Impl(CandidateSet -> Candidate) = external("selector-impl/0.6.0")
define indie_ref_impl: Impl(CandidateSet -> Candidate) = external("independent-ref-impl/0.6.0")

goal check contract_holds of selector_impl

verification {
  proof: none;
  test: differential by indie-ref-impl/0.6.0 required;
  test: property-fuzz { seeds: [1, 2, 3], cases: 10000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; memory: 2GB; }
record: all
```

**compare-models** (explicit model type):
```
spec tiny-models
version 0.6.0
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

**validator check** (D-001/D-002/D-003: three-stage pipeline, typed outcome):
```
spec validator-contract-check
version 0.6.0
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
// (decode-stage codes ERR_MALFORMED_JSON … ERR_INVALID_SCORE per §B.13)

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
    (case d.error of some(e) -> (out == rejected(e)) | none -> false)))

define validator_impl: Impl(RawInput -> ValidationOutcome) = external("validator-impl/0.6.0")

goal check validator_contract of validator_impl

verification {
  proof: none;
  test: property-fuzz { seeds: [7, 8], cases: 5000 } required;
  assurance: level-b accepted;
}
limits { timeout: 300s; }
record: all
```

Contract reading: decode failure → the outcome must be `rejected` with the
decoder's error code (D-001's `"[]"` case: decode succeeds with `[]`, then
`validate` rejects with `ERR_EMPTY_SET` — no contradiction). Decode success →
the outcome must equal `validate` applied to the decoded candidates, so an
accepted set is *exactly* the decoded input: no fabrication, omission,
alteration or reordering (D-002). Defect priority is fixed by the §B.13 table
then the `validate` if-chain — deterministic (D-003).

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
15. `forall c in cs :: P /\ Q` (bare quantifier body) → INVALID_INPUT(syntax-error):
    quantifier bodies require parentheses (D-006).
16. `define x: Nat = unwrap(none)` → INVALID_INPUT(unbound-identifier: unwrap):
    partial `unwrap` removed; use `case` analysis (D-014-implied).
17. `1.5 + 2` → INVALID_INPUT(type-mismatch): `Real + Nat` has no embedding rule;
    only the exact Nat→Int embedding is permitted (D-007).

---

## C. Supported problem classes

Matrix (`MSVE_CAPABILITY_MATRIX_v0.6.md`) normative. v0 targets (all Designed):
exact integer/rational arithmetic (with the D-007 model); SymPy-backed symbolic
computation within stated limits; decidable-fragment constraint solving;
restricted general SMT (unknown → INCONCLUSIVE(SOLVER_UNKNOWN)); model
construction/witnesses; uniqueness checking via §D; Lean-kernel proof checking
(formalization human-reviewed); L1/L2/L3 assurance (§D.1); generation restricted
to §D.5. `Real` denotes exact rationals in v0 (§G.2); `Rat` is the
lowest-terms rational type with `to_rat_exact` conversion.
FORBIDDEN: inferred historical data, NL direct execution, silent gap-filling,
unreviewed-spec execution. OUT OF SCOPE: performance prediction, objective
invention, arbitrary discovery.

---

## D. Assurance levels, uniqueness, generation, evidence taxonomy

### D.1 Three assurance levels

- **L1 — Mathematical model.** Abstract-algorithm properties by proof or sound
  procedure. For the validator: proved over the abstract decoder+validator
  (contract in §B.11) covering the full `RawInput` domain by structural case
  analysis on the §B.13 table — conditional on the table's semantics (D-012).
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

### D.6 Evidence taxonomy (D-014)

Each method: what it establishes, its assumptions, its limits. No method may
be described as establishing more.

| Method | Establishes | Assumes | Does NOT establish |
|---|---|---|---|
| Kernel-checked proof | The proposition follows from the stated assumptions in the kernel's logic | Formalization adequacy (human); kernel soundness | Truth of the assumptions; adequacy of the formalization |
| Independent recomputation | A second, independent implementation produced the same derived value | Checker independence (separation); determinism of the derivation | A formal proof of the claim; absence of shared-specification bugs |
| Solver observation (SAT/UNSAT/UNKNOWN) | The solver reported this outcome under the recorded configuration | Solver soundness within the declared fragment | A proof (UNSAT alone is not a proof); correctness outside the fragment |
| Differential test | Primary and reference agree on the tested corpus | Reference independence; corpus relevance | Universal correctness |
| Property fuzz | No counterexample in the generated cases | Generator coverage; oracle correctness | Universal correctness |
| Bounded test | The stated property held for the executed cases | Corpus adequacy | Anything about untested cases |

**Independent recomputation is not a formal proof term.** For `derive` goals it
is admissible Level A evidence *for the exact-arithmetic derivation class*
because: the derivation is deterministic; the recompute checker is developed
and run independently (separation requirements in the acceptance plan); the
comparison is exact equality of derived values. What remains assumed: no
shared misreading of the specification (that is D-014's stated limit, recorded
in the evidence bundle — never silently upgraded).

---

## E. Result-record schema (D-010, D-015: closed)

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

ErrorCode := one of the §B.9 catalog strings or the §B.13 validation codes
             (closed enumeration; represented as String).

AssuranceBasis := KERNEL_PROOF | INDEPENDENT_RECOMPUTE | SOLVER_BACKED | TEST_BACKED
# Basis derivation (normative): KERNEL_PROOF from `proof: kernel-checked …`;
# INDEPENDENT_RECOMPUTE from `proof: independent-recompute …`;
# SOLVER_BACKED when a solver observation underlies the conclusion;
# TEST_BACKED from differential/fuzz test items. Multiple bases recorded.

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
ArtifactRef := { sha256: Hash, bytes: Nat, media: String, description: String }
ExternalEvidence := { experiment_id: String, method: String,
  data_ref: Hash, recorded_at: String }

PartialResult := { description: String, semantic_fragment: SemanticResult,
  provenance_ref: Hash, labelled_partial: true }
# Validation: present only when execution ∈ {TIMEOUT, INTERRUPTED}.

Discrepancy := { property: String, involved_records: [Nat],
  description: String, required_follow_up: String, status: OPEN | RESOLVED }
# Validation: status may move OPEN → RESOLVED only with a recorded resolution.

Hash := String of exactly 64 characters in [0-9a-f]  # SHA-256, lowercase hex
# Validation: canonicalizer rejects other shapes (INTERNAL_ERROR: invalid-hash-format).
# Canonical encoding: {"$type":"hash","value":"<64 hex>"} (§G.2).
```

**Normative shortfall rule (D-010).** `assurance_shortfall` is computed, not
narrated:
```
shortfall = (required == LEVEL_A && achieved != LEVEL_A)
         || (required == LEVEL_B && achieved == NONE)
```
Invariants: `achieved == LEVEL_A` ⇒ `KERNEL_PROOF ∈ bases ∨ INDEPENDENT_RECOMPUTE ∈ bases`;
`achieved == LEVEL_B` ⇒ `bases` non-empty; `required == NONE` ⇒ `shortfall = false`
(achieved may still record what was done — informative, not a claim).
`shortfall_description` names the gap when `shortfall` is true, else `none`.

### E.2 Semantic results per goal type

- `derive` → DERIVED_VALUE (+ value + derivation record) | INCONCLUSIVE(reason).
- `construct` → ARTIFACT_CONSTRUCTED | NO_SOLUTION | INCONCLUSIVE.
- `prove` → PROVED | DISPROVED | INCONCLUSIVE.
- `check` → HOLDS | VIOLATED (+ witness) | INCONCLUSIVE (incl. NO_TEST_CORPUS).
- `compare-models` → UNIQUE_UNDER_PROJECTION | UNDERDETERMINED (+ witnesses) |
  CONTRADICTION | INCONCLUSIVE.

### E.3 INCONCLUSIVE reason codes

SOLVER_UNKNOWN (solver gave up); PROCEDURE_INCOMPLETE (method doesn't cover
the case); RESOURCE_EXHAUSTED (limits hit); EXECUTION_INTERRUPTED (external
stop); ASSURANCE_REQUIREMENT_UNMET (needed level not achieved — shortfall
recorded); NO_TEST_CORPUS (empty test corpus — never a vacuous HOLDS).

### E.4 Solver observation vs semantic conclusion vs assurance

The solver's report (`SolverObs`) is data. The semantic conclusion
(`SemanticResult`) is a judgment under the assurance policy. The assurance
triple records what was requested, on what bases, what was achieved, and the
computed shortfall.
- UNSAT observation with Level A required and only solver backing available →
  `solver_observation = {UNSAT,…}`, `semantic_result = Some(INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET))`,
  `shortfall = true`. This is the refusal rule: MSVE reports what the solver
  said and declines the stronger claim — it does not launder UNSAT into PROVED.
- A Level B conclusion (incl. CONTRADICTION from a solver) may be reported
  only with explicit `level-b accepted` in the frozen spec; the record shows
  `achieved = LEVEL_B`, `bases = [SOLVER_BACKED]`.

### E.5 Level A policy (v0)

- `prove` goals: kernel-checked proof only.
- `derive` goals (exact arithmetic): kernel-checked proof OR independent
  recomputation with agreement (evidential meaning: §D.6).
- SMT-UNSAT Level A: FUTURE — v0 has no invented certificates; unsat cores
  are diagnostic (§D.6: observation, not proof).
- Solver- or test-backed goals (`construct`/`compare-models`/`check`):
  no Level A pipeline in v0 (admission rejects `level-a required`).

### E.6 Verification aggregation (divergence-first)

Per-property `VerificationRecord`s are never collapsed. Summary precedence:
CHECKER_DIVERGENCE > FAIL > INCONCLUSIVE > PASS; no records → NOT_RUN.
A PASS/FAIL split on the same property → CHECKER_DIVERGENCE with both records
preserved and a `Discrepancy{status: OPEN}` requiring follow-up.

### E.7 Legal combinations (illustrative, not exhaustive)

- admission=INVALID_INPUT ⇒ execution=NOT_STARTED, semantic_result=None.
- execution=TIMEOUT ⇒ partial_results labelled, semantic_result=
  Some(INCONCLUSIVE(RESOURCE_EXHAUSTED)).
- verification_summary=CHECKER_DIVERGENCE ⇒ discrepancies non-empty.
- shortfall=true ⇒ shortfall_description=Some(_).
- semantic_result=Some(HOLDS) ⇒ corpus non-empty (invariant; §B.5b).

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

### G.2 Canonical encoding profile `msve-canonical-2` (D-004, D-005, D-009)

Deterministic; versioned; **no bare JSON values** — every value is a typed
object with an explicit `$type` tag. `msve-canonical-1` (v0.5) is superseded:
it failed type-injectivity (list/set collision, D-004). Both hashes are
recorded during transition; old hashes are never reinterpreted under new rules.

**Type tags (every supported type is distinguishable):**

- **nat:** `{"$type":"nat","value":"12345"}` — no sign, no leading zeros.
- **int:** `{"$type":"int","value":"-12345"}` — optional `-`; `-0`→`"0"`.
- **rat:** `{"$type":"rat","value":"-7/3"}` — lowest terms, positive denominator.
- **f64:** `{"$type":"f64","value":"-0x1.921fb54442d18p+1"}` — exact grammar:
  `"-"? "0x" H "." H{13} "p" ("+"|"-") Nat`, where `H` is one hex digit
  (lowercase) and `H{13}` exactly thirteen. Rules: if all fourteen hex digits
  are zero → exactly `0x0.0000000000000p+0` (this is +0.0; −0.0 normalizes
  here). Else if the leading digit is nonzero (normal): value =
  ±(d.fffffffffffff)₁₆ × 2^exp. Else (leading zero, fraction nonzero —
  subnormal): value = ±(0.fffffffffffff)₁₆ × 2^−1022. Sign `-` iff the value
  is negative. Every finite binary64 has exactly one such representation.
- **real:** `{"$type":"real","value":"3.14"}` — finite decimal, no exponent,
  no trailing zeros, `-0`→`"0"`. **Defined only for `Real` values with a
  finite decimal expansion** (decidable per §B.4 rule 11: the value is
  rational p/q in lowest terms with q's prime factors ⊆ {2,5}). A `Real`
  without finite decimal expansion reaching the canonicalizer →
  INVALID_INPUT(real-not-encodable). Rationale (D-009): in v0, `Real`
  denotes exact rational values (no v0 operation constructs irrationals);
  arbitrary rationals are not finitely decimal-encodable. A specification
  needing such a value in a hashed artifact must convert explicitly via
  `to_rat_exact` (when `Some`) or another spec-declared exact step; the
  conversion is part of the reviewed specification. `Rat` (lowest-terms)
  is always encodable.
- **bool:** `{"$type":"bool","value":true}` / `false` — JSON booleans.
- **string:** `{"$type":"string","value":"…"}` — NFC-validated JSON string.
- **list:** `{"$type":"list","of":"<t>","items":[...]}` — order preserved;
  `<t>` is the canonical type name of the element type.
- **set:** `{"$type":"set","of":"<t>","items":[...]}` — items sorted by the
  UTF-8 bytes of each element's canonical form. A set value with duplicate
  elements has no canonical form (cannot arise from well-typed evaluation).
- **option:** `{"$type":"option","of":"<t>","some":true,"value":<canonical>}`
  / `{"$type":"option","of":"<t>","some":false}` — the `of` tag keeps
  `none : Option<Nat>` distinct from `none : Option<String>`.
- **record:** `{"$type":"record","fields":{…}}` — keys sorted bytewise by
  UTF-8; each field value canonically encoded (field types captured
  structurally; aliases are transparent, so structural identity is type
  identity).
- **impl:** `{"$type":"impl","value":"<external descriptor>"}`.
- **hash:** `{"$type":"hash","value":"<64 lowercase hex>"}`.
- **blob:** `{"$type":"blob","sha256":"<64 hex>","bytes":<nat>}` — bytes
  carried alongside, linked by the hash.

Canonical type names `<t>`: `nat int real rat f64 bool string hash`,
`list<…>`, `set<…>`, `option<…>`, `record{f:t,…}` (fields sorted),
`impl`, function types as written. These names appear only inside
composite tags.

**Injectivity argument (D-004).** By structural induction on (type, value):
the `$type` tag distinguishes all kinds (in particular `list` ≠ `set`);
within a kind, `of`/`fields`/value-strings distinguish types; value strings
are canonical per type (no leading zeros, lowest terms, exact hexfloat
grammar, sorted keys/items). Hence distinct (type, value) pairs → distinct
byte strings. Counterexamples that collide under v0.5's profile: list `[1]`
vs set `{1}` (both were `[{"$type":"nat","value":"1"}]`); `none:Option<Nat>`
vs `none:Option<String>` (both were `{"$type":"none"}`).

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
repository's genesis commit — and it must be self-contained (D-011).

---

## I. Acceptance plan summary

Normative: `MSVE_ACCEPTANCE_PLAN_v0.6.md`. End-to-end: parse/validate frozen
spec; assess selector + validator contracts (three-stage pipeline); establish
L1 (three claims kept separate; decoder-conditional per D-012); identify L2
method per claim or mark unavailable; run L3 if authorized (well-formed corpora
vs selector; malformed corpora vs validator contract; regression cases per the
ledger); emit §E.1 result record + evidence package; assess marginal value vs
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

## Appendix 1. Glossary (v0.6)

- **Slug / special variable `output` / comparator / abstract selector /
  abstract decoder** — §B.
- **RawInput** — the validator's input type (`String`: serialized candidate set).
- **DecodeOutcome / ValidationOutcome / ErrorCode** — §B.11, §B.13.
- **Solver observation / assurance required+basis+achieved / verification
  record+summary / canonical profile `msve-canonical-2` / maturity** — §E–§G.
- **EVIDENCE_RECORDED** — external evidence ingested with provenance; MSVE
  asserts nothing about its truth.

## Appendix 2. Formal contracts v0.6

*Normative for the acceptance plan. Proposed — frozen before any execution.*

**A2.1 Selector types.** `Candidate`, `CandidateSet`, `RawInput = String` as in
§B.11. Binary64: −0.0→+0.0 at the canonical boundary; NaN/±∞ excluded from
well-formed candidates (decode rejects non-finite scores).

**A2.2 Comparator.** `prefers(a, b)`: higher score; equal scores → lower rank;
equal scores+ranks → smaller UCI (bytewise UTF-8). Output = unique maximal
element. (No key tuple.)

**A2.3 Uniqueness.** Strict total order ⇒ unique maximum for non-empty
well-formed sets. (L1.)

**A2.4 Membership.** `∃c ∈ C : (output == c)` (whole-record structural equality).

**A2.5 Validator pipeline.** Three stages, no conflation:
1. **Decode** (`decode_candidates`, §B.13): raw string → `DecodeOutcome`
   (typed candidates or a named error code; deterministic priority).
2. **Validate** (`validate`, §B.11): decoded candidates → `ValidationOutcome`
   (semantic checks: non-empty, uci shape, duplicate ucis; fixed priority).
3. **Contract** (`validator_contract`, §B.11): the implementation's outcome
   must equal `rejected(decode error)` on decode failure, else
   `validate(decoded candidates)` — binding accepted data exactly to the
   input (no fabrication/omission/alteration/reordering).

**A2.6 Numeric semantics.** Canonicalized binary64, exact comparison, no
tolerance; ranking use only. Mixed Nat/Int arithmetic via the exact embedding
(§B.4 rule 2).

**A2.7 Determinism.** Selector: pure function of the candidate set. Validator:
pure function of the raw input (decode table + validate are deterministic).

**A2.8 Historical comparison.** Matches the preserved Order 7 adapter for the
selector; validator edge-case rules are new proposals, not historical facts.

## Appendix 3. Unresolved design decisions

Lean version + proof-carrying interface; full problem-class catalog; per-class
resource defaults; generator-class widening; signed-tag key management;
whether `Real` should eventually denote true reals (v0: exact rationals).

*End of MSVE_DESIGN_SPEC_v0.6.md (draft for review — not frozen).*
