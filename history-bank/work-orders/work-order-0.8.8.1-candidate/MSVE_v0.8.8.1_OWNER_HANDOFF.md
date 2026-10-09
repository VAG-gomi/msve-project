# MSVE v0.8.8.1 Owner Handoff

**Work Order:** 0.8.8.1 — Formal Closure of Claim and Solver Linkage
**Date:** 2026-10-09
**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED

## Source (0.8.8, preserved unchanged)

- Spec: `69828cb4c1048f2e233d6d6fefeecc86b4a1e337e6566405293e65d8eef2505f` (95530 bytes)
- Model: `2a3222a9022df0da45bc5f4ba460936c3f4ded6fd800e829ba849260ce6f1762` (19714 bytes)

## Candidate (0.8.8.1, new)

- Spec: `dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782`
- Model: `fc6eb49f50eae0456d183b88b51d3a6d315c0a7cbbcaac4dff4e5abba3712c2`
- Tests: 9/9 pass, raw log preserved

## What was closed

1. **Outcome compatibility (mechanical):** `_outcome_compatible` enforces per-kind table including sr-variant check (M1 repaired). `holds`+UNSAT requires `sr=HOLDS`; `holds`+SAT requires `sr=VIOLATED`; `derive`/`prove` diagnostic-only; UNKNOWN rejected. Seven kinds explicitly marked unresolved (N-0.8.8.1-1).
2. **Descriptor completeness:** Structured slots with mandatory-field flags; all four `has_*` required; incomplete rejected (D4).
3. **spec_version/input linkage:** `ResultRecord` gains `spec_version` and `claim_kind` (N-0.8.8.1-3); inv 25/26/28 check `vr.spec_version`; inv 27 checks invocation spec_version (N-0.8.8.1-2).

## Independent reviews

**Normative:** 3 blocking (N-0.8.8.1-1/2/3) — all repaired, re-verified.
**Model:** 1 blocking (M1) — repaired, re-verified. 1 non-blocking (M2: assumptions not modeled).

## Labels

- **Normatively defined:** outcome_compatible table, descriptor mandatoriness, spec_version linkage, inv 29.
- **Mechanically enforced:** All of the above except: assumptions field, query↔kind fidelity, 7 unresolved kinds (rejected, not defined).
- **Exercised by test:** 9 cases covering all three objectives.
- **Independently reviewed:** Both reviews complete on final hashes; all blocking findings repaired.
- **Attested not verifiable:** Checker independence/authorization; query faithfully encodes claim; solver actually ran.
- **Unresolved:** 7 claim kinds in outcome table (explicitly marked); assumptions not modeled.

## Schema changes (proposals)

1. `ResultRecord.claim_id: Option<Hash>` (0.8.8)
2. `ResultRecord.claim_kind: String` (0.8.8.1)
3. `ResultRecord.spec_version: SemVer` (0.8.8.1)
4. `VerificationRecord.claim_id: Hash` (0.8.8)
5. `VerificationRecord.spec_version` now constrained (0.8.8.1)
6. `ClaimDescriptor` with stored `claim_id` (0.8.8)
7. `EvidenceBundle.claim_descriptors`, `solver_invocations` (0.8.8)
8. `SolverInvocation.claim_kind` (0.8.8)

No baseline, release, or implementation authorized.
