# PROJECT_STATE.md

**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW REQUIRED

**Candidate version label:** 0.8.9.9 (correction candidate; not an accepted baseline)

**Date of record:** 2026-10-12

## What this means

The candidate at `candidate/0.8.9.9/` is a correction candidate prepared for
owner review under work order MSVE-WO-1.9I. It addresses the P1 duplicate-JSON-key
rejection gap from the owner's source review of 0.8.9.8 and completes the
evidence manifest with full commit and artifact hashes.

Previous candidates are preserved unchanged as historical artefacts:
- `candidate/0.8.8.1/` — 0.8.8.1-FINAL (2026-10-09)
- `candidate/0.8.9/` — 0.8.9 (2026-10-11)
- `candidate/0.8.9.1/` — 0.8.9.1 correction candidate (2026-10-11)
- `candidate/0.8.9.2/` — 0.8.9.2 correction candidate (2026-10-12)
- `candidate/0.8.9.3/` — 0.8.9.3 correction candidate (2026-10-12)
- `candidate/0.8.9.4/` — 0.8.9.4 correction candidate (2026-10-12)
- `candidate/0.8.9.5/` — 0.8.9.5 correction candidate (2026-10-12)
- `candidate/0.8.9.6/` — 0.8.9.6 correction candidate (2026-10-12)
- `candidate/0.8.9.7/` — 0.8.9.7 correction candidate (2026-10-12)
- `candidate/0.8.9.8/` — 0.8.9.8 correction candidate (2026-10-12)

No design freeze, baseline acceptance, release, or production claim is
authorized. The bounded D8 exploratory prototype is separately authorized;
the full MSVE baseline remains unapproved and unfrozen.

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
- Full MSVE engine implementation (beyond the exploratory prototype below).
- Design baseline approval or product release. (Note: this repository is
  PUBLIC by owner instruction as an archival record; public visibility is
  not a design freeze, baseline approval, or product release.)

## Separately authorised: exploratory prototype (D8)

Owner ruling D8 (recorded 2026-10-10; decision-ledger DEC-015) authorises
a **bounded exploratory engine prototype** under MSVE-WO-1.0, with genuine
experiments under MSVE-WO-1.1. This is a narrow, explicitly scoped
exception to the earlier implementation prohibition:

- The prototype lives in a **separate implementation repository**,
  [VAG-gomi/msve-engine-prototype](https://github.com/VAG-gomi/msve-engine-prototype),
  not in this archival repository (D9).
- Its results are **experimental evidence only**, not verified MSVE
  capability, and never freeze or baseline evidence by themselves.
- The archival design candidate above remains unfrozen and unapproved;
  prototype existence does not change the candidate's status.

Each of the NOT-authorised items above still requires a separate explicit
owner decision.

## Open items

See `OPEN_DECISIONS.md` for the unresolved normative questions (UNKNOWN
outcome interpretation; seven unresolved claim kinds; approval boundary).
See `KNOWN_LIMITATIONS.md` for attested-but-unverified properties.
