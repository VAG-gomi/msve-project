# MSVE v0.8.7.2 — Work 3: Solver-Linkage Decision Options

## Recommended minimal mechanism

**Chain:** Exact claim → solver query + inputs → invocation record →
`SolverObs` → `SemanticResult` → `SOLVER_BACKED`.

### How the solver invocation identifies the exact claim

The invocation record must contain the `claim_id` (per Work 2,
Option A) or `claim_ref` (Option B2) of the proposition being queried.
A solver does not prove "UNSAT" in the abstract; it reports UNSAT *of a
specific formula*. The invocation binds: `claim_id` + the negated
formula (or query) + `inputs_ref`.

### Where the canonical invocation and claim data reside

New normative collection `evidence.solver_invocations:
[SolverInvocation]`, where:
```
SolverInvocation := {
  invocation_id: Hash,     # sha256 of the canonical record
  claim_id: Hash,          # the exact claim queried
  query: String,           # canonical solver input (e.g., SMT-LIB)
  inputs_ref: Hash,        # relevant inputs
  spec_version: SemVer,    # spec under which the query was formed
  config: String,          # solver configuration
}
```
`SolverObs.provenance_ref` is normatively defined to equal
`invocation_id`, resolving in `evidence.solver_invocations`.

### How provenance_ref resolves

`∃ i ∈ evidence.solver_invocations: i.invocation_id =
obs.provenance_ref`. Membership is mechanically checkable (same
`resolves_in` pattern as proof artifacts). An absent target violates
the invariant.

### Binding inputs, version, config, outcome

The `SolverInvocation` record binds `inputs_ref`, `spec_version`, and
`config` at invocation time. The `SolverObs` reports `outcome` for
*that* invocation. A revised invariant 27 requires:
```
SOLVER_BACKED ∈ bases ⇒ ∃ obs = r.solver_observation, ∃ i ∈ invocations:
  (obs.provenance_ref = i.invocation_id ∧ i.claim_id = claim_id(r)
   ∧ i.inputs_ref = r.evidence.verification_inputs_ref)
```

### Checking conclusion against outcome and interpretation

Compatibility is determined by the **goal interpretation**, not by a
generic outcome→result map:
- `check` goal, query = "P holds", outcome UNSAT (of ¬P) →
  `HOLDS` (the solver refuted the negation).
- `check` goal, query = "P holds", outcome SAT (of ¬P with model) →
  `VIOLATED{witness_ref}` (counterexample found).
- `prove` goal: solver outcomes are *diagnostic only* (§E.5: no Level A
  pipeline); UNSAT may support `INCONCLUSIVE` shortfall, never `PROVED`.
- Outcome UNKNOWN → `INCONCLUSIVE{SOLVER_UNKNOWN}`; never a positive
  conclusion.

A normative **interpretation table** per goal type (not a generic
SAT→X rule) governs compatibility. The model encodes: `invocation.claim_id
= claim_id(result) ∧ outcome ∈ allowed_outcomes(goal_type, result_variant)`.

### Mechanically enforced vs attested

| Condition | Status |
|---|---|
| `provenance_ref` resolves in invocations | MECHANICALLY ENFORCED |
| `invocation.claim_id` = result claim | MECHANICALLY ENFORCED |
| inputs/spec_version/config binding | MECHANICALLY ENFORCED (equality) |
| Outcome–conclusion compatibility | MECHANICALLY ENFORCED (per interpretation table) |
| Solver actually ran the query | ATTESTED (no execution trace in schema) |
| Query faithfully encodes the claim | ATTESTED (requires query audit) |

### Schema change necessary?

Yes — minimal: `evidence.solver_invocations` collection +
normative definition of `provenance_ref`. Existing fields cannot
represent the invocation→claim binding. This is a proposal, not an
insertion.

## Adversarial scenarios (design examples, not executed tests)

**1. UNSAT for claim A + DERIVED_VALUE for claim B + SOLVER_BACKED**
- Required disposition: REJECT.
- Enforcing rule: `invocation.claim_id (= A) ≠ claim_id(result) (= B)`
  → invariant 27 violated.

**2. Correctly linked observation, outcome conflicts with conclusion**
- Example: invocation for claim C, outcome SAT(of ¬P), but result
  asserts `HOLDS` (which requires UNSAT of ¬P).
- Required disposition: REJECT.
- Enforcing rule: outcome ∉ allowed_outcomes(check, HOLDS) →
  compatibility invariant violated.

**3. Two distinct claims sharing the same computed value**
- Example: `derive 2+2` (claim_id H1) and `derive 8/2` (claim_id H2),
  both value `4`. Solver queried for H1 reports UNSAT(of ¬(2+2=4)).
  Result asserts H2 with SOLVER_BACKED.
- Required disposition: REJECT.
- Enforcing rule: `invocation.claim_id (H1) ≠ claim_id(result) (H2)`.
  (This is why claim identity must not be the output hash alone.)

**4. Valid-looking provenance hash, target absent or for another claim**
- Example: `obs.provenance_ref = Hx`; no invocation with `Hx` exists,
  or the invocation with `Hx` has `claim_id = Hy ≠ claim_id(result)`.
- Required disposition: REJECT.
- Enforcing rule: `¬∃ i: i.invocation_id = Hx` → membership violated;
  or claim mismatch → linkage violated.
