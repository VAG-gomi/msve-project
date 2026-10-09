# MSVE Acceptance Plan v0.3 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.3 · **Design spec:** `MSVE_DESIGN_SPEC_v0.3.md`
**Supersedes:** `MSVE_ACCEPTANCE_PLAN_v0.2.md` (retained as historical draft)

Normative contract: `MSVE_DESIGN_SPEC_v0.3.md`, Appendix 2 (formal selector
contract v0.3, corrected comparator). Normative result schema: spec §E.2.
Executing this plan requires separate explicit authorization. Nothing here
authorizes Order 7.2, any repository change, or any modification of the
GrimChess archive. **Code generation is out of scope for this vertical slice**
(spec §D.5); it proceeds as a contract-verification case.

---

## 1. Baseline (preserved as reported)

- PM-E0, empty-prior condition: **candidate[0] in 75/75**; determinism 75/75;
  11/75 exact ties resolved by (lower Stockfish rank, lexicographically smaller
  UCI) — verified against the preserved adapter source.
- Status: EVIDENCE_RECORDED with provenance (Order 7 publication), not an MSVE
  semantic result. Not re-argued here; not reinterpreted to match the new contract.
- **Binding correction:** malformed-input rejection was implemented but never
  executed in Order 7. This plan executes those cases when authorized; it does
  not claim they passed.

## 2. Objects under test (Correction D)

Two separate objects, separate contracts, separate assurance:

| Object | Contract | Input domain |
|---|---|---|
| **Abstract selector** | Appendix 2 §A2.2–A2.4, A2.6–A2.7: pure function on well-formed candidate sets; unique `prefers`-maximal element; existential membership | Well-formed `CandidateSet` |
| **Abstract validator** | Appendix 2 §A2.5: accepts iff non-empty set, non-empty ASCII UCIs, pairwise-distinct UCIs, Nat ranks, finite scores; otherwise rejects naming the defect | Raw/serialized input |

No proof about the abstract selector establishes anything about the validator,
and neither establishes anything about its implementation without L2 evidence.

## 3. End-to-end acceptance path (§11)

Conceptual steps (proposed; none executed under this work order):

1. **Parse and validate** the frozen `selector-contract/0.3.0` specification
   under the §B grammar; admission must be ACCEPTED (any INVALID_INPUT here is a
   finding about the spec, recorded before any further step).
2. **Produce and assess** the abstract selector contract (`prefers`,
   `contract_holds`) and the abstract validator contract; freeze both.
3. **Establish L1 properties** (§4) by proof or sound procedure.
4. **Identify the L2 conformance method per claim** (§5) or mark the claim
   unavailable — never assume a method from a list of options.
5. **Run L3 checks** (§6) only if a later work order authorizes execution:
   75-snapshot regression, differential comparison, property fuzzing,
   malformed-input suite.
6. **Emit the result record + evidence package** under the §E.2 schema, with
   per-property verification records and the computed summary.
7. **Assess marginal value** (§7): what was established beyond the Order 7 panel,
   in L1/L2/L3 terms.

## 4. L1 claims — object, method, status

| # | Claim | Object | Proposed method | Status |
|---|---|---|---|---|
| U1 | `prefers` is a strict total order on well-formed candidates | Abstract selector | Proof: trichotomy per component (binary64 exact order on finite values; Nat; bytewise string order) composed lexicographically | Proposed (proof sketch in spec App. 2 §A2.3) |
| U2 | Every non-empty well-formed set has a unique maximal element | Abstract selector | Proof: finite non-empty set under a strict total order has a unique maximum (U1) | Proposed |
| U3 | Membership: output satisfies ∃c ∈ C | Abstract selector | Proof: the maximal element is a member of C by construction | Proposed |
| U4 | Determinism: pure function of input | Abstract selector | Proof: comparator has no external state; follows from U1–U2 | Proposed |
| V1 | Validator accepts exactly the well-formed inputs | Abstract validator | Proof: finite case analysis over the admission checklist (App. 2 §A2.5) — each checklist item decided, accept iff all pass | Proposed |
| V2 | Validator rejects every invalid input, naming the defect | Abstract validator | Proof: same case analysis — the invalid-input class is precisely the complement of the checklist, enumerated in §6 | Proposed |

**R2 note (retained):** the input class (all finite candidate sets) is unbounded;
enumeration cannot establish U1–U4. The structural arguments above are required;
fuzzing alone never upgrades a claim to L1.

## 5. L2 conformance — per-claim method or explicit unavailability

| Claim | Proposed L2 method | Availability |
|---|---|---|
| U1–U4 → selector implementation | Transcription audit: the implementation is a direct transcription of the proved comparator procedure; audit checks line-by-line correspondence + differential testing vs the independent reference (bounded conformance evidence) | Proposed; **checked refinement proof marked unavailable in v0** — the L2 claim is therefore "transcription-audited and differentially tested (bounded)", honestly labelled, not a proof of conformance |
| V1–V2 → validator implementation | Checklist review: implementation reviewed against the finite admission checklist + malformed-input fuzzing (bounded) | Proposed; full conformance proof unavailable in v0 — same bounded labelling |
| Code generation conformance | N/A — generation out of scope for this slice | Explicitly excluded |

