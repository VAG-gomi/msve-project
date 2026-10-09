# MSVE v0.8.7.2 — Work 4: Evidence-Linkage Gap Matrix

**Scope:** Current normative text (spec `48707955…`) and current model
(`audit_model_087.py` `7239f606…`). Normative requirements vs model
behaviour vs test coverage are separated.

## Per-basis matrix

| Basis | Correct claim? | Correct inputs? | Correct spec_version? | Exercised by | Independent review? |
|---|---|---|---|---|---|
| KERNEL_PROOF | Norm: YES (`property`=claim key, 7 variants). Model: YES (DERIVED_VALUE only). Tests: S4 (reject unrelated), S6 (accept). | Norm: NO (not required). Model: NO. Tests: — | Norm: NO. Model: NO. Tests: — | S4, S5, S6, S9, S10 | Normative: R1. Model: none (R2 incomplete). |
| INDEPENDENT_RECOMPUTE | Norm: YES. Model: YES (DERIVED_VALUE). Tests: S12 (accept). | Norm: YES (`inputs_ref`=verif inputs). Model: YES. Tests: S12. | Norm: NO. Model: NO. Tests: — | S3, S11, S12 | Normative: R1. Model: none. |
| SOLVER_BACKED | Norm: NO (no claim field). Model: NO. Tests: — | Norm: NO. Model: NO. Tests: — | Norm: NO. Model: NO. Tests: — | (none) | Normative: partial (Report B). Model: none. |
| TEST_BACKED | Norm: YES (`property`=claim key). Model: YES (DERIVED_VALUE). Tests: S7 (reject), S8 (accept). | Norm: NO. Model: NO. Tests: — | Norm: NO. Model: NO. Tests: — | S7, S8 | Normative: R1. Model: none. |

## Specific gaps

**claim_key() coverage:** Normative defines 7 variants (6 + VIOLATED).
Model implements only DERIVED_VALUE; all others →
`__no_claim_key__` sentinel. **The sentinel must not stand in for an
undefined key** — for non-DERIVED_VALUE results with a basis claimed,
the model demands `property = "__no_claim_key__"`, which is a
fabricated requirement, not the normative "undefined". R1-1 (4 variants)
remains blocking regardless.

**Sentinel behaviour:** If a `PROVED` result claims `KERNEL_PROOF`,
normative requires `property` = proof hash (defined). Model requires
`property` = `"__no_claim_key__"` (wrong). The model is **unfaithful**
for non-DERIVED_VALUE variants. No test exercises this (all proof
tests use DERIVED_VALUE).

**inputs_ref / spec_version:** `inputs_ref` is checked only for
recomputation (inv 26). `spec_version` on verification records is never
constrained. A record from a different spec version with otherwise
correct fields would satisfy invariants 25/28. **Gap:** no test, no
constraint.

**Checker identity vs authorization vs independence:**
- Identity (`checker ≠ ""`): enforced (inv 25, 26).
- Authorization (is this checker a valid kernel?): attested, not in schema.
- Independence (recompute checker ≠ producer): attested, not in schema.
- **Gap:** attestation has no normative format; "attested" is a prose
  claim without a checkable condition.

**Two-slot bounds:** 2 verification records, 2 slots per evidence
collection. A third record or artifact is unrepresentable. **Gap:**
bounded model; sufficient for the 18 tests but not a general guarantee.

**S1–S12 coverage:** S1/S2 (level scope), S3 (compatibility), S4/S5
(proof linkage), S6 (proof accept), S7/S8 (test linkage), S9 (hash
form), S10 (collection), S11/S12 (recompute). **Not covered:** solver
claim-linkage (no test), spec_version (no test), non-DERIVED_VALUE
proof (no test), third-record scenarios (unrepresentable).

**Independent formal-model review:** Incomplete (R2 unresponsive).
The 18/18 suite is behavioral evidence, not a review substitute.
