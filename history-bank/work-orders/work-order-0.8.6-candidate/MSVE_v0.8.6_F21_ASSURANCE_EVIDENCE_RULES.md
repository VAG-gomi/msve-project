# MSVE v0.8.6 F-21 Assurance Evidence Rules

**Principle (normative, §E.6a):** an assurance basis recorded as achieved
must be supported by an identifiable, appropriate verification record
and the evidence required to substantiate that basis. Membership in
`assurance_bases` alone is not sufficient.

## Rules by basis

### KERNEL_PROOF (invariant 25)

Applies when `assurance_achieved = LEVEL_A` and `KERNEL_PROOF ∈
assurance_bases`. Requires a verification record with:
- `source_item = "proof"`,
- `result = PASS`,
- `artifact` = exactly the 64-character lowercase hex sha256 of the
  proof artifact, resolving in `evidence.proof_artifacts`.

A record naming `KERNEL_PROOF` without this evidence violates invariant
25 (demonstrated: R5 UNSAT).

### INDEPENDENT_RECOMPUTE (invariant 26)

Applies when `assurance_achieved = LEVEL_A`, `INDEPENDENT_RECOMPUTE ∈
assurance_bases`, on a `DERIVED_VALUE` result (§E.5 scopes recomputation
to `derive` goals). Requires a verification record with:
- `source_item = "recompute"`,
- `result = PASS` (normatively: exact agreement per §D.6),
- `checker` identifying the independent checker (independence attested,
  recorded for audit; not mechanically derivable — limitation),
- `artifact` = the primary result hash (value hash when `value_ref =
  Some(h)`, else the `derivation_ref` hash),
- `inputs_ref` = `evidence.verification_inputs_ref`.

A record naming `INDEPENDENT_RECOMPUTE` without this evidence violates
invariant 26 (demonstrated: R7 UNSAT).

**Schema determination:** no new field introduced. The linkage uses
normatively constrained existing fields. Independence remains attested
rather than derived.

### Level A result requirement (invariant 24)

`assurance_achieved = LEVEL_A ⟹ semantic_result = Some(sr) ∧ sr ≠
INCONCLUSIVE{_}`. Achieved Level A requires an actual, non-inconclusive
result (demonstrated: R8 UNSAT). The invariant-11 shortfall pattern
(Level A required, Level B achieved, `INCONCLUSIVE{
ASSURANCE_REQUIREMENT_UNMET}`) is preserved (demonstrated: R9 SAT).

### SOLVER_BACKED / TEST_BACKED (invariants 27, 28)

- `LEVEL_B` achieved ∧ `SOLVER_BACKED ∈ bases ⟹ solver_observation =
  Some(_)` (any outcome; evidential weight per §D.6).
- `LEVEL_B` achieved ∧ `TEST_BACKED ∈ bases ⟹ ∃ verification record
  with `source_item ∈ {"test:differential", "test:property-fuzz"}` and
  `result = PASS`.
- Demonstrated: R10 SAT (linked evidence); unevidenced bases rejected by
  construction.

### Evidence objects per basis

| Basis | Evidence object | Verification record | Basis in record | Linking rule |
|---|---|---|---|---|
| KERNEL_PROOF | proof artifact in `evidence.proof_artifacts` | `source_item="proof"`, PASS | `assurance_bases` | inv 25; §E.6a hash rule |
| INDEPENDENT_RECOMPUTE | recomputation comparison | `source_item="recompute"`, PASS | `assurance_bases` | inv 26; §E.6a |
| SOLVER_BACKED | `solver_observation` | (observation itself) | `assurance_bases` | inv 27 |
| TEST_BACKED | test execution | `source_item="test:…"`, PASS | `assurance_bases` | inv 28 |

Only bases actually claimed for the achieved level require evidence;
no invariant requires all four bases to be present.
