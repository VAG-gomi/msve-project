# Runtime Report — WO-1.9

## Environment

- OS: Linux x86_64 (build VM)
- Python: 3.12.3 (isolated venv `/tmp/wo19-venv`)
- z3-solver: 5.1.0.0 (pip); Z3 runtime 5.1.0
- pytest: 9.1.1
- Working copies: `~/workspace/msve-wo19/archival` (from
  `a9902b4dc128…`), `~/workspace/msve-wo19/prototype` (from
  `a98b9a12407e…`); both trees clean at start.

## Commands and measured results

| Command | Result |
|---|---|
| `git ls-remote` (both repos) | prototype `a98b9a12407e…`, archival `a9902b4dc128…` |
| `sha256sum` spec/model/driver (0.8.8.1) | `dbc610c3a97d…`, `fc6eb49f50ea…`, `c750ef5c37a1…` (match pinned) |
| `python run_audit_0889.py` | exit 0; **17/17** behaved as expected |
| `python -m pytest tests/ -q` (prototype) | exit 0; **128 passed** in ~8.3s |
| `python experiments/unknown_d1/run_experiment.py` | exit 0; UNKNOWN/timeout → INCONCLUSIVE + weak SOLVER_BACKED |
| 16 golden vectors recompute | 16/16 match; order-independence, null-vs-empty, NFC verified |

## Notes

- The model audit required reconstructing `/tmp/m8test/codelists.json`
  from the spec's closed error lists (the M8-generated file was not
  preserved); the 0.8.9 codelists add the three `capacity-*` codes
  (27 → 30 admission codes). This reconstruction is documented, not
  hidden.
- Solver timeout for the UNKNOWN experiment: driver default; both runs
  reported `reason_unknown: timeout` (genuine, not injected).
- No failures, no skips, no errors in any run.
