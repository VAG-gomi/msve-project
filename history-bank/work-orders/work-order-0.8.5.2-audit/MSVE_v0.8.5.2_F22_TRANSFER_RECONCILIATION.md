# MSVE v0.8.5.2 F-22 Transfer Reconciliation

**Work Order:** 0.8.5.2 · **Date:** 2026-10-09

## Finding

F-22 is **confirmed with a refinement**. The transferred
`MSVE_v0.8.5_CHECK_RECONCILIATION.md` contains the stale range
"C-02..C-32" in **one** location (line 89, the C-01 note:
"every C-02..C-32 SAT model satisfies all 26 shared constraints"),
while the Notes bullets (lines 91–94) correctly state
"C-02..C-29, C-31, C-32, C-33" and "C-30, C-34..C-46".

The 0.8.5.1 correction pass fixed the bullets but missed the C-01 note.
The check table itself (46 rows) was and remains correct.

## Byte evidence

| File | SHA-256 |
|---|---|
| 0.8.5 source `MSVE_v0.8.5_CHECK_RECONCILIATION.md` | `4ec9afa1bab137d29ee49ab7b3e446fc2955a447801aa03180cc5a265d3c3eee` |
| 0.8.5.1 transfer copy | `4ec9afa1bab137d29ee49ab7b3e446fc2955a447801aa03180cc5a265d3c3eee` (identical) |
| Corrected candidate copy (this directory) | `658d9256f40dd8adba33c7a72c4e0e19ca5e749015abf6bc8a99e2e3edaa1506` |

Occurrences of the stale string "C-02..C-32" in the corrected copy: **0**.

## Resolution

A corrected candidate copy was created at:

`~/workspace/msve-design/work-order-0.8.5.2-audit/MSVE_v0.8.5_CHECK_RECONCILIATION_CORRECTED.md`

SHA-256 `658d9256f40dd8adba33c7a72c4e0e19ca5e749015abf6bc8a99e2e3edaa1506`.

The single change: line 89 "every C-02..C-32 SAT model" →
"every C-02..C-29, C-31, C-32, C-33 SAT model". The historical 0.8.5
report and the 0.8.5.1 transfer copy are **not overwritten**.

## Answer to the completion criteria

- Is the SAT/UNSAT count table accurate in the actual transferred bytes?
  **Yes.** The 46-row table is correct in all copies: 31 SAT (C-02..C-29,
  C-31, C-32, C-33), 1 UNKNOWN (C-01), 14 UNSAT (C-30, C-34..C-46).
  Only a prose cross-reference (line 89) carried the stale range; it is
  now corrected in the candidate copy above.
