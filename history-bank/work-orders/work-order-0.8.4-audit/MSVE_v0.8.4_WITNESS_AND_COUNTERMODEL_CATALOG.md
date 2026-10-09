# MSVE v0.8.4 Witness and Countermodel Catalog (Phase C)

**Method:** z3 5.1.0, one `Solver()` per scenario, 30 s timeout, over the
reconciled invariant set. Each witness below is a Z3 model satisfying **all**
encoded invariants jointly, not just the scenario's own rule. Each
countermodel entry is an UNSAT result: no assignment satisfies the invariants
together with the stated invalid condition.

## Valid witnesses (all SAT)

| ID | Scenario | Key record features |
|---|---|---|
| S1 | Accepted execution, derived value, packaged OK | `ACCEPTED / COMPLETED / PACKAGING_OK`; `DERIVED_VALUE(value_ref=Some, derivation_ref→derivation_records)`; `value_ref→constructed_artifacts`; `LEVEL_A/LERNEL_PROOF`, no shortfall |
| S2 | Accepted execution, artifact constructed, packaged OK | `ACCEPTED / COMPLETED / PACKAGING_OK`; `ARTIFACT_CONSTRUCTED(Some→constructed_artifacts)`; `LEVEL_B/SOLVER_BACKED` |
| S3 | Unencodable result, semantic preserved, 15b linkage | `ACCEPTED / INTERNAL_ERROR("output-not-encodable: Binary64 NaN") / PACKAGING_FAILED("output-not-encodable")`; `DERIVED_VALUE(value_ref=None)`; semantic result present (inv 10) |
| S4 | Internal error unrelated to packaging | `ACCEPTED / INTERNAL_ERROR("division-by-zero") / PACKAGING_OK`; `INCONCLUSIVE(RESOURCE_EXHAUSTED)`; no assurance |
| S5 | INVALID_INPUT | `INVALID_INPUT("unbound-identifier: foo") / NOT_STARTED / PACKAGING_OK`; no semantic result; `NOT_RUN`; `NONE/NONE` |
| S6 | UNSUPPORTED | `UNSUPPORTED("goal-not-supported: liveness") / NOT_STARTED`; no semantic result; `NOT_RUN` |
| S7 | All 11 `SemanticResult` alternatives (§E.2 goal mapping) | each alternative realized with its mandatory evidence resolving in the correct collection; `HOLDS` with a PASS record whose `inputs_ref` equals the bundle's `verification_inputs_ref` |
| S8a | Level A, no shortfall | `LEVEL_A required/achieved`, `KERNEL_PROOF` basis, `shortfall=false` |
| S8b | Level A required, Level B achieved → shortfall | `UNSAT` obs; `INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET)`; `shortfall=true`, description present (inv 5, 11) |
| S8c | Level B required, none achieved → shortfall | `shortfall=true`, description present |
| S9a–d | Summaries PASS / FAIL / INCONCLUSIVE / CHECKER_DIVERGENCE | divergence case: PASS+FAIL records on records, `discrepancies` has an `OPEN` entry (inv 4), summary `CHECKER_DIVERGENCE` |
| S10a/b | TIMEOUT / INTERRUPTED with partial results | `has_partial=true`, no semantic result |
| S11 | Projection-relative uniqueness | `UNIQUE_UNDER_PROJECTION` + `UNSAT` solver observation |
| S12 | Required evidence present | `PROVED` with proof hash resolving in `proof_artifacts` |
| S13a | Detailed admission code | `INVALID_INPUT("syntax-error: line 3: unexpected \"}\"")` — base_code `syntax-error` |
| S13b | Detailed unsupported code | `UNSUPPORTED("scope-not-supported: higher-order unification")` |
| S13c | Detailed packaging code | `INTERNAL_ERROR("canonicalization-failure: blob exceeds 1MiB")` + `PACKAGING_FAILED("canonicalization-failure: digest mismatch")` — base codes match per 15b, details differ per F-01 |

Example extracted witness (S3, abbreviated): execution
`INTERNAL_ERROR(output-not-encodable: Binary64 NaN)`, packaging
`PACKAGING_FAILED(output-not-encodable)`, `DERIVED_VALUE` with
`value_ref=None`, derivation resolving in `derivation_records`,
`assurance_shortfall=true` with description (solver picked
`LEVEL_A` required / `NONE` achieved — consistent with inv 5).

## Countermodels — invalid variants (all UNSAT, rejected for identifiable reasons)

| ID | Invalid condition | Violated invariant(s) |
|---|---|---|
| X12 | `PROVED` whose proof hash does not resolve in `proof_artifacts` | 17 |
| X13a | `INVALID_INPUT("not-a-real-code: foo")` | 1b (`is_admission_error` false) |
| X13b | `INVALID_INPUT("syntax-error:foo")` — no `": "`, so `base_code` is the whole string | 1b |
| X-a | `PACKAGING_FAILED` with `COMPLETED` execution | 15b (⟹ direction) |
| X-b | `PACKAGING_OK` with `INTERNAL_ERROR("output-not-encodable: x")` | 15b (second paragraph) |
| X-c | `INVALID_INPUT` with a semantic result present | 1 |
| X-d | `LEVEL_A` achieved with only `SOLVER_BACKED` basis | 6 |
| X-e | `LEVEL_A`/`LEVEL_A` with `shortfall=true` | 5 (biconditional with shortfall rule) |
| X-f | `UNIQUE_UNDER_PROJECTION` with no solver obs and no derivation record | 23 (weakened) |
| X-g | required FAIL record with summary `PASS` | 14 |
| X-h | partial results with `COMPLETED` execution | 13 |
| X-i | `DERIVED_VALUE` + `PACKAGING_OK` with `value_ref=None` | 15 |
| X-j | `DERIVED_VALUE` + `PACKAGING_FAILED` with `value_ref=Some` | 15 |
| X-k | `HOLDS` with PASS record whose `inputs_ref` mismatches the bundle hash | 20 (weakened) |

The 13/13 rejections confirm the encoded constraints have teeth: the
witnesses are not SAT by vacuity.
