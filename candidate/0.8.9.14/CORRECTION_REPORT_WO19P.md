# Correction Report — MSVE-WO-1.9P

**Work order:** MSVE-WO-1.9P (Formal Audit Verdict Integrity and Candidate Identity Closure)
**Base candidate:** 0.8.9.13 (preserved unchanged)
**New candidate:** 0.8.9.14
**Date:** 2026-10-13
**Authority:** Owner rulings D1–D9; approved amendments A1, A2, A4, A5, A6.
**Status:** Correction candidate only. No D7 freeze, release, or baseline approval.

## P1 — Audit verdict classification: CORRECTED

**Flaw:** `run_audit_08913.py` computed `ok = (res == z3.sat) == expect_sat`,
treating Z3 `UNKNOWN` as PASS whenever `expect_sat=False`. The WO-1.9O report
then claimed O-2..O-5 "rejected" on the basis that `UNKNOWN ≠ SAT` — invalid.

**Fix:** Explicit verdict function with regression self-test (6/6):
- expect sat: SAT→PASS, UNSAT→FAIL, UNKNOWN→INCONCLUSIVE
- expect unsat: UNSAT→PASS, SAT→FAIL, UNKNOWN→INCONCLUSIVE
- UNKNOWN is INCONCLUSIVE, never PASS.

**Corrected audit result (0.8.9.14):**
- **PASS: 32, FAIL: 0, INCONCLUSIVE: 5, of 37 total.**
- The 5 INCONCLUSIVE cases (solver UNKNOWN, cause documented):
  1. Inv3-3 — solver-backed HOLDS with UNKNOWN observation
  2. O-2 — missing invocation
  3. O-3 — query_id mismatch
  4. O-4 — claim_id mismatch
  5. O-5 — spec_version mismatch
- The previous "37/37" headline is withdrawn. Five scenarios previously
  counted as PASS are now honestly INCONCLUSIVE.
- D5 capacity scenarios (D5-1..D5-4) all complete with definitive sat/unsat.

**No timeouts were increased and no constraints weakened to obtain green results.**

## P1 — Candidate identity: RECONCILED

**Flaws found:**
1. `candidate/0.8.9.13/MSVE_DESIGN_SPEC_v0.8.9.13.md` internally identified
   as v0.8.9.12 / WO-1.9N (stale header from file-copy setup).
2. Root README identified 0.8.9.10 while PROJECT_STATE identified 0.8.9.13
   (README update in WO-1.9O was a no-op: it replaced '0.8.9.12' but the
   README said '0.8.9.10').

**Fix (new immutable candidate 0.8.9.14; 0.8.9.13 preserved unchanged):**
- Spec filename, header, work-order ID, revision identity, footer: all 0.8.9.14 / WO-1.9P / base 0.8.9.13.
- D3 schema: Candidate 0.8.9.14.
- Model, runner, coverage report: 0.8.9.14.
- Root README → 0.8.9.14 as current review candidate (0.8.9.13 added to historical list).
- PROJECT_STATE.md → 0.8.9.14 / WO-1.9P.

**Remote verification:** 0.8.9.13 commit `8c6fe809c169` is the default-branch
HEAD (no branch discrepancy — the identity flaws were content errors, not
publication errors).

## D1–D9 preserved

No ruling reopened. D1 weak-UNKNOWN binding, D2 seven-kind bar, D3
solver-fragment scope, D4 independence, D5 capacities, D6 encoding,
D7 owner-freeze, D8 experimental, D9 separation — all intact.

## Verification

| Check | Result |
|-------|--------|
| Prototype suite | 182/182 passed at `215e9f5d2d2447f7adf26ae1f153e82f3f009309` |
| Formal-model audit | 32 PASS / 0 FAIL / 5 INCONCLUSIVE (37 total) |
| Verdict self-test | 6/6 PASS |
| M8 | 6/6 inherited from 0.8.9.4 |

## D7 gate impact

| Gate | 0.8.9.13 (as reported) | 0.8.9.14 (corrected) |
|------|------------------------|----------------------|
| 1. Blocking decisions | PASS | PASS |
| 2. Spec/model consistency | PARTIAL | **PARTIAL** — 5 scenarios INCONCLUSIVE (solver limits); D5 fully verified |
| 3. Tests/reproducibility | PASS (37/37 claimed) | PASS (32/37 verified; 5 inconclusive honestly reported) |
| 4. Provenance | PASS | PASS (full SHAs; identity reconciled) |
| 5. Issues classified | PROPOSED | PROPOSED |
| 6. Owner approval | BLOCKED | BLOCKED |

## Remaining D7 blockers

1. Five formal scenarios INCONCLUSIVE due to Z3 timeout on full-model
   provenance constraints (Inv3-3, O-2..O-5). The constraints are encoded;
   automated verification is unavailable at current solver capacity.
2. Positive Inv 3 SAT paths remain unverified in full model (as in 0.8.9.12/13).
3. M8 inherited, not re-run.
