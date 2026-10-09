# REPOSITORY_AUDIT_REPORT.md

Work order MSVE-REPO-AUDIT-002 — repository integrity, metadata, and
cold-start readability audit, 2026-10-09.

## 1. Verified Git state

| Item | Value (via git protocol, fresh clone) |
|---|---|
| Remote URL | `https://github.com/VAG-gomi/msve-project.git` |
| Visibility | PUBLIC (standing owner instruction; not changed) |
| Branch / local HEAD | `main` / `604db7ed18039dfbcf6da8c7320cd9bbb7bc31c9` |
| Remote HEAD (`ls-remote`) | `604db7ed18039dfbcf6da8c7320cd9bbb7bc31c9` — agrees |
| Parent chain | `604db7e` → `e01d2eed1083d916d448a4dd5f72db95c7e9e754` → `b890636ec525fc2976f80d3af8e95d4896d10295` |
| Working tree | clean; local and remote agree |

## 2–4. Manifest statistics

Four repository states are distinguished. All counts reproducible via
`git ls-files | wc -l` and `sum(os.path.getsize(f) for f in git ls-files)`
at the named commit.

| Commit | Description | Files | Bytes |
|---|---|---:|---:|
| `604db7e` | Pre-audit (HISTORY-CHECK-001) | 424 | 3,963,072 |
| `d83c9de` | Audit (REPO-AUDIT-002) | 427 | 4,091,804 |
| `93b6117` | Bookkeeping correction | 427 | 4,093,379 |
| `64e75c947980ebc8ed93eab8ccc1601fcfbc80ba` | Chronology correction (RECONCILIATION-003) | 427 | 4,094,858 |
| `27ba081add992a944dc266c05631ded10102af6d` | Manifest sync with corrected tree | 427 | 4,094,858 |

The audit added three files over the pre-audit tree:
`REPOSITORY_MANIFEST.csv`, `SOURCE_READER_GUIDE.csv`,
`REPOSITORY_AUDIT_REPORT.md`. The bookkeeping correction modified two
files (CHANGELOG.md, REPOSITORY_AUDIT_REPORT.md). Byte totals above are
git blob sizes (`git cat-file -s`), the authoritative committed-tree
measure. The commit containing this report version is a child of
`27ba081`; its own SHA is recorded in CHANGELOG.md, not in this table,
to avoid a self-reference.

- **Files with measured size + SHA-256:** 427/427 in
  `history-bank/REPOSITORY_MANIFEST.csv` (mechanically generated from the
  tracked tree; every ordinary file; no submodules or symlinks present).
- **Manifest self-reference:** the manifest cannot contain its own final
  SHA-256 as a field. Its pre-commit hash was `f0db00c1…` (81,659 bytes);
  the independently computed post-commit hash is reported in the
  completion report. This narrow exception is documented here and does not
  omit any file.

## 5. Source-to-archive verification

- **404 comparisons** of archived copies against accessible workspace
  sources (from MASTER_INVENTORY.csv source_location): **404 match,
  0 mismatches.**
- **Unavailable sources:** 4 (already in the gaps register; unchanged).
- **Summary-only sources:** 6 (unchanged).

## 6. Metadata completeness

