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
  types: `ValidationError` (12 codes), `AdmissionError` (27 codes),
  `UnsupportedReason` (3 codes), each with a closure predicate; every
  result-schema field audited against them. (F-08: the v0.8 change summary
  said 15 and 2; the final §B.9 definitions are 27 and 3 — the summary is
  corrected here, the history preserved in the ledger.)
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
  MSVE language with a 48-case regression corpus (46 at the v0.8 gate plus
  2 added for F-01/F-04 in the 0.8.3 candidate); the §B.3 grammar is
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
8. Quantifiers: domain is `type T` or a list expression (`Option` is
   not an iterable domain — NEW-A10; set expressions are not available in
   v0 — F-05: the v0 `TypeExpr` grammar provides no `Set` former and no set
   introduction form, so no v0 surface expression denotes a set; the
   `set<`t`>` canonical type name exists for the encoding profile only and
   does not make sets available in the input language). The body is
   parenthesized (§B.3) and `Bool`.
9. `e.f`: record field; `e[i]`: list index (`i: Nat`; out of bounds is an
   execution error). Chained via Postfix.
10. Application: exact argument-type match.
11. Builtins (D-016: complete inventory — every builtin used in §B.11 is
    listed here):
    - `len: [T]->Nat` — list length.
    - `range: Nat->[Nat]` — `range(n) = [0, 1, …, n-1]`; `range(0) = []`.
    - `is_finite: Binary64->Bool` — false for ±infinity and NaN.
    - `is_nan: Binary64->Bool` — (F-04) true iff the value is NaN; false
      otherwise (including ±infinity). Declared here; referenced by §B.4
      rule 3.
    - `base_code: String->String` — (F-01) the normative detail-separator
      operation: the prefix of the argument before the first `": "`;
      the whole string if no `": "` occurs. Total on `String`.
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
  (base_code(e) == "malformed-json") \/ (base_code(e) == "invalid-top-level") \/
  (base_code(e) == "invalid-element") \/ (base_code(e) == "duplicate-key") \/
  (base_code(e) == "missing-field") \/ (base_code(e) == "unexpected-field") \/
  (base_code(e) == "invalid-field-type") \/ (base_code(e) == "invalid-rank") \/
  (base_code(e) == "invalid-score") \/ (base_code(e) == "empty-candidate-set") \/
  (base_code(e) == "invalid-uci") \/ (base_code(e) == "duplicate-uci")
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

(F-13: scope.) Every rule in this section describes **`Binary64`
operations only**. `Nat`, `Int`, `Real`, and `Rat` arithmetic is exact per
§B.4 rule 2 (including exact rational division and the `division-by-zero`
execution error for zero divisors); no rounding rule in §B.4b applies to
those types. Where a rule below says "the exact result `r`", `r` is the
mathematically exact real-number result of the `Binary64` operation, and
the rule states which `Binary64` value round-to-nearest, ties-to-even
selects. Negative cases are symmetric (sign of `r`); the intervals below
are stated for `r > 0`.
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
- **Overflow:** let `r` be the exact result. `|r| ≥ 2^1024 − 2^970`
  rounds to ±infinity (sign of `r`); at the exact threshold the tie goes to
  infinity (the even choice against the odd-significand maximum finite
  value). The maximum finite binary64 `0x1.fffffffffffffp+1023`
  (`= 2^1024 − 2^971`) is the rounding result exactly for
  `2^1024 − 3×2^970 < |r| < 2^1024 − 2^970`; at the lower midpoint
  `|r| = 2^1024 − 3×2^970` the tie goes to `2^1024 − 2^972` (even
  significand). Values with `|r| ≤ 2^1024 − 3×2^970` round to finite values
  at or below `2^1024 − 2^972` — not to the maximum finite value.
