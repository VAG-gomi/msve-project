"""Phase C: witnesses for the 13 intended scenarios + invalid/contradictory variants.

Each valid scenario must be SAT under the joint invariants; each invalid
variant must be UNSAT (rejected for an identifiable reason)."""
import sys
sys.path.insert(0, '/home/hatch/workspace/msve-design/work-order-0.8.4-audit')
from audit_model import *
from audit_model import (Admission, Execution, Packaging, SemRes, AssurLevel,
                         VerifResult, Summary, resolves, StringVal, And, Or, Not)
import z3

results = []

def scenario(name, extra, expect_sat=True):
    ok, model, R = check(name, extra, expect_sat)
    results.append((name, ok, expect_sat))
    return ok

def H(h): return StringVal(h)
def COLL(c): return StringVal(c)

# --- joint satisfiability of all invariants (no scenario constraints) ---
scenario("joint-SAT", lambda R: [], True)

# --- 1. Accepted execution, derived value, packaged OK ---
scenario("S1 derived+packaged", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
    resolves(H('b'*64), COLL('derivation_records')),
    resolves(H('a'*64), COLL('constructed_artifacts')),
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
    R['bases']['KERNEL_PROOF'],
])

# --- 2. Accepted execution, artifact constructed, packaged OK ---
scenario("S2 artifact+packaged", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.ARTIFACT_CONSTRUCTED(True, H('c'*64)),
    resolves(H('c'*64), COLL('constructed_artifacts')),
    R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
    R['bases']['SOLVER_BACKED'],
])

# --- 3. Valid computation, result unencodable: packaging/execution linked per 15b ---
scenario("S3 unencodable+15b", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: Binary64 NaN')),
    R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
    resolves(H('e'*64), COLL('derivation_records')),
    R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LEVEL_B,
    R['bases']['TEST_BACKED'],
])

# --- 4. Internal execution error unrelated to packaging ---
scenario("S4 internal-error", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERNAL_ERROR(H('division-by-zero')),
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('RESOURCE_EXHAUSTED')),
    R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE,
])

# --- 5. INVALID_INPUT: NOT_STARTED, no semantic result ---
scenario("S5 invalid-input", lambda R: [
    R['admission'] == Admission.INVALID_INPUT(H('unbound-identifier: foo')),
    R['execution'] == Execution.NOT_STARTED,
    Not(R['has_semres']),
    R['summary'] == Summary.SM_NOT_RUN,
    R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE,
])

# --- 6. UNSUPPORTED: NOT_STARTED, no semantic result ---
scenario("S6 unsupported", lambda R: [
    R['admission'] == Admission.UNSUPPORTED(H('goal-not-supported: liveness')),
    R['execution'] == Execution.NOT_STARTED,
    Not(R['has_semres']),
    R['summary'] == Summary.SM_NOT_RUN,
])

