# PROJECT_TIMELINE.md

Chronology reconstructed from the dated project log (`~/memory/2026-10-09.md`),
file timestamps, and the continuity export. All events 2026-10-09 UTC unless
noted. Each event cites its supporting record; events known only from a later
summary are marked SUMMARY-ONLY.

## Design-draft phase (morning)

| Time (UTC, approx) | Event | Evidence |
|---|---|---|
| morning | Work Order 0: MSVE v0.1 drafted (5 documents) | SUMMARY-ONLY (dated log); originals in `specifications/` |
| morning | Work Order 0.1: v0.2 revision | SUMMARY-ONLY; originals in `specifications/` |
| morning | ChatGPT review of v0.2 — defects conceded | SUMMARY-ONLY |
| morning | Work Order 0.2: v0.3 revision | SUMMARY-ONLY; originals in `specifications/` |
| morning | ChatGPT review of v0.3 — 12/12 self-review claim refuted | SUMMARY-ONLY |
| morning | v0.4 correction pass (user-directed) | SUMMARY-ONLY; originals in `specifications/` |
| morning | ChatGPT review of v0.4 — 7 freeze-blocking defects conceded | REPORTED (dated log, detailed defect list) |
| morning | v0.5 correction pass | SUMMARY-ONLY; originals in `specifications/` |
| morning | External review of v0.5 — defects conceded | SUMMARY-ONLY |
| morning | Work Order 0.6: v0.6 drafts + first regression ledger | REPORTED; originals in `specifications/` |
| morning | ChatGPT forensic review of v0.6 — gate BLOCKED (B-01..B-05, D-025..D-033) | REPORTED |
| morning | v0.7 targeted correction pass (D-016–D-024) | REPORTED; originals in `specifications/` |
| morning | ChatGPT adversarial review of v0.7 — gate BLOCKED | REPORTED |

## Work-order phase (11:22 → 14:52)

| Time (UTC) | Event | Evidence |
|---|---|---|
| ~11:22 | Work Order 0.8 AUTHORIZED (document correction + M8 tool only) | REPORTED (dated log) |
| ~11:30 | M8 parser/type-checker built; Phase-0 capability probe | ORIGINAL-PRESERVED (`models-and-validators/m8/runs/`) |
| ~11:44 | Work Order 0.8 complete; gate READY_FOR_OWNER_REVIEW | REPORTED |
| ~11:52 | Work Order 0.8.1: owner-review evidence bundle (`8db37d26…`, 111 files) | ORIGINAL-PRESERVED (`source-snapshots/`, `reviews-and-audits/owner-review/`) |
| ~12:03 | Work Order 0.8.2: Markdown evidence transfer (22 files) | ORIGINAL-PRESERVED (`reviews-and-audits/transfer/`) |
| ~12:24–12:43 | Owner review: v0.8 returned for correction; findings F-01–F-19 | REPORTED (dated log); owner findings preserved in 0.8.3 reports |
| ~12:44–12:51 | Work Order 0.8.3: correction candidate prepared (106 artefacts, bundle `1d04b898…`) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.3-candidate/`, `source-snapshots/`) |
| ~13:00–13:07 | Work Order 0.8.4: invariant satisfiability audit (46 Z3 checks; 31 SAT, 14 UNSAT, 1 unknown) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.4-audit/`) |
| ~13:08–13:14 | Work Order 0.8.5: reconciliation (F-20 adjudicated YES) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.5-audit-reconciliation/`) |
| ~13:27–13:34 | Work Order 0.8.5.2: F-21/F-22 audit (owner's own findings confirmed) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.5.2-audit/`) |
| ~13:35 | Owner accepted F-20/F-21 corrections; Work Order 0.8.6 issued | REPORTED |
| ~13:35–13:45 | Work Order 0.8.6: F-20 + F-21 normative corrections (invariants 24–28, §E.6a) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.6-candidate/`) |
| ~13:46–14:00 | Work Order 0.8.6.1 transfer; owner rejected baseline approval | REPORTED |
| ~14:00–14:07 | Work Order 0.8.7: F-22–F-27 corrections; R1-1 found (payload-free claim key) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.7-candidate/`) |
| 14:05:48Z | 0.8.7 raw log: 18/18 pass — PREDATES final R1 model change (~14:08Z) | ORIGINAL-PRESERVED (log in 0.8.7 dir); LIMITATION documented |
| ~14:21–14:23 | Work Order 0.8.7.1: owner-review evidence transfer | REPORTED |
| ~14:33–14:34 | Work Order 0.8.7.2: read-only decision packet (Option A recommended) | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.7.2-review/`) |
| ~14:37 | Owner selected Option A; Work Order 0.8.8 issued | REPORTED |
| ~14:38–14:45 | Work Order 0.8.8: Option A implemented; independent reviews (N-1/2/3, F1/F2) repaired | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.8-candidate/`) |
| ~14:46–14:49 | Work Order 0.8.8.1: bounded closure candidate created | ORIGINAL-PRESERVED (`work-orders/work-order-0.8.8.1-candidate/`) |
| 14:52:51Z | Final 9/9 regression run on final hashes (Python 3.12.3, Z3 5.1.0, exit 0) | ORIGINAL-PRESERVED (`candidate/0.8.8.1/run_audit_0881_raw.log`) |

## Repository phase (15:21 → 16:0x)

| Time (UTC) | Event | Evidence |
|---|---|---|
| ~15:21–15:23 | ChatGPT continuity export created (8 Markdown files) | ORIGINAL-PRESERVED (`records/continuity-export-01/`) |
| ~15:23–15:59 | ChatGPT continuity audit: UNKNOWN-policy inconsistency identified | REPORTED; recorded in `OPEN_DECISIONS.md` |
| 15:52:28Z | MSVE-REPO-001: repo created, initial commit `b890636e` pushed | HASH-VERIFIED (git log) |
| ~16:00 | Repo visibility set PUBLIC on owner instruction, then corrected to PRIVATE per MSVE-HISTORY-001 | REPORTED (work-order record) |
| 2026-10-09 | MSVE-HISTORY-001: this history bank committed | This commit |

## Notes

- The entire surviving MSVE history falls within a single day. The dated log
  is the primary source for morning-phase events; no independent manifests
  exist for work orders 0–0.2 and 0.4.
- "Approximate" times (~) come from the dated log's own approximations.
  Exact timestamps (14:05:48Z, 14:52:51Z, 15:52:28Z) come from preserved
  logs and git records.
