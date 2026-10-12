# Correction Report — MSVE-WO-1.9C (Candidate 0.8.9.3)

**Work order:** MSVE-WO-1.9C — Candidate 0.8.9.2 Residual Conformance Closure
**Date:** 2026-10-12
**Base:** Candidate 0.8.9.2
**Output:** Candidate 0.8.9.3 (new; 0.8.8.1/0.8.9/0.8.9.1/0.8.9.2 preserved unchanged)
**Status:** Correction candidate — owner review required. No freeze, release, or approval authorized.

## Summary

The owner's source-level review of 0.8.9.2 identified three residual conformance problems plus the M8 `base_code` failure. All are addressed in 0.8.9.3.

## M8 base_code resolution (owner decision: fix M8)

**Changes:**
- `history-bank/models-and-validators/m8/resolve.py`: added `"base_code"` to `BUILTINS`.
- `history-bank/models-and-validators/m8/typecheck.py`: added `("String" → "String")` scheme.

**Result:** 6/6 examples pass (was 5/6). Output preserved in `m8_output_0893.txt` (exit 0).

The specification's machine-checking claim now accurately states 6/6 verified 2026-10-12. The stronger verification contract is preserved; the specification was not weakened.

## P1: Specification version metadata

The 0.8.9.2 file headed "v0.8.9.1" with WO-1.9A references. Updated to v0.8.9.3 with WO-1.9C revision identity noting the 0.8.9.2 → 0.8.9.3 lineage. Historical candidates unchanged.

## P1: Embedded D3 normalization wording

Main spec's embedded D3 text said assumptions "preserved in the claim identity" without the verbatim-vs-normalized distinction. Aligned with A6: recorded values preserved byte-for-byte (§B.4a); identity uses NFC-normalized encoding. Internal consistency fix; no new owner decision needed.

## P1: Invariant 26 witness/bound bindings

**Normative (Inv 26 Path 2):** Added `is_sha256_hex(sc.witness.artifact)`, `∃ w ∈ r.evidence.witnesses: w = sc.witness.artifact`, and `(i.bound < 0 ∨ sc.configured_bound = i.bound)`.

**Model:** Solver invocations gain `bound` (Int, 7th element). `_sat_corr_ok` constrains witness hash validity, evidence resolution, and bound equality.

**Prototype:** Solver observations record `bound`; witness artifacts appended to `evidence.witnesses`.

**New adversarial scenarios:** C3e (mismatched bound), C3f (unresolvable witness), C3g (malformed hash) — all rejected as expected.

## Verification

| Check | Result |
|---|---|
| Formal model (Z3) | 30/30 scenarios |
| Prototype suite | 149/149 tests |
| M8 spec-examples | 6/6 pass |
| Query identity vectors | 4/4 match |
| Genuine UNKNOWN | Reproduced |

## Limitation

The prototype's solver `bound` (timeout) and checker's `configured_bound` (enumeration) are different bounds for different components. The normative "where applicable" permits this; stricter unification may be warranted later.
