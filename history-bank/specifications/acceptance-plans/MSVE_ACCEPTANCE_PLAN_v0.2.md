# MSVE Acceptance Plan v0.2 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.2 · **Design spec:** `MSVE_DESIGN_SPEC_v0.2.md`
**Supersedes:** `MSVE_ACCEPTANCE_PLAN_v0.1.md` (retained as historical draft)

This plan defines measurable acceptance criteria for the first proposed MSVE
vertical slice: the GrimChess Order 7 PM-E0 selector contract. Executing this
plan requires separate explicit authorization. Nothing here authorizes Order 7.2,
any repository change, or any modification to the GrimChess archive.

Normative contract: `MSVE_DESIGN_SPEC_v0.2.md`, Appendix 2 (formal selector
contract v0.2). This plan references it; it does not restate it.

---

## 1. Baseline (preserved as reported — not re-argued here)

- Published evidence: PM-E0, empty-prior condition, **selected candidate[0] in
  75/75 positions**; determinism 75/75; 11/75 exact probability ties resolved by
  (Stockfish rank, lexical UCI).
- Status of this baseline: **reported empirical evidence over the 75-position
  panel**, not a universal theorem. In v0.2 terms: EVIDENCE_RECORDED with
  provenance (the Order 7 publication), not a semantic result established by MSVE.
- **Baseline correction (binding on this plan):** malformed-input rejection was
  *implemented* in the Order 7 adapter but the malformed-input cases were **never
  executed**. This plan must execute them; it must not claim they passed.

## 2. Assurance levels (Correction D)

Acceptance evidence is separated into three levels, reported separately:

- **L1 — Mathematical model.** Properties of the *abstract selector algorithm*
  (Appendix 2, §A2.3–A2.7): membership, total-order ranking, determinism as a
  pure function. Established by proof (kernel-checked) or another sound procedure
  with recorded guarantees.
- **L2 — Implementation conformance.** Evidence that the *actual implementation*
  conforms to the mathematical model. Method must be named for each claim
  (checked refinement, translation validation, static analysis, or a documented
  limited method). An L1 proof alone establishes nothing about the code.
- **L3 — Tested behaviour.** Regression over the 75 frozen snapshots,
  differential comparison against the independent reference implementation,
  property-based and fuzz testing over executed inputs. Bounded to tested inputs.

The acceptance report must keep L1/L2/L3 visibly separate. A green L3 does not
upgrade an unproved L1; an L1 proof does not substitute for L2 conformance evidence.

## 3. Acceptance criteria

### 3.1 L1 — Universal properties (R2)

| # | Property | Method required | Pass condition |
|---|---|---|---|
| U1 | Membership (∃c ∈ C: output.uci = c.uci) for all well-formed inputs | Proof or sound procedure | Kernel-checked proof, or sound procedure with recorded guarantees |
| U2 | Unique-maximum ranking under the total order for all well-formed inputs | Proof or sound procedure | Same as U1 |
| U3 | Rejection (never silent default) for all invalid inputs | Proof or sound procedure over the enumerated invalid-input class | Same as U1; invalid-input class explicitly enumerated (empty set, malformed entries, duplicate UCIs, non-finite scores) |

**R2 — why "exhaustive argument" needs care.** The input class (finite candidate
sets) is *unbounded*: sets may be arbitrarily large, so enumeration can never
cover it. A universal property over this class cannot be established by testing,
however extensive. What is required is a **structural argument** — e.g., induction
over the selection procedure's structure, or a proof that the comparison defines
a total order and the scan returns its maximum. "Exhaustive" here means exhaustive
*over the structure of the argument* (all cases of the induction / all branches
of the procedure), not over inputs. If no such argument is available, the claim
is downgraded to a bounded L3 claim — never overstated.

If a universal claim cannot be established, the result is a **bounded claim**
(§3.3) — never an overstated universal.

### 3.2 L2 — Implementation conformance