- **Underflow:** let `r` be the exact nonzero result.
  `|r| < 2^-1075` rounds to ±0 (sign of `r`); `|r| = 2^-1075` rounds to ±0
  (ties-to-even, zero being the even choice);
  `2^-1075 < |r| < 2^-1074` rounds to the minimum subnormal `±2^-1074`;
  `2^-1074 ≤ |r| < 2^-1022 − 2^-1075` rounds to the nearest subnormal
  (round-to-nearest-even on the subnormal ladder);
  `|r| = 2^-1022 − 2^-1075` rounds to the minimum normal `±2^-1022`
  (tie; the minimum normal's significand is even, the maximum subnormal's
  is odd); `2^-1022 − 2^-1075 < |r| < 2^-1022` rounds to the minimum
  normal `±2^-1022`. (F-03: the v0.8 text said magnitudes in
  `[2^-1074, 2^-1022)` round to subnormals; that is false near the minimum
  normal — e.g. `2^-1022 − 2^-1076` is closer to the minimum normal than to
  the maximum subnormal and rounds to the minimum normal.)
- **Adversarial rounding examples (normative; exact arithmetic):**
  1. `2^-1075` → `+0` (tie between zero and the minimum subnormal; zero even).
  2. `3/4 × 2^-1074 = 1.5 × 2^-1075` → `+2^-1074` (nearer the min subnormal).
  3. `2^-1022 − 2^-1076` → `+2^-1022` (nearer the minimum normal).
  4. `2^-1022 − 2^-1075` → `+2^-1022` (exact midpoint; ties-to-even).
  5. `2^1024 − 2^970` → `+inf` (exact overflow midpoint; tie to infinity).
  6. `2^1024 − 3×2^970` → `+(2^1024 − 2^972)` (lower midpoint of the
     maximum-finite interval; ties-to-even).
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
over string literals, as in §B.13a).

**`base_code: String -> String`** (F-01: normative detail-separator
operation; also listed in the §B.4 rule 11 builtin inventory). For any
string `e`, `base_code(e)` is the prefix of `e` before the first occurrence
of `": "` (colon followed by exactly one space); if `e` contains no `": "`,
`base_code(e) = e`. The remainder after the first `": "` is the *detail*:
free text, which may be empty and may itself contain further `": "`
sequences. The operation is total on `String`. A code may carry a detail
suffix `": <detail>"` (e.g. `unbound-identifier: foo`); every closure
predicate below tests `base_code(e)`, never `e` directly.

Adversarial examples (normative):
- `base_code("unbound-identifier") = "unbound-identifier"` — valid, no detail.
- `base_code("unbound-identifier: foo") = "unbound-identifier"` — valid detailed code.
- `base_code("unbound-identifier: foo: bar") = "unbound-identifier"` — split at the *first* separator; detail is `"foo: bar"`.
- `base_code("unbound-identifier: ") = "unbound-identifier"` — empty detail is valid free text.
- `base_code("notacode: foo") = "notacode"` — unknown base code → every closure predicate is false.
- `base_code("unbound-identifier:foo") = "unbound-identifier:foo"` — no `": "` separator present (colon without space); the whole string is the base code, which is not listed → every closure predicate is false.

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
  (base_code(e) == "not-a-formal-specification") \/ (base_code(e) == "missing-header-field") \/
  (base_code(e) == "syntax-error") \/ (base_code(e) == "unbound-identifier") \/
  (base_code(e) == "duplicate-definition") \/ (base_code(e) == "reserved-context-name") \/
  (base_code(e) == "reserved-keyword-misuse") \/ (base_code(e) == "type-mismatch") \/
  (base_code(e) == "arity-mismatch") \/ (base_code(e) == "unknown-builtin") \/
  (base_code(e) == "unsupported-quantifier-domain") \/ (base_code(e) == "undefined-nonterminal") \/
  (base_code(e) == "missing-required-projection") \/
  (base_code(e) == "projection-path-unresolvable") \/
  (base_code(e) == "unbound-assumption-reference") \/
  (base_code(e) == "missing-mandatory-timeout") \/ (base_code(e) == "timeout-out-of-range") \/
  (base_code(e) == "degenerate-resource-limit") \/ (base_code(e) == "degenerate-fuzz-config") \/
  (base_code(e) == "duplicate-verification-item") \/
  (base_code(e) == "conflicting-verification-requirements") \/
  (base_code(e) == "conflicting-assurance-requirements") \/
  (base_code(e) == "assurance-level-unavailable") \/ (base_code(e) == "missing-goal") \/
  (base_code(e) == "string-not-normalized") \/ (base_code(e) == "memory-limit-exceeded") \/
  (base_code(e) == "unsupported-target")
