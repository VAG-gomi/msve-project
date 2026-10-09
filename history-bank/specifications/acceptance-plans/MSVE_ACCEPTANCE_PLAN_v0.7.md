# MSVE Acceptance Plan v0.7 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.7 · **Design spec:** `MSVE_DESIGN_SPEC_v0.7.md`
**Supersedes:** `MSVE_ACCEPTANCE_PLAN_v0.6.md` (retained as historical draft;
release gate: BLOCKED)

Normative contracts: spec Appendix 2; §B.11/§B.13; result schema §E.1.
Regression cases: `MSVE_REGRESSION_LEDGER_v0.7.md` (D-001–D-024).
Executing this plan requires separate explicit authorization. Nothing here
authorizes Order 7.2, any repository change, or any GrimChess archive
modification. **Code generation is out of scope** (spec §D.5).

---

## 1. Baseline (preserved as reported)

- PM-E0, empty-prior condition: **candidate[0] in 75/75**; determinism 75/75;
  11/75 exact ties resolved by (lower Stockfish rank, smaller UCI).
- Status: EVIDENCE_RECORDED with provenance (Order 7 publication).
- **Binding correction:** malformed-input rejection was implemented but never
  executed in Order 7. Executed here when authorized; not claimed passed until run.

## 2. Objects under test

| Object | Formal interface | Contract |
|---|---|---|
| **Abstract selector** | `CandidateSet -> Candidate` (pure) | App. 2 §A2.2–A2.4, A2.6–A2.8; whole-record membership |
| **Abstract decoder** | `RawInput -> DecodeOutcome` | §B.13 table + `DecodeOutcome` invariant + closed codes |
| **Abstract validator** | `[Candidate] -> ValidationOutcome` | `validate` (§B.11) |
| **Validator end-to-end** | `RawInput -> ValidationOutcome` | `validator_contract` (§B.11) |

Invalid inputs are tested **against the validator contract**, never against the
selector contract.

## 3. End-to-end acceptance path

1. Parse/validate frozen `selector-contract/0.7.0` and the validator spec
   (duplicate-item rule §B.7 checked at admission).
2. Assess the selector contract, the three-stage validator contract, and the
   §B.13 decode table; freeze.
3. Establish L1 (§4) — three claims separate; decoder-conditional.
4. Identify L2 method per claim (§5) or mark unavailable.
5. Run L3 (§6) only if a later work order authorizes execution.
6. Emit the §E.1 result record + evidence package (payload-carrying semantic
   results; required/bases/achieved + computed shortfall).
7. Assess marginal value (§7) vs the Order 7 panel.

## 4. L1 claims — three claims separated

- **(a) Abstract-model correctness** over the full `RawInput` domain, by
  structural case analysis on the §B.13 table — conditional on the table.
- **(b) Implementation conformance** (L2). **(c) Bounded tests** (L3).

| # | Claim | Kind | Proposed method | Status |
|---|---|---|---|---|
| U1–U4 | Selector: total order, unique maximum, membership, determinism | (a) | Proofs from the comparator | Proposed |
| V1 | Decoder implements the §B.13 table + invariant | (a) | Case analysis over table rows | Proposed |
| V2 | `validate` accepts exactly the semantically valid sets | (a) | Case analysis over the if-chain | Proposed |
| V3 | Contract binds accepted output to decoded input | (a) | From V1+V2 | Proposed |
| C1 | Canonical-3 injectivity over the supported domain | (a) | Structural induction per §G.2 | Proposed |

## 5. L2 conformance — per-claim method or explicit unavailability

| Claim | Proposed L2 method | Availability |
|---|---|---|
| U1–U4 → selector impl | Transcription audit + differential testing (bounded) | Proposed; capped, labelled |
| V1 (a) → decoder impl | Parser review row-by-row against §B.13 + malformed-input fuzzing (bounded) | Proposed; capped, labelled |
| V2–V3 (a) → validator impl | Code review + targeted regression cases (bounded) | Proposed; capped, labelled |
| C1 (a) → encoder impl | Encoder review + round-trip/collision tests (bounded) | Proposed; capped, labelled |
| Recompute checker independence | Separation requirements (dev/test independence) | Proposed |

## 6. L3 checks (bounded; execution requires separate authorization)

- **Selector corpus:** 75 frozen snapshots; differential vs independent
  reference; property fuzzing (sizes 1/2/many, exact ties, ±1 ulp near-ties,
  signed zeros).
