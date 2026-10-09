"""MSVE Work Order 0.8.4 — Phase C/D: Z3 consistency audit of §E.7 invariants.

Encodes the reconciled formalization (MSVE_v0.8.4_FORMALIZATION_RECONCILIATION.md)
as Z3 constraints over a symbolic ResultRecord. Invariants 3 and 12 are excluded
(unformalizable); 20/21/23 are in weakened form (logged). 15b uses the
restricted existential reading (R1).

Separations maintained:
  (1) source-spec interpretation  -> the reconciled formalization document
  (2) formal-model correctness    -> this encoding, cross-checked below
  (3) solver result               -> z3 5.1.0 SAT/UNSAT per scenario
  (4) conclusion about the spec   -> the consistency report (separate file)
"""
import json, sys
import z3
from z3 import (Datatype, Const, IntSort, StringSort, BoolSort, Function,
                ForAll, Exists, Implies, And, Or, Not, If, StringVal)

# ---------------------------------------------------------------- code lists
CODES = json.load(open('/tmp/m8test/codelists.json'))
C_ADM = CODES['is_admission_error']
C_UNS = CODES['is_unsupported_reason']
C_VAL = CODES['is_validation_error']
C_PKG = CODES['is_packaging_error']
assert len(C_ADM) == 27 and len(C_UNS) == 3 and len(C_VAL) == 12 and len(C_PKG) == 2

Str = StringSort()

def base_code(e):
    """F-01: prefix before first ': '; whole string if absent."""
    idx = z3.IndexOf(e, StringVal(": "), 0)
    return If(idx >= 0, z3.SubString(e, 0, idx), e)

def _pred(codes):
    def p(e):
        bc = base_code(e)
        return Or(*[bc == StringVal(c) for c in codes])
    return p

is_admission_error = _pred(C_ADM)
is_unsupported_reason = _pred(C_UNS)
is_validation_error = _pred(C_VAL)
is_packaging_error = _pred(C_PKG)
PACK_BASE = C_PKG  # ['output-not-encodable', 'canonicalization-failure']

# ---------------------------------------------------------------- datatypes
Admission = Datatype('Admission')
Admission.declare('ACCEPTED')
Admission.declare('INVALID_INPUT', ('adm_reason', Str))
Admission.declare('UNSUPPORTED', ('uns_reason', Str))
Admission = Admission.create()

Execution = Datatype('Execution')
Execution.declare('NOT_STARTED')
Execution.declare('RUNNING')
Execution.declare('COMPLETED')
Execution.declare('TIMEOUT')
Execution.declare('INTERRUPTED')
Execution.declare('INTERNAL_ERROR', ('exec_reason', Str))
Execution = Execution.create()

Packaging = Datatype('Packaging')
Packaging.declare('PACKAGING_OK')
Packaging.declare('PACKAGING_FAILED', ('pack_reason', Str))
Packaging = Packaging.create()

# SemanticResult: 11 alternatives; payloads simplified to (has_hash, hash, aux)
SemRes = Datatype('SemRes')
SemRes.declare('SR_NONE')  # for Option None
SemRes.declare('DERIVED_VALUE', ('dv_has', z3.BoolSort()), ('dv_hash', Str), ('dv_der', Str))
SemRes.declare('ARTIFACT_CONSTRUCTED', ('ac_has', z3.BoolSort()), ('ac_hash', Str))
SemRes.declare('NO_SOLUTION')
SemRes.declare('PROVED', ('pr_hash', Str))
SemRes.declare('DISPROVED', ('di_hash', Str))
SemRes.declare('HOLDS')
SemRes.declare('VIOLATED', ('vi_hash', Str))
SemRes.declare('UNIQUE_UNDER_PROJECTION', ('uu_proj', Str))
SemRes.declare('UNDERDETERMINED', ('un_hash', Str))
SemRes.declare('CONTRADICTION')
SemRes.declare('INCONCLUSIVE', ('in_reason', Str))
SemRes = SemRes.create()

