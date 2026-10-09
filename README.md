# msve-project

Canonical project bank for MSVE (Mathematical Structure and Verification Engine).

## What this is

A version-controlled archive of the MSVE design specification, its formal
model, verification evidence, and project records. This repository is the
single source of truth for MSVE project state. Future work must update and
reference this record rather than reconstructing the project from
conversational memory.

## Where things live

- `candidate/0.8.8.1/` — the current design candidate (spec, Z3 model,
  regression script, raw test log). See `ARTIFACT_REGISTER.md` for hashes.
- `records/continuity-export-01/` — the eight continuity documents prepared
  for independent review (status, timeline, finding ledger, contract,
  verification evidence, review history, owner decisions, source manifest).
- `history-bank/` — the complete historical artifact bank: every surviving
  versioned document, work-order directory, model, test log, review report,
  and snapshot, with inventory, timeline, provenance, lineage, verification
  history, gap register, and an independent completeness audit
  (`history-bank/COMPLETENESS_AUDIT.md`). Start here for project history.
- `PROJECT_STATE.md` — the current project status.
- `OPEN_DECISIONS.md` — unresolved owner decisions.
- `KNOWN_LIMITATIONS.md` — disclosed limits and attestations.
- `ARTIFACT_REGISTER.md` — every archived artifact with measured hashes.
- `CHANGELOG.md` — truthful record of repository changes.

## What is NOT authorised

No design freeze. No baseline acceptance. Version 0.8.8.1 is a correction
candidate, not an approved baseline. No engine implementation. No
experimental runs. See `PROJECT_STATE.md`.

## For reviewers

Start with `PROJECT_STATE.md`, then `records/continuity-export-01/00_START_HERE_AND_CURRENT_STATUS.md`.
