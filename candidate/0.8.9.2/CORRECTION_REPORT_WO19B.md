# Correction Report — MSVE-WO-1.9B (Candidate 0.8.9.2)

**Work order:** MSVE-WO-1.9B — Candidate 0.8.9.1 Conformance Reconciliation
**Date:** 2026-10-12
**Base:** Candidate 0.8.9.1 (archival `dd1f1743c9c0`, prototype `a79b48e45c99`)
**Output:** Candidate 0.8.9.2 (new; 0.8.8.1/0.8.9/0.8.9.1 preserved unchanged)
**Status:** Correction candidate — owner review required. No freeze, release, or approval authorized.

## Summary

The owner's source-level review of 0.8.9.1 identified five inconsistency areas (P1×3, P2×2) plus two project-record issues. All are addressed in 0.8.9.2. Verification: formal model 27/27, prototype 151/151, M8 5/6 (1 genuine failure documented, not hidden).

## §1. D1 weak-assurance unification (P1)

**Finding:** Normative `AssuranceBasis` listed `SOLVER_BACKED` only; model added separate `WEAK_SOLVER_BACKED`; weak invariant didn't enforce linkage.

**Correction:** Unified representation per owner preference: `SOLVER_BACKED` with explicit `weak` qualifier (`SOLVER_BACKED{weak=false}` ordinary, `SOLVER_BACKED{weak=true}` D1 diagnostic). The separate basis is removed from the model.

- Normative Inv 27b added: weak path requires UNKNOWN observation + INCONCLUSIVE result + no positive conclusion + full identity linkage (claim, query_id, spec_version, provenance) + D2 precedence.
- Model Inv 30 rewritten: `SOLVER_BACKED ∧ weak` → linkage + UNKNOWN + INCONCLUSIVE + ¬HOLDS + ¬VIOLATED.
- Model Inv 27 restricted to `¬weak`; Inv 31 (D2 bar) covers both qualifiers.
- Prototype already used the unified form; contract verified, no code change needed.
- New model scenarios: W1b (stale query_id rejected), W1c (spec_version mismatch rejected).

## §2. A4 invariant 26 and corroboration records (P1)

**Finding:** Normative Inv 26 required DERIVED_VALUE for every INDEPENDENT_RECOMPUTE; model allowed two paths. Record lacked required provenance fields; model used unbound `witness_checkable` flag.

**Correction:**
- Normative Inv 26 rewritten with two explicit paths:
  - Path 1: derived-value recomputation (exact equality, no witness).
  - Path 2: SAT corroboration with fully bound witness record.
- New normative `SatCorroboration` type with: claim_id, query_id, spec_version, checker, checker_version, configured_bound, witness{artifact, checked_against, checked_by, validation_result}, execution{method, detail}.
- Binding rule: `witness.checked_against = query_id`; `checked_by = checker`; validation PASS; SAT observation; provenance resolves to matching invocation.
- Model: dedicated `sat_corr` collection; Path 2 checks every binding; unbound flags removed. Independence (`checker_independent`) is enforced within each path.
- Prototype: emits typed `sat_corroborations` array in result.
- New scenarios: C3b (bound witness accepted), C3c (unbound witness rejected), C3d (wrong checker rejected), W5 (no independent checker rejected).

## §3. A6 normalization reconciliation (P1)

**Finding:** §B.4a rejected non-NFC (`string-not-normalized`); A6 requires normalize-don't-reject. D3 said assumptions "preserved byte-for-byte in the claim identity" but identity hashes NFC-normalized bytes.

**Correction:**
- §B.4a rewritten with three-way distinction: (1) recorded values preserved byte-for-byte, never rejected for non-NFC; (2) identity bytes NFC-normalized; (3) query encoding per §9.1.
- `string-not-normalized` removed from admission predicate (29 codes, was 30). Predicate, prose list, and rule 11 updated.
- D3 §7 fixed: assumptions preserved byte-for-byte as recorded values; identity uses NFC-normalized encoding.
- Prototype `identity.py` already normalizes; verified. New Unicode equivalence regression test.

## §4. Canonical query identity (P2)

**Finding:** `query_id` as "canonical JSON" underspecified.

**Correction:** D3 §9.1 now fully specifies: codepoint-sorted keys, no whitespace, ASCII-only (`ensure_ascii`) with lowercase `\uXXXX`, surrogate pairs, RFC 8259 string escapes, decimal integers, duplicate-key rejection, UTF-8 bytes, SHA-256. Golden vectors in `QUERY_ID_VECTORS.md`. Prototype tests for equivalence and distinctness.

## §5. D3 claim/query boundary (P2)

**Finding:** HOLDS might be read as prose-claim verification when link is UNVERIFIED.

**Correction:** `claim_query_link: VERIFIED | UNVERIFIED` is now a normative ResultRecord field (was prose-only). Normative text: the semantic result describes the formal query identified by `query_id`; HOLDS's mathematical meaning unchanged. Prototype already emits the field with explanatory note; test verifies.

## §6. Capacity-overflow semantics

**Finding:** `CAPACITY_EXCEEDED` named in inventory but not in typed result schema.

**Correction:** Normative: capacity overflow → typed result with `capacity_exceeded{parameter, limit, actual, detail}` + `INCONCLUSIVE{reason: "capacity-exceeded"}` + no basis. Distinct from INVALID_INPUT and INTERNAL_ERROR. Prototype: `run()` catches CAPACITY_EXCEEDED and returns typed result (no longer raises). Tests updated.

## §7. Project records

- `PROJECT_STATE.md`, `README.md`, `CHANGELOG.md` identify 0.8.9.2 as review candidate; history preserved.
- Manifest with full SHAs (see `CANDIDATE_MANIFEST_0892.md`).

## §8. Verification

| Check | Result |
|---|---|
| Formal model (Z3) | 27/27 scenarios behave as expected |
| Prototype suite | 151/151 pass (147 + 4 UNKNOWN experiment) |
| Canonical descriptor vectors | 16/16 (inherited, unchanged) |
| Query identity vectors | 4/4 golden vectors match |
| Genuine UNKNOWN | Reproduced (INCONCLUSIVE + weak SOLVER_BACKED) |
| M8 spec-examples | 5/6 pass; 1 FAIL (see below) |

**M8 finding (genuine, not hidden):** B.11 example 5 FAILs with "unbound identifier 'base_code'". The specification claims (line 16) "all §B.11 examples pass M8 parse + resolve + type-check," but M8's grammar does not resolve `base_code` (defined at spec line 336 as `String->String`). This is a spec-claim vs tool-capability inconsistency predating 0.8.9.2. The output is preserved in `m8_output_0892.txt` (exit code 1). Fixing the spec claim or extending M8's grammar is outside WO-1.9B scope; reported for owner decision.

## Limitations

1. M8 was run via isolated copy (not skipped); 1/6 examples fail as documented above.
2. The `string-not-normalized` removal changes the admission predicate from 30 to 29 codes. This is intentional per the approved A6 policy, but it is a breaking change to the closed predicate.
3. Candidate 0.8.9.2 requires owner review. No D7 decision made.
