# MSVE v0.8.7 Transfer — Report C: Formal-Model Linkage Mapping

**Model:** `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/audit_model_087.py`
**SHA-256:** `e49aee04a0c2b5ecee8d4981d0abc46b5d3b355bc9f23ed721b2eb6a7acaac56`
**Bytes:** 18391

## C1. Helper functions (verbatim)

### `is_sha256_hex` (lines 155–156)
```python
def is_sha256_hex(s):
    return And(z3.Length(s) == 64, z3.InRe(s, _hex_re))
```
where `_hex_re = z3.Star(z3.Union(z3.Range("0", "9"), z3.Range("a", "f")))`.

### `claim_key` (lines 161–170)
```python
def claim_key(R):
    # assumes R['has_semres']; returns the claim-identifying hash
    sr = R['semres']
    dv_h = SemRes.dv_hash(R['semres'])
    dv_d = SemRes.dv_der(R['semres'])
    dv_has = SemRes.dv_has(R['semres'])
    # PROVED/DISPROVED/etc. would use their hashes; modeled for DERIVED_VALUE
    return z3.If(And(SemRes.is_DERIVED_VALUE(sr), dv_has), dv_h,
           z3.If(And(SemRes.is_DERIVED_VALUE(sr), Not(dv_has)), dv_d,
                 z3.StringVal("__no_claim_key__")))
```

### `resolves_in` (lines 142–144)
```python
def resolves_in(h, slots):
    return Or(*[h == s for s in slots])
```
Evidence collections are 2-slot lists of `z3.String` per record
(`R['proof_artifacts']`, `R['derivation_records']`, `R['witnesses']`,
`R['constructed_artifacts']`).

## C2. Invariants 24–28 (verbatim excerpts)

### Invariant 24 (line ~1384 in spec; model lines ~340–342)
```python
C.append(Implies(R['assur_ach'] == AssurLevel.LEVEL_A,
    And(R['has_semres'], Not(SemRes.is_INCONCLUSIVE(R['semres'])))))
```

### Invariant 25 (model)
```python
_ck = claim_key(R)
kp_evidence = Or(*[And(v['present'],
                       v['source_item'] == StringVal('proof'),
                       v['result'] == VerifResult.VR_PASS,
                       v['method'] == StringVal('kernel-checked'),
                       v['property'] == _ck,
                       v['checker'] != StringVal(''),
                       is_sha256_hex(v['artifact']),
                       resolves_in(v['artifact'], R['proof_artifacts']))
                   for v in R['vr']])
C.append(Implies(R['bases']['KERNEL_PROOF'],
                 And(R['has_semres'], kp_evidence)))
```

### Invariant 26 (model)
```python
def _recompute_ok(v, R, _ck):
    val_hash = SemRes.dv_hash(R['semres'])
    der_hash = SemRes.dv_der(R['semres'])
    has_val = SemRes.dv_has(R['semres'])
    h = z3.String('__h26')
    art_ok = Or(And(has_val, Exists([h], And(v['artifact'] == h, h == val_hash))),
                And(Not(has_val), v['artifact'] == der_hash))
    return And(v['present'],
               v['source_item'] == StringVal('recompute'),
               v['result'] == VerifResult.VR_PASS,
               v['property'] == _ck,
               v['checker'] != StringVal(''),
               v['inputs_ref'] == R['verif_inputs_ref'],
               is_sha256_hex(v['artifact']),
               art_ok)
rc_evidence = Or(*[_recompute_ok(v, R, _ck) for v in R['vr']])
C.append(Implies(R['bases']['INDEPENDENT_RECOMPUTE'],
                 And(R['has_semres'],
                     SemRes.is_DERIVED_VALUE(R['semres']),
                     rc_evidence)))
```

### Invariant 27 (model)
```python
C.append(Implies(R['bases']['SOLVER_BACKED'], R['has_solver']))
```

### Invariant 28 (model)
```python
test_evidence = Or(*[And(v['present'],
                         Or(v['source_item'] == StringVal('test:differential'),
                            v['source_item'] == StringVal('test:property-fuzz')),
                         v['result'] == VerifResult.VR_PASS,
                         v['property'] == _ck)
                     for v in R['vr']])
C.append(Implies(R['bases']['TEST_BACKED'],
                 And(R['has_semres'], test_evidence)))
```

## C3. Claim/basis table

| Claim or basis | Normative rule | Model constraint | Evidence/test case | Fidelity status | Remaining limitation |
|---|---|---|---|---|---|
| KERNEL_PROOF substantiation | Inv 25 (§E.6a) | `kp_evidence` disjunction | S6 (SAT), S4/S5 (UNSAT) | ENFORCED for tested fields | claim_key undefined for 4 variants (R1-1); checker auth attested |
| INDEPENDENT_RECOMPUTE substantiation | Inv 26 (§E.6a) | `_recompute_ok` + DERIVED_VALUE gate | S12 (SAT), S3/S11 (UNSAT) | ENFORCED | independence attested |
| SOLVER_BACKED substantiation | Inv 27 | `has_solver` | (no direct test) | ENFORCED (presence only) | No claim linkage; provenance_ref unmodeled; wrong-claim permitted (Report B, Q-C) |
| TEST_BACKED substantiation | Inv 28 (§E.6a) | `test_evidence` disjunction | S8 (SAT), S7 (UNSAT) | ENFORCED for tested fields | inputs/spec_version unchecked |
| claim_key mapping | §E.6a | `claim_key(R)` | S4/S6/S7/S8 | ENFORCED for DERIVED_VALUE | 4 variants → `__no_claim_key__` sentinel |
| resolves_in membership | §E.6a | Slot disjunction | S10 (UNSAT wrong collection) | ENFORCED | 2 slots per collection (bounded) |
| is_sha256_hex | §E.6a | Length + regex | S9 (UNSAT malformed) | ENFORCED | — |
| Solver outcome compatibility | Inv 4/11/22 | Encoded | (no direct test) | PARTIAL | No general rule |

## C4. Approximations and omissions affecting these claims

- Verification records: 2 slots with presence flags (bounded).
- Evidence collections: 2 slots each (bounded).
- `claim_key` fallback `__no_claim_key__` for non-DERIVED_VALUE:
  the model does not distinguish "undefined" from "sentinel mismatch"
  — for the tested DERIVED_VALUE cases this is sound, but it is not a
  faithful encoding of R1-1's undefinedness.
- `provenance_ref`, `certificate_ref`, `tool`, `version`, `config`:
  not modeled.
- `spec_version` on verification records: not constrained.
- Invariants 3, 12 omitted; 20, 21, 23 weakened (per 0.8.4 scope).
