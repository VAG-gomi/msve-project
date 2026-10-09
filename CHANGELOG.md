# CHANGELOG.md

## 2026-10-09 — Repository established (work order MSVE-REPO-001)

- Created private repository `msve-project` under account VAG-gomi.
- Initial commit: archived candidate 0.8.8.1 artifacts (spec, model, test
  script, raw log — all hashes independently recalculated and verified
  against the workspace sources; byte-identical, no discrepancies).
- Archived the eight continuity-export-01 Markdown files byte-identical.
- Added project state records: README, PROJECT_STATE, ARTIFACT_REGISTER,
  OPEN_DECISIONS, KNOWN_LIMITATIONS, CHANGELOG.
- Recorded project status as CORRECTION CANDIDATE PREPARED — OWNER REVIEW
  REQUIRED. No design freeze, baseline acceptance, engine implementation,
  or experiment authorised.
- No candidate files were modified. No historical records were rewritten.

Future entries must be dated, truthful, and must not backdate verification
or imply historical checks that did not occur.

## 2026-10-09 — History bank added (work order MSVE-HISTORY-001)

- Added `history-bank/`: 391 original artifacts preserved byte-identical from
  `~/workspace/msve-design/` (all versioned specs/plans/matrices/reviews
  v0.1–v0.8, 9 work-order directories, M8 tool, check scripts, owner-review
  evidence, transfer package, 2 ZIP bundles). Zero copy mismatches.
- Added 7 navigational indexes (inventory CSV with 409 rows, timeline,
  provenance register, version lineage, verification history, gaps register,
  bank README). Indexes are reconstructions, labelled as such.
- Verified no other MSVE repositories exist on the account and no other
  MSVE workspace directories exist. No git history predated the bank.
- Visibility corrected to Private per the work order (was briefly Public on
  an earlier instruction; no sensitive material was found in a pre-change
  scan).
- Original 18-file archive untouched; initial commit `b890636e` preserved.
  No design freeze, baseline approval, implementation, or experiment.

## 2026-10-09 — Completeness audit (work order MSVE-HISTORY-CHECK-001)

- Verified remote state by git protocol: HEAD `e01d2ee` on remote main,
  parent `b890636e` intact, 421 tracked files, visibility PUBLIC per
  standing owner instruction. Root-view vs history-bank discrepancy
  investigated: no data-level discrepancy found; attributed to stale
  web-UI rendering.
- Re-audited the full source universe: all 399 workspace files confirmed
  present; no other MSVE repos, workspaces, git histories, or bundles found.
- One genuine omission preserved: the dated project log
  (`history-bank/source-records/dated-project-log-2026-10-09.md`,
  byte-identical, sensitivity-scanned clean) with provenance note.
- Same-name/different-content analysis: 13 filename groups, all distinct
  versions preserved with distinct paths (e.g. 6 versions of the v0.8 spec).
- Repaired root README to link the history bank. Inventory now 411 rows.
- Four candidate hashes recalculated: all match. No freeze, baseline,
  implementation, or experiment.

## 2026-10-09 — Repository audit (work order MSVE-REPO-AUDIT-002)

- Verified git state by protocol: remote HEAD `604db7e`, parent chain
  intact, 424 tracked files (3,963,072 bytes), visibility PUBLIC.
- Created `history-bank/REPOSITORY_MANIFEST.csv` (427 rows, mechanical:
  path, size, SHA-256, format, category, role for every tracked file).
- Created `history-bank/SOURCE_READER_GUIDE.csv` (86 evidence-grounded
  rows from three independent content inspections).
- Created `history-bank/REPOSITORY_AUDIT_REPORT.md` (this audit's findings).
- Corrected `history-bank/source-snapshots/ZIP_CONTENTS.md` (was truncated;
  now 226 complete entries). Verified (not added) the history-bank link in
  root README — git history proves it was added in `604db7e`
  (HISTORY-CHECK-001).
- 404/404 source-to-archive comparisons match. Four candidate hashes match.
- Cold-start Test C: 10/10 claims traceable via repo navigation. Tests A/B
  not performed (no isolated session available).
- No candidate, historical, or raw-log file modified.

## 2026-10-09 — Audit report bookkeeping correction (external review)

- Corrected `history-bank/REPOSITORY_AUDIT_REPORT.md`: the final commit SHA
  was misreported as `968e7882…` (a pre-amend value); the actual final
  commit is `d83c9dea70a814ed72dd8bf21a30a60ec980074a`.
- Corrected file/byte totals: 427 files, 4,091,804 bytes measured at the
  final commit `d83c9de` (the earlier 424 / 3,963,072 figures were measured
  at the pre-audit commit `604db7e`). Manifest rows (427) now reconcile
  with tracked files (427).
- No other content changed.

## 2026-10-09 — Record reconciliation (work order MSVE-RECONCILIATION-003)

- Corrected `history-bank/REPOSITORY_AUDIT_REPORT.md` and this CHANGELOG:
  the history-bank link in root README was added in `604db7e`
  (HISTORY-CHECK-001, "link history bank"), not by REPO-AUDIT-002.
  Git history (`git log -S "history-bank/" -- README.md`) proves it.
- Reconciled all commit/file/byte references: `604db7e` = 424 files /
  3,963,072 bytes; `d83c9de` = 427 / 4,091,804; `93b6117` = 427 /
  4,093,379; this tree = 427 / 4,094,099.
- Regenerated `history-bank/REPOSITORY_MANIFEST.csv` (427 rows) to match
  the corrected tree. Manifest self-hash remains the documented exception.
- No candidate, historical, or raw-log file modified. No history rewritten.
