# MSVE Acceptance Plan v0.6 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.6 · **Design spec:** `MSVE_DESIGN_SPEC_v0.6.md`
**Supersedes:** `MSVE_ACCEPTANCE_PLAN_v0.5.md` (retained as historical draft)

Normative contracts: spec Appendix 2 (selector §A2.1–A2.4/A2.6–A2.8; validator
pipeline §A2.5 + §B.11 + §B.13). Normative result schema: spec §E.1.
Regression cases: `MSVE_REGRESSION_LEDGER_v0.6.md` (D-001–D-015).
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

## 2. Objects under test

| Object | Formal interface | Contract |
|---|---|---|
| **Abstract selector** | `CandidateSet -> Candidate` (pure) | App. 2 §A2.2–A2.4, A2.6–A2.8; whole-record membership |
| **Abstract decoder** | `RawInput -> DecodeOutcome` (`RawInput = String`) | §B.13 table (10 rows, deterministic priority) |
| **Abstract validator** | `[Candidate] -> ValidationOutcome` (pure; semantic stage) | `validate` (§B.11): fixed if-chain priority |
| **Validator end-to-end** | `RawInput -> ValidationOutcome` | `validator_contract` (§B.11): decode-fail → `rejected(decode error)`; decode-ok → `validate(decoded)` — accepted data exactly equals decoded input |

Invalid inputs are tested **against the validator contract**, never against the
selector contract.

## 3. End-to-end acceptance path

1. Parse/validate frozen `selector-contract/0.6.0` and the validator spec;
   admission ACCEPTED.
2. Assess the selector contract, the three-stage validator contract, and the
   §B.13 decode table; freeze.
3. Establish L1 (§4) — three claims separate; validator L1 conditional on
   the decode table (D-012).
4. Identify L2 method per claim (§5) or mark unavailable.
5. Run L3 (§6) only if a later work order authorizes execution —
   **well-formed corpora against the selector; malformed corpora against the
   validator contract; ledger regression cases as specified**.
6. Emit the §E.1 result record + evidence package (per-property records,
   divergence-first summary, assurance required/bases/achieved + computed
   shortfall).
7. Assess marginal value (§7) vs the Order 7 panel.

## 4. L1 claims — three claims separated

For the validator pipeline, three distinct claims (never blurred):

- **(a) Abstract-model correctness.** The abstract decoder implements the
  §B.13 table; `validate` implements its if-chain; the contract binds
  accepted outputs exactly to decoded inputs — over the full `RawInput`
  domain, by structural case analysis on the table. **Conditional on the
  table's semantics** (it specifies the abstract decoder; D-012).
- **(b) Implementation conformance.** The actual implementation's parser
  and validator conform to (a) (L2).
- **(c) Bounded test evidence.** Executed tests found no failures in the
  cases tested (L3). (c) never substitutes for (b).

| # | Claim | Kind | Proposed method | Status |
|---|---|---|---|---|
| U1 | `prefers` strict total order | (a) selector | Proof: component trichotomy, lexicographic composition | Proposed |
| U2 | Unique maximum, non-empty well-formed sets | (a) selector | Proof from U1 (finite non-empty set) | Proposed |
| U3 | Whole-record membership | (a) selector | Proof: maximal element ∈ C | Proposed |
| U4 | Determinism (pure function) | (a) selector | Proof from U1–U2 | Proposed |
| V1 | Decoder implements the §B.13 table exactly | (a) decoder | Structural case analysis over the table rows; priority order total | Proposed |
| V2 | `validate` accepts exactly the semantically valid sets, with the stated error priority | (a) validator | Case analysis over the if-chain | Proposed |
| V3 | Contract binds accepted output to decoded input (no fabrication/omission/alteration/reordering) | (a) pipeline | From V1+V2: accepted ⇒ `out == validate(decoded)` and `validate` returns its input unchanged on acceptance | Proposed |

## 5. L2 conformance — per-claim method or explicit unavailability

| Claim | Proposed L2 method | Availability |
|---|---|---|
| U1–U4 → selector impl | Transcription audit + differential testing vs independent reference (bounded) | Proposed; refinement proof unavailable in v0 — capped, labelled |
| V1 (a) → decoder impl | Parser review against the §B.13 table row-by-row + malformed-input fuzzing (bounded) | Proposed; full conformance proof unavailable — capped, labelled |
| V2–V3 (a) → validator impl | Code review against `validate` + contract; targeted regression cases (bounded) | Proposed; capped, labelled |
| Claim (c) bounds | Corpora with recorded seeds; reported as bounded evidence only | Proposed |

