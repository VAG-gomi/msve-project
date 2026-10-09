# M8 — MSVE Language Audit Tool

**Version:** 0.8.0 · **Grammar version:** 0.8.0 · **Status:** review tool, not the MSVE engine.

M8 parses and type-checks MSVE formal examples against the v0.8 grammar
and type system. It exists to catch specification-language mistakes
before they survive into future versions. It does not execute
user-supplied implementations, invoke solvers, or perform experiments.

## Layout

| File | Role |
|---|---|
| `lexer.py` | Tokeniser. Reserved keywords are exactly the §B.2 list; hyphenated keywords (`property-fuzz`, …) lex as single tokens; type names and builtin names lex as `IDENT` and are matched contextually. |
| `grammar.py` | **Single machine-readable grammar source.** `PRODUCTIONS` lists every production; the normative §B.3 block in the spec is *generated* from it (`generate_markdown()`). |
| `parser.py` | Recursive-descent parser, one method per production (checked by `test_grammar_conformance`). Produces AST `Node`s with line/col. Raises `ParseError` (category `syntax`). |
| `resolve.py` | Name resolution: two passes (collect definitions; resolve references to builtin / local / definition / `output`). Raises `ResolveError` (category `name-resolution`). |
| `typecheck.py` | The §B.4 typing rules + D-025 record construction (R13) + D-031 verification-item cardinality/conflict rules (R14) + goal/reference checks. Category `type`, or `admission` for specification-admission violations. |
| `canonical.py` | msve-canonical-3 profile checks: binary64 spelling (D-026), string escape determinism, rational text, envelope shape (D-027). Category `canonical`. |
| `cli.py` | `check`, `corpus`, `grammar-conformance`, `spec-examples`. |
| `corpus/` | 36 regression files + `manifest.json` (expected outcomes) + `gen_corpus.py` (generator). |
| `tests/` | `test_canonical.py`, `test_grammar_conformance.py`, corpus runner. |
| `runs/` | Preserved run records. |

## Grammar source of truth

`m8/grammar.py:PRODUCTIONS` is the single source. Conformance is checked
two ways (see `cli grammar-conformance` and `test_grammar_conformance`):

1. Every production has a parser method and vice versa (`check_production_coverage`).
2. The spec's §B.3 fenced block must be byte-identical to `generate_markdown()`.

Type rules (§B.4) live in prose in the spec and in code in `typecheck.py`;
the mapping is rule-number → `Checker` method, documented in the spec's
§B.4 margin notes. A future improvement is a machine-readable rule table.

## Failure categories

`lexical` (lexer) · `syntax` (parser) · `name-resolution` (resolve) ·
`type` (typecheck) · `admission` (spec-admission rules: D-031 conflicts,
`cases: 0`, bad references) · `canonical` (canonical profile).

## What M8 establishes — and does not

- A successful parse proves the example is syntactically well-formed under
  the v0.8 grammar. It does **not** prove any contract is satisfiable.
- Successful type-checking proves the example obeys the stated typing
  rules. It does **not** prove canonical encodings are injective, decoders
  implement their tables, or implementations conform.
- The corpus going green proves M8 behaves as specified on those cases.
  M8's own implementation has had 12 recorded defects during construction
  (see `runs/`); it is an audit tool under test, not an oracle.
- Semantic contract correctness (validator extensional equality, decode
  table fidelity, assurance policy soundness) is established by explicit
  reasoning in the design review, not by M8.

## Running

```
cd ~/workspace/msve-design
python3 -m m8.cli corpus                # full regression suite
python3 -m m8.cli check path/to.f.msve  # one file
python3 -m m8.cli spec-examples         # every formal example in the v0.8 spec
python3 -m m8.cli grammar-conformance   # grammar.py <-> parser <-> spec §B.3
```

Exit code 0 iff all checks pass. No third-party dependencies.
