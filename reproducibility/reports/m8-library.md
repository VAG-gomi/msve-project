# M8 library modules — static verification

The M8 parser/type-checker package
(`history-bank/models-and-validators/m8/`) consists of library modules with
no standalone execution semantics. Disposition: **STATIC-ONLY**.

Verified 2026-10-09 (Python 3.12.3):

- `m8/__init__.py`, `m8/grammar.py`, `m8/lexer.py`, `m8/parser.py`,
  `m8/resolve.py`, `m8/canonical.py`, `m8/typecheck.py`, `m8/cli.py` —
  all import cleanly (`import m8.<module>` OK, no errors).
- The 0.8.3-candidate variants (`m8-candidate/resolve.py`,
  `m8-candidate/canonical.py`, `m8-candidate/typecheck.py`) differ by
  content hash from the models-and-validators versions; they were exercised
  through the candidate test suite (see `runs/m8-tests/`) rather than
  imported directly, since the archived directory name (`m8-candidate`)
  does not match the package name the tests import (`m8`).
- `m8/tests/__init__.py` — package marker, no behaviour.

Executable behaviour of these modules is covered by the test suites and
CLI runs in `runs/m8-tests/`, not by importing alone.
