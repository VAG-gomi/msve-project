# MSVE Continuity Package — 06 OWNER DECISIONS AND OPEN QUESTIONS

## Already decided [OWNER DECISION]

1. **Canonical claim descriptor (Option A)** over output-hash-only identity. Rationale: distinct goals with identical outputs (`derive 2+2` vs `derive 8/2`) must be distinct claims. Selected as the working direction for 0.8.8; implemented in 0.8.8/0.8.8.1.
2. **Syntactic identity policy.** Distinct goal/proposition/inputs → distinct `claim_id`, even if outputs coincide. Semantic equivalence not attempted. (Recorded in §E.6b.)
3. **`solver_invocations` collection.** Purpose: bind claim → query → invocation → observation → conclusion. Scope: invocation identity, claim linkage, inputs, spec_version, outcome compatibility.
4. **Claim-linked solver provenance required.** Presence of a solver observation is insufficient for SOLVER_BACKED (0.8.7.2 forensic conclusion; enforced since 0.8.8).
5. **Per-goal outcome interpretation** (not a generic SAT/UNSAT map). Implemented as `outcome_compatible`.

## Open questions [UNRESOLVED]

### Q1. The seven unresolved claim kinds (blocking for V0 scope)

The outcome table does not define solver-outcome interpretation for: `no_solution`, `contradiction`, `unique_under_projection`, `violated`, `underdetermined`, `disproved`, `artifact_constructed`.

**Options:**
- (a) Extend the table with per-kind rules (requires normative design work).
- (b) Declare these kinds explicitly unsupported for SOLVER_BACKED in V0 (a scope decision with consequences for inv 22/23, which contemplate solver observations for CONTRADICTION and UNIQUE_UNDER_PROJECTION).
- (c) Leave marked unresolved (current state; blocks any claim of formal closure).

**Technical consequence:** Until decided, a solver observation may be *recorded* for these kinds (per inv 22/23) but cannot *justify* SOLVER_BACKED. [INFERENCE]

### Q2. Query and assumption fidelity

The model does not check that a solver `query` faithfully encodes the claim, nor that `assumptions` match. These are attestations. **Question:** is attestation sufficient for V0, or is a query-audit mechanism required?

### Q3. Checker authorisation and independence

`checker ≠ ""` is enforced; that the checker is an authorized kernel, and that a recompute checker is independent of the producer, are attestations with no normative format. **Question:** define an attestation schema, or accept the gap?

### Q4. Bounded slots

Two verification records, two descriptors, two invocations per result. **Question:** is this an acceptable V0 bound, or must the schema support arbitrary counts?

## Criteria for future baseline acceptance

[INFERENCE — proposed, not decided]
1. All UNRESOLVED items above decided by the owner.
2. Fresh independent reviews on the exact final hashes, with no blocking findings open.
3. Regression suite covering every normative rule claimed as mechanically enforced.
4. The 7-kind outcome table either extended or explicitly scoped.
5. An explicit owner statement authorising freeze (per standing protocol: frozen design before execution; explicit per-gate authorization).