The plan does not assume any L2 method from the options list. Where the stronger
method is unavailable, the claim is capped and labelled — never silently upgraded.

## 6. L3 checks (bounded; execution requires separate authorization)

- **Regression:** the 75 frozen Order 7 snapshots; expected: reproduce 75/75
  selections (comparison against reported evidence, not re-proof).
- **Differential:** independent reference implementation (separation: no shared
  ranking code; preferably different author/language; own test suite) over
  snapshots + fuzz corpus; disagreements → CHECKER_DIVERGENCE, investigate.
- **Property fuzzing:** candidate sets of sizes 0/1/2/many; exact score ties;
  ±1 ulp near-ties; signed zeros; malformed entries (missing fields, wrong
  types, duplicate UCIs, NaN/±Inf scores, empty UCIs, empty sets); seeds
  recorded; oracle = the Appendix 2 comparator (corrected: smaller UCI wins ties).
- **Malformed-input suite:** the Order 7 cases never executed — executed here,
  results recorded individually. Not claimed passed until run.
- **Invalid-input class** (for V2 bounded evidence): empty set; missing `uci` /
  `rank` / `score`; wrong types; duplicate UCIs; non-finite scores; empty UCI
  strings; non-ASCII UCI content.
- **Limits:** green fuzzing bounds claims to tested inputs; never a universal proof.

## 7. Marginal value assessment (required in the acceptance report)

In L1/L2/L3 terms, the report must state:

1. **L1:** which universal properties were proved (U1–U4, V1–V2) and by what
   method — these generalize beyond the 75 positions.
2. **L2:** what conformance evidence links the properties to the actual code,
   and where conformance is capped at bounded evidence (transcription audit +
   differential testing, not refinement proof).
3. **L3:** coverage counts — fuzz cases, edge cases, malformed inputs executed —
   and the regression result against the 75-panel.
4. What remains **experimentally unknown** (chess strength — out of scope by
   design; recorded only if supplied as EVIDENCE_RECORDED).

An honest "no defects found beyond the panel; L1 proved; L2 bounded" is a
successful outcome. If nothing beyond the panel is found, the report says so.

## 8. Worked examples

### 8.1 Tie-break under the corrected comparator (adversarial case 1)

Candidates: `{uci:"e2e4", rank:0, score:0.5}`, `{uci:"d2d4", rank:0, score:0.5}`.
Scores equal; ranks equal; UCI comparison: `"d2d4" < "e2e4"` bytewise →
`prefers(d2d4-candidate, e2e4-candidate)` holds by clause 3. Selected: `d2d4`
(the lexicographically smaller UCI). Under the v0.2 key-tuple formula the
answer would have been `e2e4` — demonstrating the corrected rule differs and
why the explicit comparator is required. Matches the preserved Order 7 adapter
behaviour.

### 8.2 Projection-relative uniqueness (carried from v0.2, R5)

Models m₁ (scores [0.5,0.3,0.2]) and m₂ (scores [0.6,0.25,0.15]), both selecting
"e2e4". Under the selection projection: equivalent (exact UCI equality). Under
the probability-output projection: distinct (exact bitwise difference of
canonicalized sequences). The spec must declare the projection before
evaluation; without it, INVALID_INPUT.

## 9. Discrepancy protocol (result-record terms)

| Event | Record fields |
|---|---|
| Reference vs primary disagree | verification_records: two conflicting records → verification_summary=CHECKER_DIVERGENCE; discrepancy with required follow-up; halt acceptance |
| Fuzz finds violation | semantic_result=VIOLATED + counterexample witness; spec/impl revised only via new frozen version |
| Timeout | execution=TIMEOUT; partial_results labelled; semantic_result=INCONCLUSIVE(RESOURCE_EXHAUSTED) |
| Solver unknown | semantic_result=INCONCLUSIVE(SOLVER_UNKNOWN); uniqueness refused |
| UNSAT, Level A required, only B available | solver_observation={UNSAT,…}; semantic_result=INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET); assurance_shortfall=true |
| Split properties | records preserved individually; summary=FAIL if any FAIL |

## 10. Entry conditions (before any execution)

- [ ] Design spec v0.3 reviewed (freeze is a separate owner decision).
- [ ] Selector + validator contracts written, reviewed, frozen.
- [ ] Independent reference implementation under the separation requirements.
- [ ] Fuzz corpus design and seeds recorded.
- [ ] L2 methods per §5 confirmed or claims capped.
- [ ] Explicit authorization to execute.

*End of MSVE_ACCEPTANCE_PLAN_v0.3.md (draft for review).*
