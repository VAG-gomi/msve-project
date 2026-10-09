# MSVE Design Review v0.2

**Status:** SELF-REVIEW — NOT AN INDEPENDENT REVIEW, NOT EXECUTED VERIFICATION
**Version:** 0.2 · **Work order:** MUSE WORK ORDER 0.1
**Scope:** the five v0.2 drafts against the v0.1 baseline and the mandatory corrections A–G, R1–R5

This review was performed by the draft's own author. It does not count as
external review. Per §12 of the work order, it distinguishes corrections
completed, corrections partially completed, unresolved decisions,
freeze-blocking defects, non-blocking implementation decisions, and claims that
remain proposals.

v0.1 documents are retained unmodified as the historical baseline. All section
references below are of the form v0.1 §X → v0.2 §Y.

---

## 1. Change ledger — mandatory corrections

### Correction A — result-status architecture
- v0.1 §E (flat 11-status taxonomy) → v0.2 §E (result record with orthogonal
  fields: `admission` / `execution` / `semantic_result` / `verification` / `evidence`).
- The six required semantics → v0.2 §E.5 rules 1–6 (constructed≠verified; PROVED
  names proposition+assumptions; verification names property+method+artifact;
  timeouts preserve labelled partials; completion≠success; recording≠confirming).
- v0.1 §E.1 EXPERIMENTALLY_CONFIRMED → v0.2 §E.6 three-way split:
  EVIDENCE_RECORDED / RECORD_INTEGRITY assessment / EXTERNAL_ASSESSMENT.
- Visualisation Diagram 4 replaced (flat state machine → orthogonal-field schema
  + legal-combination table + forbidden conflations).
- **Completed.**

### Correction B — invalid vs underdetermined vs inconclusive
- v0.1 §B.5/B.6 → v0.2 §B.5: three admission situations separated
  (INVALID_INPUT / valid-multi-solution→UNDERDETERMINED / valid-undecidable→INCONCLUSIVE).
- NL rule hardened → v0.2 §B.6: unreviewed NL-extracted assumptions NEVER enter
  executable specs; the v0.1 UNREVIEWED-in-outputs allowance is removed.
- Four-way distinction (structurally incomplete / valid non-unique /
  unknown-within-procedure / outside support) → §B.5 + §E.4 reason codes.
- **Completed.**

### Correction C — solver uncertainty and trust boundary
- INCONCLUSIVE with reason codes (SOLVER_UNKNOWN / PROCEDURE_INCOMPLETE /
  RESOURCE_EXHAUSTED / EXECUTION_INTERRUPTED) → v0.2 §E.4.
- SAT/UNSAT asymmetry corrected → v0.2 §F.5: model rechecking rules; UNSAT
  assurance Levels A/B; unsat core labelled diagnostic-only; refusal rule when
  Level A is required but unavailable.
- SymPy description → v0.2 §F.4: computed / independently checkable /
  trusted-tool output. The v0.1 "correctness within its algorithms" phrasing is gone.
- **Completed** as framework; certificate *availability* for Level A is an
  implementation-time determination → **partially completed** (see §3).

### Correction D — proof vs implementation assurance
- L1/L2/L3 separation → v0.2 §D.1 and acceptance plan §2; acceptance criteria
  restructured (§3.1 L1, §3.2 L2, §3.3–3.4 L3).
- G1 narrowed → v0.2 §D.6 + matrix G1 (RESTRICTED, template-based generator
  class; general generation FUTURE).
- Marginal value in L1/L2/L3 terms → acceptance §6.
- **Completed.**

### Correction E — selector contract
- Existential membership (v0.1 §B.4 universal-quantifier error) → v0.2 §B.7 and
  Appendix 2 §A2.3.
- Complete ranking order → Appendix 2 §A2.4 (score desc, rank asc, lexical UCI
  asc; total order via distinct UCIs).
- Numeric semantics → Appendix 2 §A2.1/A2.2/A2.5: binary64 canonicalized,
  −0.0→+0.0, NaN/±Inf rejected at admission, exact bitwise equality, no
  tolerance, no calibration claim (§A2.6).
- Mismatch report → Appendix 2 §A2.8: no mismatch on observed Order 7 behaviour;
  edge-case rules flagged as new proposals, not historical facts.
