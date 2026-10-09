# Harnesses — provenance

Each file here is a **copy** of an archived driver, modified only to run
outside its original workspace. Archived originals are unchanged.

Change applied to every harness: the hardcoded absolute path
`/home/hatch/workspace/msve-design/<work-order>` was replaced with the
scratch run directory's absolute path, using a Python replacement script
that asserted the expected occurrence count before replacing. No logic,
model code, or expected outcomes were altered.

| Harness | Original | Path occurrences replaced | Harness SHA-256 (first 16) |
|---|---|---|---|
| `run_audit_0881.patched.py` | `candidate/0.8.8.1/run_audit_0881.py` | 2 | `e6f019ebaef71395…` |
| `run_audit_088.patched.py` | `…/work-order-0.8.8-candidate/run_audit_088.py` | 2 | (see runs) |
| `run_audit_087.patched.py` | `…/work-order-0.8.7-candidate/run_audit_087.py` | 2 | (see runs) |
| `run_audit_086.patched.py` | `…/work-order-0.8.6-candidate/run_audit_086.py` | 1 | (see runs) |
| `run_audit_084.patched.py` | `…/work-order-0.8.4-audit/run_audit.py` | 1 | (see runs) |
| `dump_witnesses_084.patched.py` | `…/work-order-0.8.4-audit/dump_witnesses.py` | 1 | (see runs) |
| `dump_assignment_085.patched.py` | `…/work-order-0.8.5-audit-reconciliation/dump_assignment.py` | 2 dirs | (see runs) |
| `f20_adjudication_085.patched.py` | `…/work-order-0.8.5-audit-reconciliation/f20_adjudication.py` | 2 dirs | (see runs) |
| `f21_assurance_tests_0852.patched.py` | `…/work-order-0.8.5.2-audit/f21_assurance_tests.py` | 2 dirs | (see runs) |

The `sat_models_*.json` outputs were written by the drivers into the
scratch run directories and are preserved under `runs/<era>/`.
