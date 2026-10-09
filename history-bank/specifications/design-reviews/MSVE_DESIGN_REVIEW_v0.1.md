# MSVE Design Review v0.1

**Status:** SELF-REVIEW — NOT AN INDEPENDENT REVIEW, NOT EXECUTED VERIFICATION
**Version:** 0.1 · **Scope:** the four draft documents produced under Work Order 0

Per the drafting protocol: this review was performed by the draft's own author.
It does not count as external review. External review and executed verification
must be labelled separately when they occur.

Documents reviewed:
1. `MSVE_DESIGN_SPEC_v0.1.md` (spec)
2. `MSVE_CAPABILITY_MATRIX_v0.1.md` (matrix)
3. `MSVE_ACCEPTANCE_PLAN_v0.1.md` (acceptance)
4. `MSVE_VISUALISATION_PLAN_v0.1.md` (visualisation)

---

## 1. Strongest design decisions

1. **Evidence-backed refusal.** UNDERDETERMINED requires witnesses (two
   projection-distinct models), not a slogan. The model-negation re-solve
   procedure (§D.1) makes "refuse to invent" operational.
2. **The three judgments as organizing principle** (§A.4). This is what prevents
   the "engine without heuristics" misreading from becoming a design flaw.
3. **Trust base as orchestration with per-component guarantee tables** (§F.2).
   Each component's "outside its guarantee" column is the honest boundary.
4. **Genesis-commit rule** (§H.3): the repository, if authorized, begins with the
   frozen spec — no placeholder-then-rewrite history.
5. **Baseline correction carried as a test obligation.** The acceptance plan does
   not claim the malformed-input tests passed; it requires executing them (§1, §3.3).
6. **Anti-conflation hard rules** (§E.2): timeout/unknown never reported as
   inconsistency or underdetermination; finite suites never presented as universal proof.

## 2. Counterexample challenges (applied to the draft)

| # | Challenge | Draft's answer | Verdict |
|---|---|---|---|
| 1 | `require P` + `require not P` | CONTRADICTION with unsat core (§D.1, M3) | Holds |
| 2 | Two models, same selected UCI, different probabilities, under selection projection | Equivalent, not UNDERDETERMINED (§D.2) | Holds — but see correction R3 |
| 3 | Timeout during second-model search after first model found | TIMEOUT or bounded statement; never "unique"/"underdetermined" (§D.1 step 5) | Holds |
| 4 | Reference implementation disagrees with primary | Halt; record; investigate; adjudicate (acceptance §4) | Holds |
| 5 | Proof requested over nonlinear arithmetic with kernel-checked policy | UNSUPPORTED (P2/M4 restricted) | Holds |
| 6 | Proof accepted but formalization misstates intent | Recorded as human-reviewed assumption (P2); kernel guarantees only relative acceptance (§F.2) | Holds, residual risk noted (§4) |
| 7 | "Independent" checker shares the author's misreading of the contract | Separation requirements + frozen contract as third leg (acceptance §3.2) | Mitigated, not eliminated (§4) |
| 8 | Provenance recorder itself buggy | Independent reproduction re-derives (§3.5); prior packages superseded not deleted (§G) | Mitigated (§4) |

## 3. Recommended corrections (to apply before freeze)

- **R1.** Visualisation Diagram 4 (status state machine) omits
  EXPERIMENTALLY_CONFIRMED. It is a *recording* status, not a run-terminal
  status — either add it with that annotation or add an explicit note. Current
  diagram is inconsistent with §E.1 by omission.
- **R2.** Acceptance §3.1: "exhaustive argument over the input class" must be
  clarified — for unbounded-but-finite candidate sets this means a *structural*
  argument (e.g., induction over the selection procedure), not enumeration.
- **R3.** Spec §D.2: state the consequence explicitly — a uniqueness-seeking goal
  with no declared projection is INVALID_INPUT, not attempted under a guessed
  projection.
