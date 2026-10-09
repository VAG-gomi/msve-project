# Report B — Design Evidence — Specification (Part 1/3)

**Work Order:** 0.8.2 · **Source file:** `six-docs/MSVE_DESIGN_SPEC_v0.8.md` (DIRECT ARTEFACT, sha256 `377e106ef2b00db6…`)

Complete original text, unmodified. Part 1 of 3. CONTINUED in next part.

---

# MSVE Design Specification v0.8

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.7.md` (retained as historical draft;
release gate: BLOCKED)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MSVE Work Order 0.8 (D-025–D-033; B-01–B-05 areas reopened;
D-001–D-024 kept)
**Review authority:** Project owner · **Version:** 0.8 (draft)
**Machine-checked:** the §B.3 grammar is generated from `m8/grammar.py`
(single source of truth); all §B.11 examples pass M8 parse + resolve +
type-check; all §B.12 invalid examples are rejected with the marked
categories (`python3 -m m8.cli spec-examples`). M8 is an audit tool, not
the MSVE engine; its limits are documented in `m8/README.md`.

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

**Self-containment note.** This document reproduces every normative definition
needed to interpret v0.8. The v0.7 package is superseded, not depended upon.
Changes are recorded in `MSVE_REGRESSION_LEDGER_v0.8.md`.

**Change summary (v0.7 → v0.8).** Targeted corrections, architecture preserved:
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
- D-020 (v0.7, superseded by D-029 below): `ErrorCode` closed via the
  `is_error_code` predicate + contract conjunct; `DecodeOutcome` invariant
  stated normatively.
- D-021: `recompute:` is its own verification item, separated from `proof:`.
- D-022: `SemanticResult` alternatives carry payloads; §E.7 invariants made
  exhaustive; `Discrepancy.involved_records` and `ExternalEvidence.recorded_at`
  defined; Level B ⇒ explicit spec acceptance invariant.
- D-023: (visualisation plan) all diagram sources reproduced.
- D-024: duplicate verification items defined precisely.
- **D-025 (B-01): record-construction production added to the grammar**
  (`Atom`); field rules (required/unknown/duplicate/missing/typing) and
  evaluation semantics defined; every §B.11 example now parses under a
  production that exists. M8 regression: the B-01 negative control.
- **D-026 (B-02): canonical exponent uniqueness** — the surface `HexFloat`
  lexical rule admits exactly `+0` or sign+nonzero digits (no `-0`);
  lowercase hex; M8 canonical checks + corpus cases.
- **D-027 (B-02): canonical serialisation fully specified** — deterministic
  JSON string escaping (short escapes preferred, `\uXXXX` lowercase),
  rational text grammar (`-?Nat/Nat`, lowest terms, positive denominator),
  canonical envelope field order and type-name spellings (§G.2).
- **D-028 (B-03): decoder-failure invariant enforced** — the validator
  contract's false branch now requires `len(d.candidates) == 0`; the exact
  counterexample (failed decode carrying candidates) is a regression case.
- **D-029 (B-04): coherent error model** — `ErrorCode` retired; three closed
  types: `ValidationError` (12 codes), `AdmissionError` (15 codes),
  `UnsupportedReason` (2 codes), each with a closure predicate; every
  result-schema field audited against them.
- **D-030 (B-05): result/packaging coherence** — `output_packaging` field;
  `value_ref`/`artifact_ref` optional with packaging invariants; all
  payload→evidence resolution invariants stated; payload-free tags get
  mandatory evidence links via invariants.
- **D-031: verification-item duplicates vs conflicts** — cardinality and
  conflict rules per kind; `Qualifier` default is `required`.
- **D-032: binary64 operational semantics** — full exceptional-case table
  (§B.4b); `0.0/0.0 → NaN` (not ±infinity); rounding mode stated.
- **D-033: required-item linkage** — `VerificationRecord` gains
  `source_item` and `required`; aggregation rules evaluable from the record.
- **M8 (new):** a real lexer/parser/name-resolver/type-checker for the
  MSVE language with a 36-case regression corpus; the §B.3 grammar is
  generated from `m8/grammar.py` (single source of truth). M8 caught two
  genuine v0.7 example defects during construction (`len` on `String`;
  `define accepted` colliding with a reserved keyword).

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*: domain-agnostic within the formal scope
defined by the input language (§B) and the capability matrix
(`MSVE_CAPABILITY_MATRIX_v0.8.md`). Outside the declared scope: UNSUPPORTED.

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

## B. Formal input language (complete v0.8 definition)

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
Hex       := [0-9a-fA-F]         # for \u escapes: either case lexes;
                               # the canonical profile (§G.2, D-027) requires lowercase
HexLo     := [0-9a-f]            # lowercase only (HexFloat, D-026)
Nat       := [0-9]+
RealLit   := Nat "." Nat
HexFloat  := "0x" ("0" | "1") "." HexLo{13} "p" ("+0" | ("+" | "-") [1-9] [0-9]*)
            # NEW-A7: no leading "-?" — negation is unary minus (the Unary
            # production). This avoids the maximal-munch ambiguity where
            # `a-0x1…p+0` (subtraction) would lex `-0x1…p+0` as one token.
            # The canonical *value* spelling (§G.2) still includes "-" for
            # negative values; only the source *token* excludes it.
                               # D-026: exactly "+0" or sign + nonzero digits; no "-0"
SemVer    := Nat "." Nat "." Nat
Duration  := Nat ("ms" | "s" | "min" | "h")
MemSize   := Nat ("B" | "KB" | "MB" | "GB")
CheckerID := Slug "/" SemVer
```

