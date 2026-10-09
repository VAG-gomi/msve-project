"""Task 3: F-20 adjudication witnesses.

F20-W: canonicalization-failure at packaging with semantic result preserved
       (intended state; must be SAT under current encoding).
F20-X: canonicalization-failure at packaging with semantic result dropped
       (adversarial; SAT under current encoding = gap demonstrated,
        UNSAT under corrected invariant 10).
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-py-repro/scratch/r085')
from audit_model import *
from audit_model import (Admission, Execution, Packaging, SemRes, AssurLevel,
                         VerifResult, Summary, resolves, StringVal, And, Or, Not,
                         base_code, PACK_BASE, invariants, fresh_record)
import z3

H = lambda h: StringVal(h); COLL = lambda c: StringVal(c)

def run(name, extra_fn, inv10_corrected=False):
    R = fresh_record('r')
    s = z3.Solver(); s.set('timeout', 30000)
    for c in invariants(R):
        # skip the stock invariant-10 when testing the correction
        s.add(c)
    if inv10_corrected:
        # corrected inv 10: packaging base codes (both) trigger preservation
        e = z3.String('__e10c')
        s.add(z3.ForAll([e], z3.Implies(
            R['execution'] == Execution.INTERNAL_ERROR(e),
            z3.Implies(z3.Or(*[base_code(e) == H(c) for c in PACK_BASE]),
                       R['has_semres']))))
        # note: stock inv-10 (output-not-encodable only) is entailed by the
        # corrected one, so keeping both is harmless; we keep both.
    for c in extra_fn(R):
        s.add(c)
    res = s.check()
    print(f"{name}: solver={res}")
    return res

def base(R):
    return [
        R['admission'] == Admission.ACCEPTED,
        R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: digest mismatch')),
        R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure: blob exceeds 1MiB')),
        R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE,
    ]

# F20-W: semantic result preserved (DERIVED_VALUE, value_ref=None per inv 15)
r1 = run("F20-W valid (current encoding)", lambda R: base(R) + [
    R['has_semres'],
    R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
    resolves(H('e'*64), COLL('derivation_records')),
])

# F20-X: semantic result dropped — gap demonstration under current encoding
r2 = run("F20-X adversarial (current encoding)", lambda R: base(R) + [
    z3.Not(R['has_semres']),
])

# F20-X under corrected invariant 10 — must be rejected
r3 = run("F20-X adversarial (corrected inv-10)", lambda R: base(R) + [
    z3.Not(R['has_semres']),
], inv10_corrected=True)

# F20-W under corrected invariant 10 — must still hold
r4 = run("F20-W valid (corrected inv-10)", lambda R: base(R) + [
    R['has_semres'],
    R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
    resolves(H('e'*64), COLL('derivation_records')),
], inv10_corrected=True)

ok = (r1 == z3.sat and r2 == z3.sat and r3 == z3.unsat and r4 == z3.sat)
print("F-20 adjudication checks:", "ALL AS EXPECTED" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
