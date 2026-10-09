"""Work Order 0.8.8.1 adversarial regression suite.

Closes: outcome compatibility (mechanical), descriptor completeness,
spec_version/input linkage. Retains 0.8.8 cases.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-design/work-order-0.8.8.1-candidate')
from audit_model_0881 import *
from audit_model_0881 import (Admission, Execution, Packaging, SemRes, AssurLevel,
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

def base_record(R, claim='c'*64, kind='derive', specver='1.0.0'):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_claim_id'], R['claim_id'] == H(claim),
        R['claim_kind'] == H(kind), R['spec_version'] == H(specver),
        R['claim_descriptors'][0]['claim_id'] == H(claim),
        R['claim_descriptors'][0]['claim_kind'] == H(kind),
        R['claim_descriptors'][0]['has_proposition'],
        R['claim_descriptors'][0]['has_goal_ref'],
        R['claim_descriptors'][0]['has_inputs_ref'],
        R['claim_descriptors'][0]['has_spec_version'],
        R['claim_descriptors'][0]['spec_version'] == H(specver),
        R['verif_inputs_ref'] == H('inputs1')]

def vr_spec(R, idx, specver='1.0.0'):
    return [R['vr'][idx]['spec_version'] == H(specver)]

# ============ Retained 0.8.8 cases (updated) ============
def _r1(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: NaN')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        R['has_semres'], R['has_claim_id'], R['claim_id'] == H('c'*64),
        R['claim_kind'] == H('derive'), R['spec_version'] == H('1.0.0'),
        R['claim_descriptors'][0]['claim_id'] == H('c'*64),
        R['claim_descriptors'][0]['claim_kind'] == H('derive'),
        R['claim_descriptors'][0]['has_proposition'],
        R['claim_descriptors'][0]['has_goal_ref'],
        R['claim_descriptors'][0]['has_inputs_ref'],
        R['claim_descriptors'][0]['has_spec_version'],
        R['claim_descriptors'][0]['spec_version'] == H('1.0.0'),
        R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        R['derivation_records'][0] == H('e'*64),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R1 pkg encodable, result present", _r1, True)

def _c2(R):
    cs = base_record(R, claim='c1'*32, kind='derive')
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['constructed_artifacts'][0] == H('ab'*32),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['claim_id'] == H('c1'*32),
        R['vr'][0]['spec_version'] == H('1.0.0'),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        R['vr'][0]['artifact'] == H('cd'*32),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("C2 proof, correct claim_id", _c2, True)

def _c3(R):
    cs = base_record(R, claim='h'*64, kind='holds')
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['TEST_BACKED'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('test:property-fuzz'),
        R['vr'][0]['claim_id'] == H('h'*64),
        R['vr'][0]['spec_version'] == H('1.0.0'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("C3 HOLDS + TEST_BACKED", _c3, True)

# ============ New 0.8.8.1 cases ============
# 1. holds + UNSAT -> SOLVER_BACKED OK
def _o1(R):
    cs = base_record(R, claim='h'*64, kind='holds')
    cs += [R['has_semres'], R['semres'] == SemRes.HOLDS,
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('h'*64),
        R['solver_invocations'][0][2] == H('inputs1'),
        R['solver_invocations'][0][3] == H('holds'),
        R['solver_invocations'][0][4] == H('1.0.0'),
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("O1 holds+UNSAT solver-backed", _o1, True)

# 2. holds + UNKNOWN -> reject SOLVER_BACKED
def _o2(R):
    cs = base_record(R, claim='h'*64, kind='holds')
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('h'*64),
        R['solver_invocations'][0][2] == H('inputs1'),
        R['solver_invocations'][0][3] == H('holds'),
        R['solver_invocations'][0][4] == H('1.0.0'),
        R['solver_invocations'][1][0] != H('inv1'),
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("O2 holds+UNKNOWN rejected", _o2, False)

# 3. derive + UNSAT -> reject (diagnostic only)
def _o3(R):
    cs = base_record(R, claim='d'*64, kind='derive')
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'],
        R['has_solver'], R['solver_outcome'] == H('UNSAT'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('d'*64),
        R['solver_invocations'][0][2] == H('inputs1'),
        R['solver_invocations'][0][3] == H('derive'),
        R['solver_invocations'][0][4] == H('1.0.0'),
        R['solver_invocations'][1][0] != H('inv1'),
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("O3 derive+UNSAT rejected (diagnostic)", _o3, False)

# 4. Missing descriptor field -> reject
def _d4(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_claim_id'], R['claim_id'] == H('c'*64),
        R['claim_kind'] == H('derive'), R['spec_version'] == H('1.0.0'),
        R['claim_descriptors'][0]['claim_id'] == H('c'*64),
        R['claim_descriptors'][0]['claim_kind'] == H('derive'),
        z3.Not(R['claim_descriptors'][0]['has_proposition']),  # missing!
        R['claim_descriptors'][0]['has_goal_ref'],
        R['claim_descriptors'][0]['has_inputs_ref'],
        R['claim_descriptors'][0]['has_spec_version'],
        R['claim_descriptors'][0]['spec_version'] == H('1.0.0'),
        R['claim_descriptors'][1]['claim_id'] != H('c'*64),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF']]
scenario("D4 missing descriptor field rejected", _d4, False)

# 5. spec_version mismatch on vr -> reject
def _v5(R):
    cs = base_record(R, claim='c'*64, kind='derive', specver='1.0.0')
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['claim_id'] == H('c'*64),
        R['vr'][0]['spec_version'] == H('2.0.0'),  # mismatch!
        R['vr'][0]['checker'] == H('k/1.0'),
        R['vr'][0]['artifact'] == H('cd'*32),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("V5 vr spec_version mismatch rejected", _v5, False)

# 6. derive 2+2 vs 8/2 distinct
def _d6(R):
    cs = base_record(R, claim='claim-2plus2', kind='derive')
    cs += [R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
        R['derivation_records'][0] == H('d'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('cd'*32),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['claim_id'] == H('claim-8div2'),  # different claim, same output
        R['vr'][0]['spec_version'] == H('1.0.0'),
        R['vr'][0]['checker'] == H('k/1.0'),
        R['vr'][0]['artifact'] == H('cd'*32),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("D6 2+2 vs 8/2 distinct rejected", _d6, False)

print()
print(f"{sum(results)}/{len(results)} 0.8.8.1 checks behaved as expected")
import json
json.dump(models, open('/home/hatch/workspace/msve-design/work-order-0.8.8.1-candidate/sat_models_0881.json','w'), indent=2)
sys.exit(0 if all(results) else 1)
