# MSVE Acceptance Plan v0.1 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.1 · **Design spec:** `MSVE_DESIGN_SPEC_v0.1.md`

This plan defines measurable acceptance criteria for the first proposed MSVE
vertical slice: the GrimChess Order 7 PM-E0 selector contract. Executing this
plan requires separate explicit authorization. Nothing here authorizes Order 7.2,
any repository change, or any modification to the GrimChess archive.

---

## 1. Baseline (preserved as reported — not re-argued here)

- Published evidence: PM-E0, empty-prior condition, **selected candidate[0] in
  75/75 positions**; determinism 75/75; 11/75 exact probability ties resolved by
  (Stockfish rank, lexical UCI).
- Status of this baseline: **reported empirical evidence over the 75-position
  panel**, not a universal theorem.
- **Baseline correction (binding on this plan):** malformed-input rejection was
  *implemented* in the Order 7 adapter but the malformed-input cases were **never
  executed**. This plan must execute them; it must not claim they passed.

## 2. Formal contract under test (to be frozen before execution)

The selector contract to be specified, frozen, then checked:

1. **Membership:** output ∈ supplied candidate set (no invented moves).
2. **Ranking:** output = argmax over the declared ordering (probability,
   tie-break (rank, lexical UCI)).
3. **Determinism:** identical inputs → identical outputs, across processes.
4. **Invalid-input handling:** empty candidate set, malformed entries, and
   candidates violating the type contract are rejected with declared errors —
   never silently defaulted.

## 3. Acceptance criteria

### 3.1 Universal properties (formal or sound-procedure claims)

| # | Property | Method required | Pass condition |
|---|---|---|---|
| U1 | Membership for all well-formed inputs | Proof or exhaustive argument over the input class | Kernel-checked proof, or sound procedure with recorded guarantees |
| U2 | Deterministic tie-breaking for all ties | Proof or exhaustive argument | Same as U1 |
| U3 | Rejection (never silent default) for all invalid inputs | Proof or exhaustive argument over the invalid-input class | Same as U1; invalid-input class explicitly enumerated |

If a universal claim cannot be established, the result is a **bounded claim**
(§3.3) — never an overstated universal.

### 3.2 Differential testing (independent reference implementation)

- An **independently written reference selector** implements the same frozen
  contract. Separation requirements: written without reusing the primary
  implementation's ranking code; preferably a different author or a different
  implementation language/strategy; its own test suite.
- **Differential test:** both implementations run over the 75 frozen Order 7
  snapshots plus the fuzz corpus (§3.3); every disagreement is a recorded
  discrepancy triggering investigation — never silent selection of the more
  plausible result.

### 3.3 Property-based and fuzz testing (bounded claims)

- **Fuzz corpus:** randomly generated candidate sets — varying sizes (0, 1, 2,
  many), exact probability ties (2-way, 3-way, all-tie), near-ties at float
  boundaries, malformed entries (missing fields, wrong types, duplicate UCIs),
  empty sets. Seeds recorded; runs reproducible.
- **Properties checked on every case:** membership, declared ordering,
  determinism (run twice, compare), rejection behaviour on invalid inputs.
- **Malformed-input suite:** the cases Order 7 never executed — executed here,
  results recorded individually.
- **Limits stated:** a green fuzz corpus bounds the claim to tested inputs; it
  does not prove the universal property (§E anti-conflation rule).

### 3.4 Agreement with the empirical baseline

- The verified implementation must reproduce the 75/75 Order 7 selections when
  run over the frozen snapshots (regression check against reported evidence).
- Any deviation is a finding, not a failure to hide: investigate, record, adjudicate.

### 3.5 Provenance and independent reproduction

- Every acceptance run produces a result package per §G of the design spec:
  spec hash, input hashes, tool/checker versions, seeds, witnesses, outputs.
- An independent re-run (different machine or reviewer) must reproduce the
  recorded results.

## 4. Discrepancy protocol

| Event | Required response |
|---|---|
| Reference vs. primary disagree | Halt acceptance; record both outputs and inputs; investigate root cause; adjudicate explicitly |
| Checker divergence | CHECKER_DIVERGENCE status; discrepancy preserved in the record |
| Fuzz finds a contract violation | Record as counterexample witness; contract or implementation revised only via a new frozen spec version |
| Timeout / resource exhaustion | TIMEOUT; never reinterpreted as a property holding or failing |

## 5. Marginal value statement (required in the acceptance report)

The report must answer, in writing:

1. Which guarantees established here **generalize beyond the 75 recorded
   positions** (universal properties, §3.1)?
2. Which remain **bounded to tested examples** (§3.3)?
3. What did formal verification detect that the empirical panel could not
   (if anything)? — and honestly report "nothing beyond the panel" if that is
   the outcome.
4. What remains **experimentally unknown** (e.g., chess strength — out of scope
   for MSVE by design)?

A finding of "no additional defects; universal properties proved for the input
class" is a successful outcome. The acceptance case tests the *engine's
guarantees*, not the selector's cleverness.

## 6. Entry conditions (before any execution)

- [ ] Design spec reviewed and frozen (genesis-commit rule applies at repo creation).
- [ ] Selector contract specification written, reviewed, frozen.
- [ ] Independent reference implementation written under the separation requirements.
- [ ] Fuzz corpus design and seeds recorded.
- [ ] Explicit authorization to execute the vertical slice.

*End of MSVE_ACCEPTANCE_PLAN_v0.1.md (draft for review).*
