# MSVE Continuity Package — 01 COMPLETE WORK ORDER TIMELINE

## v0.8 initial design (2026-10-09, morning)

**Objective:** Produce MSVE design specification v0.8 with six documents (spec, acceptance plan, capability matrix, design review, regression ledger, visualisation plan) plus the M8 audit tool.

**Authorization:** User work orders 0 through 0.7 (document revision only; no freeze, implementation, or experiments).

**Key defect discovered:** The M8 tool (a real parser/type-checker for normative examples) exposed a **specification-versus-validator defect**: the spec's normative examples used syntax the grammar couldn't parse. This led to the standing methodological lesson: "hand-derivation claims require mechanical per-token checking" (recorded in `~/AGENTS.md`).

**Outcome:** v0.8 draft produced; ChatGPT adversarial review found blockers B-01–B-05 and D-025–D-033. Gate BLOCKED. v0.7 retained as historical draft.

## Work Order 0.8.1 — Owner-review evidence bundle

**Objective:** Package 101 artefacts with SHA-256 for owner review.

**Findings:** 12-claim evidence matrix (10 SUPPORTED, 1 PARTIALLY_SUPPORTED — later corrected to 11+1 per owner audit). One gap: Reviewer B's collision-sweep script not preserved.

**Owner audit findings (conceded):** CLM-12 arithmetic wrong; CLM-09 overstated; D-017 ambiguous; ZIP file-count breakdown missing; D-007/D-011/D-012 ledger gaps; reviewer reports lacked spec hashes.

## Work Order 0.8.3 — F-01–F-19 corrections

**Objective:** Targeted correction for 19 owner findings.

**Changes:** 106 artefacts; base_code operator consistency (F-01); assurance field paths (F-02); Binary64 intervals (F-03); is_nan builtin (F-04); error-domain boundary invariant 1b (F-06); matrix totals 11+1 (F-17); CLM-09 split (F-18).

**Limitation:** 7 findings were specification-review-only (no executed verification). The 2,998-value sweep was not preserved (F-19 provenance gap unfillable).

## Work Order 0.8.4 — Invariant satisfiability audit

**Objective:** Formalize all 23 §E.7 invariants in Z3; check satisfiability.

**Result:** 45/46 checks as expected (31 SAT valid, 13 UNSAT invalid, 1 `unknown` on joint query — honestly reported as UNKNOWN, not converted). Two reviewers independently formalized and converged.

**Key reconciliation:** The 15b ⟸-direction was resolved as restricted-existential. Invariants 3/12 unformalizable (external refs); 20/21/23 weakened (evidence aboutness has no schema discriminator).

**New finding F-20:** Invariant 10's packaging test omitted `canonicalization-failure`.

## Work Order 0.8.5 — Reconciliation

**Objective:** Reconcile the 46 checks from the raw solver log.

**Correction:** The 0.8.4 report hand-counted 13 expected-UNSAT; the log showed 14 (X12 dropped). 45/46 behaved as expected.

**F-20 adjudicated YES:** `canonicalization-failure` must trigger semantic-result preservation. Minimal fix proposed (`is_packaging_error(r)`), candidate unmodified.

## Work Order 0.8.5.2 — Owner's F-21, F-22

**F-21 (confirmed):** Assurance evidence gap — the model admitted LEVEL_A + KERNEL_PROOF with no proof artifact, INDEPENDENT_RECOMPUTE with no agreement evidence, and LEVEL_A on INCONCLUSIVE. Invariant 6 was formalized exactly as written; the spec never required basis→evidence linkage.

**F-22 (confirmed):** Stale range "C-02..C-32" (line 89); corrected copy created.

## Work Order 0.8.6 — F-20 + F-21 corrections

**Changes:** Invariant 10 corrected to `is_packaging_error(e)` (both codes). New §E.6a linkage definitions + invariants 24–28 (Level A requires non-inconclusive; KERNEL_PROOF → proof record; INDEPENDENT_RECOMPUTE → recompute record; SOLVER_BACKED/TEST_BACKED evidence for Level B).

**Tests:** 13/13 Z3 checks pass.

**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW PENDING.

## Work Order 0.8.7 — F-22–F-27

**Owner findings addressed:** F-22 (narrow assurance scope), F-23 (unrelated evidence), F-24 (checker/hash/membership), F-25 (unrelated-evidence countermodels), F-26 (binder notation), F-27 (manifest overstatement).

