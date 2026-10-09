"""Work Order 0.8.5.2, F-21: audit the S1 assurance claim.

Five cases against the formalized constraints (audit_model.invariants).
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-design/work-order-0.8.4-audit')
from audit_model import *
from audit_model import (Admission, Execution, Packaging, SemRes, AssurLevel,
                         VerifResult, Summary, resolves, StringVal, And, Or, Not,
                         invariants, fresh_record)
import z3

H = lambda h: StringVal(h); COLL = lambda c: StringVal(c)

def base_derived(R):
    return [
        R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'],
        R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
        resolves(H('b'*64), COLL('derivation_records')),
        resolves(H('a'*64), COLL('constructed_artifacts')),
        R['assur_req'] == AssurLevel.LEVEL_A,
        R['assur_ach'] == AssurLevel.LEVEL_A,
    ]

def run(name, extra):
    R = fresh_record('r')
    s = z3.Solver(); s.set('timeout', 30000)
    for c in invariants(R): s.add(c)
    for c in extra(R): s.add(c)
    res = s.check()
    print(f"{name}: solver={res}")
    return res

# Case 1: Level A with recorded kernel-proof basis AND supporting evidence
r1 = run("F21-1 valid Level A (proof artifact + PASS record)", lambda R: base_derived(R) + [
    R['bases']['KERNEL_PROOF'],
    resolves(H('p'*64), COLL('proof_artifacts')),
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
    R['summary'] == Summary.SM_PASS,
])

# Case 2: Level A with KERNEL_PROOF basis but NO supporting evidence
r2 = run("F21-2 Level A, KERNEL_PROOF, no evidence (no proof artifact, no verif records, NOT_RUN)",
    lambda R: base_derived(R) + [
        R['bases']['KERNEL_PROOF'],
        z3.Not(resolves(H('p'*64), COLL('proof_artifacts'))),
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_NOT_RUN,
        z3.Not(R['has_solver']),
    ])

# Case 3: Level A via INDEPENDENT_RECOMPUTE with agreement evidence
r3 = run("F21-3 Level A via INDEPENDENT_RECOMPUTE (+ recompute PASS record)", lambda R: base_derived(R) + [
    R['bases']['INDEPENDENT_RECOMPUTE'],
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
    R['summary'] == Summary.SM_PASS,
])

# Case 3b: Level A via INDEPENDENT_RECOMPUTE with NO agreement evidence
r3b = run("F21-3b Level A via INDEPENDENT_RECOMPUTE, no agreement evidence", lambda R: base_derived(R) + [
    R['bases']['INDEPENDENT_RECOMPUTE'],
    z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present']),
    R['summary'] == Summary.SM_NOT_RUN,
])

# Case 4: Level A required but not achieved, shortfall recorded
r4 = run("F21-4 Level A required, LEVEL_B achieved, shortfall", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_solver'], R['solver_outcome'] == H('UNSAT'),
    R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('ASSURANCE_REQUIREMENT_UNMET')),
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_B,
    R['bases']['SOLVER_BACKED'], R['assur_short'], R['has_shortdesc'],
])

# Case 5: claimed Level A assurance on an INCONCLUSIVE result (basis/evidence conflict)
r5 = run("F21-5 LEVEL_A achieved + KERNEL_PROOF basis + INCONCLUSIVE semantic result",
    lambda R: [
        R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
        R['packaging'] == Packaging.PACKAGING_OK,
        R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')),
        R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
        R['bases']['KERNEL_PROOF'],
        z3.Not(R['vr'][0]['present']), z3.Not(R['vr'][1]['present']),
        R['summary'] == Summary.SM_NOT_RUN,
    ])

print()
print("F21-1 (valid, expect sat):", r1)
print("F21-2 (evidence-free basis, gap if sat):", r2)
print("F21-3 (recompute+agreement, expect sat):", r3)
print("F21-3b (recompute no agreement, gap if sat):", r3b)
print("F21-4 (shortfall, expect sat):", r4)
print("F21-5 (Level A on INCONCLUSIVE, gap if sat):", r5)
