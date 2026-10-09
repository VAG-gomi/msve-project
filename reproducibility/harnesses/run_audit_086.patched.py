"""Work Order 0.8.6 regression scenarios: F-20 + F-21 corrections.

Extends the 0.8.4/0.8.5 audit with the corrected invariant 10 and new
invariants 24-28. Uses audit_model_086 (extended vr slots).
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-py-repro/scratch/r086')
from audit_model_086 import *
from audit_model_086 import (Admission, Execution, Packaging, SemRes, AssurLevel,
                             VerifResult, Summary, resolves, StringVal, And, Or, Not,
                             invariants, fresh_record)
import z3

H = lambda h: StringVal(h); COLL = lambda c: StringVal(c)
results = []

def scenario(name, extra, expect_sat=True):
    R = fresh_record('r')
    s = z3.Solver(); s.set('timeout', 30000)
    for c in invariants(R): s.add(c)
    for c in extra(R): s.add(c)
    res = s.check()
    ok = (res == z3.sat) == expect_sat
    print(f"{'PASS' if ok else 'FAIL'} [{name}] solver={res} expected={'sat' if expect_sat else 'unsat'}")
    results.append(ok)

# --- 1. output-not-encodable packaging failure, result present ---
def _s1(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: Binary64 NaN')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        resolves(H('e'*64), COLL('derivation_records')),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R1 pkg-fail encodable, result present", _s1, True)

# --- 2. canonicalization-failure packaging failure, result present ---
def _s2(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: digest mismatch')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure: blob too large')),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        resolves(H('e'*64), COLL('derivation_records')),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R2 pkg-fail canonicalization, result present", _s2, True)

# --- 3a/3b. either packaging failure, result missing -> rejected ---
def _s3a(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        z3.Not(R['has_semres'])]
scenario("R3a pkg-fail encodable, result missing", _s3a, False)

def _s3b(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure')),
        z3.Not(R['has_semres'])]
scenario("R3b pkg-fail canonicalization, result missing", _s3b, False)

# --- 4. Level A + KERNEL_PROOF + valid evidence ---
def _s4(R):
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
scenario("R4 Level A + KERNEL_PROOF + evidence", _s4, True)

# --- 5. Level A + KERNEL_PROOF label, no evidence -> rejected ---
def _s5(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present'])]
scenario("R5 Level A + KERNEL_PROOF, no evidence", _s5, False)

# --- 6. Level A + INDEPENDENT_RECOMPUTE + agreement evidence ---
def _s6(R):
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
scenario("R6 Level A + RECOMPUTE + agreement", _s6, True)

# --- 7. Level A + INDEPENDENT_RECOMPUTE, no agreement -> rejected ---
def _s7(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present'])]
scenario("R7 Level A + RECOMPUTE, no agreement", _s7, False)

# --- 8. Level A achieved on INCONCLUSIVE -> rejected ---
def _s8(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        resolves(H('p'*64), COLL('proof_artifacts')),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['artifact'] == H('p'*64)]
scenario("R8 Level A on INCONCLUSIVE", _s8, False)

# --- 9. Level A required, Level B achieved, ASSURANCE_REQUIREMENT_UNMET -> representable ---
def _s9(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('ASSURANCE_REQUIREMENT_UNMET')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'], R['assur_short'], R['has_shortdesc']]
scenario("R9 shortfall Level A->B, inconclusive", _s9, True)

# --- 10. Level B + SOLVER_BACKED + TEST_BACKED linked ---
def _s10(R):
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
scenario("R10 Level B + solver/test evidence", _s10, True)

# --- 11. PASS proof record with unresolved artifact -> rejected ---
def _s11(R):
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
scenario("R11 proof record, unresolved artifact", _s11, False)

# --- 12. Level A claimed but proof record FAILs -> rejected (stronger-than-evidence) ---
def _s12(R):
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
scenario("R12 Level A claim, proof record FAIL", _s12, False)

print()
print(f"{sum(results)}/{len(results)} 0.8.6 regression checks behaved as expected")
sys.exit(0 if all(results) else 1)
