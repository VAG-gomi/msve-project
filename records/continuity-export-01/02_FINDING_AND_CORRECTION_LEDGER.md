# MSVE Continuity Package — 02 FINDING AND CORRECTION LEDGER

**Columns:** Finding ID | First discovered in | Exact defect | Supporting evidence | Affected clause | Affected constraint | Correction candidate | Regression coverage | Reviewer disposition | Current status | Remaining limitation

---

**F-20** | 0.8.4 | Invariant 10 omitted `canonicalization-failure` from packaging-error test | Z3 F20-X SAT under current, UNSAT under corrected | Inv 10 | `is_packaging_error` | 0.8.6 | R1–R3 (0.8.6, 0.8.7, 0.8.8) | Adjudicated YES | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | —

**F-21** | 0.8.5.2 (owner) | Spec never required basis→evidence linkage; LEVEL_A + KERNEL_PROOF with no artifact admitted | 6 solver tests all SAT | Inv 6, §E.6a (missing) | Inv 24–28 (missing) | 0.8.6 (§E.6a, inv 24–28) | 13/13 (0.8.6) | Confirmed genuine | CORRECTED IN CANDIDATE, TESTED | —

**F-22** | 0.8.7 (owner) | Assurance checks applied too narrowly (Level A only) | Owner review of transfer | Inv 24–28 (0.8.6) | Model scope | 0.8.7 (any-level substantiation) | 18/18 | Conceded | CORRECTED IN CANDIDATE, TESTED | —

**F-23** | 0.8.7 (owner) | Evidence could be correctly classified but unrelated to exact claim | Owner review | §E.6a claim-key | `claim_key()` | 0.8.7 (property match) → 0.8.8 (claim_id) | S4/S5/S7 (0.8.7); C1 (0.8.8) | Conceded | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | —

**F-24** | 0.8.7 (owner) | Model omitted checker/hash/membership requirements | Owner review | Inv 25 | Model inv 25 | 0.8.7 (`is_sha256_hex`, `resolves_in`, checker) | S9/S10/S11 | Conceded | CORRECTED IN CANDIDATE, TESTED | —

**F-25** | 0.8.7 (owner) | Missing unrelated-evidence countermodels | Owner review | — | — | 0.8.7 (S4/S5/S7) | S4/S5/S7 | Conceded | CORRECTED IN CANDIDATE, TESTED | —

**F-26** | 0.8.7 (owner) | Ambiguous `Some(x)` binder notation | Owner review | Inv 24, 26 | — | 0.8.7 (explicit binders) | — | Conceded | CORRECTED IN CANDIDATE | —

**F-27** | 0.8.7 (owner) | Transfer manifest overstated source/transfer identity | Owner review | Manifest | — | 0.8.7.2 (forensic reconciliation) | — | Conceded | SUPERSEDED by 0.8.7.2 audit | Historical record preserved

**R1-1** | 0.8.7 (R1 normative) | `claim_key` undefined for HOLDS, NO_SOLUTION, CONTRADICTION, UNIQUE_UNDER_PROJECTION | Spec §E.6a text | `claim_key()` sentinel | 0.8.8 (ClaimDescriptor, Option A) | C3 (0.8.8); O1 (0.8.8.1) | Blocking | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | 7 kinds' outcome interpretation unresolved (N-0.8.8.1-1)

**N-1 / F2** | 0.8.8 (normative/model) | `outcome_compatible` used in inv 27 but never defined | Spec line 1487 (0.8.8) | Inv 27 | `_solver_linked` | 0.8.8 (formal definition) | O1/O2/O3 (0.8.8.1) | Blocking | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | —

**N-2** | 0.8.8 (normative) | `d.claim_id` field-access but no `claim_id` field on ClaimDescriptor | Spec 1166-1174 | Inv 25/26/28 | 0.8.8 (stored field added) | — | Blocking | CORRECTED IN CANDIDATE, INDEPENDENTLY REVIEWED | Well-formedness comment-only (N-0.8.8.1-4)

**N-3** | 0.8.8 (normative) | `claim_id = None` + basis satisfies inv 25–28 vacuously | Spec 1321 prose vs 1462-1497 | Inv 25–28 antecedents | 0.8.8 (invariant 29) | C5 | Blocking | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | —

**F1** | 0.8.8 (model) | Model inv 27 omits inputs_ref and outcome_compatible | Spec inv 27 | `_solver_linked` | 0.8.8 (inputs_ref); 0.8.8.1 (outcome) | S6/S8/S9; O1/O2/O3 | Blocking | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | —

**N-0.8.8.1-1** | 0.8.8.1 (normative) | 7 kinds fall into "Otherwise: False", tension with inv 22/23 | Spec 1355-1364 | `_outcome_compatible` | 0.8.8.1 (explicit unresolved marking) | — | Blocking | CORRECTED (marked unresolved), INDEPENDENTLY REVIEWED | OWNER DECISION REQUIRED to extend table

**N-0.8.8.1-2** | 0.8.8.1 (normative) | `vr.spec_version` never constrained by inv 25–28 | Spec inv 25-28 | Model (enforced without anchor) | 0.8.8.1 (vr.spec_version conjuncts) | V5 | Blocking | CORRECTED IN CANDIDATE, TESTED, INDEPENDENTLY REVIEWED | —

**N-0.8.8.1-3** | 0.8.8.1 (normative) | Model enforced R['spec_version']/R['claim_kind'] with no normative anchor | Spec ResultRecord | Model lines 143-144 | 0.8.8.1 (fields added to ResultRecord) | — | Blocking | CORRECTED IN CANDIDATE, INDEPENDENTLY REVIEWED | —

**M1** | 0.8.8.1 (model) | `_outcome_compatible` omits sr-variant check for holds | Spec 1357-1359 | Model 365-387 | 0.8.8.1 (sr check added) | O1 | Blocking | CORRECTED, TESTED, RE-INSPECTED on final hash | —

**M2** | 0.8.8.1 (model) | `assumptions` not represented in descriptor slots | Spec 1168 | Model 146-156 | — | — | Non-blocking | ATTESTED / NOT MECHANICALLY VERIFIABLE | —

---

**Status key:**
- CORRECTED IN CANDIDATE: normative/model change applied in the stated candidate.
- TESTED: a regression case exercises the specific defect (named test).
- INDEPENDENTLY REVIEWED: reviewer confirmed the correction against final hashes.
- OWNER DECISION REQUIRED: needs owner ruling, not a technical fix.
- SUPERSEDED: replaced by a later finding or correction.
- HISTORICAL / NOT RETROACTIVELY VERIFIABLE: e.g., the unpreserved 2,998-value sweep (F-19); the 0.8.7 18/18 log predating the R1-4 fix.

**F-01–F-19:** Corrected in 0.8.3 per the correction report; 7 were specification-review-only (no executed verification); F-19 provenance gap unfillable. [HISTORICAL]
