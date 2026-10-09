# MSVE Acceptance Plan v0.5 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.5 · **Design spec:** `MSVE_DESIGN_SPEC_v0.5.md`
**Supersedes:** `MSVE_ACCEPTANCE_PLAN_v0.4.md` (retained as historical draft)

Normative contracts: spec Appendix 2 (selector App. 2 §A2.1–A2.8; validator
App. 2 §A2.9 + §B.11 validator example). Normative result schema: spec §E.1.
Executing this plan requires separate explicit authorization. Nothing here
authorizes Order 7.2, any repository change, or any GrimChess archive
modification. **Code generation is out of scope** (spec §D.5).

---

## 1. Baseline (preserved as reported)

- PM-E0, empty-prior condition: **candidate[0] in 75/75**; determinism 75/75;
  11/75 exact ties resolved by (lower Stockfish rank, smaller UCI) — verified
  against the preserved adapter source.
- Status: EVIDENCE_RECORDED with provenance (Order 7 publication).
- **Binding correction:** malformed-input rejection was implemented but never
  executed in Order 7. Executed here when authorized; not claimed passed until run.

## 2. Objects under test (defect 03: interfaces defined)

| Object | Formal interface | Contract |
|---|---|---|
| **Abstract selector** | `CandidateSet -> Candidate` (pure) | App. 2 §A2.2–A2.4, A2.6–A2.7; whole-record membership |
| **Abstract validator** | `RawInput -> Option<CandidateSet>` (`RawInput = String`; `None` = rejected) | `validator_contract` (spec §B.11): accept iff `parses_as_valid(raw)` and the parsed set is well-formed; reject otherwise |

Invalid inputs are tested **against the validator contract**, never against the
selector contract: feeding a malformed set to `contract_holds` makes the
selector contract false by its `is_wellformed` precondition — that is a
test-design error, not validator evidence (defect 03).

## 3. End-to-end acceptance path

1. Parse/validate frozen `selector-contract/0.5.0` and the validator spec;
   admission ACCEPTED.
2. Assess the selector contract, the validator contract, and the
   `parses_as_valid` builtin definition (App. 2 §A2.9); freeze.
3. Establish L1 (§4) — with the three claims kept separate.
4. Identify L2 method per claim (§5) or mark unavailable.
5. Run L3 (§6) only if a later work order authorizes execution —
   **well-formed corpora against the selector; malformed corpora against the
   validator**.
6. Emit the §E.1 result record + evidence package (per-property records,
   divergence-first summary).
7. Assess marginal value (§7) vs the Order 7 panel.

## 4. L1 claims — with the three claims separated (mathematical correction)

For the validator, three distinct claims (never blurred):

- **(a) Abstract-model correctness.** The abstract validator (as formalized)
  accepts exactly the well-formed serializations over the **full** `RawInput`
  (String) domain.
- **(b) Implementation conformance.** The actual validator implementation
  conforms to the abstract model (L2).
- **(c) Bounded test evidence.** Executed malformed-input tests found no
  failures in the cases tested (L3). (c) never substitutes for (b).

| # | Claim | Claim-kind | Proposed method | Status |
|---|---|---|---|---|
| U1 | `prefers` strict total order | (a) selector | Proof: component trichotomy, lexicographic composition | Proposed |
| U2 | Unique maximum, non-empty well-formed sets | (a) selector | Proof from U1 (finite non-empty set) | Proposed |
| U3 | Whole-record membership | (a) selector | Proof: maximal element ∈ C | Proposed |
| U4 | Determinism (pure function) | (a) selector | Proof from U1–U2 | Proposed |
| V1 | Validator accepts exactly well-formed serializations | (a) validator | Proof over the abstract validator **covering the full String domain**: case analysis on the parse outcome (valid shape vs each failure mode) + per-field checklist verification; the "finite" aspect is the checklist branching — exhaustiveness over the domain is shown by the algorithm's structure (every string either satisfies `parses_as_valid` or fails a named checklist item), never by enumeration | Proposed |
| V2 | Validator rejects every invalid input, naming the defect | (a) validator | Same structural proof: the invalid class is the complement, partitioned by the first failing checklist item | Proposed |

The v0.4 phrasing ("finite case analysis over the checklist") is withdrawn as
insufficient: finiteness of the checklist does not by itself cover the infinite
input space. The proof obligation is structural coverage of the domain.

## 5. L2 conformance — per-claim method or explicit unavailability

