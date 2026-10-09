# decisions-and-repairs — scope note

Owner decisions and repair records are preserved **inside their work-order
directories** under `../work-orders/`, not duplicated here. Key instances:

- `work-orders/work-order-0.8.7.2-review/` — the read-only owner decision
  packet (Option A recommendation; claim-identity and solver-linkage options)
- `work-orders/work-order-0.8.8-candidate/MSVE_v0.8.8_DISPOSITION_TABLE.md`
- `work-orders/work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_DISPOSITION_TABLE.md`
- `work-orders/work-order-0.8.3-candidate/MSVE_v0.8.3_CORRECTION_REPORT.md`
- `work-orders/work-order-0.8.6-candidate/MSVE_v0.8.6_CORRECTION_REPORT.md`

Open decisions (UNKNOWN policy, seven claim kinds, approval boundary) are
recorded at the repository root in `OPEN_DECISIONS.md`. No decision recorded
here has been resolved by archival.