AssurLevel = Datatype('AssurLevel')
AssurLevel.declare('LV_NONE'); AssurLevel.declare('LEVEL_A'); AssurLevel.declare('LEVEL_B')
AssurLevel = AssurLevel.create()

Basis = Datatype('Basis')
Basis.declare('KERNEL_PROOF'); Basis.declare('INDEPENDENT_RECOMPUTE')
Basis.declare('SOLVER_BACKED'); Basis.declare('TEST_BACKED')
Basis = Basis.create()

VerifResult = Datatype('VerifResult')
VerifResult.declare('VR_PASS'); VerifResult.declare('VR_FAIL'); VerifResult.declare('VR_INCONCLUSIVE')
VerifResult = VerifResult.create()

Summary = Datatype('Summary')
Summary.declare('SM_NOT_RUN'); Summary.declare('SM_PASS'); Summary.declare('SM_FAIL')
Summary.declare('SM_INCONCLUSIVE'); Summary.declare('SM_CHECKER_DIVERGENCE')
Summary = Summary.create()

# ---------------------------------------------------------------- record
def fresh_record(prefix="r"):
    """A symbolic ResultRecord. Verification records: 2 slots with presence flags."""
    R = {}
    R['admission'] = Const(prefix + '_admission', Admission)
    R['execution'] = Const(prefix + '_execution', Execution)
    R['packaging'] = Const(prefix + '_packaging', Packaging)
    R['semres'] = Const(prefix + '_semres', SemRes)
    R['has_semres'] = z3.Bool(prefix + '_has_semres')
    R['solver_outcome'] = z3.String(prefix + '_solver_outcome')  # SAT|UNSAT|UNKNOWN|''
    R['has_solver'] = z3.Bool(prefix + '_has_solver')
    R['assur_req'] = Const(prefix + '_assur_req', AssurLevel)
    R['assur_ach'] = Const(prefix + '_assur_ach', AssurLevel)
    R['assur_short'] = z3.Bool(prefix + '_assur_short')
    R['has_shortdesc'] = z3.Bool(prefix + '_has_shortdesc')
    # assurance bases as 4 booleans
    R['bases'] = {b: z3.Bool(f'{prefix}_basis_{b}') for b in
                  ['KERNEL_PROOF', 'INDEPENDENT_RECOMPUTE', 'SOLVER_BACKED', 'TEST_BACKED']}
    # verification records: 2 slots
    R['vr'] = []
    for i in range(2):
        R['vr'].append({
            'present': z3.Bool(f'{prefix}_vr{i}_present'),
            'result': Const(f'{prefix}_vr{i}_result', VerifResult),
            'required': z3.Bool(f'{prefix}_vr{i}_required'),
            'inputs_ref': z3.String(f'{prefix}_vr{i}_inputs'),
        })
    R['summary'] = Const(prefix + '_summary', Summary)
    # evidence: resolves(h, coll) uninterpreted
    R['verif_inputs_ref'] = z3.String(prefix + '_verif_inputs_ref')
    # discrepancies: 1 slot
    R['disc_present'] = z3.Bool(prefix + '_disc_present')
    R['disc_open'] = z3.Bool(prefix + '_disc_open')
    # partial results: presence flag
    R['has_partial'] = z3.Bool(prefix + '_has_partial')
    return R

resolves = Function('resolves', Str, Str, BoolSort())

def shortfall_rule(R):
    return Or(And(R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] != AssurLevel.LEVEL_A),
              And(R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LV_NONE))

