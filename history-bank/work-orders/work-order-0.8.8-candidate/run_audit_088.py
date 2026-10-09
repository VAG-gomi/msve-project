"""Work Order 0.8.8 adversarial regression suite.

Tests canonical claim identity (Option A), solver invocation linkage,
and all four assurance bases against claim_id.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-design/work-order-0.8.8-candidate')
from audit_model_088 import *
from audit_model_088 import (Admission, Execution, Packaging, SemRes, AssurLevel,
                             VerifResult, Summary, resolves_in, is_sha256_hex,
                             claim_descriptor_present, StringVal, And, Or, Not,
                             invariants, fresh_record)
import z3

H = lambda h: StringVal(h)
results = []
models = {}

def scenario(name, extra, expect_sat=True):
    R = fresh_record('r')
    s = z3.Solver(); s.set('timeout', 30000)
    for c in invariants(R): s.add(c)
    for c in extra(R): s.add(c)
    res = s.check()
    ok = (res == z3.sat) == expect_sat
    if res == z3.sat:
        models[name] = str(s.model())[:2000]
    print(f"{'PASS' if ok else 'FAIL'} [{name}] solver={res} expected={'sat' if expect_sat else 'unsat'}", flush=True)
    results.append(ok)

def base_record(R, claim='c'*64):
    """Basic record with claim_id and descriptor."""
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_claim_id'], R['claim_id'] == H(claim),
        R['claim_descriptors'][0] == H(claim)]

# ============ F-20 retained ============
def _r1(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: NaN')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        R['has_semres'], R['has_claim_id'], R['claim_id'] == H('c'*64),
        R['claim_descriptors'][0] == H('c'*64),
        R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        R['derivation_records'][0] == H('e'*64),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R1 pkg encodable, result present", _r1, True)

def _r3a(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        z3.Not(R['has_semres'])]
scenario("R3a pkg encodable, result missing", _r3a, False)

# ============ Claim identity ============
def _c1(R):
    cs = base_record(R, claim='c1'*32)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['constructed_artifacts'][0] == H('v'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['claim_id'] == H('c2'*32),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        R['vr'][0]['artifact'] == H('cd'*32),
        z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("C1 proof for different goal, same output", _c1, False)

def _c2(R):
    cs = base_record(R, claim='c1'*32)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['constructed_artifacts'][0] == H('v'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['claim_id'] == H('c1'*32),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        R['vr'][0]['artifact'] == H('cd'*32),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("C2 proof, correct claim_id", _c2, True)

def _c3(R):
    cs = base_record(R, claim='h'*64)
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['TEST_BACKED'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('test:property-fuzz'),
        R['vr'][0]['claim_id'] == H('h'*64),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("C3 HOLDS + TEST_BACKED, valid descriptor", _c3, True)

def _c4(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_claim_id'], R['claim_id'] == H('c'*64),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['claim_id'] == H('c'*64),
        R['vr'][0]['checker'] == H('k/1.0'),
        R['vr'][0]['artifact'] == H('cd'*32),
        R['claim_descriptors'][0] != H('c'*64),
        R['claim_descriptors'][1] != H('c'*64)]
scenario("C4 missing descriptor rejected", _c4, False)

def _c5(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        z3.Not(R['has_claim_id']),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF']]
scenario("C5 no claim_id with basis rejected", _c5, False)

# ============ Solver linkage ============
def _s6(R):
    cs = base_record(R, claim='b'*64)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('a'*64),
        R['solver_invocations'][1][0] != H('inv1'),
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("S6 UNSAT(A) + result(B) rejected", _s6, False)

def _s7(R):
    cs = base_record(R, claim='c'*64)
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('c'*64),
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("S7 solver linked, compatible", _s7, True)

def _s8(R):
    cs = base_record(R, claim='c'*64)
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['provenance_ref'] == H('nonexistent'),
        R['solver_invocations'][0][0] != H('nonexistent'),
        R['solver_invocations'][1][0] != H('nonexistent')]
    return cs
scenario("S8 missing provenance target rejected", _s8, False)

def _s9(R):
    cs = base_record(R, claim='c'*64)
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('other'*16),
        R['solver_invocations'][1][0] != H('inv1'),
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("S9 provenance for other claim rejected", _s9, False)

def _s10(R):
    cs = base_record(R, claim='c'*64)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
    return cs
scenario("S10 no basis, valid result", _s10, True)

# ============ Assurance basis linkage ============
def _b13(R):
    cs = base_record(R, claim='c1'*32)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('recompute'),
        R['vr'][0]['claim_id'] == H('zz'*32),
        R['vr'][0]['checker'] == H('rc/1.0'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['vr'][0]['artifact'] == H('ab'*32),
        z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("B13 recompute, unrelated claim", _b13, False)

def _b14(R):
    cs = base_record(R, claim='c1'*32)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('recompute'),
        R['vr'][0]['claim_id'] == H('c1'*32),
        R['vr'][0]['checker'] == H('rc/1.0'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['vr'][0]['artifact'] == H('ab'*32),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("B14 recompute, correct linkage", _b14, True)

def _b16(R):
    cs = base_record(R, claim='c'*64)
    cs += [R['verif_inputs_ref'] == H('correct-inputs')]
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['TEST_BACKED'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('test:differential'),
        R['vr'][0]['claim_id'] == H('c'*64),
        R['vr'][0]['inputs_ref'] == H('wrong-inputs'),
        z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("B16 test, mismatched inputs", _b16, False)

def _b17(R):
    cs = base_record(R, claim='c'*64)
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('smt-solver'),
        R['vr'][0]['claim_id'] == H('c'*64),
        R['vr'][0]['checker'] == H('z3/4.12'),
        R['vr'][0]['artifact'] == H('cd'*32),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("B17 proof, wrong method", _b17, False)

print()
print(f"{sum(results)}/{len(results)} 0.8.8 checks behaved as expected")
import json
json.dump(models, open('/home/hatch/workspace/msve-design/work-order-0.8.8-candidate/sat_models_088.json','w'), indent=2)
sys.exit(0 if all(results) else 1)
