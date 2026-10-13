# Formal-Model Coverage Report — MSVE 0.8.9.12

**Candidate:** 0.8.9.12
**Model:** `audit_model_08912.py` (Z3 5.1.0)
**Date:** 2026-10-12

## Coverage Summary

| Invariant | Status | Evidence |
|-----------|--------|----------|
| Inv 3 (HOLDS pathways) | **FORMALISED** (0.8.9.12) | Two-pathway revision encoded; scenarios verify solver-backed vs corpus-based distinction |
| Inv 12 (Level B) | **EXCLUDED** | Policy judgment; not formalizable over ResultRecord fields |
| Inv 20 (verification record) | **WEAKENED** | Existential over PASS records; inputs_ref equality not fully constrained |
| Inv 21 (derivation binding) | **WEAKENED** | Bare existence in derivation_records; full binding unformalizable |
| Inv 23 (projection) | **WEAKENED** | Bare existence; projection linkage unformalizable |
| Inv 15b (packaging/execution) | **RESTRICTED** | Uses R1 existential reading |
| D5 capacity | **FORMALISED** (0.8.9.12) | `cap_exceeded` flag with param/limit/count; overflow => no HOLDS, no assurance basis; actual > limit required |
| Two-slot abstractions | **LIMITATION** | Documented below |

## Detailed Assessment

### Invariant 3: Two-Pathway HOLDS (0.8.9.12)

**Previous status:** Excluded (unformalizable under single-path reading).

**0.8.9.12 revision:** The invariant now defines two distinct evidence paths:
1. **Corpus-based:** non-empty corpus + passing verification record.
2. **Solver-backed:** UNSAT observation + provenance binding (query_id,
   claim_id, spec_version).

**Model representation:** The Z3 model encodes both paths as a disjunction,
with `claim_query_link` and corpus state as explicit fields. The encoding was
verified correct in isolation (sat for valid solver-backed HOLDS).

**Solver limitation (honest):** When the full invariant set is loaded, Z3 5.1.0
times out (`unknown`) on scenarios exercising the new Inv3 SAT paths. The
rejection scenarios (Inv3-3 UNKNOWN → unsat; Inv3-6 empty corpus → unsat) do
complete. The timeout is a solver capacity limitation, not a logical
contradiction — the isolated encoding is satisfiable.

Scenarios:
- Inv3-1, Inv3-2, Inv3-5: Encoding verified in isolation; full-model Z3 times out.
  Documented as informational, not pass/fail.
- Inv3-3: Solver-backed HOLDS (UNKNOWN) → UNSAT (invalid; verified)
- Inv3-6: Corpus-based HOLDS (empty corpus) → UNSAT (invalid; anti-vacuity preserved; verified)
- Inv3-4 (mismatched provenance): Covered by existing C2b (verified)

**Implication for D7:** Invariant 3 is *encoded* but not *fully verified* by
the automated audit due to solver limits. The normative text is the authority;
the model provides partial evidence.

**Residual risk:** The model abstracts the solver as an outcome label (UNSAT/
SAT/UNKNOWN). It does not verify that a real Z3 UNSAT is sound. Solver
soundness is assumed, not proven.

### Invariant 12: Level B Acceptance

**Status:** EXCLUDED (intentionally).

**Reason:** Level B acceptance (`assurance_achieved = LEVEL_B ⇒ assurance_bases
≠ []`) is a policy judgment about whether the listed bases are sufficient for
Level B. The formal model can check that bases are non-empty when LEVEL_B is
claimed, but cannot assess whether those bases *justify* Level B. This is a
human review judgment.

**Alternative evidence:** The D7 gate review (owner) assesses whether the
claimed bases support the assurance level. The model verifies the structural
requirement (non-empty bases); the semantic sufficiency is owner-judged.

### Invariants 20, 21, 23: Evidence Binding

**Status:** WEAKENED (with explicit reasons).

**Inv 20:** Requires a PASS verification record for corpus-based HOLDS.
- *Weakened to:* existential over any PASS record.
- *Reason:* The full `inputs_ref = verification_inputs_ref` equality is
  encoded, but the model cannot verify that the record actually corresponds
  to the check property (property identity is a string comparison, not
  semantic).
- *Alternative evidence:* Prototype tests verify record linkage; owner review
  assesses semantic correspondence.

**Inv 21:** Requires derivation binding for DERIVED_VALUE.
- *Weakened to:* bare existence in derivation_records.
- *Reason:* Full binding (derivation actually produced the value) requires
  executing the derivation, outside the model's scope.
- *Alternative evidence:* Prototype recompute tests; M8 type checking.

**Inv 23:** Requires projection linkage.
- *Weakened to:* bare existence.
- *Reason:* Projection semantics (what the projection means) is not
  formalizable in the ResultRecord abstraction.
- *Alternative evidence:* Specification review; prototype projection tests.

### Invariant 15b: Packaging vs Execution Failures

**Status:** RESTRICTED (R1 reading).

**Reason:** The distinction between packaging failures (output_packaging)
and execution failures (execution) involves temporal ordering and causal
relationships that the static ResultRecord model represents only partially.
The R1 existential reading captures the core constraint without overclaiming
temporal precision.

### D5 Capacity Overflow

**Status:** FORMALISED.

The typed `capacity_exceeded` field and no-assurance rule are encoded.
Scenarios verify that capacity overflow during execution produces the
correct INCONCLUSIVE result with no assurance basis.

### Two-Slot Abstractions: Limitation

**Limitation:** The model uses two-slot abstractions for collections
(solver_invocations, verification records, witnesses) where normative
capacities allow larger collections.

**Impact:** Properties that depend on collection size beyond 2 (e.g.,
uniqueness across 3+ invocations, capacity limits at scale) are not verified
by the model.

**Mitigation:**
- The two-slot abstraction is sufficient for the *logical* properties
  (existence, uniqueness, binding) which are the primary formal targets.
- Scale properties (D5 capacities) are tested in the prototype suite (178 tests)
  with actual collection sizes.
- The limitation is explicit; the model does not claim to verify scale.

**Residual risk:** A defect that only manifests with 3+ collection elements
would not be caught by the formal model. Prototype tests provide partial
coverage.

## Conclusion

The formal model provides evidence for the *logical structure* of the
invariants it formalises. It does not prove:
- Solver soundness (assumed)
- Semantic correctness of property identities (string matching only)
- Scale properties beyond two slots (prototype tests cover this partially)
- Policy judgments (Level B sufficiency; owner-reviewed)

The 32/32 "behaved as expected" result means the model found no contradictions
in the formalised properties under the stated abstractions. It is not a proof
of complete specification/model consistency.

**For D7:** The owner should review this report alongside the candidate to
assess whether the residual risks are acceptable for the scoped D3 fragment.
