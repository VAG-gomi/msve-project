# MSVE Acceptance Plan v0.4 — First Selector Vertical Slice

**Status:** DRAFT FOR REVIEW — PROPOSED, NOT AUTHORISED FOR EXECUTION
**Version:** 0.4 · **Design spec:** `MSVE_DESIGN_SPEC_v0.4.md`
**Supersedes:** `MSVE_ACCEPTANCE_PLAN_v0.3.md` (retained as historical draft)

Normative contract: spec Appendix 2 (v0.4, corrected membership and
well-formedness). Normative result schema: spec §E.1. Executing this plan
requires separate explicit authorization. Nothing here authorizes Order 7.2,
any repository change, or any modification of the GrimChess archive. **Code
generation is out of scope** (spec §D.5); this slice is contract verification.

---

## 1. Baseline (preserved as reported)

- PM-E0, empty-prior condition: **candidate[0] in 75/75**; determinism 75/75;
  11/75 exact ties resolved by (lower Stockfish rank, lexicographically smaller
  UCI) — verified against the preserved adapter source.
- Status: EVIDENCE_RECORDED with provenance (Order 7 publication), not an MSVE
  semantic result. Not reinterpreted to match the new contract.
- **Binding correction:** malformed-input rejection was implemented but never
  executed in Order 7. This plan executes those cases when authorized; it does
  not claim they passed.

## 2. Objects under test

| Object | Contract | Input domain |
|---|---|---|
| **Abstract selector** | App. 2 §A2.2–A2.4, A2.6–A2.7: pure function on well-formed sets; unique `prefers`-maximal element; **whole-record** existential membership | Well-formed `CandidateSet` |
| **Abstract validator** | App. 2 §A2.5: accepts iff non-empty set, non-empty ASCII-printable whitespace-free UCIs, pairwise-distinct UCIs (position-sensitive, identical duplicates rejected), Nat ranks, finite scores; else rejects naming the defect | Raw/serialized input |

## 3. End-to-end acceptance path

1. **Parse and validate** frozen `selector-contract/0.4.0` under the §B grammar
   (hyphenated names lex as `Slug`; trailing semicolons accepted; `output`
   resolves as the special variable). Admission must be ACCEPTED.
2. **Assess** the abstract selector contract (`prefers`, `contract_holds` with
   whole-record membership) and the validator contract; freeze both.
3. **Establish L1** (§4) by proof or sound procedure.
4. **Identify the L2 method per claim** (§5) or mark unavailable — never assumed.
5. **Run L3** (§6) only if a later work order authorizes execution.
6. **Emit the §E.1 result record + evidence package**, with per-property
   verification records and the divergence-first summary.
7. **Assess marginal value** (§7) vs the Order 7 panel, in L1/L2/L3 terms.

## 4. L1 claims — object, method, status

| # | Claim | Object | Proposed method | Status |
|---|---|---|---|---|
| U1 | `prefers` is a strict total order on well-formed candidates | Abstract selector | Proof: trichotomy per component, lexicographic composition | Proposed |
| U2 | Unique maximal element for every non-empty well-formed set | Abstract selector | Proof: finite non-empty set under strict total order (U1) | Proposed |
| U3 | Membership: `∃c ∈ C : output == c` (whole record) | Abstract selector | Proof: the maximal element is a member of C | Proposed |
| U4 | Determinism: pure function of input | Abstract selector | Proof: no external state; follows from U1–U2 | Proposed |
| V1 | Validator accepts exactly the well-formed inputs | Abstract validator | Proof: finite case analysis over the App. 2 §A2.5 checklist | Proposed |
| V2 | Validator rejects every invalid input, naming the defect | Abstract validator | Proof: invalid class = complement of the checklist, enumerated in §6 | Proposed |

**R2 note:** the input class is unbounded; enumeration cannot establish U1–U4.
Structural arguments required; fuzzing never upgrades a claim to L1.

**Defect-02 rationale (why whole-record membership):** the v0.3 UCI-only
predicate admitted an implementation returning a genuine UCI with a fabricated
score (e.g. 100.0), which could then satisfy maximality. Whole-record equality
closes the hole: the output must *be* a supplied candidate, not merely share
its UCI.

## 5. L2 conformance — per-claim method or explicit unavailability

| Claim | Proposed L2 method | Availability |
|---|---|---|
| U1–U4 → selector implementation | Transcription audit (line-by-line correspondence to the proved comparator) + differential testing vs independent reference (bounded) | Proposed; checked refinement proof **unavailable in v0** — claim capped as bounded evidence, labelled |
| V1–V2 → validator implementation | Checklist review against App. 2 §A2.5 + malformed-input fuzzing (bounded) | Proposed; full conformance proof unavailable in v0 — capped and labelled |
| Code generation conformance | N/A — out of scope | Explicitly excluded |

