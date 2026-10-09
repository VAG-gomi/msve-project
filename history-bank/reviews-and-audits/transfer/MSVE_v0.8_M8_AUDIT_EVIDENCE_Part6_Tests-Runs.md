# Report C — M8 Source — Tests and Run Records (Part 6/7)

**Work Order:** 0.8.2 · **Evidence:** DIRECT ARTEFACT (complete source text from the ZIP, unmodified).

---



## File: `m8/tests/test_canonical.py`

```
"""Unit tests for m8/canonical.py (D-026, D-027 regression)."""
from m8.canonical import (check_f64_canonical, canonical_f64,
                          check_string_canonical, check_rational_canonical,
                          check_envelope, check_typename, CanonicalError)

def expect_ok(fn, *args):
    fn(*args)

def expect_fail(fn, *args):
    try:
        fn(*args)
    except CanonicalError:
        return
    raise AssertionError(f"expected CanonicalError for {args}")

def run():
    # D-026: exponent uniqueness
    expect_ok(check_f64_canonical, "0x1.0000000000000p+0")
    expect_ok(check_f64_canonical, "0x1.0000000000000p+1")
    expect_ok(check_f64_canonical, "0x1.0000000000000p-1")
    expect_ok(check_f64_canonical, "0x0.0000000000001p-1074")
    expect_ok(check_f64_canonical, "0x0.0000000000000p+0")
    expect_fail(check_f64_canonical, "0x1.0000000000000p-0")   # the v0.7 survivor
    expect_fail(check_f64_canonical, "0x2.0000000000000p+0")   # bad leading digit
    expect_fail(check_f64_canonical, "0x1.0000000000000p+01")  # leading-zero exp
    expect_fail(check_f64_canonical, "0x1.0000000000000p-1074")  # normal-form subnormal
    expect_fail(check_f64_canonical, "0x1.000000000000AP+0")   # upper hex
    expect_fail(check_f64_canonical, "0x0.0000000000001p-1022")  # subnormal wrong exp
    # canonical_f64 round-trips through the validator
    import struct, random
    random.seed(7)
    for _ in range(2000):
        bits = random.getrandbits(64)
        f = struct.unpack("<d", struct.pack("<Q", bits))[0]
        if f != f or f in (float("inf"), float("-inf")):
            continue
        c = canonical_f64(f)
        back = check_f64_canonical(c)
        bf = struct.unpack("<Q", struct.pack("<d", back))[0]
        want = struct.unpack("<Q", struct.pack("<d", 0.0 if f == 0.0 else f))[0]
        assert bf == want, (f, c)
    # D-027: string escapes
    expect_ok(check_string_canonical, r'"a\nB"')
    expect_ok(check_string_canonical, r'"\u001a"')
    expect_fail(check_string_canonical, r'"\u001A"')   # must be lowercase
    expect_fail(check_string_canonical, r'"\u000a"')   # must use \n
    expect_fail(check_string_canonical, r'"\u0041"')  # printable ASCII must not be escaped
    # D-027: rationals
    assert check_rational_canonical("7/3") == (7, 3)
    assert check_rational_canonical("-7/3") == (-7, 3)
    expect_fail(check_rational_canonical, "6/4")    # not lowest terms
    expect_fail(check_rational_canonical, "1/0")    # zero denominator
    expect_fail(check_rational_canonical, "-0/5")   # signed zero
    expect_fail(check_rational_canonical, "07/3")   # leading zeros
    # D-027: envelope
    expect_ok(check_envelope, {"$type": "nat", "value": "1"})
    expect_ok(check_envelope, {"$type": "f64", "value": "0x1.0000000000000p+0"})
    expect_ok(check_envelope, {"$type": "list", "of": "nat", "items": []})
    expect_ok(check_envelope, {"$type": "option", "of": "nat", "some": False})
    expect_ok(check_envelope, {"$type": "option", "of": "nat", "some": True, "value": {"$type": "nat", "value": "1"}})
    expect_ok(check_envelope, {"$type": "impl", "sig": "(nat)->nat", "value": "ext/1.0.0"})
    expect_fail(check_envelope, {"$type": "nat", "value": "1", "extra": 0})
    expect_fail(check_envelope, {"value": "1", "$type": "nat"})  # order
    expect_fail(check_envelope, {"$type": "frob"})
    expect_fail(check_envelope, {"$type": "binary64", "value": "0x1.0000000000000p+0"})  # tag is f64
    expect_fail(check_envelope, {"$type": "list", "items": []})  # missing "of"
    # NEW-B2: string escape codepoint ranges
    expect_fail(check_string_canonical, r'"\u00a0"')  # must be raw UTF-8
    expect_fail(check_string_canonical, r'"\ud83d"')  # lone surrogate
    expect_ok(check_string_canonical, r'"\u001f"')
    expect_ok(check_string_canonical, r'"\u0085"')
    # NEW-B3/B4: type-name grammar + envelope value checking
    expect_ok(check_typename, "impl(nat->nat)")
    expect_fail(check_typename, "impl(nat -> nat)")
    expect_ok(check_typename, "record{a:nat,b:list<f64>}")
    expect_fail(check_typename, "list<nat> ")
    expect_fail(check_envelope, {"$type": "list", "of": "frob", "items": []})
    expect_fail(check_envelope, {"$type": "list", "of": "Nat", "items": []})
    expect_fail(check_envelope, {"$type": "nat", "value": "007"})
    expect_fail(check_envelope, {"$type": "f64", "value": "0x1.0000000000000p-0"})
    expect_ok(check_envelope, {"$type": "list", "of": "nat",
                               "items": [{"$type": "nat", "value": "3"}]})
    expect_fail(check_envelope, {"$type": "option", "of": "nat", "some": True,
                                  "value": {"$type": "nat", "value": "01"}})
    print("test_canonical: all assertions hold")

if __name__ == "__main__":
    run()
    print("PASS")

```


