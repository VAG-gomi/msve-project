# MSVE v0.8.6 Transfer — Report C: Regression and Countermodel Evidence

**Test script:** `~/workspace/msve-design/work-order-0.8.6-candidate/run_audit_086.py`
**Model:** `audit_model_086.py` (31 shared constraints)
**Source of truth for outcomes:** `MSVE_v0.8.6_VERIFICATION_EVIDENCE.md`
(13/13 as expected; no raw log file was preserved — see Report D).

The input constraints for each case are the Python constraint lists in
`run_audit_086.py` (functions `_s1`–`_s12`). Verbatim excerpts follow each
case summary. Raw model assignments were not preserved as files; the
scenario constraints below are the complete inputs.

---
## R1: Packaging failure (output-not-encodable), semantic result present

**Purpose:** F-20: corrected invariant 10 preserves result for output-not-encodable

**Expected:** sat · **Actual:** sat · **Responsible:** invariant 10 (corrected)

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: Binary64 NaN')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        resolves(H('e'*64), COLL('derivation_records')),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
```

---
## R2: Packaging failure (canonicalization-failure), semantic result present

**Purpose:** F-20: corrected invariant 10 preserves result for canonicalization-failure

**Expected:** sat · **Actual:** sat · **Responsible:** invariant 10 (corrected)

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: digest mismatch')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure: blob too large')),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        resolves(H('e'*64), COLL('derivation_records')),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
```

---
## R3a: Packaging failure (output-not-encodable), semantic result missing

**Purpose:** F-20: corrected invariant 10 rejects result-dropping

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 10 (corrected)

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        z3.Not(R['has_semres'])]
```

---
## R3b: Packaging failure (canonicalization-failure), semantic result missing

**Purpose:** F-20: corrected invariant 10 rejects result-dropping

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 10 (corrected)

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure')),
        z3.Not(R['has_semres'])]
```

---
## R4: Level A + KERNEL_PROOF basis + valid supporting evidence

**Purpose:** F-21: invariant 25 satisfied by passing proof record linked to proof_artifacts

**Expected:** sat · **Actual:** sat · **Responsible:** invariants 6, 24, 25

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        resolves(H('p'*64), COLL('proof_artifacts')),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
```

---
## R5: Level A + KERNEL_PROOF label, no supporting evidence

**Purpose:** F-21: invariant 25 rejects evidence-free basis claim

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 25

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present'])]
```

---
## R6: Level A + INDEPENDENT_RECOMPUTE + agreement evidence

**Purpose:** F-21: invariant 26 satisfied by passing recompute record

**Expected:** sat · **Actual:** sat · **Responsible:** invariants 6, 24, 26

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('recompute'),
        R['vr'][0]['artifact'] == H('a'*64),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
```

---
## R7: Level A + INDEPENDENT_RECOMPUTE label, no agreement evidence

**Purpose:** F-21: invariant 26 rejects evidence-free recompute claim

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 26

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present'])]
```

---
## R8: Level A achieved on INCONCLUSIVE semantic result

**Purpose:** F-21: invariant 24 rejects Level A on inconclusive

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 24

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        resolves(H('p'*64), COLL('proof_artifacts')),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['artifact'] == H('p'*64)]
```

---
## R9: Level A required, Level B achieved, ASSURANCE_REQUIREMENT_UNMET

**Purpose:** Shortfall case preserved: invariant 24 does not apply (achieved=LEVEL_B)

**Expected:** sat · **Actual:** sat · **Responsible:** invariants 5, 11

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('ASSURANCE_REQUIREMENT_UNMET')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'], R['assur_short'], R['has_shortdesc']]
```

---
## R10: Level B + SOLVER_BACKED + TEST_BACKED with linked evidence

**Purpose:** F-21: invariants 27, 28 satisfied

**Expected:** sat · **Actual:** sat · **Responsible:** invariants 7, 27, 28

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_solver'], R['solver_outcome'] == H('SAT'),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'], R['bases']['TEST_BACKED'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('test:differential'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
```

---
## R11: PASS proof record with unresolved artifact

**Purpose:** F-21: invariant 25 requires artifact to resolve in proof_artifacts

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 25

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['artifact'] == H('q'*64),
        z3.Not(resolves(H('q'*64), COLL('proof_artifacts'))),
        z3.Not(R['vr'][1]['present'])]
```

---
## R12: Level A claim with FAILing proof record

**Purpose:** F-21: invariant 25 requires result=PASS; stronger-than-evidence rejected

**Expected:** unsat · **Actual:** unsat · **Responsible:** invariant 25

**Input constraints (verbatim from `run_audit_086.py`):**
```python
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        resolves(H('p'*64), COLL('proof_artifacts')),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_FAIL,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['required'],
        z3.Not(R['vr'][1]['present'])]
```

---

## F-20 questions

- **Does each packaging-failure code preserve a present semantic result?**
  Yes: R1 (output-not-encodable) and R2 (canonicalization-failure) both
  SAT with `has_semres=True` under corrected invariant 10.
- **Does the test require result presence, rather than only matching
  execution/packaging status?** Yes: R3a/R3b assert `Not(has_semres)` and
  are UNSAT — the rejection is due to the missing result, not the
  status linkage (which is satisfied in all four cases).
- **Does the tested formula correspond exactly to the candidate's
  normative wording?** The formula is
  `INTERNAL_ERROR(e) ∧ is_packaging_error(e) ⟹ has_semres`; the normative
  wording is "if the failure occurred at packaging
  (`is_packaging_error(e)`), the established `semantic_result` is still
  recorded". The condition aligns exactly; the consequent aligns up to
  the accepted temporal weakening (see 0.8.5.2 F-20 alignment report).

## F-21 questions

- **Does Level A require a non-null, non-inconclusive result?** Yes:
  R8 (Level A + INCONCLUSIVE) is UNSAT by invariant 24; R4/R6 SAT with
  DERIVED_VALUE results.
- **Does a kernel-proof claim require a successful, relevant verification
  record and linked proof artefact?** Yes: R4 SAT (proof record PASS +
  artifact resolves); R5 UNSAT (no record); R11 UNSAT (artifact does not
  resolve); R12 UNSAT (record result is FAIL, not PASS).
- **Does independent recomputation require explicit exact-agreement
  evidence?** Yes: R6 SAT (recompute record PASS + artifact linkage);
  R7 UNSAT (no record). PASS normatively attests exact agreement (§D.6).
- **Are SOLVER_BACKED / TEST_BACKED links sufficient for Level B?** Yes:
  R10 SAT with solver observation + passing test record (invariants 27,
  28).
- **Can fabricated/unrelated/missing/mismatched evidence satisfy the new
  invariants?** No: R5 (missing), R11 (mismatched/unresolved), R12
  (FAIL result) are all UNSAT. "Unrelated" evidence (e.g., a proof record
  for a recompute claim) does not satisfy the source_item-specific
  existentials.