- **Completed.**

### Correction F — projection and uniqueness
- Tolerance-based distinctness (v0.1 §D.2) → exact canonical equality,
  v0.2 §D.3 (transitive by construction).
- Second-model query construction ("π(m₂) ≠ π(m₁)" as disjunction of exact
  inequalities) → v0.2 §D.4.
- Auto-discovery of uniqueness-restoring assumptions removed → v0.2 §D.5
  (user-supplied or declared-finite-family candidates only; sufficient ≠ justified).
- **Completed.**

### Correction G — provenance and maturity
- Separated claims (identity / integrity-vs-reference / authenticity /
  correctness) → v0.2 §G.1; canonical JSON rules §G.2; "tamper-proof" eliminated
  in favour of "tamper-evident relative to a trusted reference".
- Maturity field → v0.2 §G.4 and matrix two-column layout; every v0.2 entry at
  DESIGN_ONLY.
- **Completed.**

### Review corrections R1–R5
- **R1** (status-model omission): resolved structurally via Correction A — the
  diagram was replaced, not patched. → Completed.
- **R2** (exhaustive argument): acceptance §3.1 R2 note — enumeration cannot
  cover unbounded input classes; structural argument required. → Completed.
- **R3** (missing projection): spec §B.5 + grammar — INVALID_INPUT, never
  guessed. → Completed.
- **R4** (grammar/examples): §B.2 revised grammar; §B.3 assume/require/forbid
  roles; §B.4 resource-limit rules; proof/test requirements separated;
  §B.7 example aligned with the grammar. → Completed.
- **R5** (worked example): acceptance §4 — two models, selection vs
  probability-output projections, exact comparison rules recorded. → Completed.

## 2. Corrections partially completed

1. **UNSAT Level A certificate availability** (Correction C): the assurance
   levels and refusal rule are fully specified (§F.5), but whether the v0 solver
   stack actually emits independently checkable certificates is undetermined
   until implementation. If unavailable, v0 CONTRADICTION claims are Level B by
   default and the refusal rule governs.
2. **L2 conformance method selection**: options are named (checked refinement,
   translation validation, static analysis) and the acceptance plan requires
   naming one per claim (§3.2), but no method is selected for the selector case
   yet — correctly, since selection belongs to implementation authorization.

## 3. Unresolved decisions (carried, not hidden)

1. Exact Lean version and proof-carrying interface format (carried from v0.1).
2. Full v0 problem-class catalog beyond the matrix (carried; matrix authoritative).
3. Per-class timeout/memory defaults (carried; set at implementation authorization).
4. Widening the v0 generator class beyond the initial template class (new in v0.2).
5. Key management / operational details for signed release tags (mechanism
   defined; operations deferred).

## 4. Freeze-blocking defects

The following must be resolved before the design can be frozen. This list is
complete to the author's knowledge; it is not a claim that nothing else will
emerge under external review.

1. **The grammar is still a fragment.** v0.2 §B.2 is revised but not complete;
   a freeze requires the full grammar with complete type rules and the full
   invalid-input catalog.
2. **UNSAT Level A availability** (§2.1 above) must be determined — it decides
   whether v0 CONTRADICTION claims can meet Level A or are Level B by scope.
3. **L2 conformance method** for the selector acceptance case must be selected
   and recorded before the acceptance plan can be frozen (selection is an
   owner decision at or before implementation authorization).

## 5. Non-blocking implementation decisions

Lean version; timeout/memory defaults; fuzzer seed registry vs per-run
recording; canonical-JSON number format choice (exact decimal vs hexfloat —
fixed per release); signed-tag key management; widening the generator class.

## 6. Claims that remain proposals

Everything. The engine is unimplemented; every matrix entry is at maturity
DESIGN_ONLY. Specifically proposals, not established capabilities: the
orthogonal status architecture, the three-level assurance model, the selector
contract edge-case rules (Appendix 2 §A2.8), the refusal rule's operational
behaviour, and all "SUPPORTED" target dispositions.

## 7. Counterexample challenges (design challenges, not executed tests)