## 6. L3 checks (bounded; execution requires separate authorization)

- **Regression:** 75 frozen Order 7 snapshots; expected 75/75 reproduction.
- **Differential:** independent reference implementation (no shared ranking code;
  preferably different author/language; own suite) over snapshots + fuzz corpus;
  disagreements → CHECKER_DIVERGENCE, investigate.
- **Property fuzzing:** sizes 0/1/2/many; exact score ties; ±1 ulp near-ties;
  signed zeros; malformed entries (missing fields, wrong types, duplicate UCIs
  **including identical duplicates**, NaN/±Inf scores, empty UCIs,
  non-ASCII UCIs, whitespace-containing UCIs); empty sets. Seeds recorded.
  **Oracle:** App. 2 comparator + whole-record membership
  (`∃c ∈ C : output == c`).
- **Membership-hole probe (new):** implementation returning a genuine UCI with
  an inflated score must yield VIOLATED with the `(input, output)` pair as
  witness — this case passes under the withdrawn v0.3 predicate and fails
  under v0.4, demonstrating the fix.
- **Malformed-input suite:** the Order 7 cases never executed — executed here,
  recorded individually. Not claimed passed until run.
- **Invalid-input class** (V2 bounded evidence): empty set; missing fields;
  wrong types; duplicate UCIs (incl. identical records); non-finite scores;
  empty/non-ASCII/whitespace UCIs.
- **Limits:** green fuzzing bounds claims to tested inputs; never universal proof.

## 7. Marginal value assessment (required in the acceptance report)

1. **L1:** universal properties proved (U1–U4, V1–V2) and methods — generalizing
   beyond the 75 positions.
2. **L2:** conformance evidence per §5; where capped at bounded evidence.
3. **L3:** coverage counts; regression result vs the 75-panel.
4. Experimentally unknown: chess strength — out of scope by design.

Honest "no defects beyond the panel; L1 proved; L2 bounded" is success. If
nothing beyond the panel is found, the report says so.

## 8. Worked examples

### 8.1 Tie-break (corrected comparator)

Candidates `{uci:"e2e4",rank:0,score:0.5}`, `{uci:"d2d4",rank:0,score:0.5}`:
scores equal, ranks equal, `"d2d4" < "e2e4"` bytewise → `prefers` clause 3
selects `d2d4`. Matches the preserved Order 7 adapter.

### 8.2 Projection-relative uniqueness

Models m₁ ([0.5,0.3,0.2]) and m₂ ([0.6,0.25,0.15]), both selecting "e2e4":
equivalent under the selection projection (exact UCI equality); distinct under
the probability-output projection (exact bitwise difference of canonicalized
sequences). Projection declared before evaluation; absent → INVALID_INPUT.

### 8.3 Membership-hole witness (defect 02)

Candidate supplied: `{uci:"e2e4", rank:0, score:0.5}`. Implementation returns
`{uci:"e2e4", rank:0, score:100.0}`. v0.3 predicate
(`output.uci == c.uci`) holds; v0.4 predicate (`output == c`) fails on
`score` → semantic_result=VIOLATED with the `(input, output)` witness. The
maximality clause would then also be evaluated against the fabricated score —
the witness exposes both.

## 9. Discrepancy protocol (result-record terms)

| Event | Record fields |
|---|---|
| Reference vs primary disagree | Two conflicting verification records → verification_summary=CHECKER_DIVERGENCE (divergence-first rule); discrepancy + follow-up; halt |
| Fuzz finds violation | semantic_result=Some(VIOLATED) + counterexample witness; new frozen version required for revision |
| Timeout | execution=TIMEOUT; partial_results labelled; semantic_result=Some(INCONCLUSIVE(RESOURCE_EXHAUSTED)) |
| Solver unknown | semantic_result=Some(INCONCLUSIVE(SOLVER_UNKNOWN)); uniqueness refused |
| UNSAT, Level A required, B only | solver_observation={UNSAT,…}; semantic_result=Some(INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET)); shortfall=true |
| Split properties | Records preserved; summary FAIL if any FAIL (no divergence); DIVERGENCE dominates per §E.6 |

## 10. Entry conditions (before any execution)

- [ ] Design spec v0.4 reviewed (freeze is a separate owner decision).
- [ ] Selector + validator contracts (App. 2 v0.4) written, reviewed, frozen.
- [ ] Independent reference implementation under separation requirements.
- [ ] Fuzz corpus design and seeds recorded.
- [ ] L2 methods per §5 confirmed or claims capped.
- [ ] Explicit authorization to execute.

*End of MSVE_ACCEPTANCE_PLAN_v0.4.md (draft for review).*