Hyphenated reserved keywords (`compare-models`, `kernel-checked`,
`property-fuzz`, `level-a`, `level-b`, `spec-hash`, `input-hash`,
`tool-versions`) lex as single tokens. Type names (`String`, `Nat`, …)
and builtin names (`len`, `is_some`, …) are **not** reserved; they lex as
`Ident` and are matched contextually. `output` is not a keyword (§B.5a).

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
Specification   := Header Body
Header          := "spec" Slug "version" SemVer "scope" Slug "authors" "[" (String ("," String)*)? "]"
Body            := Definition* ConstraintGroup* Projection* Goal Verification ResourceLimits ProvenanceReq
Definition      := TypeAlias | ValueDef | FunDef | AxiomDecl | AssumptionDecl | ExternalDecl
TypeAlias       := "type" Ident "=" TypeExpr
ValueDef        := "define" Ident ":" TypeExpr "=" Expr
FunDef          := "define" Ident "(" Params ")" ":" TypeExpr "=" Expr
Params          := (Ident ":" TypeExpr ("," Ident ":" TypeExpr)*)?
AxiomDecl       := "axiom" Ident ":" Proposition
AssumptionDecl  := "assume" Ident ":" Proposition
ExternalDecl    := "define" Ident ":" ImplType "=" "external" "(" String ")"
ConstraintGroup := "constraints" Ident "{" (";" | Constraint ";")* "}"
Constraint      := "require" Ident ":" Predicate | "forbid" Ident ":" Predicate
Projection      := "projection" Ident "=" "[" ProjPath ("," ProjPath)* "]"
ProjPath        := Ident ("." Ident)*
Goal            := "goal" (DeriveGoal | ConstructGoal | ProveGoal | CheckGoal | CompareGoal)
DeriveGoal      := "derive" Expr
ConstructGoal   := "construct" TypeExpr "satisfying" "[" Ident ("," Ident)* "]"
ProveGoal       := "prove" Proposition "assuming" "[" Ident ("," Ident)* "]"
CheckGoal       := "check" Ident "of" Ident
CompareGoal     := "compare-models" TypeExpr "satisfying" "[" Ident ("," Ident)* "]" ("under" Ident)?
Verification    := "verification" "{" (";" | VerifItem ";")* "}"
VerifItem       := ProofReq | RecomputeReq | TestReq | AssuranceReq
ProofReq        := "proof" ":" ("none" | "kernel-checked" "by" CheckerID Qualifier)
RecomputeReq    := "recompute" ":" ("none" | "by" CheckerID Qualifier)
TestReq         := "test" ":" ("none" | "differential" "by" CheckerID Qualifier | "property-fuzz" FuzzConfig Qualifier)
AssuranceReq    := "assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")
Qualifier       := ("required" | "optional")?
FuzzConfig      := "{" "seeds" ":" "[" Nat ("," Nat)* "]" "," "cases" ":" Nat "}"
ResourceLimits  := "limits" "{" "timeout" ":" Duration ";" ("memory" ":" MemSize ";")? ("steps" ":" Nat ";")? "}"
ProvenanceReq   := "record" ":" ("all" | "[" ProvItem ("," ProvItem)* "]")
ProvItem        := "spec-hash" | "input-hash" | "tool-versions" | "witness" | "outputs"
TypeExpr        := "String" | "Nat" | "Int" | "Real" | "Rat" | "Binary64" | "Bool" | "{" (Ident ":" TypeExpr ("," Ident ":" TypeExpr)*)? "}" | "[" TypeExpr "]" | "Option" "<" TypeExpr ">" | ImplType | "(" (TypeExpr ("," TypeExpr)*)? ")" "->" TypeExpr | Ident
ImplType        := "Impl" "(" TypeExpr "->" TypeExpr ")"
Expr            := OrExpr
OrExpr          := AndExpr ("\\/" AndExpr)*
AndExpr         := ImplExpr ("/\\" ImplExpr)*
ImplExpr        := CmpExpr ("==>" CmpExpr)?
CmpExpr         := AddExpr (("==" | "!=" | "<" | "<=" | ">" | ">=") AddExpr)?
AddExpr         := MulExpr (("+" | "-") MulExpr)*
MulExpr         := Unary (("*" | "/") Unary)*
Unary           := ("!" | "-")? Postfix
Postfix         := Atom ("." Ident | "[" Expr "]")*
Atom            := Literal | Ident | Ident "(" (Expr ("," Expr)*)? ")" | "(" Expr ")" | "{" (Ident ":" Expr ("," Ident ":" Expr)*)? "}" | "if" Proposition "then" Expr "else" Expr | "let" Ident "=" Expr "in" Expr | "case" Expr "of" "some" "(" Ident ")" "->" Expr "|" "none" "->" Expr | "some" "(" Expr ")" | "forall" Ident "in" Domain "::" "(" Proposition ")" | "exists" Ident "in" Domain "::" "(" Proposition ")"
Domain          := "type" TypeExpr | Expr
Literal         := String | Nat | RealLit | HexFloat | "true" | "false" | "none"
Proposition     := Expr
Predicate       := Expr
```
```

