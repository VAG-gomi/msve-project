# MSVE v0.8.5 Transfer Manifest

**Work Order:** 0.8.5.1 · **Date:** 2026-10-09
**Purpose:** byte-identity transfer of the four 0.8.5 reconciliation
records for external review. No content was altered during transfer.

## Transferred files

| # | Source path | Transfer path | Bytes | SHA-256 (source = transfer) | Byte-identity |
|---|---|---|---|---|---|
| 1 | `work-order-0.8.5-audit-reconciliation/MSVE_v0.8.5_CHECK_RECONCILIATION.md` | `work-order-0.8.5-audit-reconciliation/transfer/MSVE_v0.8.5_CHECK_RECONCILIATION.md` | 5354 | `4ec9afa1bab137d29ee49ab7b3e446fc2955a447801aa03180cc5a265d3c3eee` | IDENTICAL |
| 2 | `work-order-0.8.5-audit-reconciliation/MSVE_v0.8.5_SATISFIABILITY_SCOPE.md` | `work-order-0.8.5-audit-reconciliation/transfer/MSVE_v0.8.5_SATISFIABILITY_SCOPE.md` | 4268 | `e13bc5b70d1a4a103a6f6d8b98137956ad6665d5f4f22dfa65a91c0a6238b336` | IDENTICAL |
| 3 | `work-order-0.8.5-audit-reconciliation/MSVE_v0.8.5_F20_ADJUDICATION.md` | `work-order-0.8.5-audit-reconciliation/transfer/MSVE_v0.8.5_F20_ADJUDICATION.md` | 4796 | `c94b8dc0b19654ae7eee7a3da0e85521a5dddfe07406929fbcb8ee5e41ff4376` | IDENTICAL |
| 4 | `work-order-0.8.5-audit-reconciliation/MSVE_v0.8.5_EVIDENCE_INDEX.md` | `work-order-0.8.5-audit-reconciliation/transfer/MSVE_v0.8.5_EVIDENCE_INDEX.md` | 3290 | `4d8df7bcc37e488cb9979b74d36a1ee0abb13f0d14a600fefb1e6e69e79a8923` | IDENTICAL |

Verification method: `sha256sum` on source and transfer copy compared
equal for all four files. Matching hashes establish that the transfer
copies are faithful reproductions; they do not independently validate
the correctness of the contents.

## Candidate specification hash used by the audit

`9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`
(`work-order-0.8.3-candidate/MSVE_DESIGN_SPEC_v0.8.md`, 83036 bytes).

## Layer distinction (do not conflate)

- **Original v0.8 design documents** (historical, immutable):
  spec SHA-256 `377e106ef2b00db648c18beeed798bcf91804f1cbe3813853a62c1385474715d`
  (`~/workspace/msve-design/MSVE_DESIGN_SPEC_v0.8.md`).
- **v0.8.3 candidate** (correction candidate, owner review pending):
  candidate spec `9f692585…7c003` (above); bundle
  `MSVE_v0.8.3_CANDIDATE_BUNDLE.zip`
  SHA-256 `1d04b8989a7c4b647dc2fdf772316220dc06649329ce0e7964bf13b62d24c850`.
- **v0.8.4 formal audit** (read-only inputs to 0.8.5):
  `~/workspace/msve-design/work-order-0.8.4-audit/` — formalizations A/B,
  reconciliation, `audit_model.py`, `run_audit.py`, consistency report,
  witness catalog, verification evidence, owner handoff.
- **v0.8.5 reconciliation records** (transferred here):
  `~/workspace/msve-design/work-order-0.8.5-audit-reconciliation/`
  — the four files above plus supporting scripts and this manifest.

## Pre-transfer corrections (disclosed, not silent)

After the 0.8.5 audit manifest (`MSVE_v0.8.5_AUDIT_MANIFEST.json`) was
written and before this transfer, two check-ID range references were
corrected in the Notes prose (the check table itself was already
correct):

- `MSVE_v0.8.5_CHECK_RECONCILIATION.md` and
  `MSVE_v0.8.5_SATISFIABILITY_SCOPE.md`: "C-02..C-32" →
  "C-02..C-29, C-31, C-32, C-33" for the expected-SAT set (C-30 is the
  X12 unsat variant).

Consequence: the current SHA-256 values of files #1 and #2 above differ
from those recorded in `MSVE_v0.8.5_AUDIT_MANIFEST.json`. The transferred
copies match the current sources exactly. The correction was disclosed
in chat before transfer; no other 0.8.5 content was changed.

## Omissions relative to the special preservation rules

The following details the reviewer may expect are **not contained** in
the four transferred files; their locations are given so the reviewer
can request them, and nothing has been inserted to fill the gaps:

1. **Full source-to-constraint mapping for the 23 invariants + 15b:**
   in `work-order-0.8.4-audit/MSVE_v0.8.4_FORMALIZATION_RECONCILIATION.md`
   (per-invariant formalizations) and `audit_model.py` (the Z3 encoding).
   The four files state the 26-constraint arithmetic (21 + 2 + 3) and the
   per-invariant encoding-status table, but not the full mapping.
2. **Per-variant rejection reasons for the 14 UNSAT countermodels:**
   in `work-order-0.8.4-audit/MSVE_v0.8.4_WITNESS_AND_COUNTERMODEL_CATALOG.md`.
   The transferred check table names each countermodel; the detailed
   reason-per-variant table is referenced, not reproduced.
3. **Raw solver log:** `work-order-0.8.5-audit-reconciliation/run_audit_raw_output.txt`
   (46 lines, one per check). The transferred files contain the derived
   table, commands, exit statuses and solver version, not the raw log.
4. **Explicit S1 model dump:** `work-order-0.8.5-audit-reconciliation/s1_assignment.json`;
   the transferred scope file contains the assignment and its
   invariant-by-invariant assessment in prose form.

No source file was missing or unreadable. No substitute was fabricated.
No original audit or design artefact was modified during this transfer.
