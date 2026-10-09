# MSVE v0.8.7 Transfer — Report B: Solver-Observation Linkage Audit

**Method:** Read-only inspection of the candidate spec and model.
No new tests run (per work order).

## The chain (normative clause → model constraint per arrow)

**Arrow 1: ResultRecord claim → claim-key/property identity**
- Normative: §E.6a "Claim linkage" — `vr.property` must equal the claim
  key of `r.semantic_result` (six variants + VIOLATED defined; HOLDS,
  NO_SOLUTION, CONTRADICTION, UNIQUE_UNDER_PROJECTION undefined — R1-1).
- Model: `claim_key(R)` implements DERIVED_VALUE → value/derivation
  hash; `v['property'] == _ck` in inv 25/26/28.
- Labels: NORMATIVELY DEFINED (for 7 variants) / MECHANICALLY ENFORCED
  (for DERIVED_VALUE) / UNDEFINED OR UNDERCONSTRAINED (for 4 variants).

**Arrow 2: claim-key/property identity → solver invocation/provenance**
- Normative: None. `SolverObs.provenance_ref: Hash` has no defined
  target (Report A, A6).
- Model: `R['has_solver']` boolean + `R['solver_outcome']` string. No
  provenance field modeled.
- Labels: UNDEFINED OR UNDERCONSTRAINED.

**Arrow 3: solver invocation/provenance → SolverObs**
- Normative: `SolverObs := { outcome, tool, version, config,
  provenance_ref, certificate_ref? }`. No rule links `provenance_ref`
  to an invocation record.
- Model: presence only.
- Labels: NORMATIVELY DEFINED (structure) / UNDEFINED OR
  UNDERCONSTRAINED (provenance relationship).

**Arrow 4: SolverObs → SemanticResult**
- Normative: Inv 4 (CHECKER_DIVERGENCE → discrepancy), inv 11 (UNSAT +
  Level A shortfall → INCONCLUSIVE), inv 22 (CONTRADICTION → UNSAT ∨
  proof artifact).
- Model: these three constraints encoded.
- Labels: NORMATIVELY DEFINED / MECHANICALLY ENFORCED (partial — only
  these three patterns).

**Arrow 5: SemanticResult → assurance basis**
- Normative: Inv 6 (LEVEL_A → KERNEL_PROOF ∨ INDEPENDENT_RECOMPUTE),
  inv 7 (LEVEL_B → bases non-empty), inv 24–28 (substantiation).
- Model: encoded.
- Labels: NORMATIVELY DEFINED / MECHANICALLY ENFORCED.

## Question A: Claim identity

The claim-key identifies the result *variant* and the *specific hash*
(value, derivation, proof, artifact, witness). It does **not**
distinguish the proposition beyond the hash, nor the goal, projection,
or inputs — except that recomputation records link `inputs_ref` to
`verification_inputs_ref`. For solver observations, there is no
claim-identity linkage at all: `SolverObs` has no `property` or claim
field.

**Answer:** The claim-key maps variant + hash. It does not encode goal,
projection, or inputs. Solver observations are not claim-linked.

## Question B: Solver identity

v0.8.7 `SolverObs` (spec lines 1142–1144):
```
SolverObs := { outcome: SAT | UNSAT | UNKNOWN, tool: String, version: SemVer,
               config: String, provenance_ref: Hash,
               certificate_ref: Option<Hash> }
```
`provenance_ref: Hash` — **no normative definition** of its target
exists in the specification. It is not represented in the formal model
(`has_solver` boolean only). The relationship is **not
machine-checkable**: no constraint references `provenance_ref`.

Labels: NORMATIVELY DEFINED (field exists) / UNDEFINED OR
UNDERCONSTRAINED (target and checkability).

## Question C: Wrong-claim counterexample

**Scenario:** solver observation present, well-formed provenance_ref,
solver reports UNSAT for claim A; SemanticResult asserts DERIVED_VALUE
for claim B; SOLVER_BACKED claimed.

**Analysis against encoded constraints:**
- Inv 27 (revised): `SOLVER_BACKED ∈ bases ⇒ has_solver`. Satisfied
  (observation present).
- Inv 4: not CHECKER_DIVERGENCE. N/A.
- Inv 11: requires Level A required + not achieved. If Level B
  achieved, N/A.
