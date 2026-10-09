# MSVE v0.8.7 Transfer Handoff

**Work Order:** 0.8.7.1 · **Date:** 2026-10-09
**Candidate:** `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/`
**Candidate spec SHA-256:** `48707955c81c4731e8533fa5135de2001388fd11461e2b0cef5a518730c4080e`
(90498 bytes; includes R1-4/R1-5/VIOLATED fixes)

## Transfer contents

`owner-review-transfer/` contains:
- Report A: `MSVE_v0.8.7_TRANSFER_NORMATIVE_TEXT.md` — verbatim normative excerpts
- Report B: `MSVE_v0.8.7_TRANSFER_SOLVER_LINKAGE.md` — solver-observation linkage audit
- Report C: `MSVE_v0.8.7_TRANSFER_MODEL_LINKAGE.md` — formal-model mapping
- Report D: `MSVE_v0.8.7_TRANSFER_REGRESSION_EVIDENCE.md` + byte-identical `run_audit_087_raw.log`, `sat_models_087.json`, `run_audit_087.py`
- Report E: `MSVE_v0.8.7_TRANSFER_REVIEW_STATUS.md` — review provenance
- `MSVE_v0.8.7_TRANSFER_MANIFEST.md` — integrity manifest (true source paths)

## Missing or unavailable artefacts

- No independent formal-model review (R2 unresponsive; closed).
- No wrong-claim solver counterexample test (not in preserved evidence;
  Report B identifies the constraints needed).
- `provenance_ref` target: undefined in the specification.

## Narrow unresolved questions

1. **R1-1 (blocking):** What identifies the claim for payload-free
   variants (`HOLDS`, `NO_SOLUTION`, `CONTRADICTION`,
   `UNIQUE_UNDER_PROJECTION`)? Owner normative decision required.
2. **Solver claim-linkage:** Does `SOLVER_BACKED` require a claim-linked
   solver observation, or is presence + outcome-compatibility sufficient?
   The wrong-claim counterexample is currently permitted.
3. **R1-2/R1-3:** Formal `claim_key` function definition (deferred
   pending Q1).

## Primary decision criterion

Does v0.8.7 establish that the evidence and solver observation support
the exact claim asserted in the semantic result, rather than merely
being present and correctly labelled?

**Answer from this transfer:** For proof, recomputation, and test bases
with defined claim keys — yes, mechanically (S4/S5/S7). For solver
observations — no: presence is enforced, claim-linkage is absent, and
the wrong-claim record is permitted. For payload-free variants — cannot
be evaluated (R1-1).

---

EVIDENCE TRANSFER PREPARED — OWNER REVIEW REQUIRED