## 6. L3 checks (bounded; execution requires separate authorization)

- **Selector corpus (well-formed only):** 75 frozen snapshots (regression,
  expect 75/75); differential vs independent reference; property fuzzing over
  well-formed sets (sizes 1/2/many, exact ties, ±1 ulp near-ties, signed
  zeros). Oracle: App. 2 comparator + whole-record membership.
- **Validator corpus:** the §B.13 table rows as cases (malformed JSON,
  non-array top level, non-object element, duplicate keys, missing/extra/
  mistyped fields, fractional rank, negative rank, overflowing score,
  underflowing score, negative-zero score); semantic cases (empty array →
  `empty-candidate-set`; duplicate UCIs → `duplicate-uci`; whitespace UCI →
  `invalid-uci`); binding probes (swapped order, fabricated candidate,
  omitted candidate → contract false). Oracle: `validator_contract`.
  **Invalid inputs never go to the selector contract.**
- **Canonical cases:** list-vs-set collision pair (must differ under
  `msve-canonical-2`); nested composites; `none` across option types;
  f64 `±0`, subnormals, short vs canonical hexfloat spellings.
- **Grammar/type cases:** bare quantifier body rejected; nested quantifiers
  derive; `-3 + 2 : Int`; `1.5 + 2` type error; guarded `case` analysis.
- Seeds recorded; limits stated; green fuzzing bounds claims to tested inputs.

## 7. Marginal value assessment (required in the acceptance report)

1. **L1:** universal properties proved (U1–U4; V1–V3 claim (a), decoder-
   conditional) and methods — generalizing beyond the 75 positions.
2. **L2:** conformance evidence per §5; where capped at bounded evidence.
3. **L3:** coverage counts for all corpora; regression vs the 75-panel.
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

### 8.4 Validator routing (D-001/D-003/D-013)

- `[{"uci":"e2e4","rank":"x","score":0.5}]` (valid JSON, rank mistyped) →
  decode: `invalid-field-type` → outcome must be `rejected("invalid-field-type")`.
- `"[]"` → decode ok with `[]` → `validate` → `rejected("empty-candidate-set")`.
  (The v0.5 contradiction is gone: rejection flows through `validate`, not
  through a negated shape predicate.)
- `[{uci:"e2e4","rank":1,"score":0.5}]` (unquoted keys) → `malformed-json`
  — kept as the separate malformed-JSON case, not conflated with the
  type-error case.
- Valid 2-candidate input, implementation returns candidates swapped →
  `validator_contract` false → VIOLATED (D-002 binding probe).

## 9. Discrepancy protocol (result-record terms)

| Event | Record fields |
|---|---|
| Reference vs primary disagree | Conflicting verification records → CHECKER_DIVERGENCE (divergence-first); halt; investigate |
| Fuzz finds violation | semantic_result=Some(VIOLATED) + witness; new frozen version for revision |
| Timeout | execution=TIMEOUT; partial_results labelled; Some(INCONCLUSIVE(RESOURCE_EXHAUSTED)) |
| Solver unknown | Some(INCONCLUSIVE(SOLVER_UNKNOWN)) |
| Empty corpus on check | Some(INCONCLUSIVE(NO_TEST_CORPUS)) — never vacuous HOLDS |
| UNSAT, Level A required, B only | solver_observation={UNSAT,…}; Some(INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET)); shortfall=true (computed) |
| Test-backed Level B | achieved=LEVEL_B, bases=[TEST_BACKED] — representable (D-010) |
| Split properties | Records preserved; DIVERGENCE dominates; else FAIL if any FAIL |

## 10. Entry conditions (before any execution)

- [ ] Design spec v0.6 reviewed (freeze is a separate owner decision).
- [ ] Selector + validator contracts (App. 2 v0.6) written, reviewed, frozen.
- [ ] Independent reference implementation under separation requirements.
- [ ] All corpora designed, seeds recorded; ledger regression cases mapped.
- [ ] L2 methods per §5 confirmed or claims capped.
- [ ] Explicit authorization to execute.

*End of MSVE_ACCEPTANCE_PLAN_v0.6.md (draft for review).*
