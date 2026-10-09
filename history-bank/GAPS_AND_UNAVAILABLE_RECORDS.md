# GAPS_AND_UNAVAILABLE_RECORDS.md

What is missing, why it matters, and what would resolve it. The bank's
completeness claim never exceeds the evidence preserved.

## G-1 — F-19 2,998-value sweep: script and output unpreserved

- **Classification:** UNAVAILABLE.
- **Impact:** a numerical sweep claimed during v0.4 review cannot be
  re-verified or even re-examined. Any historical claim depending on it
  rests on testimony alone.
- **Resolution:** none possible; the run cannot be reconstructed honestly.

## G-2 — Reviewer B's 0.8.1 collision-sweep script

- **Classification:** UNAVAILABLE.
- **Impact:** one reviewer's supporting script is missing; the review
  report survives but its mechanical basis cannot be checked.
- **Resolution:** none possible from surviving records.

## G-3 — 0.8.7 post-R1-4 full stdout

- **Classification:** UNAVAILABLE.
- **Impact:** the preserved 18/18 log (14:05:48Z) predates the final model
  change (~14:08Z), so no passing log exists for the final 0.8.7 bytes.
  This is a genuine hole in the 0.8.7 verification chain, honestly
  documented at the time.
- **Resolution:** none possible; the run is in the past.

## G-4 — Pre-0.8 work-order records (Work Orders 0–0.2, 0.4)

- **Classification:** SUMMARY-ONLY.
- **Impact:** early authorizations and review exchanges survive only as
  dated-log summaries. Exact review texts (ChatGPT's v0.2–v0.7 reviews)
  are not preserved as artifacts.
- **Resolution:** none; the exchanges happened in chat and were not exported.

## G-5 — No version-control history before the bank

- **Classification:** UNAVAILABLE (never existed).
- **Impact:** file-level chronology within 2026-10-09 relies on log
  timestamps and filesystem mtimes, not commits. The per-work-order
  directory structure is the de facto versioning.
- **Resolution:** the bank itself (from MSVE-REPO-001 onward) is now the
  versioned record.

## G-6 — SAT witness strings truncated

- **Classification:** SUMMARY-ONLY (partial).
- **Impact:** `sat_models_0881.json` (and 087/088 equivalents) store
  truncated model strings. A future reviewer cannot fully reconstruct the
  solver's assignments from these files.
- **Resolution:** would require re-running the models (not authorized here).

## G-7 — Reviewer hash anchoring

- **Classification:** UNVERIFIED (limitation, not a missing file).
- **Impact:** reviewers A–D did not record the exact spec hashes they
  inspected, so their reports cannot be cryptographically tied to specific
  bytes. Documented in the 0.8.3 correction report; accepted as a standing
  limitation.
- **Resolution:** procedural — future reviews must record inspected hashes.

## G-8 — Morning-phase timestamps are approximate

- **Classification:** INFERRED.
- **Impact:** events before ~11:22 UTC carry approximate times from the
  dated log. Ordering is as recorded; exact times are not established.
- **Resolution:** none possible.

## Overall assessment

The bank preserves the complete *surviving* record: every versioned
document, every work-order directory, the M8 tool, all review reports, both
bundle snapshots, and the final candidate. The gaps above are disclosed,
not hidden. No gap has been filled by invention.