- **Validator corpus:** §B.13 rows as cases; semantic cases (empty →
  `empty-candidate-set`; dup UCIs → `duplicate-uci`; whitespace UCI →
  `invalid-uci`); binding probes (swapped/fabricated/omitted → contract false).
- **Canonical cases (D-017/D-018):** the v0.6 collision pairs (must be
  rejected/distinguished under canonical-3); normals/subnormals/±0 round-trip;
  `inf`/`-inf` encodings; NaN → packaging failure; same-descriptor
  different-signature Impls; function value → packaging failure.
- **Grammar/type cases (D-016/D-024):** bare quantifier rejected; nested
  quantifiers derive; `-3 + 2 : Int`; `1.5 + 2` type error; `case` analysis;
  duplicate `test: differential` rejected; differential+fuzz legal.
- **Schema cases (D-022):** payload presence; §E.7 invariants (shortfall
  without description; VIOLATED without witness; Level B without spec
  acceptance).
- Seeds recorded; limits stated; green fuzzing bounds claims to tested inputs.

## 7. Marginal value assessment (required in the acceptance report)

1. **L1:** universal properties proved (U1–U4; V1–V3 claim (a),
   decoder-conditional; C1) — generalizing beyond the 75 positions.
2. **L2:** conformance evidence per §5; where capped at bounded evidence.
3. **L3:** coverage counts for all corpora; regression vs the 75-panel.
4. Experimentally unknown: chess strength — out of scope by design.

## 8. Worked examples

### 8.1 Tie-break

`{uci:"e2e4",rank:0,score:0.5}` vs `{uci:"d2d4",rank:0,score:0.5}` → selects
`d2d4` (smaller UCI). Matches the preserved Order 7 adapter.

### 8.2 Projection-relative uniqueness

m₁ vs m₂ selecting "e2e4": equivalent under selection projection; distinct
under probability-output projection. Projection declared before evaluation.

### 8.3 Membership-hole witness

Supplied `{uci:"e2e4",rank:0,score:0.5}`; implementation returns
`{uci:"e2e4",rank:0,score:100.0}` → `sel == c` fails → VIOLATED with witness.

### 8.4 Validator routing (D-001/D-003/D-013/D-020)

- `[{"uci":"e2e4","rank":"x","score":0.5}]` → `invalid-field-type`.
- `"[]"` → `empty-candidate-set` (via `validate`, no contradiction).
- `[{uci:"e2e4","rank":1,"score":0.5}]` → `malformed-json` (separate case).
- Swapped/fabricated candidates → contract false → VIOLATED.
- A decoder returning `{ok:true, error:some("malformed-json")}` →
  contract false (DecodeOutcome invariant).

## 9. Discrepancy protocol (result-record terms)

| Event | Record fields |
|---|---|
| Reference vs primary disagree | CHECKER_DIVERGENCE; halt; investigate |
| Fuzz finds violation | Some(VIOLATED {witness_ref}) + witness; new frozen version |
| Timeout | TIMEOUT; labelled partials; INCONCLUSIVE {RESOURCE_EXHAUSTED} |
| Solver unknown | INCONCLUSIVE {SOLVER_UNKNOWN} |
| Empty corpus | INCONCLUSIVE {NO_TEST_CORPUS} — never vacuous HOLDS |
| UNSAT, Level A required, B only | solver_observation={UNSAT,…}; INCONCLUSIVE {ASSURANCE_REQUIREMENT_UNMET}; shortfall=true |
| Test-backed Level B | achieved=LEVEL_B, bases=[TEST_BACKED] |
| NaN / function value at packaging | INTERNAL_ERROR(output-not-encodable: …); semantic result preserved |
| Split properties | DIVERGENCE dominates; else FAIL if any FAIL |

## 10. Entry conditions (before any execution)

- [ ] Design spec v0.7 reviewed (freeze is a separate owner decision).
- [ ] Contracts (App. 2 v0.7) written, reviewed, frozen.
- [ ] Independent reference + recompute checker under separation requirements.
- [ ] All corpora designed, seeds recorded; ledger cases mapped.
- [ ] L2 methods per §5 confirmed or claims capped.
- [ ] Explicit authorization to execute.

*End of MSVE_ACCEPTANCE_PLAN_v0.7.md (draft for review).*
