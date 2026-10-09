# MSVE History Bank — README

## Purpose

This directory is the historical artifact bank for MSVE (Mathematical
Structure and Verification Engine). It preserves the original project
records — specifications, work-order outputs, models, test logs, reviews,
decisions, and snapshots — so that future work resumes from the actual
surviving record rather than from conversational memory.

## What is banked here

| Directory | Contents |
|---|---|
| `specifications/` | Versioned design documents v0.1–v0.8 (specs, acceptance plans, capability matrices, design reviews, regression ledgers, visualisation plans) |
| `work-orders/` | Complete per-work-order directories 0.8.3 → 0.8.8.1 plus the 0.8.3 draft |
| `models-and-validators/` | The M8 parser/type-checker tool and standalone check scripts |
| `tests-and-raw-logs/` | Scope note — raw logs live inside their work-order directories |
| `reviews-and-audits/` | Owner-review evidence and the 0.8.2 transfer package |
| `decisions-and-repairs/` | Scope note — decision records live in work-order directories |
| `experiments-and-results/` | Scope note — no experiments were ever authorised or run |
| `repository-history/` | Scope note — no git history predates the bank |
| `source-snapshots/` | The two original ZIP bundles with a contents listing |
| `source-records/` | The dated project log (primary source for the timeline) |

## Indexes

- `MASTER_INVENTORY.csv` — one row per archived artifact (409 rows) plus
  rows for known-unavailable sources. Columns include measured SHA-256,
  size, source location, and evidence classification.
- `PROJECT_TIMELINE.md` — chronology reconstructed from dated records.
- `PROVENANCE_REGISTER.md` — where records came from and how copies were verified.
- `VERSION_LINEAGE.md` — how specs, models, and reports relate across versions.
- `VERIFICATION_HISTORY.md` — historical verification claims and their evidence.
- `GAPS_AND_UNAVAILABLE_RECORDS.md` — what is missing and what that costs.

## Coverage boundaries

- **Time span:** all surviving records date from 2026-10-09 (single-day
  project history). Earlier work orders 0–0.2 and 0.4 predate manifest
  discipline and survive only as summaries.
- **Originals vs. indexes:** files under the category directories are
  byte-identical copies of workspace originals (verified at archival).
  The seven index files in this directory were *created* by work order
  MSVE-HISTORY-001 as navigational aids; they are reconstructions, not
  originals. They are labelled as such in the inventory.
- **Already archived elsewhere in this repo:** the 0.8.8.1 candidate
  (`candidate/0.8.8.1/`) and the continuity export
  (`records/continuity-export-01/`) are not duplicated here; the inventory
  references them.
- **Excluded:** `__pycache__/` directories and `*.pyc` files (build
  artifacts, not project records) were not archived.

## Evidence classifications

See `PROVENANCE_REGISTER.md` for the label set
(ORIGINAL-PRESERVED, HASH-VERIFIED, REPORTED, SUMMARY-ONLY, INFERRED,
UNVERIFIED, UNAVAILABLE, CONFLICTING). Classifications describe the
strength of *historical* evidence, not the mathematical correctness of
the design.