def invariants(R):
    """The reconciled constraint set. Returns list of Z3 Bool exprs."""
    C = []
    adm, exe, pack = R['admission'], R['execution'], R['packaging']
    # -- Inv 1
    C.append(Implies(Or(Admission.is_INVALID_INPUT(adm), Admission.is_UNSUPPORTED(adm)),
        And(exe == Execution.NOT_STARTED,
            Not(R['has_semres']),
            R['summary'] == Summary.SM_NOT_RUN,
            And(*[Not(b) for b in R['bases'].values()]),
            R['assur_ach'] == AssurLevel.LV_NONE)))
    # -- Inv 1b (F-06)
    r_adm = z3.String('__r1b')
    C.append(ForAll([r_adm], Implies(adm == Admission.INVALID_INPUT(r_adm),
                                     is_admission_error(r_adm))))
    r_uns = z3.String('__r1u')
    C.append(ForAll([r_uns], Implies(adm == Admission.UNSUPPORTED(r_uns),
                                     is_unsupported_reason(r_uns))))
    # -- Inv 2
    C.append(Implies(Or(exe == Execution.NOT_STARTED, exe == Execution.RUNNING),
                     Not(R['has_semres'])))
    # -- Inv 3: EXCLUDED (unformalizable)
    # -- Inv 4
    C.append(Implies(R['summary'] == Summary.SM_CHECKER_DIVERGENCE,
                     And(R['disc_present'], R['disc_open'])))
    # -- Inv 5
    C.append(And((R['assur_short'] == shortfall_rule(R)),
                 Implies(R['assur_short'], R['has_shortdesc'])))
    # -- Inv 6, 7
    C.append(Implies(R['assur_ach'] == AssurLevel.LEVEL_A,
                     Or(R['bases']['KERNEL_PROOF'], R['bases']['INDEPENDENT_RECOMPUTE'])))
    C.append(Implies(R['assur_ach'] == AssurLevel.LEVEL_B,
                     Or(*R['bases'].values())))
    # -- Inv 8 (VIOLATED)
    w = z3.String('__w8')
    C.append(ForAll([w], Implies(And(R['has_semres'], SemRes.is_VIOLATED(R['semres']),
                                     SemRes.vi_hash(R['semres']) == w),
                                resolves(w, StringVal('witnesses')))))
    # -- Inv 9 (DERIVED_VALUE derivation_ref)
    d = z3.String('__d9')
    C.append(ForAll([d], Implies(And(R['has_semres'], SemRes.is_DERIVED_VALUE(R['semres']),
                                     SemRes.dv_der(R['semres']) == d),
                                resolves(d, StringVal('derivation_records')))))
    # -- Inv 10
    s10 = z3.String('__s10')
    C.append(ForAll([s10], Implies(exe == Execution.INTERNAL_ERROR(s10),
        Implies(base_code(s10) == StringVal('output-not-encodable'), R['has_semres']))))
    # -- Inv 11
    C.append(Implies(And(R['has_solver'], R['solver_outcome'] == StringVal('UNSAT'),
                         R['assur_req'] == AssurLevel.LEVEL_A,
                         R['assur_ach'] != AssurLevel.LEVEL_A),
                     And(R['has_semres'],
                         SemRes.is_INCONCLUSIVE(R['semres']),
                         SemRes.in_reason(R['semres']) == StringVal('ASSURANCE_REQUIREMENT_UNMET'))))
    # -- Inv 12: EXCLUDED (unformalizable)
    # -- Inv 13
    C.append(Implies(R['has_partial'],
                     Or(exe == Execution.TIMEOUT, exe == Execution.INTERRUPTED)))
    # -- Inv 14
    vr_req_fail = Or(*[And(v['present'], v['result'] == VerifResult.VR_FAIL, v['required'])
                       for v in R['vr']])
    C.append(Implies(vr_req_fail,
                     Or(R['summary'] == Summary.SM_FAIL,
                        R['summary'] == Summary.SM_CHECKER_DIVERGENCE)))
    # -- Inv 15 (DERIVED_VALUE packaging)
    C.append(Implies(And(R['has_semres'], SemRes.is_DERIVED_VALUE(R['semres'])),
        And(
            Implies(pack == Packaging.PACKAGING_OK,
                    And(SemRes.dv_has(R['semres']),
                        resolves(SemRes.dv_hash(R['semres']), StringVal('constructed_artifacts')))),
            Implies(Packaging.is_PACKAGING_FAILED(pack),
                    Not(SemRes.dv_has(R['semres']))))))
    # -- Inv 15b (restricted existential reading, R1)
    p15 = z3.String('__p15'); e15 = z3.String('__e15')
    C.append(ForAll([p15], Implies(pack == Packaging.PACKAGING_FAILED(p15),
        Exists([e15], And(exe == Execution.INTERNAL_ERROR(e15),
                          base_code(e15) == base_code(p15))))))
    C.append(ForAll([e15], Implies(
        And(exe == Execution.INTERNAL_ERROR(e15),
            Or(*[base_code(e15) == StringVal(c) for c in PACK_BASE])),
        Exists([p15], And(pack == Packaging.PACKAGING_FAILED(p15),
                          base_code(p15) == base_code(e15))))))
    C.append(Implies(pack == Packaging.PACKAGING_OK,
        Not(Exists([e15], And(exe == Execution.INTERNAL_ERROR(e15),
                             Or(*[base_code(e15) == StringVal(c) for c in PACK_BASE]))))))
    # -- Inv 16 (ARTIFACT_CONSTRUCTED)
    C.append(Implies(And(R['has_semres'], SemRes.is_ARTIFACT_CONSTRUCTED(R['semres'])),
        And(
            Implies(SemRes.ac_has(R['semres']),
                    resolves(SemRes.ac_hash(R['semres']), StringVal('constructed_artifacts'))),
            (Not(SemRes.ac_has(R['semres'])) == Packaging.is_PACKAGING_FAILED(pack)))))
    # -- Inv 17, 18, 19
    h17 = z3.String('__h17')
    C.append(ForAll([h17], Implies(And(R['has_semres'], SemRes.is_PROVED(R['semres']),
                                       SemRes.pr_hash(R['semres']) == h17),
                                  resolves(h17, StringVal('proof_artifacts')))))
    h18 = z3.String('__h18')
    C.append(ForAll([h18], Implies(And(R['has_semres'], SemRes.is_DISPROVED(R['semres']),
                                       SemRes.di_hash(R['semres']) == h18),
                                  resolves(h18, StringVal('derivation_records')))))
    h19 = z3.String('__h19')
    C.append(ForAll([h19], Implies(And(R['has_semres'], SemRes.is_UNDERDETERMINED(R['semres']),
                                       SemRes.un_hash(R['semres']) == h19),
                                  resolves(h19, StringVal('witnesses')))))
    # -- Inv 20 (weakened: existential over any PASS record)
    any_pass = Or(*[And(v['present'], v['result'] == VerifResult.VR_PASS,
                        v['inputs_ref'] == R['verif_inputs_ref']) for v in R['vr']])
    C.append(Implies(And(R['has_semres'], SemRes.is_HOLDS(R['semres'])), any_pass))
    # -- Inv 21 (weakened: bare existence in derivation_records)
    C.append(Implies(And(R['has_semres'], SemRes.is_NO_SOLUTION(R['semres'])),
        Or(R['has_solver'],
           resolves(StringVal('__any_der'), StringVal('derivation_records')))))
    # -- Inv 22
    C.append(Implies(And(R['has_semres'], SemRes.is_CONTRADICTION(R['semres'])),
        Or(And(R['has_solver'], R['solver_outcome'] == StringVal('UNSAT')),
           resolves(StringVal('__any_proof'), StringVal('proof_artifacts')))))
    # -- Inv 23 (weakened: bare existence; projection linkage unformalizable)
    C.append(Implies(And(R['has_semres'], SemRes.is_UNIQUE_UNDER_PROJECTION(R['semres'])),
        Or(And(R['has_solver'], R['solver_outcome'] == StringVal('UNSAT')),
           resolves(StringVal('__any_der2'), StringVal('derivation_records')))))
    return C

def check(name, extra, expect_sat=True, timeout_ms=30000):
    R = fresh_record('r')
    s = z3.Solver()
    s.set('timeout', timeout_ms)
    for c in invariants(R):
        s.add(c)
    for c in extra(R):
        s.add(c)
    res = s.check()
    ok = (res == z3.sat) == expect_sat
    print(f"{'PASS' if ok else 'FAIL'} [{name}] solver={res} expected={'sat' if expect_sat else 'unsat'}")
    return ok, (s.model() if res == z3.sat else None), R