# --- 7. Every SemanticResult alternative with normative goal mapping ---
ALTS = [
    ("derived",      SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
     [resolves(H('b'*64), COLL('derivation_records')), resolves(H('a'*64), COLL('constructed_artifacts'))]),
    ("artifact",     SemRes.ARTIFACT_CONSTRUCTED(True, H('c'*64)),
     [resolves(H('c'*64), COLL('constructed_artifacts'))]),
    ("no_solution",  SemRes.NO_SOLUTION,
     [R['has_solver'] if False else True]),  # placeholder, replaced below
    ("proved",       SemRes.PROVED(H('f'*64)), [resolves(H('f'*64), COLL('proof_artifacts'))]),
    ("disproved",    SemRes.DISPROVED(H('g'*64)), [resolves(H('g'*64), COLL('derivation_records'))]),
    ("holds",        SemRes.HOLDS, None),  # needs a PASS verification record
    ("violated",     SemRes.VIOLATED(H('h'*64)), [resolves(H('h'*64), COLL('witnesses'))]),
    ("unique_proj",  SemRes.UNIQUE_UNDER_PROJECTION(H('proj-x')),
     [R['has_solver'] if False else True]),
    ("underdet",     SemRes.UNDERDETERMINED(H('i'*64)), [resolves(H('i'*64), COLL('witnesses'))]),
    ("contradiction",SemRes.CONTRADICTION, [R['has_solver'] if False else True]),
    ("inconclusive", SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')), []),
]
for alt_name, sem in [(a, s) for a, s, _ in ALTS]:
    def mk(alt_name=alt_name, sem=sem):
        def ex(R):
            base = [R['admission'] == Admission.ACCEPTED,
                    R['execution'] == Execution.COMPLETED,
                    R['packaging'] == Packaging.PACKAGING_OK,
                    R['has_semres'], R['semres'] == sem,
                    R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE]
            if alt_name == "no_solution":
                base += [R['has_solver'], R['solver_outcome'] == H('UNKNOWN')]
            elif alt_name == "unique_proj":
                base += [R['has_solver'], R['solver_outcome'] == H('UNSAT')]
            elif alt_name == "contradiction":
                base += [R['has_solver'], R['solver_outcome'] == H('UNSAT')]
            elif alt_name == "holds":
                base += [R['vr'][0]['present'],
                         R['vr'][0]['result'] == VerifResult.VR_PASS,
                         R['vr'][0]['inputs_ref'] == R['verif_inputs_ref']]
            elif alt_name == "inconclusive":
                base += []
            else:
                pass
            return base
        return ex
    # attach evidence extras for the simple ones
    ev = {"derived": [resolves(H('a'*64), COLL('constructed_artifacts')), resolves(H('b'*64), COLL('derivation_records'))],
          "artifact": [resolves(H('c'*64), COLL('constructed_artifacts'))],
          "proved": [resolves(H('f'*64), COLL('proof_artifacts'))],
          "disproved": [resolves(H('g'*64), COLL('derivation_records'))],
          "violated": [resolves(H('h'*64), COLL('witnesses'))],
          "underdet": [resolves(H('i'*64), COLL('witnesses'))]}.get(alt_name, [])
    base_mk = mk()
    def ex2(R, base_mk=base_mk, ev=ev):
        return base_mk(R) + ev
    scenario(f"S7 alt-{alt_name}", ex2)

# --- 8. Assurance levels: required/achieved/shortfall combinations ---
scenario("S8 levelA-no-shortfall", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
    resolves(H('a'*64), COLL('constructed_artifacts')), resolves(H('b'*64), COLL('derivation_records')),
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
    R['bases']['KERNEL_PROOF'], Not(R['assur_short']),
])
scenario("S8 levelA-shortfall", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_solver'], R['solver_outcome'] == H('UNSAT'),
    R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('ASSURANCE_REQUIREMENT_UNMET')),
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_B,
    R['bases']['SOLVER_BACKED'], R['assur_short'], R['has_shortdesc'],
])
scenario("S8 levelB-shortfall", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
    resolves(H('a'*64), COLL('constructed_artifacts')), resolves(H('b'*64), COLL('derivation_records')),
    R['assur_req'] == AssurLevel.LEVEL_B, R['assur_ach'] == AssurLevel.LV_NONE,
    R['assur_short'], R['has_shortdesc'],
])

# --- 9. PASS / FAIL / INCONCLUSIVE / CHECKER_DIVERGENCE summaries ---
scenario("S9 summary-pass", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.HOLDS,
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
    R['summary'] == Summary.SM_PASS,
])
scenario("S9 summary-fail", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.VIOLATED(H('h'*64)),
    resolves(H('h'*64), COLL('witnesses')),
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_FAIL,
    R['vr'][0]['required'], R['summary'] == Summary.SM_FAIL,
])
scenario("S9 summary-divergence", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')),
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][1]['present'], R['vr'][1]['result'] == VerifResult.VR_FAIL,
    R['vr'][1]['required'],
    R['summary'] == Summary.SM_CHECKER_DIVERGENCE,
    R['disc_present'], R['disc_open'],
])
scenario("S9 summary-inconclusive", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')),
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_INCONCLUSIVE,
    R['summary'] == Summary.SM_INCONCLUSIVE,
])

# --- 10. TIMEOUT / INTERRUPTED with labelled partial results ---
scenario("S10 timeout-partial", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.TIMEOUT,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_partial'], Not(R['has_semres']),
    R['assur_req'] == AssurLevel.LV_NONE, R['assur_ach'] == AssurLevel.LV_NONE,
])
scenario("S10 interrupted-partial", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERRUPTED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_partial'], Not(R['has_semres']),
])

# --- 11. Projection-relative uniqueness with mandatory evidence ---
scenario("S11 unique-projection", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.UNIQUE_UNDER_PROJECTION(H('proj-vars')),
    R['has_solver'], R['solver_outcome'] == H('UNSAT'),
])

# --- 12. Required evidence reference missing/mismatched ---
# valid: required evidence present and resolving
scenario("S12 evidence-present", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.PROVED(H('f'*64)),
    resolves(H('f'*64), COLL('proof_artifacts')),
])
# invalid: required evidence reference does NOT resolve -> must be rejected
scenario("X12 evidence-missing", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.PROVED(H('f'*64)),
    Not(resolves(H('f'*64), COLL('proof_artifacts'))),
], expect_sat=False)

