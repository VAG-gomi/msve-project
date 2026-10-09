# MSVE Design Review v0.3

**Status:** SELF-REVIEW — NOT AN INDEPENDENT REVIEW, NOT EXECUTED VERIFICATION
**Version:** 0.3 · **Work order:** MUSE WORK ORDER 0.2
**Scope:** the five v0.3 drafts against the v0.2 baseline and corrections A–H

This review was performed by the draft's own author. Per the standing lesson
(AGENTS.md), every PASS below was earned by attempting refutation first — the
v0.2 failure mode (marking grammar–example alignment PASS while the grammar was
fragmentary) must not recur. One defect was found during this review and fixed
in the spec before delivery (§6, check 2).

---

## 1. Correction ledger (v0.2 → v0.3)

| Correction | v0.2 source | v0.3 resolution | Status |
|---|---|---|---|
| A. Selector order | App. 2 §A2.4 key tuple (mathematically reversed) | Explicit `prefers` comparator, App. 2 §A2.2; uniqueness argument §A2.3; corrected historical comparison §A2.8 | Resolved |
| B. Complete language | §B fragment; undefined nonterminals; unreferenceable assumptions | §B rewritten: full EBNF (§B.3), lexical rules (§B.2), type system (§B.4/B.4a), name resolution (§B.5), named assumptions (§B.6), verification syntax (§B.7), resource rules (§B.8), error catalog (§B.9), 5 valid + 8 invalid examples (§B.11/B.12) | Resolved |
| C. UNSAT semantics | §F.5 self-contradiction (refuse + report CONTRADICTION) | Solver observation vs semantic result vs assurance (§E.5); refusal rule; v0 Level A policy — SMT UNSAT Level A is FUTURE (§E.6) | Resolved |
| D. Validator separation | Acceptance §3.1 invalid-input as L1 | Two objects (§2 of acceptance plan); App. 2 §A2.5 validator contract; U1–U4 vs V1–V2 claims; separate L2 rows | Resolved |
| E. Generator domain | §D.6 "finite enumerable domains" excluded the selector | §D.5: structural-recursion template class; three finiteness notions distinguished; generation out of scope for first slice | Resolved |
| F. Result schema | §E.2 five fields; `assurance` referenced but undefined | Complete typed schema §E.2 (solver_observation, assurance triple, per-property records, partials, discrepancies); aggregation rule §E.7; 9 legal combinations §E.8 | Resolved |
| G. Canonicalisation | §G.2 hexfloat/JSON ambiguity | `msve-canonical-1` profile §G.2: no bare JSON numbers; typed int/rat/f64 objects; deterministic hexfloat format; versioned; transition policy §G.5 | Resolved |
| H. Maturity vocabulary | §J vs matrix mismatch | Unified 7-stage ladder §G.4, used identically in §J, matrix §7, acceptance plan, review, diagrams | Resolved |
| R1–R5 (v0.1 carryovers) | — | Carried through v0.2; R5 worked example retained and extended (acceptance §8) | Resolved |

## 2. Corrections partially resolved

1. **UNSAT Level A availability.** The policy is fully specified (§E.6) and the
   refusal rule is coherent, but whether any v0 solver stack emits independently
   checkable certificates remains an implementation-time determination. v0
   therefore treats SMT-UNSAT Level A as FUTURE — an honest bound, not a gap.
2. **L2 method selection.** Options are narrowed per claim (acceptance §5) but
   the final method choice belongs to implementation authorization; affected
   claims are explicitly capped as bounded evidence meanwhile.

## 3. Unresolved decisions (carried)

Lean version + proof-carrying interface; full problem-class catalog beyond the
matrix; per-class timeout/memory defaults; widening the generator class;
signed-tag key management (bounded implementation decision).

## 4. Freeze-blocking defects

**None found in this review.** The three v0.2 blockers are resolved:
(1) the grammar is now complete, not a fragment; (2) UNSAT Level A availability
is decided as a policy (FUTURE for SMT UNSAT, with the refusal rule operative);
(3) L2 methods are identified per claim with explicit capping where unavailable.
This is a self-review finding, not an independent verdict — external review may
still find blockers.

## 5. Non-blocking implementation decisions

Checker registry mechanics; fuzz harness implementation; exact Lean version;
timeout/memory defaults per class; canonical-profile operational rollout;
signed-tag key management.

## 6. Claims that remain proposals (no implementation evidence)

Everything normative in the package: the language (§B), the status schema
(§E.2), the comparator contract (App. 2), the generator class (§D.5), the
canonical profile (§G.2), and all SUPPORTED target dispositions (maturity:
Designed). The Order 7 baseline remains EVIDENCE_RECORDED, not an MSVE result.

## 7. Claims supported only by finite or external observations

The 75/75 Order 7 panel; the 11 tie cases (support the comparator's tie clause
as observed behaviour, not as proof); any future fuzz corpus (bounded L3).

---

## 8. Adversarial review (§14) — expected result-record fields per case

1. **Equal scores, equal ranks, UCIs "e2e4" vs "d2d4".**
   admission=ACCEPTED; execution=COMPLETED; semantic_result=DERIVED_VALUE
   ("d2d4"); verification per policy. Claim permitted: the comparator selects
   the smaller UCI. Claim refused: nothing about historical intent beyond the
   recorded match (App. 2 §A2.8).
2. **Two models, same selected UCI, different probability vectors.**
   Under selection projection: equivalent (exact UCI equality) — uniqueness
   question proceeds on the full query, not the pair. Under probability-output
   projection: distinct → if both satisfy constraints,
   semantic_result=UNDERDETERMINED with witnesses (m₁, m₂) and differing
   sequences recorded.
