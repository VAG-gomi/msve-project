# REPRODUCTION REPORT — MSVE-REPRO-001

Controlled reproduction of the 0.8.8.1 nine-check run. Scratch-only task;
the public repository was not modified.

## 1. Repository cloned

- URL: `https://github.com/VAG-gomi/msve-project`
- Commit: `3d801a9e238a1b719f45bb6f9d988f88d5ce554c`
- Branch: `main`
- Working-tree status at clone: clean (`git status --porcelain` empty)

## 2. Candidate hash verification

All four hashes calculated independently before use:

| File | Expected | Match |
|---|---|---|
| `candidate/0.8.8.1/MSVE_DESIGN_SPEC_v0.8.md` | `dbc610c3…7782` | YES |
| `candidate/0.8.8.1/audit_model_0881.py` | `fc6eb49f…31ae` | YES |
| `candidate/0.8.8.1/run_audit_0881.py` | `c750ef5c…71f83` | YES |
| `candidate/0.8.8.1/run_audit_0881_raw.log` | `525cd406…480a` | YES |

No discrepancy found; the pinned candidate was used.

## 3. Execution environment

- Python: `3.12.3` (isolated venv)
- `z3-solver` package: `5.1.0.0` (installed exactly; no substitution)
- Z3 runtime (`z3.get_version_string()`): `5.1.0`
- Matches the archived log's recorded environment (Python 3.12.3, z3 5.1.0).

## 4. Reconstructed code-list input

- Path check: `/tmp/m8test/codelists.json` did not exist; the path was clean.
  Created only by this task and removed afterward (see §11 note).
- Derivation: lists extracted mechanically (regex over backtick-quoted codes)
  from the pinned spec `dbc610c3…`: `is_admission_error` from §B.9 prose
  (between "covers exactly:" and "(27 codes.)"); `is_unsupported_reason`
  similarly (3); `is_validation_error` from the §B.13a paragraph (12);
  `is_packaging_error` from the `define is_packaging_error` disjunction
  (2), cross-checked against the model's inline comment
  `PACK_BASE = ['output-not-encodable', 'canonicalization-failure']`.
- Validation: sizes 27/3/12/2 confirmed; no duplicates in any list.
- Status: **RECONSTRUCTED — NOT THE HISTORICAL ORIGINAL.** The historical
  file's exact byte representation and hash cannot be established.

## 5. Reconstructed input identity

- SHA-256: `824853642cc0e86be970941e738d1567ea2fa55f4a2c19c97e75cd2d09034adb`
- Size: 1370 bytes

## 6. Patched driver

- The archived driver was copied, never modified. The old absolute path
  `/home/hatch/workspace/msve-design/work-order-0.8.8.1-candidate`
  occurred exactly twice (asserted); both were replaced via a Python
  replacement script with `/home/hatch/workspace/msve-repro-001/run`.
  Post-patch: old path absent, new path present exactly twice.
- Patched driver (harness) SHA-256:
  `e6f019ebaef713956098f1948101090255097be8d3236ecbd221dd0f01db9905`
  (recorded as the harness hash, not the archived driver hash)
- Copied model SHA-256: `fc6eb49f…31ae` — matches the archived model
  exactly. Model, spec, and archived log untouched.

## 7. Execution

- Command (single run, from the run directory):
  `/home/hatch/workspace/msve-repro-001/venv/bin/python run_audit_0881.py`
- stdout and stderr captured separately; exit status: **0**
- `sat_models_0881.json` produced in the run directory (7613 bytes).

## 8. Outcomes

- PASS lines: **9** (R1, C2, C3, O1, O2, O3, D4, V5, D6)
- FAIL lines: **0**
- Summary: `9/9 0.8.8.1 checks behaved as expected`
- All success conditions met in the single run.

## 9. Output comparison

- Extracted PASS/FAIL/9-9 lines from the archived raw log and from this
  run's stdout; `diff` showed **no differences** — identical outcome lines.
- The historical metadata header (timestamp, working_dir) was not compared
  as though it should match; it differs by construction.

## 10. Output hashes

- stdout: `b932cfa25944c693f59ff7d49788ceb8a7719a2c49e84bd41e2b2c6759ad96b6`
- stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)

## 11. Deviations, warnings, and unverified conditions

- None blocking. The reconstruction is not the historical original (§4).
  The driver was patched to run in the scratch directory (§6); the
  historical working directory no longer exists.
- `/tmp/m8test/codelists.json` was created solely for this run and removed
  afterward; no pre-existing material was touched.

## Conclusion (justified)

The nine expected checks were reproduced in a new run using the pinned
model bytes, a modified copy of the driver, reconstructed code lists, and
the recorded dependency environment.

Not concluded: the historical 2026-10-09T14:52:51Z event has not been
recreated; the reconstructed JSON is not the original input; the historical
log is not cryptographically bound to the candidate hashes; the checks do
not establish real-world mathematical correctness; the specification is not
fully proved; no engine is implemented; the seven unresolved claim kinds
and the UNKNOWN-policy decision are unsettled.
