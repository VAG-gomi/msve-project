# MSVE v0.8.6 Transfer Handoff (Report E, part 2)

**Work Order:** 0.8.6.1 · **Date:** 2026-10-09

## Candidate specification hash used for the audit

`13a5aced8bb77cb25394ea7ba324e5bb732fefaa9c213e797dfee48638050245`
(`work-order-0.8.6-candidate/MSVE_DESIGN_SPEC_v0.8.md`, 88466 bytes;
as recorded in `MSVE_v0.8.6_CANDIDATE_MANIFEST.json`).

## Layer distinction (preserved)

1. **Original v0.8 design documents** (historical, immutable):
   spec SHA-256 `377e106ef2b00db648c18beeed798bcf91804f1cbe3813853a62c1385474715d`.
2. **v0.8.3 correction candidate** (owner review pending):
   spec `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`;
   bundle `1d04b8989a7c4b647dc2fdf772316220dc06649329ce0e7964bf13b62d24c850`.
3. **v0.8.4 / v0.8.5 / 0.8.5.2 formal audit** (read-only inputs):
   `~/workspace/msve-design/work-order-0.8.4-audit/`,
   `.../work-order-0.8.5-audit-reconciliation/`,
   `.../work-order-0.8.5.2-audit/`.
4. **v0.8.6 correction candidate** (this transfer's subject):
   `~/workspace/msve-design/work-order-0.8.6-candidate/`.

## Missing or unavailable evidence

- **No raw solver log file** was preserved for the 0.8.6 regression run.
  Report D transcribes the observed output and states this explicitly.
  Expected path had one been saved:
  `work-order-0.8.6-candidate/run_audit_086_output.txt` (does not exist).
- **No saved model assignments** for R1–R13 (no equivalent of
  `s1_assignment.json` was produced for the 0.8.6 scenarios). Report C
  provides the complete input constraints; assignments were not
  preserved.
- The 0.8.4/0.8.5 raw log (`run_audit_raw_output.txt`) exists in the
  0.8.5 reconciliation directory and was not re-transferred here.

## Quality checks (per §7)

- ✅ All requested excerpts are verbatim (programmatic extraction; one
  spacing irregularity noted, not repaired).
- ✅ The 31-constraint model is presented as source code, not a summary
  (Report B, B2).
- ✅ Source-to-constraint map includes invariants 24–28 (Report B, B3).
- ✅ All R1–R13 cases accounted for (Report C); the R11/R12 harness fix
  is documented (Report D).
- ✅ Evidence requirements for proof, recomputation, solver, test bases
  explicit (Reports A, B, C).
- ✅ All paths and hashes refer to actual files (verified 2026-10-09).
- ✅ Transfer files created by extraction; no separate source/transfer
  divergence to check (manifest states provenance).
- ✅ No original artefact modified (candidate spec, model, and test
  script hashes verified unchanged after transfer creation).

## What could not be independently reproduced from preserved records

- The exact per-check solver timing and memory behavior (not recorded).
- The R1–R13 model assignments (not preserved as files).
- Any run beyond the single recorded 13/13 execution (tests were not
  re-run for this transfer, per the work order).