# --- 13. Detailed error codes under F-01 suffix rules ---
scenario("S13 detailed-admission", lambda R: [
    R['admission'] == Admission.INVALID_INPUT(H('syntax-error: line 3: unexpected "}"')),
    R['execution'] == Execution.NOT_STARTED, Not(R['has_semres']),
])
scenario("S13 detailed-unsupported", lambda R: [
    R['admission'] == Admission.UNSUPPORTED(H('scope-not-supported: higher-order unification')),
    R['execution'] == Execution.NOT_STARTED, Not(R['has_semres']),
])
scenario("S13 detailed-packaging", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERNAL_ERROR(H('canonicalization-failure: blob exceeds 1MiB')),
    R['packaging'] == Packaging.PACKAGING_FAILED(H('canonicalization-failure: digest mismatch')),
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('d'*64), H('e'*64)),
    resolves(H('e'*64), COLL('derivation_records')),
])
# invalid: detail suffix on a non-code must be rejected
scenario("X13 invalid-code", lambda R: [
    R['admission'] == Admission.INVALID_INPUT(H('not-a-real-code: foo')),
    R['execution'] == Execution.NOT_STARTED,
], expect_sat=False)
scenario("X13 colon-no-space", lambda R: [
    # 'syntax-error:foo' has no ': ' so base_code is the whole string -> not a code
    R['admission'] == Admission.INVALID_INPUT(H('syntax-error:foo')),
    R['execution'] == Execution.NOT_STARTED,
], expect_sat=False)

# ================= invalid / contradictory variants =================
scenario("X packaging-failed+completed", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
], expect_sat=False)

scenario("X packaging-ok+encodable-error", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable: x')),
    R['packaging'] == Packaging.PACKAGING_OK,
], expect_sat=False)

scenario("X invalid-input+semres", lambda R: [
    R['admission'] == Admission.INVALID_INPUT(H('syntax-error')),
    R['execution'] == Execution.NOT_STARTED,
    R['has_semres'],
], expect_sat=False)

scenario("X levelA-without-basis", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.HOLDS,
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
    Not(R['bases']['KERNEL_PROOF']), Not(R['bases']['INDEPENDENT_RECOMPUTE']),
    R['bases']['SOLVER_BACKED'],
], expect_sat=False)

scenario("X shortfall-inconsistent", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.HOLDS,
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][0]['inputs_ref'] == R['verif_inputs_ref'],
    R['assur_req'] == AssurLevel.LEVEL_A, R['assur_ach'] == AssurLevel.LEVEL_A,
    R['bases']['KERNEL_PROOF'], R['assur_short'],
], expect_sat=False)

scenario("X unique-no-evidence", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.UNIQUE_UNDER_PROJECTION(H('p')),
    Not(R['has_solver']),
    Not(resolves(H('__any_der2'), COLL('derivation_records'))),
], expect_sat=False)

scenario("X required-fail+pass-summary", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.INCONCLUSIVE(H('SOLVER_UNKNOWN')),
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_FAIL,
    R['vr'][0]['required'],
    R['summary'] == Summary.SM_PASS,
], expect_sat=False)

scenario("X partial+completed", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['has_partial'],
], expect_sat=False)

scenario("X derived-ok+value-missing", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(False, H('a'*64), H('b'*64)),
    resolves(H('b'*64), COLL('derivation_records')),
], expect_sat=False)

scenario("X derived-failed+value-present", lambda R: [
    R['admission'] == Admission.ACCEPTED,
    R['execution'] == Execution.INTERNAL_ERROR(H('output-not-encodable')),
    R['packaging'] == Packaging.PACKAGING_FAILED(H('output-not-encodable')),
    R['has_semres'], R['semres'] == SemRes.DERIVED_VALUE(True, H('a'*64), H('b'*64)),
    resolves(H('b'*64), COLL('derivation_records')),
], expect_sat=False)

scenario("X verif-input-mismatch", lambda R: [
    R['admission'] == Admission.ACCEPTED, R['execution'] == Execution.COMPLETED,
    R['packaging'] == Packaging.PACKAGING_OK,
    R['has_semres'], R['semres'] == SemRes.HOLDS,
    R['vr'][0]['present'], R['vr'][0]['result'] == VerifResult.VR_PASS,
    R['vr'][0]['inputs_ref'] != R['verif_inputs_ref'],
    Not(Or(*[And(v['present'], v['result'] == VerifResult.VR_PASS,
                 v['inputs_ref'] == R['verif_inputs_ref']) for v in R['vr']])),
], expect_sat=False)

print()
n_ok = sum(1 for _, ok, _ in results if ok)
print(f"{n_ok}/{len(results)} scenario checks behaved as expected")
sys.exit(0 if n_ok == len(results) else 1)
