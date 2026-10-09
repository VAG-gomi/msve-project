"""Work Order 0.8.7 regression: F-22..F-27 corrections.

Retains 0.8.6 F-20 cases; adds claim-linkage countermodels (F-23),
hash/collection fidelity (F-24), unrelated-evidence tests (F-25),
and level-scope tests (F-22).
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-design/work-order-0.8.7-candidate')
from audit_model_087 import *
from audit_model_087 import (Admission, Execution, Packaging, SemRes, AssurLevel,
                             VerifResult, Summary, resolves_in, is_sha256_hex,
                             claim_key, StringVal, And, Or, Not,
                             invariants, fresh_record)
import z3

H = lambda h: StringVal(h)
results = []
models = {}  # case -> model string (for SAT cases)

def scenario(name, extra, expect_sat=True):
    R = fresh_record('r')
    s = z3.Solver(); s.set('timeout', 30000)
    for c in invariants(R): s.add(c)
    for c in extra(R): s.add(c)
    res = s.check()
    ok = (res == z3.sat) == expect_sat
    if res == z3.sat:
        m = s.model()
        # preserve key assignments
        models[name] = str(m)[:2000]
    print(f"{'PASS' if ok else 'FAIL'} [{name}] solver={res} expected={'sat' if expect_sat else 'unsat'}", flush=True)
    results.append(ok)

def base_dv(R, vh='a'*64, dh='b'*64, has_val=True):
    """Common DERIVED_VALUE setup with claim key vh."""
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'],
        R['semres'] == SemRes.DERIVED_VALUE(has_val, H(vh), H(dh)),
        resolves_in(H(dh), R['derivation_records']),
        R['derivation_records'][0] == H(dh),
        resolves_in(H(vh), R['constructed_artifacts']),
        R['constructed_artifacts'][0] == H(vh)]

# ============ F-20 retained ============
def _r1(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: Binary64 NaN')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        R['derivation_records'][0] == H('e'*64),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R1 pkg encodable, result present", _r1, True)

def _r2(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: digest mismatch')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure: blob too large')),
        R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
        R['derivation_records'][0] == H('e'*64),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R2 pkg canonicalization, result present", _r2, True)

def _r3a(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
        z3.Not(R['has_semres'])]
scenario("R3a pkg encodable, result missing", _r3a, False)

def _r3b(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: x')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure')),
        z3.Not(R['has_semres'])]
scenario("R3b pkg canonicalization, result missing", _r3b, False)

# F-20 control: non-packaging internal error, result missing -> allowed by inv 10
def _r3c(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('solver-crash: segfault')),
        R['packaging'] == Packaging.PACKAGING_OK,
        z3.Not(R['has_semres']),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
scenario("R3c non-pkg internal error, result missing (control)", _r3c, True)

# F-20: base-code suffix handling — detail with colons still packaging
def _r3d(R):
    return [R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: type: Binary64: NaN payload')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable: detail')),
        z3.Not(R['has_semres'])]
scenario("R3d pkg with colon detail, result missing", _r3d, False)

# ============ F-22: level scope ============
# Level B + KERNEL_PROOF + proper evidence -> SAT (new: substantiation at Level B)
def _s1(R):
    cs = base_dv(R)
    cs += [R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('p'*64),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("S1 Lvl B + KERNEL_PROOF + evidence", _s1, True)

# Level B + KERNEL_PROOF, no evidence -> UNSAT (F-22: must substantiate at Level B)
def _s2(R):
    cs = base_dv(R)
    cs += [R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['KERNEL_PROOF'],
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S2 Lvl B + KERNEL_PROOF, no evidence", _s2, False)

# Level A + INDEPENDENT_RECOMPUTE with non-DERIVED_VALUE -> UNSAT (incompatible)
def _s3(R):
    return [R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.PROVED(H('p'*64)),
        R['proof_artifacts'][0] == H('p'*64),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE']]
scenario("S3 recompute + non-DERIVED_VALUE (incompatible)", _s3, False)

# ============ F-23: claim linkage ============
# Level A + KERNEL_PROOF, correct label but WRONG property -> UNSAT
def _s4(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('p'*64),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['property'] == H('z'*64),  # unrelated claim
        R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S4 proof, unrelated property", _s4, False)

# Level A + KERNEL_PROOF, wrong method -> UNSAT
def _s5(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('p'*64),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('smt-solver'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['checker'] == H('z3/4.12'),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S5 proof, wrong method", _s5, False)

# Level A + KERNEL_PROOF, correct linkage -> SAT
def _s6(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('p'*64),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("S6 proof, correct linkage", _s6, True)

# TEST_BACKED with unrelated property -> UNSAT
def _s7(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['TEST_BACKED'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('test:differential'),
        R['vr'][0]['property'] == H('q'*64),  # unrelated
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS,
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S7 test, unrelated property", _s7, False)

# TEST_BACKED with correct property -> SAT
def _s8(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['TEST_BACKED'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('test:property-fuzz'),
        R['vr'][0]['property'] == H('a'*64),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("S8 test, correct property", _s8, True)

# ============ F-24: hash/collection fidelity ============
# Malformed hash (not 64 hex) -> UNSAT
def _s9(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['proof_artifacts'][0] == H('SHORT'),
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['artifact'] == H('SHORT'),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S9 proof, malformed hash", _s9, False)

# Hash resolves in WRONG collection (witnesses, not proof_artifacts) -> UNSAT
def _s10(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        R['witnesses'][0] == H('p'*64),  # wrong collection
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('proof'), R['vr'][0]['method'] == H('kernel-checked'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['artifact'] == H('p'*64),
        R['vr'][0]['checker'] == H('lean-kernel/4.9.0'),
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S10 proof, wrong collection", _s10, False)

# Recompute with empty checker -> UNSAT
def _s11(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('recompute'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['checker'] == H(''),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['vr'][0]['artifact'] == H('a'*64),
        R['summary'] == Summary.SM_PASS,
        z3.Not(R['vr'][1]['present'])]
    return cs
scenario("S11 recompute, empty checker", _s11, False)

# Recompute with correct linkage -> SAT
def _s12(R):
    cs = base_dv(R, vh='a'*64)
    cs += [R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['INDEPENDENT_RECOMPUTE'],
        R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
        R['vr'][0]['source_item'] == H('recompute'),
        R['vr'][0]['property'] == H('a'*64), R['vr'][0]['checker'] == H('recompute-checker/1.0.0'),
        R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
        R['vr'][0]['artifact'] == H('a'*64),
        R['summary'] == Summary.SM_PASS]
    return cs
scenario("S12 recompute, correct linkage", _s12, True)

print()
print(f"{sum(results)}/{len(results)} 0.8.7 checks behaved as expected")
# save models for SAT cases
import json
json.dump(models, open('/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/sat_models_087.json','w'), indent=2)
sys.exit(0 if all(results) else 1)
