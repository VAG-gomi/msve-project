# MSVE v0.8.6 Transfer — Report B: Formal Model and Source-to-Constraint Mapping

**Model file:** `~/workspace/msve-design/work-order-0.8.6-candidate/audit_model_086.py`
**SHA-256:** `99d68de70bddec92e0f45f4cee1863856a7ec7d10e6fec6868d67d472ac562de`
**Byte size:** 16341
**Derived from:** `~/workspace/msve-design/work-order-0.8.4-audit/audit_model.py`
(0.8.4 model) extended with the F-20 correction and invariants 24–28.

---

## B1. Helper functions (verbatim, lines 29–40 and 102–141)

```python
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
    # verification records: 2 slots (extended with source_item, artifact for F-21)
    R['vr'] = []
    for i in range(2):
        R['vr'].append({
            'present': z3.Bool(f'{prefix}_vr{i}_present'),
            'result': Const(f'{prefix}_vr{i}_result', VerifResult),
            'required': z3.Bool(f'{prefix}_vr{i}_required'),
            'inputs_ref': z3.String(f'{prefix}_vr{i}_inputs'),
            'source_item': z3.String(f'{prefix}_vr{i}_source_item'),
            'artifact': z3.String(f'{prefix}_vr{i}_artifact'),
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

```

---

## B2. Complete `invariants(R)` implementation (verbatim, lines 146–312)

```python
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
    # -- Inv 10 (F-20 corrected): packaging failure (either base code) preserves result
    s10 = z3.String('__s10')
    C.append(ForAll([s10], Implies(exe == Execution.INTERNAL_ERROR(s10),
        Implies(is_packaging_error(s10), R['has_semres']))))
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
    # -- Inv 24 (F-21): LEVEL_A achieved requires a non-inconclusive result
    C.append(Implies(R['assur_ach'] == AssurLevel.LEVEL_A,
        And(R['has_semres'], Not(SemRes.is_INCONCLUSIVE(R['semres'])))))
    # -- Inv 25 (F-21): KERNEL_PROOF basis requires linked proof evidence
    kp_evidence = Or(*[And(v['present'],
                           v['source_item'] == StringVal('proof'),
                           v['result'] == VerifResult.VR_PASS,
                           resolves(v['artifact'], StringVal('proof_artifacts')))
                       for v in R['vr']])
    C.append(Implies(And(R['assur_ach'] == AssurLevel.LEVEL_A,
                         R['bases']['KERNEL_PROOF']),
                     kp_evidence))
    # -- Inv 26 (F-21): INDEPENDENT_RECOMPUTE basis requires linked recompute evidence
    # (scoped to DERIVED_VALUE per §E.5; artifact = primary result hash per §E.6a)
    def _recompute_ok(v, R):
        dv = And(R['has_semres'], SemRes.is_DERIVED_VALUE(R['semres']))
        val_hash = SemRes.dv_hash(R['semres'])
        der_hash = SemRes.dv_der(R['semres'])
        has_val = SemRes.dv_has(R['semres'])
        art_ok = Or(And(has_val, v['artifact'] == val_hash),
                    And(Not(has_val), v['artifact'] == der_hash))
        return And(v['present'],
                   v['source_item'] == StringVal('recompute'),
                   v['result'] == VerifResult.VR_PASS,
                   v['inputs_ref'] == R['verif_inputs_ref'],
                   art_ok)
    rc_evidence = Or(*[_recompute_ok(v, R) for v in R['vr']])
    C.append(Implies(And(R['assur_ach'] == AssurLevel.LEVEL_A,
                         R['bases']['INDEPENDENT_RECOMPUTE'],
                         R['has_semres'],
                         SemRes.is_DERIVED_VALUE(R['semres'])),
                     rc_evidence))
    # -- Inv 27 (F-21): SOLVER_BACKED basis requires a solver observation
    C.append(Implies(And(R['assur_ach'] == AssurLevel.LEVEL_B,
                         R['bases']['SOLVER_BACKED']),
                     R['has_solver']))
    # -- Inv 28 (F-21): TEST_BACKED basis requires a passing test record
    test_evidence = Or(*[And(v['present'],
                             Or(v['source_item'] == StringVal('test:differential'),
                                v['source_item'] == StringVal('test:property-fuzz')),
                             v['result'] == VerifResult.VR_PASS)
                         for v in R['vr']])
    C.append(Implies(And(R['assur_ach'] == AssurLevel.LEVEL_B,
                         R['bases']['TEST_BACKED']),
                     test_evidence))
    return C

```

---

## B3. Source-to-constraint mapping