- For each L1 property, name the conformance method linking the abstract
  algorithm to the actual implementation (e.g., "the implementation is a direct
  transcription of the proved selection procedure; transcription checked by
  [method]").
- Where v0 provides no conformance method for a claimed property, the property's
  acceptance is capped at L3 and the gap recorded explicitly.
- Generated code (if the restricted G1 generator is used) carries template-
  instantiation links to spec lines; generation correctness itself is established
  only via L2/L3 methods, not asserted from generation.

### 3.3 L3 — Differential testing (independent reference implementation)

- An **independently written reference selector** implements the same frozen
  contract (Appendix 2). Separation requirements: written without reusing the
  primary implementation's ranking code; preferably a different author or a
  different implementation language/strategy; its own test suite.
- **Differential test:** both implementations run over the 75 frozen Order 7
  snapshots plus the fuzz corpus (§3.4); every disagreement is a recorded
  discrepancy triggering investigation — never silent selection of the more
  plausible result.

### 3.4 L3 — Property-based and fuzz testing (bounded claims)

- **Fuzz corpus:** randomly generated candidate sets — varying sizes (0, 1, 2,
  many), exact score ties (2-way, 3-way, all-tie), near-ties at binary64
  boundaries (±1 ulp), signed-zero cases, malformed entries (missing fields, wrong
  types, duplicate UCIs, NaN/±Inf scores), empty sets. Seeds recorded; runs
  reproducible. Numeric edge cases follow the contract's exact-comparison rule
  (Appendix 2, §A2.5) — no tolerance-based oracles.
- **Properties checked on every case:** membership, declared ordering,
  determinism (run twice, compare), rejection behaviour on invalid inputs.
- **Malformed-input suite:** the cases Order 7 never executed — executed here,
  results recorded individually.
- **Limits stated:** a green fuzz corpus bounds the claim to tested inputs; it
  does not prove the universal property (R2).

### 3.5 Agreement with the empirical baseline

- The implementation must reproduce the 75/75 Order 7 selections when run over
  the frozen snapshots (regression check against reported evidence).
- Any deviation is a finding, not a failure to hide: investigate, record, adjudicate.

### 3.6 Provenance and independent reproduction

- Every acceptance run produces a result package per §G of the design spec:
  result record (orthogonal status fields), spec hash, input hashes, tool/checker
  versions, seeds, witnesses, outputs.
- An independent re-run (different machine or reviewer) must reproduce the
  recorded results.

## 4. Worked uniqueness mini-example (R5)

*Illustrative — shows the §D procedure applied. Not an executed test.*

Suppose a `compare-models` goal asks about the selector's probability model under
two candidate projections, with the frozen contract's numeric semantics
(exact canonicalized binary64 comparison):

- **Model m₁:** scores [0.5, 0.3, 0.2] → selects UCI "e2e4".
- **Model m₂:** scores [0.6, 0.25, 0.15] → selects UCI "e2e4".

**Under the selection projection** (π(m) = selected UCI):
π(m₁) = π(m₂) = "e2e4". Exact string equality holds → the models are
**equivalent** under this projection. The second-model query
"π(m₂) ≠ π(m₁)" is UNSAT *for this pair* — but pair-wise equivalence is not a
uniqueness result; the procedure must run the query against the full constraint
system, and uniqueness requires the query to be UNSAT with a complete decision
procedure (§D.2).

**Under the probability-output projection** (π(m) = canonicalized score sequence):
π(m₁) = [0.5, 0.3, 0.2] ≠ [0.6, 0.25, 0.15] = π(m₂) by exact bitwise comparison
of canonical forms → the models are **distinct**. If both satisfy the spec
constraints, the semantic result is UNDERDETERMINED with (m₁, m₂) as witnesses
and the differing score sequences recorded.

**The point:** the specification must declare which projection the uniqueness
question is asked under *before* the engine evaluates it. The same two models
are equivalent under one projection and distinct under another — there is no
projection-free fact of the matter. A uniqueness-seeking goal without a declared
projection is INVALID_INPUT (R3).

## 5. Discrepancy protocol

| Event | Required response (result-record terms) |
|---|---|
| Reference vs. primary disagree | Halt acceptance; `verification: CHECKER_DIVERGENCE`; record both outputs and inputs; investigate; adjudicate explicitly |
| Fuzz finds a contract violation | Record as counterexample witness; `semantic_result: VIOLATED`; contract or implementation revised only via a new frozen spec version |
| Timeout / resource exhaustion | `execution: TIMEOUT`; partial results labelled; never reinterpreted as a property holding or failing |
| Solver returns unknown | `semantic_result: INCONCLUSIVE(SOLVER_UNKNOWN)`; uniqueness/coverage claims refused |
| UNSAT assurance shortfall | `semantic_result: CONTRADICTION` with `assurance: LEVEL_B_SOLVER_BACKED` and the unmet requirement flagged (spec §F.5) |

## 6. Marginal value statement (required in the acceptance report)

The report must answer, in L1/L2/L3 terms:

1. **L1:** which guarantees generalize beyond the 75 recorded positions as
   universal properties — and by which proof or sound procedure?
2. **L2:** what conformance evidence links those properties to the actual code —
   and where is conformance *not* established?
3. **L3:** what did differential testing and fuzzing cover that the 75-panel did
   not (counts: fuzz cases, edge cases, malformed inputs executed)?
4. What remains **experimentally unknown** (e.g., chess strength — out of scope
   for MSVE by design; recorded as EVIDENCE_RECORDED only if supplied)?

A finding of "no additional defects; L1 properties proved for the input class;
L2 conformance established by [method]; L3 green over N cases" is a successful
outcome. The acceptance case tests the *engine's guarantees*, not the
selector's cleverness. If the honest outcome is "nothing beyond the panel was
found," the report says so.

## 7. Entry conditions (before any execution)

- [ ] Design spec reviewed and frozen (genesis-commit rule applies at repo creation).
- [ ] Selector contract specification (Appendix 2) written, reviewed, frozen.
- [ ] Independent reference implementation written under the separation requirements.
- [ ] Fuzz corpus design and seeds recorded.
- [ ] Conformance methods for L2 claims named.
- [ ] Explicit authorization to execute the vertical slice.

*End of MSVE_ACCEPTANCE_PLAN_v0.2.md (draft for review).*