## File: `m8/tests/test_grammar_conformance.py`

```
"""Grammar-conformance test: grammar.py <-> parser.py <-> spec §B.3."""
import re, os

def run():
    from m8.grammar import PRODUCTIONS, PRODUCTION_NAMES, generate_markdown
    from m8.parser import check_production_coverage, Parser
    # 1. production <-> parser method
    missing, extra = check_production_coverage()
    assert not missing, f"productions without parser method: {missing}"
    assert not extra, f"parser methods without production: {extra}"
    # 2. no duplicate production names
    assert len(set(PRODUCTION_NAMES)) == len(PRODUCTION_NAMES), "duplicate productions"
    # 3. spec §B.3 matches the generated block (when the spec exists)
    design = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    spec = os.path.join(design, "MSVE_DESIGN_SPEC_v0.8.md")
    if not os.path.exists(spec):
        print("test_grammar_conformance: v0.8 spec absent — parts 1-2 only")
        return
    text = open(spec).read()
    m = re.search(r"### B\.3 Grammar.*?\n(```\n.*?\n```)", text, re.S)
    assert m, "no §B.3 grammar block in spec"
    assert m.group(1).strip() == generate_markdown().strip(), \
        "spec §B.3 differs from m8/grammar.py"
    print(f"test_grammar_conformance: {len(PRODUCTIONS)} productions OK")

if __name__ == "__main__":
    run()
    print("PASS")

```


## File: `m8/tests/__init__.py`

```
"""M8 test package: corpus runner + unit tests.

Run everything with:  python3 -m m8.cli corpus
Run one module with:  python3 -m m8.tests.test_canonical
"""
import os, json, sys

def run_corpus():
    from m8.cli import check_source, DESIGN_DIR
    corpus_dir = os.path.join(DESIGN_DIR, "m8", "corpus")
    manifest = json.load(open(os.path.join(corpus_dir, "manifest.json")))
    failures = 0
    for entry in manifest:
        path = os.path.join(corpus_dir, entry["file"])
        src = open(path).read()
        ok, errors = check_source(src, entry["file"])
        cats = {c for c, _ in errors}
        want = entry["expect"]
        if want == "pass":
            good = ok
        else:
            good = (not ok) and entry.get("category") in cats
        status = "PASS" if good else "FAIL"
        if not good:
            failures += 1
        detail = "" if good else f"  <- want {want}/{entry.get('category')}, got ok={ok} cats={sorted(cats)}"
        print(f"{entry['file']}: {status}{detail}")
        if not good:
            for cat, msg in errors[:3]:
                print(f"    [{cat}] {msg}")
    # unit test modules
    for mod in ("test_canonical", "test_grammar_conformance"):
        print(f"--- {mod} ---")
        __import__(f"m8.tests.{mod}")
        m = sys.modules[f"m8.tests.{mod}"]
        try:
            m.run()
            print(f"{mod}: PASS")
        except AssertionError as e:
            failures += 1
            print(f"{mod}: FAIL: {e}")
    print(f"corpus: {failures} failures")
    return 1 if failures else 0

```


## File: `m8/README.md`

```
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

```


## File: `m8/runs/2026-10-09-m8-build.md`

