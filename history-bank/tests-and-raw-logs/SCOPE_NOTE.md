# tests-and-raw-logs — scope note

Raw test logs, solver witnesses, and run outputs are preserved **inside
their originating work-order directories** under `../work-orders/`
(original filenames retained), not duplicated here. Key instances:

- `work-orders/work-order-0.8.8.1-candidate/run_audit_0881_raw.log` (final 9/9)
- `work-orders/work-order-0.8.8.1-candidate/sat_models_0881.json`
- `work-orders/work-order-0.8.8-candidate/run_audit_088_raw.log`
- `work-orders/work-order-0.8.7-candidate/run_audit_087_raw.log` (predates final 0.8.7 model change — see VERIFICATION_HISTORY.md)
- `work-orders/work-order-0.8.5-audit-reconciliation/run_audit_raw_output.txt`, `s1_assignment.json`
- `models-and-validators/m8/runs/` (M8 build and probe records)
- `reviews-and-audits/owner-review/logs/` (corpus and conformance logs)

See `MASTER_INVENTORY.csv` (artifact_type = raw-log / log / solver-witness)
for the full list. No test suite was re-executed during archival.
