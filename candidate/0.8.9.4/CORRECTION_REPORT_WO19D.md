# Correction Report — MSVE-WO-1.9D (Candidate 0.8.9.4)

**Work order:** MSVE-WO-1.9D — Candidate 0.8.9.3 Residual Schema and Provenance Closure
**Date:** 2026-10-12
**Base:** Candidate 0.8.9.3
**Output:** Candidate 0.8.9.4 (new; 0.8.8.1/0.8.9/0.8.9.1/0.8.9.2/0.8.9.3 preserved unchanged)
**Status:** Correction candidate — owner review required. No freeze, release, or approval authorized.

## Summary

The owner's source-level review of 0.8.9.3 found stale version metadata, an undeclared `i.bound` field, and an incorrect bound-equality rule comparing Z3 timeout with Core B enumeration bound. All are addressed in 0.8.9.4.

## 1. Version and project metadata reconciled

The published 0.8.9.3 spec file still headed "v0.8.9.1" (the WO-1.9C reconstruction lost the metadata edit). Corrected to v0.8.9.4 with WO-1.9D revision identity. `PROJECT_STATE.md`, root `README.md`, `CHANGELOG.md`, and prototype `README.md` (149 tests) now consistently identify 0.8.9.4.

## 2. Bound schema and semantics corrected

**Problem:** Inv 26 equated `SatCorroboration.configured_bound` (Core B enumeration bound, range [-n,+n]) with the solver invocation's bound (Z3 timeout_ms). Different quantities, different units.

**Correction:**
- `SolverInvocation` gains `timeout_ms: Nat` (declared normatively).
- The incorrect equality `(i.bound < 0 ∨ sc.configured_bound = i.bound)` is removed from Inv 26.
- Binding rule clarified: `configured_bound` records Core B's enumeration bound; it is never equated with `timeout_ms`. "Where applicable" means `Some(n)` for bounded enumeration, `None` otherwise.
- No undeclared fields remain in the invariant.

## 3. Formal model aligned

- `_sat_corr_ok`: removed bound equality; added `ispecver == R['spec_version']` and `ispecver == sc['spec_version']` (invocation spec_version must match).
- `sc['configured_bound'] >= 0` validates the bound is recorded (not compared).
- The 7th invocation element is now `timeout_ms` (was mislabeled `bound`).

## 4. Adversarial coverage

- **C3e repurposed:** solver timeout=100 vs corroboration bound=50 is now ACCEPTED (proves unlike quantities are not equated).
- **C3h new:** invocation spec_version mismatch (9.9.9 vs result version) → rejected.
- Retained: C3f (unresolvable witness), C3g (malformed hash).

## Verification

| Check | Result |
|---|---|
| Formal model (Z3) | 31/31 scenarios |
| Prototype suite | 149/149 tests |
| M8 spec-examples | 6/6 pass |
| Query identity vectors | 4/4 match |
| Genuine UNKNOWN | Reproduced |

## Limitation

Candidate 0.8.9.4 requires owner review. No D7 decision made.