| # | Challenge | Design answer | Section |
|---|---|---|---|
| 1 | Inconsistent spec (`require P`, `require ¬P`) | admission ACCEPTED; execution COMPLETED; semantic_result CONTRADICTION (Level B unless certificate); assurance labelled | §E.3, §F.5 |
| 2 | Two models, same UCI, different scores | Equivalent under selection projection; UNDERDETERMINED with witnesses under probability-output projection | §D.3, acceptance §4 |
| 3 | `compare-models` without projection | INVALID_INPUT at admission; never guessed | §B.5 (R3) |
| 4 | Float edges: −0.0 vs +0.0; NaN; ±1 ulp near-tie | −0.0 normalized → equal; NaN → INVALID_INPUT; near-ties distinct by exact comparison, deterministic | App. 2 §A2.5 |
| 5 | Solver returns `unknown` on second-model query | INCONCLUSIVE(SOLVER_UNKNOWN); uniqueness refused | §E.4, §D.2 |
| 6 | Timeout after first model re-checked | execution TIMEOUT; established model kept, labelled partial; semantic INCONCLUSIVE(RESOURCE_EXHAUSTED) | §E.5 rule 4 |
| 7 | UNSAT without checkable certificate, Level A required | Shortfall reported; stronger claim refused; Level B recorded | §F.5 |
| 8 | Reference vs primary disagree | verification CHECKER_DIVERGENCE; halt; investigate; adjudicate | Acceptance §5 |
| 9 | L1 proved but no L2 method available | Acceptance capped at L3 for that property; gap recorded explicitly | §D.1, acceptance §3.2 |

## 8. Guarantee → method audit (v0.2)

| Guarantee | Method | Present? |
|---|---|---|
| No silent gap-filling | Parser rejects under-specified inputs; NL assumptions never executable | Yes (§B.5, §B.6) |
| UNDERDETERMINED is evidence-backed | Witness requirement; exact projection equality; well-defined negation query | Yes (§D.2–D.4) |
| Timeout/unknown never misreported | Separate execution/semantic fields; INCONCLUSIVE reason codes; anti-conflation rules | Yes (§E.2, §E.4, §E.7) |
| Unsat not overstated | Level A/B assurance; diagnostic-only unsat cores; refusal rule | Yes (§F.5) |
| Independent checking | Differential testing + fuzzing with separation requirements; CHECKER_DIVERGENCE | Yes (acceptance §3.3, §5) |
| Provenance claims bounded | Four separated claims; canonicalization; no "tamper-proof" | Yes (§G.1–G.2) |
| Capability claims honest | Target disposition + maturity field; all DESIGN_ONLY | Yes (§G.4, matrix) |
| Judgment explicit | Assumption sets (human-reviewed only); three-judgment separation; sufficient≠justified | Yes (§A.4, §B.3, §D.5) |

## 9. Consistency verification (work-order §13 checklist)

1. Status dimensions consistent across definitions (§E.2), tables (§E.3),
   examples (acceptance §5), diagrams (vis. Diagram 4 + table), glossary
   (Appendix 1). **Pass.**
2. All requested corrections addressed explicitly. **Pass** (§1 above).
3. Grammar matches examples and error rules (§B.2/B.7/B.8). **Pass.**
4. Every promised guarantee has a proposed verification method. **Pass** (§8).
5. SAT/UNSAT assurance matches trust policies (§F.5). **Pass.**
6. Uniqueness uses well-defined projection + exact comparison (§D.3/D.4). **Pass.**
7. Mathematical model and implementation assurance separated (L1/L2/L3). **Pass.**
8. Disposition and maturity cannot be confused (two columns; all DESIGN_ONLY). **Pass.**
9. Provenance claims do not exceed mechanisms (§G.1; no "tamper-proof"). **Pass.**
10. No part authorizes implementation, repository creation, or a GrimChess
    experiment (headers on all five documents; restrictions observed). **Pass.**

## 10. Review verdict

**v0.2 addresses every mandatory correction structurally — not cosmetically.**
The flat status taxonomy, the tolerance-based distinctness, the overstated G1,
the unqualified EXPERIMENTALLY_CONFIRMED, and the blurred provenance claims are
all replaced, not patched. Three defects block freezing (§4), all identified
above rather than hidden. No implementation, repository, or experiment is
authorized by this package.

*End of MSVE_DESIGN_REVIEW_v0.2.md (self-review).*
