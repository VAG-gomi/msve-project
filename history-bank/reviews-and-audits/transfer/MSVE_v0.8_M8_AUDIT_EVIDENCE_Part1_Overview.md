# Report C — M8 Audit Evidence — Overview and Coverage (Part 1/7)

**Work Order:** 0.8.2 · **Evidence:** DIRECT ARTEFACT (read from the ZIP) unless labeled otherwise.

Inventory, grammar-conformance method, coverage map, limitations.

---

## 1. Source inventory (DIRECT ARTEFACT)

| File | Bytes | Purpose |
|---|---|---|
| `m8/__init__.py` | 67 | M8 module |
| `m8/canonical.py` | 13480 | M8 module |
| `m8/cli.py` | 5930 | M8 module |
| `m8/grammar.py` | 6321 | M8 module |
| `m8/lexer.py` | 6375 | M8 module |
| `m8/parser.py` | 30216 | M8 module |
| `m8/resolve.py` | 7428 | M8 module |
| `m8/typecheck.py` | 36470 | M8 module |

| `m8/tests/test_canonical.py` | 4807 | Canonical checker tests |
| `m8/tests/test_grammar_conformance.py` | 1326 | Grammar coverage tests |
| `m8/corpus/manifest.json` | — | 46-case index |
| `m8/corpus/*.msve` (46 in manifest; 63 on disk) | — | Regression cases |
| `m8/corpus/v08/*.msve` (11 files) | — | §B.11/B.12 spec examples (used by spec-examples, not corpus) |
| `m8/runs/2026-10-09-m8-build.md` | — | Contemporaneous build record |
| `m8/runs/phase0-capability-probe.md` | — | Phase-0 probe record |

## 2. Grammar conformance — how the 48-production result was computed (DIRECT ARTEFACT)

`m8/cli.py::cmd_grammar_conformance` performs two checks:
1. Every production in `m8/grammar.py::PRODUCTIONS` has a corresponding parser method
   in `m8/parser.py` (and vice versa) — `check_production_coverage()`.
2. The spec's `### B.3 Grammar` fenced block is byte-identical to
   `m8/grammar.py::generate_markdown()` output.

The recorded output (RECORDED OUTPUT, reproduced 0.8.1):
```
grammar-conformance: OK (48 productions, parser methods present, spec §B.3 matches generated)
```
**What this establishes:** the spec's grammar section is single-sourced from the
tool's grammar module. **What it does not establish:** that the grammar is correct,
complete, or adequate — only that the two artefacts agree.

## 3. Coverage map (INFERENCE from source inspection)

| Property | Covered by | Not covered |
|---|---|---|
| Lexical analysis | `lexer.py`; `f64-*.msve`, `string-*.msve` cases | — |
| Parsing | `parser.py`; `bare-quantifier.msve` etc. | — |
| Name resolution | `resolve.py`; `unbound-ident.msve`, `type-unbound-name.msve` | — |
| Typing | `typecheck.py`; `arith-*.msve`, `record-*.msve` | — |
| Canonicalisation | `canonical.py`; `test_canonical.py` | Full injectivity proof |
| Resource limits | `check_limits` (§B.8 ranges) | — |
| Projection paths | `check_proj_paths` (§B.5a) | — |

## 4. What M8 does not establish (REPORT CLAIM, from design review §3)

- Contract satisfiability (the D-028 logic is hand-verified, not machine-checked).
- Injectivity as a machine-checked proof (structural-induction sketch only).
- Implementation conformance (no MSVE engine exists).
- Execution semantics beyond the type system.

## 5. Historical vs reproduced (evidence discipline)

- `m8/runs/2026-10-09-m8-build.md`: RECORDED OUTPUT (contemporaneous 0.8 build record).
- `owner-review/logs/*.log`: RECORDED OUTPUT from Work Order 0.8.1 reproduction (2026-10-09).
- **No tests were rerun during Work Order 0.8.2.** All outputs below are transcribed
  from the archive.