```
# M8 build + self-test run record — 2026-10-09

Tool: M8 v0.8.0, grammar v0.8.0. Environment: python3 (stdlib only).
Command: `cd ~/workspace/msve-design && python3 -m m8.cli corpus`

## Results
- 36/36 corpus files: expected outcome obtained (pass, or fail with the
  expected category: lexical / syntax / name-resolution / type / admission /
  canonical).
- tests/test_canonical.py: PASS (D-026 exponent cases incl. the `p-0`
  survivor; D-027 escape/rational/envelope cases; 2000-value f64 round-trip).
- tests/test_grammar_conformance.py: PASS for parts 1–2 (production <->
  parser-method coverage, no duplicates). Part 3 (spec §B.3 == generated
  block) pending the v0.8 spec document.

## v0.7 examples (discriminating power)
- ex0, ex1, ex2, ex4 (v0.7 §B.11): PASS under the v0.8 grammar.
- ex3 (selector contract): FAIL — `[type] len: argument type String does not
  match [?T]` at 17:24. GENUINE v0.7 example defect: `len(c.uci)` calls the
  list-only `len` on a String. (To be fixed in the v0.8 example, not in M8.)
- ex5 (validator contract): FAIL — `[syntax] expected identifier, found
  'accepted'` at 34:8. GENUINE v0.7 example defect: `define accepted`
  uses a reserved keyword as a definition name. (To be fixed in v0.8.)

## B-01 negative control
Patched parser with the record-literal branch disabled (simulating the v0.7
grammar, which had no record-construction production): the v0.7 validator
example fails with `syntax error at 32:3: expected expression, found '{'`.
With the v0.8 production enabled it parses. This confirms M8 would have
caught B-01 mechanically.

## Bugs found in M8 itself during this run (fixed)
1. Single-char punctuation missing from the lexer master regex.
2. `ProveGoal` missing from the production->method map.
3. Hyphenated keywords (`property-fuzz`, `kernel-checked`, `level-a`, ...)
   split into three tokens.
4. Missing `;` after timeout in resource-limits parsing.
5. `CheckError` node-vs-line/col calling convention.
6. Infinite recursion in `_apply` on unbound type variables.
7. FunDef body checked against the full fn type instead of the return type.
8. Builtin call arguments not alias-resolved before unification.
9. Axiom/assume propositions not name-resolved (quantifier binders).
10. ProveGoal proposition not name-resolved.
11. Reserved keywords (`accepted`, `seeds`, ...) rejected as record field
    names — fixed via expect_field_name (unambiguous positions).
12. Two corpus expectations wrong on the author's side (`5-3 : Nat`,
    `6/3 : Nat` — the Nat/Int embedding fires only on mixed operands).

All fixed; corpus re-run green after each fix. The tool's own defects are
recorded here rather than hidden: M8 is an audit tool under test, not an
oracle.

```


## File: `m8/runs/phase0-capability-probe.md`

```
# Phase 0 — Sub-agent capability probe (MSVE Work Order 0.8)

Date: 2026-10-09. Runtime: Muse Spark, side chat.

## Method
Spawned one child agent via `subagent.spawn` with a deterministic task:
compute SHA-256 of "m8-probe-0.8" (no newline), return as `PROBE-RESULT:<hex>`.
The expected value was computed locally and NOT included in the prompt.

## Observed evidence
- Explicit spawning: SUPPORTED (spawn accepted, agent_id returned, status pending_init → done).
- Task assignment + result collection: SUPPORTED (final response delivered via
  runtime; observed in `subagent.list` with final_response_preview).
- Execution: the agent ran to completion (~5s wall clock).
- Context isolation: separate agent_dir, depth=1, own execution record.
- Returned value: `2ecd5df35df647d1f04d7fa8c4113cc3ddd326001ebffe8d1883dd8b8d0d75b7`
  — EXACT match with the locally computed value. A simulated persona could not
  have produced this without executing the computation.
- Parallel execution: supported by the async spawn API (not exercised in probe).
- Tool-permission controls on children: NOT investigated — not established.
- Persistent execution records: YES (agent_id, timestamps, final response
  retained in `subagent.list`).

## Conclusion
Genuine internal sub-agent spawning is AVAILABLE and VERIFIED by an
independent-computation test. The lead-and-reviewer structure (agents A–D)
will use real spawned agents. Limitation: child tool-permission controls not
verified; agents inherit the lead's context (independence is procedural, not
informational — reviewers will be instructed to ground findings in document
text and will not see each other's conclusions before submitting).

```
