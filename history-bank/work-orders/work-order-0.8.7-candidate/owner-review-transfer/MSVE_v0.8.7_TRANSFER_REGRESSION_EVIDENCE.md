# MSVE v0.8.7 Transfer — Report D: Regression and Execution Evidence

**Test script:** `/home/hatch/workspace/msve-design/work-order-0.8.7-candidate/run_audit_087.py`
(SHA-256 `c343ea23022e575dfa3466db71657b5edde6541f46057b329912fd7a63f54474`;
transfer copy in `owner-review-transfer/run_audit_087.py`, byte-identical)
**Raw log:** `run_audit_087_raw.log` (1385 bytes,
SHA-256 `94816387678c057f760086df1e6e025cfac50e389fc552687602b8375c6890b3`; transfer copy byte-identical)
**SAT witnesses:** `sat_models_087.json` (SHA-256 `3e37f98f52509b9522268f316e8c57c4f527f02cc674a6e93bdb93a64b8dbf27`;
transfer copy byte-identical)

## D1. The 18 cases

| ID | Name | Expected | Actual (per raw log) | Responsible constraint |
|---|---|---|---|---|
| R1 | pkg encodable, result present | sat | sat | inv 10 |
| R2 | pkg canonicalization, result present | sat | sat | inv 10 |
| R3a | pkg encodable, result missing | unsat | unsat | inv 10 |
| R3b | pkg canonicalization, result missing | unsat | unsat | inv 10 |
| R3c | non-pkg internal error, result missing (control) | sat | sat | inv 10 (not triggered) |
| R3d | pkg with colon detail, result missing | unsat | unsat | inv 10 + base_code |
| S1 | Lvl B + KERNEL_PROOF + evidence | sat | sat | inv 25 (any level) |
| S2 | Lvl B + KERNEL_PROOF, no evidence | unsat | unsat | inv 25 |
| S3 | recompute + non-DERIVED_VALUE | unsat | unsat | inv 26 compatibility |
| S4 | proof, unrelated property | unsat | unsat | inv 25 (property) |
| S5 | proof, wrong method | unsat | unsat | inv 25 (method) |
| S6 | proof, correct linkage | sat | sat | inv 25 |
| S7 | test, unrelated property | unsat | unsat | inv 28 (property) |
| S8 | test, correct property | sat | sat | inv 28 |
| S9 | proof, malformed hash | unsat | unsat | inv 25 (is_sha256_hex) |
| S10 | proof, wrong collection | unsat | unsat | inv 25 (resolves_in) |
| S11 | recompute, empty checker | unsat | unsat | inv 26 (checker) |
| S12 | recompute, correct linkage | sat | sat | inv 26 |

**Result: 18/18 behaved as expected** (per raw log; exit status 0).

## D2. What S4, S5, S7 prove (and do not prove)

**S4 (proof, unrelated property → UNSAT):** Proves that a passing
`source_item="proof"` record with `method="kernel-checked"` and a
valid hash resolving in `proof_artifacts`, but whose `property` is
`'z'*64` (not the claim key `'a'*64`), does **not** satisfy invariant
25. Establishes: classification + valid hash are insufficient without
claim linkage. Does not test: a record with the *correct* property but
wrong *inputs* (proof records don't check inputs_ref in inv 25).

**S5 (proof, wrong method → UNSAT):** Proves that a record with correct
property and valid hash but `method="smt-solver"` (not
`"kernel-checked"`) does **not** satisfy invariant 25. Establishes:
method is enforced. Does not test: other wrong methods, or method
spoofing.

**S7 (test, unrelated property → UNSAT):** Proves that a passing
`test:differential` record with `property='q'*64` (not the claim key)
does **not** satisfy invariant 28. Establishes: test classification
alone is insufficient. Does not test: wrong inputs, wrong spec_version
(not constrained), or a test for a *related but different* claim.

## D3. SAT witness file

`sat_models_087.json` contains truncated (2000-char) Z3 model strings
for the 9 SAT cases (R1, R2, R3c, S1, S6, S8, S12 — plus R3d is UNSAT;
the file keys are the scenario names as passed to `scenario()`).
[COMMENTARY: The exact key-to-scenario mapping is the `name` argument
in `run_audit_087.py`; no separate mapping document was created. The
models are truncated and are witnesses to satisfiability, not full
assignments.]

## D4. Raw log (byte-for-byte copy in transfer dir; transcription below labeled)

[TRANSCRIPTION of `run_audit_087_raw.log` — the authoritative copy is
the file in `owner-review-transfer/`:]
```
=== MSVE 0.8.7 test run ===
timestamp: 2026-10-09T14:05:48Z
python: Python 3.12.3
z3: 5.1.0
command: python3 run_audit_087.py

PASS [R1 pkg encodable, result present] solver=sat expected=sat
PASS [R2 pkg canonicalization, result present] solver=sat expected=sat
PASS [R3a pkg encodable, result missing] solver=unsat expected=unsat
PASS [R3b pkg canonicalization, result missing] solver=unsat expected=unsat
PASS [R3c non-pkg internal error, result missing (control)] solver=sat expected=sat
PASS [R3d pkg with colon detail, result missing] solver=unsat expected=unsat
PASS [S1 Lvl B + KERNEL_PROOF + evidence] solver=sat expected=sat
PASS [S2 Lvl B + KERNEL_PROOF, no evidence] solver=unsat expected=unsat
PASS [S3 recompute + non-DERIVED_VALUE (incompatible)] solver=unsat expected=unsat
PASS [S4 proof, unrelated property] solver=unsat expected=unsat
PASS [S5 proof, wrong method] solver=unsat expected=unsat
PASS [S6 proof, correct linkage] solver=sat expected=sat
PASS [S7 test, unrelated property] solver=unsat expected=unsat
PASS [S8 test, correct property] solver=sat expected=sat
PASS [S9 proof, malformed hash] solver=unsat expected=unsat
PASS [S10 proof, wrong collection] solver=unsat expected=unsat
PASS [S11 recompute, empty checker] solver=unsat expected=unsat
PASS [S12 recompute, correct linkage] solver=sat expected=sat

18/18 0.8.7 checks behaved as expected
exit: 0
```

## D5. Execution environment (per preserved record)

- Timestamp: 2026-10-09T14:05:xxZ (per log header; exact seconds in file).
- Python 3.12.3, z3 5.1.0, timeout 30000ms per check.
- Command: `python3 run_audit_087.py` (from the candidate directory).
- Exit status: 0.
- [COMMENTARY: The environment claim rests on the log header, which was
  written by the test harness itself, not independently verified.]