| Claim | Proposed L2 method | Availability |
|---|---|---|
| U1–U4 → selector impl | Transcription audit + differential testing vs independent reference (bounded) | Proposed; refinement proof unavailable in v0 — capped, labelled |
| V1–V2 (a) → validator impl | Parser/validator code review against App. 2 §A2.5 + the `parses_as_valid` definition; malformed-input fuzzing (bounded) | Proposed; full conformance proof unavailable — capped, labelled |
| Claim (c) bounds | Fuzz/malformed corpora with recorded seeds; reported as bounded evidence only | Proposed |

## 6. L3 checks (bounded; execution requires separate authorization)

- **Selector corpus (well-formed only):** 75 frozen snapshots (regression,
  expect 75/75); differential vs independent reference; property fuzzing over
  well-formed sets (sizes 0-excluded/1/2/many, exact ties, ±1 ulp near-ties,
  signed zeros). Oracle: App. 2 comparator + whole-record membership.
- **Validator corpus (malformed + edge):** the Order 7 unexecuted cases;
  generated malformed serializations (missing fields, wrong types, duplicate
  UCIs incl. identical records, non-finite scores, empty/non-ASCII/whitespace
  UCIs, non-JSON text, truncated input). Oracle: `validator_contract`
  (accept/reject + defect naming). **Invalid inputs never go to the selector
  contract.**
- **Membership-hole probe:** genuine UCI with inflated score → VIOLATED under
  the whole-record predicate (passes under the withdrawn v0.3 predicate).
- Seeds recorded; limits stated; green fuzzing bounds claims to tested inputs.

## 7. Marginal value assessment (required in the acceptance report)

1. **L1:** universal properties proved (U1–U4; V1–V2 claim (a)) and methods —
   generalizing beyond the 75 positions.
2. **L2:** conformance evidence per §5; where capped at bounded evidence.
3. **L3:** coverage counts for both corpora; regression vs the 75-panel.
4. Experimentally unknown: chess strength — out of scope by design.

Honest "no defects beyond the panel; L1 proved; L2 bounded" is success.

## 8. Worked examples

### 8.1 Tie-break

`{uci:"e2e4",rank:0,score:0.5}` vs `{uci:"d2d4",rank:0,score:0.5}` → selects
`d2d4` (smaller UCI, clause 3). Matches the preserved Order 7 adapter.

### 8.2 Projection-relative uniqueness

m₁ ([0.5,0.3,0.2]) vs m₂ ([0.6,0.25,0.15]), both selecting "e2e4": equivalent
under selection projection; distinct under probability-output projection.
Projection declared before evaluation.

### 8.3 Membership-hole witness

Supplied `{uci:"e2e4",rank:0,score:0.5}`; implementation returns
`{uci:"e2e4",rank:0,score:100.0}` → `sel == c` fails → VIOLATED with witness.

### 8.4 Validator routing (defect 03)

Raw input `"[{uci:\"e2e4\",rank:\"x\",score:0.5}]"` (rank as string):
- Against `validator_contract`: `parses_as_valid` false → expected `None`;
  implementation returning `Some` → VIOLATED (validator defect).
- Against `contract_holds`: not applicable — the input is not a `CandidateSet`;
  routing it there would be a test-design error (the v0.4 flaw), now prohibited.

## 9. Discrepancy protocol (result-record terms)

| Event | Record fields |
|---|---|
| Reference vs primary disagree | Conflicting verification records → CHECKER_DIVERGENCE (divergence-first); halt; investigate |
| Fuzz finds violation | semantic_result=Some(VIOLATED) + witness; new frozen version for revision |
| Timeout | execution=TIMEOUT; partial_results labelled; Some(INCONCLUSIVE(RESOURCE_EXHAUSTED)) |
| Solver unknown | Some(INCONCLUSIVE(SOLVER_UNKNOWN)) |
| Empty corpus on check | Some(INCONCLUSIVE(NO_TEST_CORPUS)) — never vacuous HOLDS |
| UNSAT, Level A required, B only | solver_observation={UNSAT,…}; Some(INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET)); shortfall=true |
| Split properties | Records preserved; DIVERGENCE dominates; else FAIL if any FAIL |

## 10. Entry conditions (before any execution)

- [ ] Design spec v0.5 reviewed (freeze is a separate owner decision).
- [ ] Selector + validator contracts (App. 2 v0.5) written, reviewed, frozen.
- [ ] Independent reference implementation under separation requirements.
- [ ] Both corpora (well-formed; malformed) designed, seeds recorded.
- [ ] L2 methods per §5 confirmed or claims capped.
- [ ] Explicit authorization to execute.

*End of MSVE_ACCEPTANCE_PLAN_v0.5.md (draft for review).*
