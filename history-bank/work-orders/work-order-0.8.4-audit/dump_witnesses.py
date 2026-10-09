"""Dump readable witness models for the catalog."""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-design/work-order-0.8.4-audit')
from audit_model import *
from audit_model import (Admission, Execution, Packaging, SemRes, AssurLevel,
                         VerifResult, Summary, resolves, StringVal, And, Or, Not)
import z3, json

def show(name, extra):
    R = fresh_record('r')
    s = z3.Solver(); s.set('timeout', 30000)
    for c in invariants(R): s.add(c)
    for c in extra(R): s.add(c)
    assert s.check() == z3.sat, name
    m = s.model()
    def ev(x):
        v = m.eval(x, model_completion=True)
        return str(v).replace('"', '')
    out = {'scenario': name}
    out['admission'] = ev(R['admission'])
    out['execution'] = ev(R['execution'])
    out['packaging'] = ev(R['packaging'])
    out['has_semres'] = ev(R['has_semres'])
    if m.eval(R['has_semres'], model_completion=True) == z3.BoolVal(True):
        out['semantic_result'] = ev(R['semres'])
    out['assurance'] = {k: ev(R[k]) for k in ['assur_req', 'assur_ach', 'assur_short', 'has_shortdesc']}
    out['bases'] = {k: ev(v) for k, v in R['bases'].items()}
    out['summary'] = ev(R['summary'])
    out['has_partial'] = ev(R['has_partial'])
    out['has_solver'] = ev(R['has_solver'])
    if m.eval(R['has_solver'], model_completion=True) == z3.BoolVal(True):
        out['solver_outcome'] = ev(R['solver_outcome'])
    print(json.dumps(out, indent=1))
    print('---')

H = lambda h: StringVal(h)
COLL = lambda c: StringVal(c)

show("S1 derived+packaged", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
    resolves(H('b'*64), COLL('derivation_records')),
    resolves(H('a'*64), COLL('constructed_artifacts')),
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
    R['bases']['KERNEL_PROOF']])
show("S3 unencodable+15b", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: Binary64 NaN')),
    R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
    resolves(H('e'*64), COLL('derivation_records'))])
show("S5 invalid-input", lambda R: [
    R['admission'] == Admission.INVALID_INPUT(H('unbound-identifier: foo')),
    R['execution'] == Execution.NOT_STARTED, Not(R['has_semres']),
    R['summary'] == Summary.SM_NOT_RUN])