- **R4.** Spec §B.4 example vs §B.2 grammar: the example embeds the checker ID
  inside `differential-tested(...)` while the grammar separates ProofPolicy and
  CheckerPolicy. Align the example with the grammar.
- **R5.** Add a worked mini-example of the §D procedure on the selector tie case
  (two models, same UCI, different probabilities → equivalent under selection
  projection, distinct under probability-output projection) to the acceptance
  plan. The spec states the rule; the plan should show it being applied.

## 4. Residual risks (acknowledged, not solvable at design level)

1. **Formalization adequacy** (challenge 6): no mechanism inside MSVE detects that
   a formal spec misstates the researcher's intent. Mitigation is human review at
   the freeze gate. This is honest; it is also the load-bearing human step.
2. **Checker independence limits** (challenge 7): two implementations can share a
   misreading. The frozen contract + differential testing reduce but do not
   eliminate this.
3. **Timeout tuning:** per-class resource defaults are deferred to implementation
   authorization (spec Appendix 2.4). Too-tight limits produce uninformative
   TIMEOUTs; too-loose limits waste resources. Needs owner judgment at that stage.

## 5. Missing decisions — blocking vs non-blocking for design freeze

| Decision | Blocks freeze? |
|---|---|
| R1–R5 corrections above | Should be applied before freeze, but none is structural |
| Lean version + proof-carrying interface format (spec App. 2.1) | No — deferred to implementation authorization by design |
| Full v0 problem-class catalog beyond the matrix | No — the matrix is authoritative; extensions get their own review |
| Fuzzer seed registry vs per-run recording | No — per-run recording specified; registry optional |
| Per-class timeout/memory defaults | No — set at implementation authorization |

**No blocking issues found.** The draft is freezable after R1–R5 and owner review.

## 6. Cross-document consistency check

- Statuses: spec §E (11) ↔ matrix §5 (E1/E2) — consistent. ↔ Diagram 4 (10 shown):
  **inconsistency by omission** → R1.
- Refusal procedure: spec §D ↔ matrix M5/M6/M7 — consistent.
- Release gates: spec §J ↔ matrix §7 — consistent (6 gates, same criteria).
- Governance: spec §H ↔ acceptance §6 entry conditions — consistent.
- NL handling: spec §B.6 hard rule ↔ matrix G3 FORBIDDEN — consistent.
- Grammar vs example: **minor misalignment** → R4.
- "All-rounder" definition: spec §A.5 ↔ matrix §7 — consistent; scope+version
  qualifier required in both.

No silent reconciliations were performed; the two discrepancies found are listed
as R1 and R4 above.

## 7. Guarantee → method audit

Every promised guarantee was checked for a corresponding method:

| Guarantee | Method | Present? |
|---|---|---|
| No silent gap-filling | Parser rejects under-specified inputs (§B.5) | Yes |
| UNDERDETERMINED is evidence-backed | Witness requirement (§D.1) | Yes |
| Timeout never misreported | Separate statuses + anti-conflation rules (§E.2) | Yes (design level; implementation must enforce separate code paths) |
| Independent checking | Differential testing + fuzzing with separation requirements (acceptance §3.2–3.3) | Yes |
| Tamper-evident provenance | Hashing/versioning (§G) + independent reproduction (acceptance §3.5) | Yes |
| Judgment made explicit | Assumption sets, UNREVIEWED tracking, three-judgment separation | Yes |
| Capability claims evidenced | Staged gates (§J) + normative matrix | Yes |

## 8. Review verdict

**The draft is coherent and freezable after corrections R1–R5 and owner review.**
No structural redesign needed. The central risk is not in the draft's logic but
in its most honest admission: formalization adequacy rests on human review
(§4.1), and the draft is only as good as the freeze gate that follows it.

*End of MSVE_DESIGN_REVIEW_v0.1.md (self-review).*