```
(NEW-C1: the v0.8 draft stated the closure predicate normatively but
never wrote it; the 27 disjuncts above are exactly the prose list.)

**`UnsupportedReason`** — reasons for `UNSUPPORTED` (in-scope but not
supported in v0). `is_unsupported_reason` covers exactly:
`scope-not-supported`, `goal-not-supported`,
`construct-not-decidable-for-proof`. (3 codes.)

```
define is_unsupported_reason(e: UnsupportedReason): Bool =
  (base_code(e) == "scope-not-supported") \/ (base_code(e) == "goal-not-supported") \/
  (base_code(e) == "construct-not-decidable-for-proof")
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
  (base_code(e) == "malformed-json") \/ (base_code(e) == "invalid-top-level") \/
  (base_code(e) == "invalid-element") \/ (base_code(e) == "duplicate-key") \/
  (base_code(e) == "missing-field") \/ (base_code(e) == "unexpected-field") \/
  (base_code(e) == "invalid-field-type") \/ (base_code(e) == "invalid-rank") \/
  (base_code(e) == "invalid-score") \/ (base_code(e) == "empty-candidate-set") \/
  (base_code(e) == "invalid-uci") \/ (base_code(e) == "duplicate-uci")

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

AdmissionError := closed per §B.9 (27 codes; is_admission_error).
UnsupportedReason := closed per §B.9 (3 codes; is_unsupported_reason).
ValidationError := closed per §B.13a (12 codes; is_validation_error).
PackagingError := String; closure is enforced by the predicate (F-01):
```define is_packaging_error(e: PackagingError): Bool =
  (base_code(e) == "output-not-encodable") \/
  (base_code(e) == "canonicalization-failure")```
which covers exactly {output-not-encodable, canonicalization-failure}
(D-030); the `": <detail>"` suffix convention of §B.9 applies (base code
checked before `": "`).

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
assurance_shortfall = (assurance_required == LEVEL_A && assurance_achieved != LEVEL_A)
         || (assurance_required == LEVEL_B && assurance_achieved == NONE)
