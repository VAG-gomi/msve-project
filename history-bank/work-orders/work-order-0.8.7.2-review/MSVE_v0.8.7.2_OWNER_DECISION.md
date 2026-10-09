# MSVE v0.8.7.2 — Owner Decision Packet

## Decisions ranked by importance

### 1. Claim identity for payload-free variants (BLOCKING)

**Question:** What identifies the exact mathematical claim for `HOLDS`,
`NO_SOLUTION`, `CONTRADICTION`, and `UNIQUE_UNDER_PROJECTION`?

**Options:** (A) Canonical claim descriptor (new field + collection);
(B2) single `claim_ref: Hash` field; (B1) pure convention (not
recommended).

**Recommendation:** Option A. Claim identity is load-bearing for the
central requirement; it should be first-class, not convention-encoded.
Cost: schema change, canonical encoding specification, producer updates.

**If declined:** The `TEST_BACKED` + `HOLDS` path — the natural
test-backed check-goal outcome — cannot satisfy the evidence-relevance
requirement. Either prohibit bases for payload-free variants (a
normative restriction with its own consequences) or accept that
relevance is unevaluable there.

### 2. Solver-observation claim linkage (HIGH)

**Question:** Must `SOLVER_BACKED` link the observation to the exact
claim, or is presence + outcome-compatibility sufficient?

**Finding:** The wrong-claim counterexample (UNSAT for A + result for
B + SOLVER_BACKED) is currently permitted. `provenance_ref` is
undefined.

**Recommendation:** Define `provenance_ref` → `solver_invocations`
collection with `claim_id` binding (Work 3 proposal). Cost: one new
collection + normative definition. Without this, SOLVER_BACKED remains
the weakest basis — presence without relevance.

### 3. Reverification of the final model (MEDIUM)

**Question:** Can the 18/18 report be treated as verification of the
final model (`7239f606…`)?

**Finding:** No. The raw log (14:05:48Z) predates the R1-4 fix
(14:08:11). The SAT witnesses (14:08:14) tie to the final model, but
the full 18/18 stdout for the final model was not preserved.

**Recommendation:** Re-run the suite with raw-log preservation in a
future work order. Do not treat the current 18/18 as covering the
final model file.

### 4. Independent model review (MEDIUM)

**Status:** Incomplete. The 18/18 suite is behavioral evidence, not a
substitute. Recommend completing an independent review before any
baseline consideration.

### 5. Sentinel removal (LOW, contingent on #1)

The `__no_claim_key__` sentinel must be deleted once claim identity is
decided. It currently fabricates a requirement for undefined cases.

## Least ambiguous path

1. Owner decides claim identity (recommend Option A).
2. Owner decides solver-linkage scope (recommend invocation binding).
3. Apply both as a bounded v0.8.8 correction (new candidate dir).
4. Re-run full suite with raw-log preservation.
5. Complete independent model review.
6. Then — and only then — consider baseline.

## What must be clear

- A solver observation's **presence is insufficient** for
  `SOLVER_BACKED` when its connection to the claim is not established.
- Unsupported claim identity must not be hidden behind a sentinel or
  inferred from an unrelated artefact.
- The current 18/18 report **cannot** be treated as verification of the
  final model until source identity and execution provenance are
  reconciled (see `MSVE_v0.8.7.2_SOURCE_IDENTITY_AUDIT.md`).
- An independent model review **remains incomplete**.

---

OWNER DECISION PACKET PREPARED — NO NORMATIVE CHANGES MADE
