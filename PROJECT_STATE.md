# PROJECT_STATE.md

**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED

**Candidate version label:** 0.8.8.1-FINAL (supplied version label, not an accepted baseline)

**Date of record:** 2026-10-09

## What this means

The candidate at `candidate/0.8.8.1/` is a correction candidate prepared for
owner review. It is the latest in a sequence of document-revision work orders
(0.8 through 0.8.8.1). Independent normative and formal-model reviews were
completed; all blocking findings were repaired. Review provenance, stated
precisely: the normative review examined the pre-repair specification hash
(`69828cb4…`) and its findings were subsequently addressed — a normative
re-review of the final specification hash (`dbc610c3…`) is not documented.
The formal model was re-inspected on its final hash (`fc6eb49f…`). The
recorded 9/9 regression result remains a reported result with the provenance
limitations documented in `ARTIFACT_REGISTER.md` (raw log preserved).

## Provenance correction notice (read before the continuity package)

Some preserved continuity records contradict the primary review evidence
above. Specifically:

- `records/continuity-export-01/00_START_HERE_AND_CURRENT_STATUS.md` says
  the normative review examined the final specification hash (`dbc610c3…`).
- `history-bank/work-orders/work-order-0.8.8.1-candidate/MSVE_v0.8.8.1_FINAL_MANIFEST.json`
  records `"reviewed_spec": "dbc610c3…"`.

The preserved reviewer report
(`MSVE_v0.8.8.1_NORMATIVE_REVIEW.md`) itself records the pre-repair
specification hash `69828cb4…`. The findings were addressed, but a
normative re-review of the final hash `dbc610c3…` is **not documented** in
the available record. The formal model was separately re-inspected on its
final hash `fc6eb49f…` — a distinct event.

The same continuity file says the historical raw log "corresponds to the
exact final spec/model/test hashes." The raw log records the timestamp,
environment, nine outcomes, and exit status; it does **not** record file
hashes. The log-to-hash binding is reported via the final handoff and
manifest, not cryptographically demonstrated by the log bytes.

Treat the preserved continuity statements as historical claims that are not
established by the primary reports. Use
`history-bank/VERIFICATION_HISTORY.md` for the current corrected provenance
account. These historical records are preserved unchanged; this notice
supersedes their review-coverage claims. This notice does not constitute
the missing normative re-review.

## Explicitly NOT authorised

- Design freeze / baseline acceptance. The candidate is not frozen.
- Version 0.8.8.1 approved or production-ready. It is not.
- MSVE engine implementation.
- Vertical-slice experiment or any experimental run.
- Design baseline approval or product release. (Note: this repository is
  PUBLIC by owner instruction as an archival record; public visibility is
  not a design freeze, baseline approval, or product release.)

Each of the above requires a separate explicit owner decision.

## Open items

See `OPEN_DECISIONS.md` for the unresolved normative questions (UNKNOWN
outcome interpretation; seven unresolved claim kinds; approval boundary).
See `KNOWN_LIMITATIONS.md` for attested-but-unverified properties.
