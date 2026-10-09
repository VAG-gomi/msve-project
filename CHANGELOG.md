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

## 2026-10-09 — Audit table final correction (external review)

- Replaced the `THIS_COMMIT` placeholder in `REPOSITORY_AUDIT_REPORT.md`
  with explicit full-SHA rows for `64e75c9` and `27ba081` (both: 427 files,
  4,094,858 bytes by git blob size). The current commit's own SHA is
  recorded here, not in the report table, to avoid self-reference.
- No other content changed.

## 2026-10-09 — Cold-start documentation corrections (MSVE-COLDSTART-CORRECTIONS-001)

Verified each finding against original sources before correcting:

1. `PROJECT_STATE.md`: removed "private archival repository" language.
   The archive is PUBLIC by owner instruction; public visibility is
   distinguished from baseline approval and product release.
2. `history-bank/VERIFICATION_HISTORY.md` Claim 6: clarified that the
   0.8.8.1 normative review inspected the pre-repair spec hash `69828cb4…`,
   not the final `dbc610c3…`. No final-hash normative re-review is
   documented. (Model re-inspection WAS on the final hash.)
3. `ARTIFACT_REGISTER.md`: distinguished the raw log's contents (no hashes
   recorded) from the REPORTED log-to-hash association (via FINAL_HANDOFF /
   FINAL_MANIFEST).
4. SemanticResult: verified the spec defines a closed set of 11
   alternatives; no secondary description claimed otherwise. No change.
5. `KNOWN_LIMITATIONS.md`: recorded absolute-path dependencies
   (`/tmp/m8test/codelists.json`; hardcoded workspace paths) and the
   resulting clean-clone reproducibility limitation. Candidate code
   unmodified.

Historical reports untouched; corrections are in current-status records only.

## 2026-10-09 — Final-hash review wording correction (MSVE-COLDSTART-FINAL-001)

- `PROJECT_STATE.md`: replaced "reviews have been completed on the final
  file hashes" with the precise provenance: normative review examined the
  pre-repair spec hash `69828cb4…` (findings addressed; no final-hash
  re-review documented); the model was re-inspected on its final hash
  `fc6eb49f…`; the 9/9 result remains reported with documented provenance
  limits. No other status summary carried the same implication.
- Historical reports preserved as written.

## 2026-10-09 — Repository-wide Python reproducibility records (MSVE-PYTHON-REPRO-001)

- Added `reproducibility/`: PYTHON_SOURCE_INVENTORY.csv (46 tracked .py
  files, 33 distinct sources), REPRODUCIBILITY_MATRIX.csv,
  ENVIRONMENT_REGISTER.md, KNOWN_BLOCKERS.md, per-era run evidence
  (0.8.4–0.8.8.1, M8 tests/tools/CLI), patched harnesses with provenance,
  and reports. All 12+12 ZIP .py members verified byte-identical to
  tracked files.
- Results: 21 files REPRODUCED (0.8.8.1 9/9, 0.8.8 16/16, 0.8.7 18/18,
  0.8.6 13/13, 0.8.4 45/46 with documented joint-SAT miss, 0.8.5/0.8.5.2
  scripts), 9 TESTS-PASSED (M8 suites, CLI, tools), 16 STATIC-ONLY
  (library modules, import-verified). No FAILED or BLOCKED.
- All Z3 runs used reconstructed code lists, labelled RECONSTRUCTED — NOT
  THE HISTORICAL ORIGINAL. Historical artifacts and candidate sources
  unchanged. Linked from root README.

## 2026-10-09 — Reproducibility scope and review provenance (MSVE-DOC-CORRECTIONS-002)

1. `reproducibility/README.md`: clarified inventory scope — 46 rows cover
   original/source tracked `.py` files at commit `4f395ef`; the nine
   derived harnesses are catalogued separately in `harnesses/PROVENANCE.md`;
   55 tracked `.py` files total.
2. `PROJECT_STATE.md`: added a provenance correction notice superseding
   the preserved continuity claims that the normative review examined the
   final spec hash `dbc610c3…` (the report records `69828cb4…`; no
   final-hash re-review documented) and clarifying the raw log does not
   itself record file hashes. Historical records preserved unchanged.
3. Root `README.md`: continuity bullet now directs readers to the
   PROJECT_STATE.md notice first.

## 2026-10-09 — Brainstorm synthesis and owner decision packet (MSVE-WO-0.9)

- Added `decision-ledger/`: MSVE_BRAINSTORM_DECISION_LEDGER.csv (26
  records: 7 ACCEPTED-BY-OWNER, 4 SUPPORTED, 4 PROPOSED, 2 CONFLICTED,
  1 DEFERRED, 8 UNRESOLVED), OWNER_DECISION_PACKET.md (D1–D9 with options,
  arguments, spec constraints, recommendations), README.md with tracing
  guide. Covers UNKNOWN policy, seven claim kinds (with inv 22/23
  dependencies), query/assumption fidelity, checker independence, slot
  bounds, canonical escaping, freeze criteria, V0 scope, and the §H
  archival-bank vs implementation-repo clarification.
- Root README links the ledger. No candidate, spec, model, or test files
  modified; no experiments run.
