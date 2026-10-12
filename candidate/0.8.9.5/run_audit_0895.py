"""Work Order 0.8.8.1 adversarial regression suite.

Closes: outcome compatibility (mechanical), descriptor completeness,
spec_version/input linkage. Retains 0.8.8 cases.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-wo19d/archival/candidate/0.8.9.4')
from audit_model_0895 import *
from audit_model_0895 import (Admission, Execution, Packaging, SemRes, AssurLevel,
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
        R['solver_invocations'][0][5] == H('q'*64),
        R['query_id'] == H('q'*64), R['has_query_id'],
        R['provenance_ref'] == H('inv1')]
    return cs
scenario("O1 holds+UNSAT solver-backed", _o1, True)

# 2. holds + UNKNOWN -> reject SOLVER_BACKED
def _o2(R):
    cs = base_record(R, claim='h'*64, kind='holds')
    cs += [R['has_semres'],
        R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
        R['bases']['SOLVER_BACKED'], z3.Not(R['solver_backed_weak']),
        R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
        R['solver_invocations'][0][0] == H('inv1'),
        R['solver_invocations'][0][1] == H('h'*64),
        R['solver_invocations'][0][2] == H('inputs1'),
        R['solver_invocations'][0][3] == H('holds'),
        R['solver_invocations'][0][4] == H('1.0.0'),
        R['solver_invocations'][0][5] == H('q'*64),
        R['query_id'] == H('q'*64), R['has_query_id'],
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
        R['solver_invocations'][0][5] == H('q'*64),
        R['query_id'] == H('q'*64), R['has_query_id'],
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

# ============ New 0.8.9 checks: A1/A2/D3/A4/A5/A6 ============
def base_089(R, kind='derive'):
    cs = base_record(R, kind=kind)
    cs += [R['query_language'] == H('msve-arith-v1'),
           R['identity_encoding'] == H('msve-descriptor-1'),
           R['cap_max_records'] == 10000,
           R['cap_max_descriptors'] == 1000]
    return cs

# A1: UNKNOWN + INCONCLUSIVE + weak basis is consistent (unified: SOLVER_BACKED + weak)
def _w1(R):
    cs = base_089(R, kind='prove')
    cs += [R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
           R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('solver-unknown')),
           R['bases']['SOLVER_BACKED'], R['solver_backed_weak'],
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('prove'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['query_id'] == H('q'*64), R['has_query_id'],
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1')]
    return cs
scenario("W1 weak SOLVER_BACKED on UNKNOWN+INCONCLUSIVE consistent", _w1, True)

# A1: weak basis with a positive conclusion is rejected
def _w2(R):
    cs = base_089(R, kind='holds')
    cs += [R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
           R['has_semres'], R['semres'] == SemRes.HOLDS,
           R['bases']['SOLVER_BACKED'], R['solver_backed_weak'],
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['query_id'] == H('q'*64), R['has_query_id'],
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1')]
    return cs
scenario("W2 weak basis with HOLDS rejected", _w2, False)

# A1: weak basis with UNLINKED observation (stale query_id) is rejected
def _w1b(R):
    cs = base_089(R, kind='prove')
    cs += [R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
           R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('solver-unknown')),
           R['bases']['SOLVER_BACKED'], R['solver_backed_weak'],
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('prove'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q-old'*16),
           R['query_id'] == H('q-new'*16), R['has_query_id'],
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1')]
    return cs
scenario("W1b weak basis with stale query_id rejected", _w1b, False)

# A1: weak basis with mismatched spec_version is rejected
def _w1c(R):
    cs = base_089(R, kind='prove')
    cs += [R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
           R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('solver-unknown')),
           R['bases']['SOLVER_BACKED'], R['solver_backed_weak'],
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('prove'),
           R['solver_invocations'][0][4] == H('9.9.9'),
           R['solver_invocations'][0][5] == H('q'*64),
           R['query_id'] == H('q'*64), R['has_query_id'],
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1')]
    return cs
scenario("W1c weak basis with spec_version mismatch rejected", _w1c, False)

# A2: seven kinds barred from weak basis even on UNKNOWN+INCONCLUSIVE
def _w3(R):
    cs = base_089(R, kind='contradiction')
    cs += [R['has_solver'], R['solver_outcome'] == H('UNKNOWN'),
           R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('solver-unknown')),
           R['bases']['SOLVER_BACKED'], R['solver_backed_weak'],
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('contradiction'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['query_id'] == H('q'*64), R['has_query_id'],
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1')]
    return cs
scenario("W3 D2 bar precedes D1 exception (contradiction)", _w3, False)

def _w3b(R):
    cs = base_089(R, kind='no_solution')
    cs += [R['has_solver'], R['solver_outcome'] == H('UNSAT'),
           R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('x')),
           R['bases']['SOLVER_BACKED']]
    return cs
scenario("W3b D2 bar blocks strong basis (no_solution)", _w3b, False)

# D3: solver-backed assurance requires the defined fragment
def _w4(R):
    cs = base_089(R, kind='holds')
    cs += [R['query_language'] == H('some-other-language'),
           R['has_solver'], R['solver_outcome'] == H('UNSAT'),
           R['has_semres'], R['semres'] == SemRes.HOLDS,
           R['bases']['SOLVER_BACKED']]
    # solver invocation linkage for the strong basis
    iid = R['solver_invocations'][0]
    cs += [R['provenance_ref'] == iid[0], iid[1] == R['claim_id'],
           iid[2] == R['verif_inputs_ref'], iid[3] == R['claim_kind'],
           iid[4] == R['spec_version'], iid[5] == R['query_id'],
           R['has_query_id']]
    return cs
scenario("W4 undefined query language blocks SOLVER_BACKED", _w4, False)

# A4: recompute without independent checker / checkable witness rejected
def _w5(R):
    cs = base_089(R, kind='derive')
    cs += [R['has_semres'],
           R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
           R['derivation_records'][0] == H('d'*64),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
           R['vr'][0]['source_item'] == H('recompute'),
           R['vr'][0]['claim_id'] == R['claim_id'],
           R['vr'][0]['spec_version'] == R['spec_version'],
           R['vr'][0]['checker'] == H('wrapper/1.0'),
           R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
           R['vr'][0]['artifact'] == H('ab'*32),
           R['vr'][0]['checker_independent'] == z3.BoolVal(False),
           z3.Not(R['vr'][1]['present']),
           z3.Not(R['sat_corr'][0]['present']),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("W5 recompute without independent checker rejected", _w5, False)

# Finding 3: witness scoped to SAT corroboration, not derived-value recompute
def _c3a(R):
    # derived-value path (sat_corroboration=False): no witness required
    cs = base_089(R, kind='derive')
    cs += [R['has_semres'],
           R['semres'] == SemRes.DERIVED_VALUE(True, H('ab'*32), H('d'*64)),
           R['derivation_records'][0] == H('d'*64),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
           R['vr'][0]['source_item'] == H('recompute'),
           R['vr'][0]['claim_id'] == R['claim_id'],
           R['vr'][0]['spec_version'] == R['spec_version'],
           R['vr'][0]['checker'] == H('checker/1.0'),
           R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
           R['vr'][0]['artifact'] == H('ab'*32),
           R['vr'][0]['checker_independent'] == z3.BoolVal(True),
           z3.Not(R['vr'][1]['present']),
           z3.Not(R['sat_corr'][0]['present']),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3a derived-value recompute needs no witness", _c3a, True)

def _c3b(R):
    # SAT corroboration with a fully bound witness record -> accepted
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 100,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('cd'*32),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 100,
           sc['witness_artifact'] == H('cd'*32),
           sc['witness_checked_against'] == H('q'*64),
           sc['witness_checked_by'] == H('checker-B/2.0'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3b SAT corroboration with bound witness accepted", _c3b, True)

def _c3c(R):
    # SAT corroboration with UNBOUND witness (checked against different query) -> rejected
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 100,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('cd'*32),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 100,
           sc['witness_artifact'] == H('cd'*32),
           sc['witness_checked_against'] == H('q-OTHER'*10),  # wrong query
           sc['witness_checked_by'] == H('checker-B/2.0'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3c SAT corroboration with unbound witness rejected", _c3c, False)

def _c3d(R):
    # SAT corroboration with mismatched configured bound context -> rejected
    # (witness bound to a different query than the result's)
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 100,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('cd'*32),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 100,
           sc['witness_artifact'] == H('cd'*32),
           sc['witness_checked_against'] == H('q'*64),
           sc['witness_checked_by'] == H('WRONG-CHECKER'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3d witness checked by wrong component rejected", _c3d, False)

def _c3e(R):
    # 0.8.9.4: solver timeout (100) vs Core B enumeration bound (50) are
    # DIFFERENT quantities and are NOT equated. This scenario is ACCEPTED.
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 100,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('cd'*32),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 50,
           sc['witness_artifact'] == H('cd'*32),
           sc['witness_checked_against'] == H('q'*64),
           sc['witness_checked_by'] == H('checker-B/2.0'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3e timeout vs enumeration bound not equated (accepted)", _c3e, True)

def _c3f(R):
    # SAT corroboration with witness NOT in evidence -> rejected
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 100,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('ab'*32),
           R['witnesses'][1] == H('ef'*32),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 100,
           sc['witness_artifact'] == H('cd'*32),
           sc['witness_checked_against'] == H('q'*64),
           sc['witness_checked_by'] == H('checker-B/2.0'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3f SAT corroboration with unresolvable witness rejected", _c3f, False)

def _c3g(R):
    # SAT corroboration with MALFORMED witness hash -> rejected
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 100,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('not-a-hash'),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 100,
           sc['witness_artifact'] == H('not-a-hash'),
           sc['witness_checked_against'] == H('q'*64),
           sc['witness_checked_by'] == H('checker-B/2.0'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3g SAT corroboration with malformed witness hash rejected", _c3g, False)

def _c3h(R):
    # SAT corroboration with WRONG invocation spec_version -> rejected
    cs = base_089(R, kind='holds')
    sc = R['sat_corr'][0]
    cs += [R['has_semres'], R['semres'] == SemRes.VIOLATED(H('cd'*32)),
           R['bases']['INDEPENDENT_RECOMPUTE'],
           R['has_solver'], R['solver_outcome'] == H('SAT'),
           R['has_query_id'], R['query_id'] == H('q'*64),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][1] == R['claim_id'],
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == H('9.9.9'),
           R['solver_invocations'][0][5] == H('q'*64),
           R['solver_invocations'][0][6] == 5000,
           R['solver_invocations'][1][0] != H('inv1'),
           R['provenance_ref'] == H('inv1'),
           R['witnesses'][0] == H('cd'*32),
           sc['present'],
           sc['claim_id'] == R['claim_id'],
           sc['query_id'] == H('q'*64),
           sc['spec_version'] == R['spec_version'],
           sc['checker'] == H('checker-B/2.0'),
           sc['checker_version'] == H('2.0'),
           sc['checker_independent'] == z3.BoolVal(True),
           sc['configured_bound'] == 50,
           sc['witness_artifact'] == H('cd'*32),
           sc['witness_checked_against'] == H('q'*64),
           sc['witness_checked_by'] == H('checker-B/2.0'),
           sc['witness_validation'] == H('PASS'),
           z3.Not(R['sat_corr'][1]['present'])]
    return cs
scenario("C3h invocation spec_version mismatch rejected", _c3h, False)

# A5: capacity out of range is unsatisfiable as a configuration
def _w6(R):
    cs = base_089(R, kind='derive')
    cs += [R['cap_max_records'] == 2000000]  # above permitted maximum
    return cs
scenario("W6 capacity above maximum rejected", _w6, False)

# A6: wrong identity encoding version rejected when claim_id present
def _w7(R):
    cs = base_record(R, kind='derive')
    cs += [R['identity_encoding'] == H('msve-descriptor-0')]
    return cs
scenario("W7 wrong identity encoding version rejected", _w7, False)

print()
print(f"{sum(results)}/{len(results)} total checks behaved as expected")

# ============ New 0.8.9.1 checks: WO-1.9A findings ============
# C1: all 30 admission codes accepted by the predicate; unknown rejected
def _c1(R):
    return []
def _c1_check():
    import json as _json
    codes = _json.load(open('/tmp/m8test/codelists.json'))['is_admission_error']
    assert len(codes) == 29, f"expected 29 codes, got {len(codes)}"
    s = z3.Solver()
    # every declared code satisfies the predicate
    for c in codes:
        s.push()
        s.add(is_admission_error(H(c)))
        assert s.check() == z3.sat, f"code rejected: {c}"
        s.pop()
    # unknown codes are rejected
    for bad in ["capacity-out-of-bounds", "not-a-code", "CAPACITY-OUT-OF-RANGE"]:
        s.push()
        s.add(is_admission_error(H(bad)))
        assert s.check() == z3.unsat, f"unknown code accepted: {bad}"
        s.pop()
    # the three A5 codes specifically
    for c in ["capacity-out-of-range", "capacity-not-an-object", "capacity-missing-key"]:
        assert c in codes, f"A5 code missing: {c}"
    print("PASS [C1 admission predicate: 29/29 accepted, unknown rejected]")
    return True
results.append(_c1_check())

# C2: query-identity binding (Finding 2)
def _c2_base(R, inv_claim=None, inv_query=None):
    cs = base_089(R, kind='holds')
    cs += [R['has_semres'], R['semres'] == SemRes.HOLDS,
           R['bases']['SOLVER_BACKED'],
           R['has_solver'], R['solver_outcome'] == H('UNSAT'),
           R['solver_invocations'][0][0] == H('inv1'),
           R['solver_invocations'][0][2] == R['verif_inputs_ref'],
           R['solver_invocations'][0][3] == H('holds'),
           R['solver_invocations'][0][4] == R['spec_version'],
           R['provenance_ref'] == H('inv1')]
    # invocation claim_id / query_id: default to matching, overridable
    cs += [R['solver_invocations'][0][1] == (H(inv_claim) if inv_claim else R['claim_id'])]
    cs += [R['solver_invocations'][0][5] == (H(inv_query) if inv_query else R['query_id'])]
    cs += [R['has_query_id']]
    # second slot cannot satisfy the linkage (provenance_ref is fixed to inv1)
    cs += [R['solver_invocations'][1][0] != H('inv1')]
    return cs

def _c2a(R):
    # stale query_id: result's query_id != invocation's -> rejected
    cs = _c2_base(R, inv_query='q-old'*16)
    cs += [R['query_id'] == H('q-new'*16)]
    return cs
scenario("C2a stale query_id blocks SOLVER_BACKED", _c2a, False)

def _c2b(R):
    # invocation's claim_id != result's -> rejected
    cs = _c2_base(R, inv_claim='other'*16, inv_query='q'*64)
    cs += [R['query_id'] == H('q'*64)]
    return cs
scenario("C2b invocation claim_id mismatch blocks SOLVER_BACKED", _c2b, False)

def _c2c(R):
    # correctly linked -> accepted
    cs = _c2_base(R, inv_query='q'*64)
    cs += [R['query_id'] == H('q'*64)]
    return cs
scenario("C2c correctly linked observation accepted", _c2c, True)

print()
print(f"{sum(results)}/{len(results)} total checks behaved as expected")
import json
json.dump(models, open('/home/hatch/workspace/msve-wo19d/archival/candidate/0.8.9.4/sat_models_0894.json','w'), indent=2)
sys.exit(0 if all(results) else 1)
