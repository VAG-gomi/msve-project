# MSVE v0.8.8.1 — Evidence Linkage Matrix

| Basis | claim_id | spec_version | inputs_ref | Descriptor | Test |
|---|---|---|---|---|---|
| KERNEL_PROOF | vr.claim_id = r.claim_id | vr.spec = r.spec | — | Present | C2, V5 |
| INDEPENDENT_RECOMPUTE | vr.claim_id = r.claim_id | vr.spec = r.spec | vr.inputs = verif_inputs | Present | B14 (0.8.8) |
| SOLVER_BACKED | inv.claim_id = r.claim_id | — (invocation) | inv.inputs = verif_inputs | Present | O1, O2 |
| TEST_BACKED | vr.claim_id = r.claim_id | vr.spec = r.spec | vr.inputs = verif_inputs | Present | C3 |

**Notes:**
- spec_version on solver invocations: normative field exists; model does not yet check invocation spec_version (gap noted).
- A matching claim hash does not make stale evidence valid: spec_version and inputs_ref mismatches are rejected (V5, B16 in 0.8.8).
- All: normatively defined, mechanically enforced, exercised, pending review.