- **Complete records** (size + hash + source + classification): 404.
- **Partial records** (archived file, source is a created-in-repo index):
  13 (the bank's own indexes and notes — labelled as reconstructions).
- **Unresolved** (row but no file): 10 UNAVAILABLE/SUMMARY-ONLY rows —
  by design, not a defect.

## 7. Reader-guide coverage

- **86 evidence-grounded description rows** in
  `history-bank/SOURCE_READER_GUIDE.csv`, built from three independent
  content inspections (specifications/reviews, work-order reports,
  m8 code — each read directly, not inferred from filenames).
- **Covered individually or by type:** all 6 root records, 4 candidate
  files, 8 continuity docs, 11 bank indexes, 15 key work-order reports,
  15 m8/tool modules, 4 reviewer reports + provenance, transfer set,
  2 snapshots, 2 source-records, 6 spec types (43 files), corpus (52 files
  + manifest), work-order supporting files (grouped).
- **Remaining unexplained:** none of historical/technical relevance; the
  ~250 individually-undescribed files are corpus cases and per-stage
  supporting files covered by justified group rows.

## 8. Format findings

- **Broken links:** 0 (all backtick-quoted repo paths in key docs resolve).
- **Missing paths:** 0.
- **Inconsistent status statements:** 0 — every status reference resolves
  to CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED; no document
  claims approval, freeze, or implementation.
- **Contradictions found and corrected:**
  1. `history-bank/source-snapshots/ZIP_CONTENTS.md` was truncated
     (`head -8` output, ~4 entries per ZIP). Replaced with complete
     listings: 226 entries with sizes.
- **Correction to this report (RECONCILIATION-003):** an earlier version
  of this report claimed this audit added the history-bank link to the
  root `README.md`. That is incorrect. Git history (`git log -S
  "history-bank/" -- README.md`) proves the link was added in commit
  `604db7e` (HISTORY-CHECK-001), whose message reads "link history bank".
  This audit verified the link exists; it did not create it. The
  CHANGELOG entry making the same claim is corrected alongside.
- **Stale content noted (not corrected — historical records):**
  m8 `README.md` corpus counts (36 vs measured 52/46); `lexer.py`
  docstring citing the v0.7 keyword list; `grammar.py` HexFloat `-?`
  vs NEW-A7. These are preserved originals; the audit documents them
  rather than rewriting history.

## 9. Cold-start tests

- **Test A (fresh AI session): NOT PERFORMED.** No genuinely isolated AI
  session was available; spawned subagents inherit the author's context,
  which would not prove independence.
- **Test B (fresh Muse session): NOT PERFORMED.** Same reason.
- **Test C (evidence traceability): PERFORMED.** 10/10 major claims
  (purpose/status, candidate identity, test-result scope, lineage, UNKNOWN
  divergence, seven kinds, limitations, gaps, manifest, audit) resolve to
  supporting sources through the repository's own navigation alone —
  verified by path-existence checks against the repo tree, no conversation
  memory used.

## 10. Corrections made

| Path | Change | Rationale |
|---|---|---|
| `history-bank/REPOSITORY_MANIFEST.csv` | Created (427 rows, mechanical) | §4: no complete manifest existed |
| `history-bank/SOURCE_READER_GUIDE.csv` | Created (86 rows, inspection-grounded) | §6: hashes alone don't explain files |
| `history-bank/source-snapshots/ZIP_CONTENTS.md` | Replaced truncated listing with complete 226-entry listing | Truncation defect found by inspection |
| `README.md` | No change (link verified present; added in `604db7e`) | Format check confirmed the entry added by HISTORY-CHECK-001 |
| `history-bank/REPOSITORY_AUDIT_REPORT.md` | This file | §10 requirement |

No candidate, historical, or raw-log file was modified.

## 11a. Post-audit correction (external review)

An external review of this report found two bookkeeping errors, corrected
in a follow-up commit:
1. Section 12 named commit `968e7882…` as final; the actual final commit
   (after an amend) is `d83c9dea70a814ed72dd8bf21a30a60ec980074a`.
   The amend changed the SHA after the report text was written.
2. File/byte totals (424 files, 3,963,072 bytes) were measured at the
   pre-audit commit `604db7e`; the final tree at `d83c9de` has 427 files
   and 4,091,804 bytes. Both figures are now stated with their commit.

## 11. Remaining limitations

- Isolated-session cold-start (A/B) could not be tested; Test C is
  structural, not behavioural.
- Reader-guide descriptions are concise; deep understanding still
  requires reading the sources.
- The manifest's own hash is reported out-of-band (self-reference).
- Eight historical gaps (G-1..G-8) remain unrecoverable; unchanged.

## 12. Commit

- Final commit: `d83c9dea70a814ed72dd8bf21a30a60ec980074a`
  ("Audit: manifest, reader guide, audit report, ZIP contents fix")
- Parent: `604db7ed18039dfbcf6da8c7320cd9bbb7bc31c9` (history unrewritten)
- Manifest post-commit SHA-256: `56e92034d9e945e4bb1ecb33c3929bb2ab62e1f43c22436d686618a7558beb78`
  (self-reference exception; the manifest lists every other file).
- Count reconciliation: 427 tracked files = 427 manifest rows; the manifest
  was regenerated after the audit's own files were added, so no drift.