**Changes:** Every basis requires substantiation at any level; KERNEL_PROOF requires PASS + method + property/claim-key match + checker + hash + membership; `is_sha256_hex` added; explicit binders; `VIOLATED{witness_ref}` added.

**Tests:** 18/18 pass — **but** the raw log (14:05:48Z) predates the R1-4 model fix (14:08:11Z). The preserved log does not correspond to the final model file. [OBSERVED EXECUTION — provenance gap]

**Independent normative review (R1):** Found blocking R1-1: `claim_key` undefined for payload-free variants (HOLDS, NO_SOLUTION, CONTRADICTION, UNIQUE_UNDER_PROJECTION). The TEST_BACKED+HOLDS path — described as a core check-goal path — cannot be evaluated. **Status: BLOCKED — NORMATIVE DECISION REQUIRED.**

**Independent model review (R2):** Did not complete (reviewer unresponsive).

## Work Order 0.8.7.2 — Claim identity decisions (read-only)

**Objective:** Answer three questions without modifying the candidate: (1) claim identity for all variants, (2) solver→claim linkage, (3) which test results apply to final files.

**Deliverables:** 5 reports. Key conclusions:
- Report C had a stale model hash (`e49aee04…`); the manifest (`7239f606…`) was correct.
- The 18/18 raw log cannot be tied to the final model (pre-R1-4).
- Recommended Option A (canonical claim descriptor) over schema-preserving conventions.
- Solver linkage requires invocation binding; presence is insufficient.

**Status:** OWNER DECISION PACKET PREPARED — NO NORMATIVE CHANGES MADE.

## Work Order 0.8.8 — Canonical claim identity + solver linkage

**Owner decision:** Option A selected as working direction.

**Changes (new candidate):** `ClaimDescriptor` with stored `claim_id`; `solver_invocations` collection; `SolverObs.provenance_ref` → `invocation_id`; invariants 25–28 revised for `claim_id` linkage; `__no_claim_key__` sentinel deleted; invariant 29 (`bases ≠ [] ⇒ claim_id = Some(_)`).

**Tests:** 16/16 adversarial tests pass.

**Reviews:**
- Normative: 3 blocking (N-1: `outcome_compatible` undefined; N-2: `claim_id` field ambiguity; N-3: vacuous satisfaction) — all repaired, re-verified.
- Model: 2 blocking (F1: inputs_ref/outcome missing; F2 = N-1) — F1(a) repaired; F1(b) documented as normative-only.

**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED.

## Work Order 0.8.8.1 — Formal closure

**Objective:** Close three gaps: (1) outcome compatibility mechanical, (2) descriptor completeness, (3) spec_version/input linkage.

**Changes:** `claim_kind` on record/descriptors/invocations; structured descriptor slots with mandatory-field flags; `spec_version` on vr; `outcome_compatible` implemented in model; `ResultRecord` gains `spec_version` and `claim_kind` normatively.

**Tests:** 9/9 pass (raw log 14:52:51Z, exit 0).

**Reviews:**
- Normative: 3 blocking (N-0.8.8.1-1: 7 kinds unresolved; N-0.8.8.1-2: vr.spec_version; N-0.8.8.1-3: model enforced non-existent fields) — all repaired.
- Model: 1 blocking (M1: sr-variant check) — repaired, **confirmed by re-inspection** on final hash `fc6eb49f…`.

**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED.

## Causal summary

Each round's verification targeted the previous round's defect class, and each round's new defects hid in the next unchecked layer:
- v0.8 → M8 exposed spec/validator mismatch
- 0.8.3 → owner exposed evidence-package defects
- 0.8.4 → Z3 exposed invariant 10 packaging gap (F-20)
- 0.8.5.2 → owner exposed assurance-evidence gap (F-21)
- 0.8.6 → corrections exposed claim-linkage gaps (F-22–F-27)
- 0.8.7 → R1 exposed payload-free claim identity (R1-1, blocking)
- 0.8.7.2 → forensic review exposed provenance gaps
- 0.8.8 → reviewers exposed undefined outcome_compatible, field ambiguity, vacuous satisfaction
- 0.8.8.1 → reviewers exposed unresolved kinds, spec_version gaps, sr-variant check

The external reviews have been doing the verification. The standing lesson (from v0.4, recorded in AGENTS.md): no PASS without a recorded refutation attempt.