| Spec invariant | Z3 constraint(s) | Status |
|---|---|---|
| 1 | `Implies(Or(is_INVALID_INPUT, is_UNSUPPORTED), And(...))` | Exact |
| 1b | 2× `ForAll` over reason strings | Exact |
| 2 | `Implies(Or(NOT_STARTED, RUNNING), Not(has_semres))` | Exact |
| 3 | — | Omitted (unformalizable: external check corpus) |
| 4 | `Implies(CHECKER_DIVERGENCE, And(disc_present, disc_open))` | Exact |
| 5 | biconditional + description implication | Exact |
| 6 | `Implies(LEVEL_A, Or(KERNEL_PROOF, INDEPENDENT_RECOMPUTE))` | Exact |
| 7 | `Implies(LEVEL_B, Or(bases))` | Exact |
| 8 | `ForAll` w: VIOLATED → resolves(w, witnesses) | Exact (resolves = interpretation) |
| 9 | `ForAll` d: DERIVED_VALUE → resolves(d, derivation_records) | Exact (resolves = interpretation) |
| 10 (F-20 corrected) | `ForAll` s10: INTERNAL_ERROR(s10) → (is_packaging_error(s10) → has_semres) | Exact (corrected text) |
| 11 | UNSAT + LEVEL_A required + not achieved → INCONCLUSIVE | Exact |
| 12 | — | Omitted (unformalizable: external frozen spec) |
| 13 | `Implies(has_partial, Or(TIMEOUT, INTERRUPTED))` | Exact |
| 14 | required FAIL record → summary ∈ {FAIL, DIVERGENCE} | Exact |
| 15 | PACKAGING_OK → value Some+resolves; PACKAGING_FAILED → value None | Exact |
| 15b | 3 constraints: ⟹; restricted ⟸ (existential); PACKAGING_OK exclusion | Exact (R1 reconciled reading) |
| 16 | ARTIFACT_CONSTRUCTED → conditional + biconditional | Exact |
| 17 | `ForAll` h: PROVED → resolves(h, proof_artifacts) | Exact |
| 18 | `ForAll` h: DISPROVED → resolves(h, derivation_records) | Exact |
| 19 | `ForAll` h: UNDERDETERMINED → resolves(h, witnesses) | Exact |
| 20 | HOLDS → ∃ PASS record with matching inputs_ref | Weakened (check-property qualifier omitted) |
| 21 | NO_SOLUTION → has_solver ∨ resolves(any, derivation_records) | Weakened (search-record qualifier omitted) |
| 22 | CONTRADICTION → (solver UNSAT) ∨ resolves(any, proof_artifacts) | Exact (weakened form as specified) |
| 23 | UNIQUE_UNDER_PROJECTION → (solver UNSAT) ∨ resolves(any, derivation_records) | Weakened (projection linkage omitted) |
| 24 (F-21) | `Implies(LEVEL_A, And(has_semres, Not(is_INCONCLUSIVE)))` | Exact (new normative text) |
| 25 (F-21) | `Implies(LEVEL_A ∧ KERNEL_PROOF, ∃ vr: proof+PASS+resolves(artifact, proof_artifacts))` | Exact (new normative text; §E.6a hash rule) |
| 26 (F-21) | `Implies(LEVEL_A ∧ INDEPENDENT_RECOMPUTE ∧ DERIVED_VALUE, ∃ vr: recompute+PASS+inputs+artifact-linkage)` | Exact (new normative text; §E.6a) |
| 27 (F-21) | `Implies(LEVEL_B ∧ SOLVER_BACKED, has_solver)` | Exact (new normative text) |
| 28 (F-21) | `Implies(LEVEL_B ∧ TEST_BACKED, ∃ vr: test:+PASS)` | Exact (new normative text) |

**Count:** 21 (single) + 2 (1b) + 3 (15b) + 5 (24–28) = 31 shared constraints.
Invariants 3 and 12 are omitted (not encodable as record constraints).

---

## B4. Approximations, weakenings, and external assumptions

- `resolves(h, L)`: uninterpreted predicate; normative "resolves in" is
  interpreted as hash-membership. The spec never defines "resolves".
- `base_code`: exact F-01 definition via Z3 string theory
  (`IndexOf`/`SubString`).
- Closure predicates: explicit disjunctions over code lists extracted
  programmatically from the candidate spec (27/3/12/2).
- Invariants 20, 21, 23: weakened as in the 0.8.4 reconciliation
  (qualifiers without schema discriminators omitted).
- Verification records: 2 slots with presence flags (bounded model;
  sufficient for the tested scenarios).
- `solver_observation`: modeled as `has_solver` boolean + `solver_outcome`
  string (SAT/UNSAT/UNKNOWN).
- Checker independence (§E.6a): attested via `checker` ID, not mechanically
  derived (the record carries no primary-producer field).
