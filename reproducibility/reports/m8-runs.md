# Run report — M8 tests, CLI, tools

All runs: Python 3.12.3, stdlib only, no network. Captured outputs in
`runs/m8-tests/`.

| Check | Command | Result |
|---|---|---|
| `test_canonical` | `PYTHONPATH=. python m8/tests/test_canonical.py` | PASS — all assertions hold, exit 0 |
| `test_grammar_conformance` | `PYTHONPATH=. python m8/tests/test_grammar_conformance.py` | PASS — exit 0 (notes "v0.8 spec absent — parts 1-2 only") |
| 0.8.3-candidate `test_canonical` | scratch copy renamed `m8-candidate/`→`m8/`, `python -m m8.tests.test_canonical` | PASS — all assertions hold, exit 0 |
| CLI corpus | `python -m m8.cli corpus` | 0 failures, exit 0 |
| CLI check | `python -m m8.cli check m8/corpus/arith-div-int-exact.msve` | M8: PASS, exit 0 |
| `gen_corpus.py` | `python m8/corpus/gen_corpus.py` (scratch copy) | wrote 36 corpus files + manifest, exit 0 |
| `check_f64.py` (M6) | `python tools/check_f64.py` | M6: OK — 19451 values round-tripped, exit 0 |
| `check_grammar.py` | `python tools/check_grammar.py …/MSVE_DESIGN_SPEC_v0.6.md` | OK: every referenced nonterminal defined, exit 0 |
| `check_identifiers.py` | `python tools/check_identifiers.py …/MSVE_DESIGN_SPEC_v0.6.md` | examples 4–5 resolve, exit 0 |

Notes:

- The 0.8.3-candidate test imports `from m8.canonical import …` but the
  archived directory is named `m8-candidate`. The historical record
  (`MSVE_DESIGN_REVIEW_v0.8.md`) shows it ran as `python3 -m
  m8.tests.test_canonical`, i.e. the package was named `m8` at execution.
  Reproduction used a scratch rename; the archived directory is unchanged.
- `check_grammar.py` / `check_identifiers.py` were written against v0.5/v0.6
  spec layout; they were run against the banked v0.6 spec, which carries the
  expected headers.
- `test_grammar_conformance` prints "v0.8 spec absent — parts 1-2 only":
  the test degrades gracefully when the v0.8 spec file is not on its
  expected path. Recorded as observed, not corrected.
