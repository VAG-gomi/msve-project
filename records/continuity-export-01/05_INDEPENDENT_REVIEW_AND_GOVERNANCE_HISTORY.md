# MSVE Continuity Package — 05 INDEPENDENT REVIEW AND GOVERNANCE HISTORY

## Review rounds (chronological)

### 0.8.4: Reviewers A and B (formalization)

**Scope:** Independent formalization of all 23 §E.7 invariants from the 0.8.3 candidate bytes.
**Result:** Converged; reconciliation resolved 15b as restricted-existential. [REVIEWER FINDING]

### 0.8.7: R1 (normative) — completed; R2 (model) — incomplete

**R1 scope:** Normative text of the 0.8.7 candidate.
**R1 findings:** R1-1 (blocking: claim_key undefined for payload-free variants); R1-2–R1-5 (non-blocking; R1-4 repaired: checker in inv 25).
**R2:** Spawned, unresponsive, closed without report. **No independent model review of 0.8.7 was completed.** [OBSERVED]

### 0.8.7.2: No new reviewers (read-only forensic review by the assistant)

### 0.8.8: Normative + model reviewers

**Normative:** 3 blocking (N-1: outcome_compatible undefined; N-2: claim_id field ambiguity; N-3: vacuous satisfaction). All repaired; re-verified (16/16).
**Model:** 2 blocking (F1: inputs_ref/outcome missing from inv 27; F2 = N-1). F1(a) repaired; F1(b) documented as normative-only at that time.
**Retrieval problem:** The model reviewer's full report was initially unretrievable from the session archive; it was later recovered via handoff. This caused a temporary BLOCKED status that was resolved. [OBSERVED]

### 0.8.8.1: Normative + model reviewers (final)

**Normative** (verified spec `dbc610c3…`):
- N-0.8.8.1-1 (blocking): 7 kinds unresolved in outcome table → repaired (explicitly marked).
- N-0.8.8.1-2 (blocking): vr.spec_version unconstrained → repaired (conjuncts added).
- N-0.8.8.1-3 (blocking): model enforced non-existent fields → repaired (fields added normatively).

**Model** (verified model `efd8e40b…`):
- M1 (blocking): sr-variant check omitted → repaired.
- M2 (non-blocking): assumptions not modeled → acknowledged.

**Re-inspection** (verified final model `fc6eb49f…`): M1 confirmed repaired at lines 375/377. No other substantive changes. [REVIEWER FINDING]

**Agreement:** Both reviewers' blocking findings are repaired and re-verified. No reviewer disagreement remains open. The 7 unresolved kinds are marked, not decided — this is a documented limitation, not a disagreement.

## Governance notes

- **No reviewer agreement** was reached before 0.8.7's initial finalisation (R2 incomplete). This was disclosed, not hidden.
- **Reviews do not transfer across modifications:** each repair invalidated the prior run; fresh runs and re-inspections were obtained. The 0.8.8.1 model re-inspection explicitly verified the final hash.
- **Normative vs. model review are separate:** neither implies the other. Both were obtained for 0.8.8 and 0.8.8.1.
- **No manufactured quotations:** all findings above are from the actual reviewer reports preserved in the candidate directories (`MSVE_v0.8.8.1_NORMATIVE_REVIEW.md`, `MSVE_v0.8.8.1_MODEL_REVIEW.md`).
