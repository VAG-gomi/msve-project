# MSVE v0.8.3 Verification Evidence

**Work Order:** 0.8.3 · **Date:** 2026-10-09
**Environment:** `python3` on Linux; candidate M8 at
`work-order-0.8.3-candidate/m8-candidate/` (imported as `m8` via symlink
in `/tmp/m8test/`).

## Executed checks (all passed)

| Command | Exit | Output |
|---|---|---|
| `python3 -m m8.cli corpus` | 0 | `corpus: 0 failures` (48 cases: 46 gate + 2 new) |
| `python3 -m m8.cli spec-examples` | 0 | `spec-examples: 0 failures` (6/6 valid; 5/5 invalid rejected) |
| `python3 -m m8.cli grammar-conformance` | 0 | `OK (48 productions, parser methods present, spec §B.3 matches generated)` |
| `python3 -m m8.tests.test_canonical` | 0 | `test_canonical: all assertions hold` (incl. new F-12/F-14/F-15 vectors) |
| `python3 -m m8.tests.test_grammar_conformance` | 0 | `PASS` |

## New regression artefacts

- `m8-candidate/corpus/f01-base-code.msve` — exercises `base_code` and
  `is_nan` typing; manifest entry added (48 cases total).
- `m8-candidate/corpus/f04-is-nan-typed.msve` — exercises `is_nan` /
  `is_finite` on `Binary64`.
- `test_canonical.py` — 14 new assertions: `record{}` / `()->nat` /
  `record{a:()->bool}` accept; `record{` / `()->` reject; `\u20ac`,
  `\u001A`, `\u000a`, `\ud800` reject; raw-UTF-8 `café` accepts;
  blob uppercase/short digests reject, lowercase 64-hex accepts.

## F-03 derivation record (exact arithmetic)

Binary64: min subnormal `2^-1074`; max subnormal `2^-1022 − 2^-1074`;
min normal `2^-1022`; max finite `2^1024 − 2^971`; ULP near max finite
`2^971`; overflow threshold `2^1024 − 2^970` (midpoint between max finite
and +∞; tie → ∞ as the even choice).

1. `2^-1075` → `+0`: exact midpoint between 0 and min subnormal; tie → 0 (even).
2. `3/4 × 2^-1074 = 1.5 × 2^-1075` → `+2^-1074`: in `(2^-1075, 2^-1074)`, nearer the min subnormal.
3. `2^-1022 − 2^-1076` → `+2^-1022`: the subnormal/normal midpoint is `2^-1022 − 2^-1075`; `2^-1076 < 2^-1075`, so this value is above the midpoint, nearer min normal.
4. `2^-1022 − 2^-1075` → `+2^-1022`: exact midpoint; tie → min normal (significand `1.000…0` even; max subnormal significand all-ones odd).
5. `2^1024 − 2^970` → `+∞`: exact overflow midpoint; tie → ∞ (even choice).
6. `2^1024 − 3×2^970` → `+(2^1024 − 2^972)`: lower midpoint of the max-finite interval; tie → the even-significand neighbour below max finite.

## Specification-review-only judgements

F-02, F-03 (wording), F-05, F-06, F-07, F-10, F-13, F-16, F-18: corrected
in prose; verified by reading, not by execution. No MSVE engine exists;
M8 checks parsing, name resolution, and typing only — it does not
establish contract satisfiability, predicate semantics, or invariant
joint satisfiability.

## Not verified

- Joint satisfiability of the 23 §E.7 invariants (open question for owner).
- Reviewer B's 2,998-value sweep (script not preserved; still EVIDENCE_NOT_AVAILABLE).
- Historical reviewer interleaving (F-19 limitation stands).