3. **Syntactically invalid but meaningful selector example** (e.g., missing
   `limits`). admission=INVALID_INPUT(missing-mandatory-timeout);
   execution=NOT_STARTED; verification_summary=NOT_RUN. No semantic result.
4. **Referenced assumption never declared** (`assuming [ghost]`).
   admission=INVALID_INPUT(unbound-assumption-reference: ghost). The proof is
   not attempted.
5. **Solver UNSAT, Level A mandatory, only Level B available.**
   solver_observation={UNSAT, tool, version, config, provenance};
   semantic_result=INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET);
   assurance_required=LEVEL_A; assurance_achieved=LEVEL_B_SOLVER_BACKED;
   assurance_shortfall=true. The contradiction is refused, not lowered.
6. **Abstract selector proved; no validator proof.**
   Selector claims at L1 per §4 (U1–U4); validator claims V1–V2 remain
   unestablished — the acceptance record must show them as missing, and any
   "rejects all invalid inputs" claim is capped at bounded L3 evidence or
   marked unavailable. No L1 selector proof leaks into validator assurance.
7. **Unbounded class of finite candidate lists under the generator scope.**
   Admitted to the v0 generator class *only* via the structural-recursion
   template (§D.5) with the comparator's total-order obligations discharged at
   L1. Finite enumeration of the class is never claimed; termination is by
   structural recursion. If the template's obligations are undischarged,
   generation is refused for that spec.
8. **Timeout after a first satisfying witness.**
   execution=TIMEOUT; partial_results=[witness m₁, re-checked, labelled
   partial]; semantic_result=INCONCLUSIVE(RESOURCE_EXHAUSTED). The witness is
   preserved; no uniqueness or unsatisfiability conclusion is drawn.
9. **One property PASS, another FAIL, same package.**
   verification_records preserved individually; verification_summary=FAIL
   (rule §E.7). The PASS is not hidden; the package is not green.
10. **Checker A PASS, checker B FAIL, same property.**
    verification_summary=CHECKER_DIVERGENCE; discrepancy recorded with required
    follow-up (investigate, adjudicate); acceptance halts for that property.
11. **Canonicalisation change altering a previous hash.**
    New profile version (`msve-canonical-2`); both hashes recorded during
    transition; old hashes never reinterpreted under new rules (§G.5). A
    package verified under -1 is not claimed verified under -2 without re-hashing.
12. **Capability "integrated" but never independently reproduced.**
    Maturity recorded as "Integrated and reproducible" (stage 5), NOT stage 6.
    Any claim of independent reproduction without the evidence is a maturity
    mislabel — the matrix forbids it.

## 9. Cross-document consistency gate (§15)

Method: each check was attempted against the supplied text with refutation in
mind. PASS = the document-level relationship was verified in the text (not an
executed test).

| # | Check | Result | Reason |
|---|---|---|---|
| 1 | Selector order identical across grammar example, contract, oracle, reference spec, worked examples | PASS | `prefers` three clauses identical in §B.11, App. 2 §A2.2, acceptance §6 oracle, §8.1 |
| 2 | Grammar accepts every valid example, rejects every invalid example | PASS* | *One defect found and fixed during review: `under` was syntactically mandatory while §B.14 promised semantic `missing-required-projection`; grammar now makes it optional with the admission rule in §B.5. All 5 valid examples parse; all 8 invalid examples rejected with stated reasons (verified by hand-derivation) |
| 3 | Assumption references resolve per defined syntax/scope | PASS | `assuming [add_zero]` → axiom; `assuming [ghost]` → unbound-assumption-reference; §B.5/B.6 rules |
| 4 | UNSAT observation / conclusion / shortfall follow one rule | PASS | §E.5 rule ≡ acceptance §9 row ≡ vis. Diagram 5 branches |
| 5 | Validator not confused with abstract selector | PASS | Separate objects, contracts, L1 claims (U vs V), L2 rows |
| 6 | Generator scope covers claimed operations | PASS | G1 claims only the structural-recursion template class; slice excludes generation explicitly |
| 7 | All referenced result-record fields defined in one schema | PASS | §E.2 defines every field used in §E.8, acceptance §9, vis. Diagram 4 |
| 8 | Per-property outcomes preserved; aggregation cannot conceal | PASS | §E.7 ordered rule; acceptance §9 split-property row |
| 9 | Canonicalisation deterministic, type-safe, versioned | PASS | §G.2 profile; no bare numbers; typed objects; §G.5 transitions |
| 10 | Maturity ladder ≡ release gates terminology | PASS | Identical 7 names in §G.4, §J, matrix §7, diagrams |
| 11 | Capabilities at genuinely supported maturity | PASS | All matrix entries: Designed |
| 12 | No document authorises repo/implementation/experiments | PASS | Headers + acceptance entry conditions + work-order restrictions |

**Gate verdict: 12/12 PASS** (check 2 after the in-review fix, recorded above —
not concealed). The gate is a document-level check, not an executed test.

## 10. Review verdict

v0.3 resolves every mandatory correction A–H structurally. The package is
internally consistent to the limits of self-review: one defect was found by the
review process itself and repaired (§9, check 2), which is the process working as
designed. No freeze-blocking defects were found **by this self-review** — that
determination, and the design itself, now require the project owner's review and
the external adversarial reading that self-review cannot supply.

*End of MSVE_DESIGN_REVIEW_v0.3.md (self-review).*