```
Invariants: `assurance_achieved == LEVEL_A` ⇒ `KERNEL_PROOF ∈ assurance_bases ∨ INDEPENDENT_RECOMPUTE ∈ assurance_bases`;
`assurance_achieved == LEVEL_B` ⇒ `assurance_bases` non-empty; `assurance_required == NONE` ⇒ `assurance_shortfall = false`.

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

### E.6a Assurance-evidence linkage definitions (F-21)

An assurance basis recorded in `assurance_bases` is a claim, not evidence.
The following definitions make that claim auditable. They constrain the
existing `VerificationRecord` fields; no new field is introduced.

- **Proof basis (`source_item = "proof"`).** A verification record with
  `source_item = "proof"` and `result = PASS` substantiates a
  `KERNEL_PROOF` basis only if its `artifact` field contains exactly the
  64-character lowercase hexadecimal sha256 of the proof artifact, and
  that hash resolves in `evidence.proof_artifacts`
  (`∃ a ∈ evidence.proof_artifacts: a.sha256 = vr.artifact`).
- **Recomputation basis (`source_item = "recompute"`).** A verification
  record with `source_item = "recompute"` and `result = PASS`
  substantiates an `INDEPENDENT_RECOMPUTE` basis only if:
  (i) `vr.checker` identifies the checker that performed the independent
  recomputation (normative: this checker must be independent of the
  primary derivation producer; independence is attested by the producer
  and recorded via the checker ID for audit — it is not mechanically
  derivable from the record, which carries no primary-producer field);
  (ii) `vr.artifact` contains exactly the 64-character hash identifying
  the primary result compared — for `DERIVED_VALUE{value_ref = Some(h),
  …}` the value hash `h`, else the `derivation_ref` hash;
  (iii) `vr.inputs_ref` is the hash of the inputs the recomputation ran
  on (equal to `evidence.verification_inputs_ref` per F-07, as
  recomputation is a verification activity);
  (iv) `vr.result = PASS` normatively means the recomputation produced a
  value exactly equal to the primary result (§D.6: agreement is exact
  equality of derived values).
- **Solver basis.** `SOLVER_BACKED` is substantiated by the presence of a
  `solver_observation` (any outcome: the observation underlies the
  conclusion; its evidential weight follows §D.6).
- **Test basis.** `TEST_BACKED` is substantiated by a verification record
  with `source_item ∈ {"test:differential", "test:property-fuzz"}` and
  `result = PASS`.

### E.7 Cross-field invariants (exhaustive; D-022)

1. `admission ∈ {INVALID_INPUT, UNSUPPORTED}` ⇒ `execution = NOT_STARTED` ∧
   `semantic_result = None` ∧ `verification_summary = NOT_RUN` ∧
   `assurance_bases = []` ∧ `assurance_achieved = NONE`.
1b. (F-06) `admission = INVALID_INPUT(reason)` ⇒
    `is_admission_error(reason) = true`;
    `admission = UNSUPPORTED(reason)` ⇒
    `is_unsupported_reason(reason) = true` (with `base_code` applied per
    §B.9, so detailed values such as `"unbound-identifier: foo"` satisfy the
    predicates). Defining the predicates is not enforcement: this invariant
    is the record-boundary check. M8 parses and type-checks these reasons as
    `String` but does not evaluate the predicates; the enforcement claim
    rests on this invariant (SPECIFICATION_REVIEW), not on M8.
2. `execution ∈ {NOT_STARTED, RUNNING}` ⇒ `semantic_result = None`.
3. `semantic_result = Some(HOLDS {})` ⇒ the check corpus was non-empty.
4. `verification_summary = CHECKER_DIVERGENCE` ⇒ `discrepancies` contains an
   entry with `status = OPEN`.
5. `assurance_shortfall = true` ⇔ the §E.1 shortfall rule holds; ⇒
   `shortfall_description = Some(_)`.
6. `assurance_achieved = LEVEL_A` ⇒ `KERNEL_PROOF ∈ assurance_bases ∨ INDEPENDENT_RECOMPUTE ∈ assurance_bases`.
7. `assurance_achieved = LEVEL_B` ⇒ `assurance_bases ≠ []`.
8. `semantic_result = Some(VIOLATED {witness_ref})` ⇒ the witness artifact is
   in `evidence.witnesses`.
9. `semantic_result = Some(DERIVED_VALUE {value_ref, derivation_ref})` ⇒
   `derivation_ref` resolves in `evidence.derivation_records`; `value_ref`
   per invariant 15. (NEW-C5: the v0.8 draft said "the evidence bundle"
   without naming a list.)
10. (F-20) `∀ r: ResultRecord. ∀ e: String. (r.execution = INTERNAL_ERROR(e) ∧ is_packaging_error(e)) ⇒ r.semantic_result ≠ None`.
    In prose: `execution = INTERNAL_ERROR(e)` ⇒ the `reason` field `e` is recorded; if the failure
    occurred at packaging (`is_packaging_error(e)`, i.e. `base_code(e) ∈ {output-not-encodable, canonicalization-failure}`),
    the established `semantic_result` is still recorded (D-019: a valid
    result with an unserializable output is never INVALID_INPUT).
    Temporal note: the static record establishes the result's presence and its evidence linkage;
    it cannot by itself prove the historical transition from pre-packaging to post-packaging state.
11. `solver_observation = Some({outcome: UNSAT, …})` ∧ `assurance_required = LEVEL_A`
    ∧ `assurance_achieved ≠ LEVEL_A` ⇒ `semantic_result =
    Some(INCONCLUSIVE {ASSURANCE_REQUIREMENT_UNMET})`.
12. `assurance_achieved = LEVEL_B` ⇒ the frozen spec contains `assurance: level-b accepted`.
13. `partial_results ≠ []` ⇒ `execution ∈ {TIMEOUT, INTERRUPTED}`.
14. Every `VerificationRecord` with `result = FAIL` ∧ `required = true` ⇒
    `verification_summary ∈ {FAIL, CHECKER_DIVERGENCE}` (D-033: evaluated
    from the recorded `source_item`/`required` fields).
15. (D-030) `output_packaging = PACKAGING_OK` ∧ `semantic_result =
    Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = Some(h)` ∧ `h`
    resolves to a canonicalized value artifact in
    `evidence.constructed_artifacts`. (NEW-C5: named list; the v0.8 draft
    said "the evidence bundle".)
    `output_packaging = PACKAGING_FAILED(_)` ∧ `semantic_result =
    Some(DERIVED_VALUE {value_ref, …})` ⇒ `value_ref = None`. (F-16: the
    previous wording left `value_ref` unbound outside the `DERIVED_VALUE`
    alternative.) A NaN or function value therefore yields
    `PACKAGING_FAILED(output-not-encodable)` with the semantic result
    preserved — never INVALID_INPUT.
15b. (D-030, NEW-B7) Joint packaging/execution state:
    `output_packaging = PACKAGING_FAILED(r)` ⇔ `execution =
    INTERNAL_ERROR(e)` ∧ `base_code(e) = base_code(r)` (F-01: the reason's
    base code must equal the packaging reason's base code; details may
    differ).
    `output_packaging = PACKAGING_OK` ⇒ `execution` is not
    `INTERNAL_ERROR` with an `output-not-encodable`/`canonicalization-failure`
    base code.
16. (D-030) `semantic_result = Some(ARTIFACT_CONSTRUCTED {artifact_ref})`    ⇒ `artifact_ref = Some(h)` resolves in
    `evidence.constructed_artifacts`, or `artifact_ref = None` iff
    `output_packaging = PACKAGING_FAILED(_)`.
17. (D-030) `semantic_result = Some(PROVED {proof_artifact})` ⇒ the hash
    resolves in `evidence.proof_artifacts`.
18. (D-030) `semantic_result = Some(DISPROVED {refutation_ref})` ⇒ the
    hash resolves in `evidence.derivation_records`.
19. (D-030) `semantic_result = Some(UNDERDETERMINED {witnesses_ref})` ⇒
    the hash resolves in `evidence.witnesses`.
20. (D-030, F-07) `semantic_result = Some(HOLDS {})` ⇒ some
    `VerificationRecord` has `result = PASS` for the check property with
    `inputs_ref = evidence.verification_inputs_ref`. (F-07 resolution rule:
    the bundle exposes exactly one verification-inputs hash, so each
    record's `inputs_ref` must equal it; there is no separately
    addressable input collection. Valid: `inputs_ref` equal to the bundle's
    `verification_inputs_ref`. Invalid: any other hash — the record's
    inputs cannot be located.)
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
24. (F-21) `∀ r: ResultRecord. (r.assurance_achieved = LEVEL_A) ⇒ (r.semantic_result = Some(sr) ∧ sr ≠ INCONCLUSIVE{_})`
    for some `sr: SemanticResult`. In prose: achieved Level A requires an
    actual, non-inconclusive semantic result. This preserves the valid
    shortfall case: Level A required, Level B achieved, and
    `INCONCLUSIVE{ASSURANCE_REQUIREMENT_UNMET}` (invariant 11) has
    `assurance_achieved = LEVEL_B`, so this invariant does not apply.
25. (F-21) `∀ r: ResultRecord. ((r.assurance_achieved = LEVEL_A ∧ KERNEL_PROOF ∈ r.assurance_bases)
    ⇒ ∃ vr ∈ r.verification_records: (vr.source_item = "proof" ∧ vr.result = PASS
    ∧ ∃ a ∈ r.evidence.proof_artifacts: a.sha256 = vr.artifact))`.
    In prose: a claimed `KERNEL_PROOF` basis for achieved Level A must be
    substantiated by a passing proof verification record whose `artifact`
    is the proof artifact's hash resolving in `evidence.proof_artifacts`
    (per §E.6a). A record that merely names `KERNEL_PROOF` without this
    evidence violates this invariant. Consistency: such a record also
    constrains `verification_summary` via invariants 4 and 14 and the §E.6
    precedence (a PASS proof record with no worse record ⇒ summary PASS).
26. (F-21) `∀ r: ResultRecord. ∀ v: Option<Hash>. ∀ d: Hash.
    ((r.assurance_achieved = LEVEL_A ∧ INDEPENDENT_RECOMPUTE ∈ r.assurance_bases
    ∧ r.semantic_result = Some(DERIVED_VALUE{value_ref = v, derivation_ref = d}))
    ⇒ ∃ vr ∈ r.verification_records: (vr.source_item = "recompute" ∧ vr.result = PASS
    ∧ vr.inputs_ref = r.evidence.verification_inputs_ref
    ∧ ((v = Some(h) ∧ vr.artifact = h) ∨ (v = None ∧ vr.artifact = d))))`.
    In prose: a claimed `INDEPENDENT_RECOMPUTE` basis for achieved Level A
    on a derived value must be substantiated by a passing recomputation
    verification record identifying the primary result compared
    (per §E.6a). `vr.result = PASS` normatively attests exact agreement
    (§D.6); checker independence is attested via `vr.checker` (§E.6a).
    A record that merely names `INDEPENDENT_RECOMPUTE` without this
    evidence violates this invariant.
27. (F-21) `∀ r: ResultRecord. ((r.assurance_achieved = LEVEL_B ∧ SOLVER_BACKED ∈ r.assurance_bases)
    ⇒ r.solver_observation = Some(_))`.
    In prose: a claimed `SOLVER_BACKED` basis for achieved Level B must be
    substantiated by a present solver observation.
28. (F-21) `∀ r: ResultRecord. ((r.assurance_achieved = LEVEL_B ∧ TEST_BACKED ∈ r.assurance_bases)
    ⇒ ∃ vr ∈ r.verification_records: ((vr.source_item = "test:differential" ∨ vr.source_item = "test:property-fuzz")
    ∧ vr.result = PASS))`.
    In prose: a claimed `TEST_BACKED` basis for achieved Level B must be
    substantiated by a passing differential or property-fuzz test
    verification record.

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
  - `/` is not escaped;
  - (F-14) every other Unicode **scalar value** — i.e. every codepoint
    except the surrogate range U+D800–U+DFFF — that is not listed above
    (notably printable non-ASCII such as U+00A0, U+20AC) appears as raw
    UTF-8; it must not be `\uXXXX`-escaped;
  - (F-14) surrogate codepoints U+D800–U+DFFF are **forbidden**: they are
    not Unicode scalar values, so no string containing them (raw or
    escaped, e.g. `"\ud83d"`) has a canonical form.
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
- **blob:** `{"$type":"blob","sha256":"<64 lowercase hex>","bytes":<nat>}`.
  (F-15: the v0.8 text said `"<64 hex>"`, admitting uppercase spellings;
  lowercase is normative, consistent with the `Hash` type.)

Canonical type names `<t>` (D-027 — exact grammar, no whitespace anywhere):
`nat | int | real | rat | f64 | bool | string | hash`
`list<` t `>`, `set<` t `>`, `option<` t `>`,
`record{` (f `:` t (`,` f `:` t)*)? `}` with fields sorted bytewise by field
name (F-12: the empty record `record{}` is a legal type name, since the
surface grammar permits the empty record type), `impl(` t `->` t `)`,
function types `(` (t (`,` t)*)? `)->` t (F-12: zero-argument function
types `()->` t are legal, since the surface grammar permits them).
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