Quantifier bodies are parenthesized in the grammar itself; the bare form is a
syntax error.

**Single source of truth (D-025/B-01).** The production block above is
generated from `m8/grammar.py:PRODUCTIONS` — the normative presentation
and M8's parser share one machine-readable source. `python3 -m m8.cli
grammar-conformance` verifies that the spec's §B.3 is byte-identical to
the generated block and that every production has a parser method. Do not
edit the block by hand; edit `m8/grammar.py` and regenerate.

**Record construction (D-025).** The `Atom` alternative
`"{" (Ident ":" Expr ("," Ident ":" Expr)*)? "}"` constructs record
values. Field names may be reserved keywords (e.g. `accepted`, `seeds`);
the position is unambiguous. *Definition* names (`define`, `type`,
`axiom`, `assume`) must not be reserved keywords — `define accepted …`
is `reserved-keyword-misuse` (M8 caught this in the v0.7 validator
example).

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
8. Quantifiers: domain is `type T` or a list/set expression (`Option` is
   not an iterable domain — NEW-A10); the body is
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
13. **Record construction (D-025).** `{ f1: e1, …, fn: en }`:
    - No duplicate field names — a duplicate is a type error.
    - Each `ei` is typed normally.
    - Against an expected record type (from the enclosing `define`'s
      declared type, a function parameter type, etc.): the field-name set
      must match **exactly** — a missing field or an unknown field is a
      type error — and each field type must match.
    - With no expected type, the record type is inferred from the fields.
    - Evaluation is field-wise; field order in the literal is
      insignificant (canonical order is by field name, §G.2).
    - `len` is list-only (`len: [T] -> Nat`); `len(s)` on a `String` is a
      type error — the v0.7 examples' `len(c.uci)` is corrected to
      `c.uci != ""` in §B.11.

**B.4a String order.** Bytewise lexicographic over UTF-8. Input strings must
be NFC-normalized; non-normalized strings in hashed artifacts →
INVALID_INPUT(string-not-normalized) at admission. The parser never silently
normalizes.

### B.13 Abstract decoding relation

`decode_candidates` maps a raw string to a `DecodeOutcome`:

```
type RawInput = String
type ValidationError = String
type DecodeOutcome = { ok: Bool, candidates: [Candidate], error: Option<ValidationError> }
```

`Candidate = { uci: String, rank: Nat, score: Binary64 }`;
`ValidationError = String` (closed per §B.13a). On every `ok=false` row,
`candidates` is `[]`.

**Normative invariant (D-020, D-028):** a `DecodeOutcome` with `ok=true`
has `error=none`; with `ok=false` has `error=some(e)` for an
`is_validation_error` `e` **and `candidates=[]`**. The §B.11 contract
enforces the full invariant: its false branch conjoins
`is_some(d.error)`, `len(d.candidates) == 0`, `is_validation_error(e)`,
and `out == rejected(e)`. A decoder returning `ok=false` with a valid
error code but a **non-empty** candidate list therefore **fails** the
contract (D-028 regression case — the v0.7 contract omitted the
`len(d.candidates) == 0` conjunct and wrongly accepted it).

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

#### B.13a Closed validation codes (D-020, D-029)

```
type ValidationError = String
```

The twelve constants below are the **only** inhabitants. Closure is
enforced by the predicate (every use site is checked against it):

```
define is_validation_error(e: ValidationError): Bool =
  (e == "malformed-json") \/ (e == "invalid-top-level") \/
  (e == "invalid-element") \/ (e == "duplicate-key") \/
  (e == "missing-field") \/ (e == "unexpected-field") \/
  (e == "invalid-field-type") \/ (e == "invalid-rank") \/
  (e == "invalid-score") \/ (e == "empty-candidate-set") \/
  (e == "invalid-uci") \/ (e == "duplicate-uci")
```

**Closure rule (normative):** any `ValidationError`-typed value with
`is_validation_error(e) = false` is rejected — at contract evaluation
(the §B.11 contract conjoins `is_validation_error` on produced errors)
and at packaging. Membership test (M7): the disjuncts above are exactly
the §B.13 table's 9 codes plus the 3 `validate`-stage codes — verified
mechanically. The other two closed types (`AdmissionError`,
`UnsupportedReason`) are defined in §B.9; the v0.7 single-`ErrorCode`
model is retired (D-029).

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