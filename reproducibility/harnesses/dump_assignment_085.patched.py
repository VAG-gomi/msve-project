"""Task 2: dump an explicit satisfying assignment for the shared constraints (S1)."""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-py-repro/scratch/r085')
from audit_model import *
from audit_model import (Admission, Execution, Packaging, SemRes, AssurLevel,
                         VerifResult, Summary, resolves, StringVal, And, Or, Not)
import z3, json

R = fresh_record('r')
s = z3.Solver(); s.set('timeout', 30000)
inv = invariants(R)
for c in inv: s.add(c)
H = lambda h: StringVal(h); COLL = lambda c: StringVal(c)
for c in [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
    resolves(H('b'*64), COLL('derivation_records')),
    resolves(H('a'*64), COLL('constructed_artifacts')),
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
    R['bases']['KERNEL_PROOF'],
]: s.add(c)
assert s.check() == z3.sat
m = s.model()
print(f"num_invariant_constraints={len(inv)}")
out = {}
def ev(x):
    return m.eval(x, model_completion=True).sexpr()
for k in ['admission','execution','packaging','has_semres','semres','solver_outcome',
          'has_solver','assur_req','assur_ach','assur_short','has_shortdesc',
          'summary','verif_inputs_ref','disc_present','disc_open','has_partial']:
    out[k] = ev(R[k])
out['bases'] = {k: ev(v) for k, v in R['bases'].items()}
out['vr'] = [{kk: ev(v[kk]) for kk in ('present','result','required','inputs_ref')} for v in R['vr']]
# sample resolves facts
for h, c in [('a'*64,'constructed_artifacts'),('b'*64,'derivation_records'),
             ('x'*64,'witnesses')]:
    out[f'resolves({h[:8]}..,{c})'] = ev(resolves(H(h), COLL(c)))
json.dump(out, open('/home/hatch/workspace/msve-py-repro/scratch/r085/s1_assignment.json','w'), indent=1)
print(json.dumps(out, indent=1)[:3000])