- Inv 22: requires CONTRADICTION result. Not applicable (DERIVED_VALUE).
- No constraint links `solver_outcome` to the semantic result's claim.

**Conclusion:** The model **permits** this record. The wrong-claim
solver counterexample is **not ruled out** by the encoded constraints.

**Test evidence:** No preserved test evaluates this scenario. The 18
tests include no SOLVER_BACKED + mismatched-claim case.

**Constraints needed to evaluate later:** (1) a `claim` or `property`
field on the solver observation (schema change) OR a normative rule
linking `provenance_ref` to the claim; (2) an invariant requiring
outcome-claim consistency; (3) a test with solver UNSAT for claim A +
DERIVED_VALUE for claim B + SOLVER_BACKED, expecting UNSAT. No solver
verdict is fabricated here.

## Question D: Outcome and conclusion compatibility

| Outcome | Result | Constrained? |
|---|---|---|
| UNSAT | INCONCLUSIVE{ASSURANCE_REQUIREMENT_UNMET} | Yes (inv 11, shortfall only) |
| UNSAT | CONTRADICTION | Yes (inv 22, disjunctive) |
| SAT | CONTRADICTION | Partial (inv 22 allows via resolves disjunct) |
| UNKNOWN | any | No general rule |
| Any | DERIVED_VALUE/HOLDS/etc. | No general compatibility rule |

**Answer:** Compatibility is constrained only for the three specific
patterns (inv 4, 11, 22). There is no general "solver outcome must be
compatible with semantic conclusion" invariant. An observation is not
treated as a proof merely by existing (inv 22 requires UNSAT *or*
artifact; inv 6 forbids solver-only Level A), but an *incompatible*
observation is not generally rejected.

## Question E: Other bases — field-by-field

| Basis | Field | Status |
|---|---|---|
| KERNEL_PROOF | `source_item="proof"` | MECHANICALLY ENFORCED |
| KERNEL_PROOF | `result=PASS` | MECHANICALLY ENFORCED |
| KERNEL_PROOF | `method="kernel-checked"` | MECHANICALLY ENFORCED |
| KERNEL_PROOF | `property`=claim key | MECHANICALLY ENFORCED (7 variants) / UNDEFINED (4 variants) |
| KERNEL_PROOF | `artifact` hash form | MECHANICALLY ENFORCED |
| KERNEL_PROOF | `artifact` ∈ proof_artifacts | MECHANICALLY ENFORCED |
| KERNEL_PROOF | `checker` non-empty | MECHANICALLY ENFORCED |
| KERNEL_PROOF | checker authorization | ATTESTED / NOT MECHANICALLY ENFORCED |
| INDEPENDENT_RECOMPUTE | `source_item`, PASS, property, checker≠"", inputs_ref, artifact | MECHANICALLY ENFORCED |
| INDEPENDENT_RECOMPUTE | checker independence | ATTESTED / NOT MECHANICALLY ENFORCED |
| INDEPENDENT_RECOMPUTE | DERIVED_VALUE compatibility | MECHANICALLY ENFORCED |
| TEST_BACKED | `source_item`, PASS, property=claim key | MECHANICALLY ENFORCED |
| TEST_BACKED | inputs, spec_version | UNDEFINED OR UNDERCONSTRAINED (not checked) |
| SOLVER_BACKED | observation present | MECHANICALLY ENFORCED |
| SOLVER_BACKED | outcome compatibility | PARTIAL (inv 4/11/22 only) |
| SOLVER_BACKED | provenance_ref | UNDEFINED OR UNDERCONSTRAINED |
| SOLVER_BACKED | claim linkage | UNDEFINED OR UNDERCONSTRAINED |

## Summary

The v0.8.7 corrections **demonstrably resolve** claim-linkage for
proof, recomputation, and test bases *where claim keys are defined*
(S4/S5/S7 reject unrelated evidence). They **partially resolve**
solver linkage (presence required; outcome compatibility partial).
They **leave open**: (1) solver claim-identity (no field, no
constraint — the wrong-claim counterexample is permitted); (2)
`provenance_ref` (undefined target); (3) claim keys for four variants
(R1-1, blocking). Items (1) and (3) require owner normative decisions.
