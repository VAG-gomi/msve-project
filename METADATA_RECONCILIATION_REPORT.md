# MSVE-WO-1.9K Metadata Reconciliation Report

**Work order:** MSVE-WO-1.9K (Public Metadata Reconciliation)
**Date:** 2026-10-12
**Type:** Documentation-only. No source code, specification, or model changed.

## Verified repository heads (via git ls-remote)

| Repository | HEAD SHA (40-char) |
|------------|-------------------|
| VAG-gomi/msve-project | `4b16bf008ec0bc7ab1d4e9d3515c4e783516878e` |
| VAG-gomi/msve-engine-prototype | `a89f473275b4cf97bec92106e17d533a0442f574` |

## Files changed

### 1. Archival README.md (`VAG-gomi/msve-project`)

**Before:** Linked to `candidate/0.8.8.1/MSVE_DESIGN_SPEC_v0.8.md` as "the design
specification"; described "0.8.8.1-FINAL"; listed `candidate/0.8.9.2/` as current.

**After:**
- Identifies **0.8.9.10** as the current correction candidate with direct links
  to spec, D3 schema, manifest, and PROJECT_STATE.md.
- States explicitly: awaiting owner review, not an accepted baseline; D7 freeze
  and release unapproved; D8 prototype is experimental in the separate repo
  (with link); prototype status does not confer approval.
- Lists all historical candidates 0.8.8.1 through 0.8.9.9 as preserved/unchanged.

### 2. Prototype README.md (`VAG-gomi/msve-engine-prototype`)

**Before:** "`tests/` — 153 automated tests (...)"

**After:** "`tests/` — 178 automated tests (... + WO-1.9F through WO-1.9J coverage)"

**Source of count:** `candidate/0.8.9.10/outputs/pytest_08910.txt` in the archival
bank records "178 passed in 8.34s". The count was not replaced with an
unverified number.

Added evidence-separation note: 178 tests, 32-check formal audit, inherited M8
6/6, and genuine UNKNOWN experiment are distinct artefacts, not one total.

## Repository descriptions (no change needed)

Both descriptions were already accurate:
- Archival: "Design candidate archive; no baseline frozen, no implementation authorised."
- Prototype: "experimental, D8-authorised" + pointer to archival bank.

GitHub descriptions cannot be changed via git push; they require web/API access.
No change was claimed.

## Consistency checks

- ✅ Archival README and PROJECT_STATE.md agree: 0.8.9.10 current candidate.
- ✅ Prototype README (178) agrees with manifest's preserved output.
- ✅ All updated links are relative and resolve within the repos.
- ✅ No specification, formal-model, or historical artefact modified.
- ✅ Candidate 0.8.9.10 content unchanged (no new candidate revision needed).

## Remaining discrepancies

None found in public entry documents. The 0.8.9.10 candidate, manifest,
PROJECT_STATE.md, and both READMEs are now consistent.

## Limitations

- Test counts are reported from preserved execution logs, not independently
  re-executed for this documentation pass (per work-order instruction not to
  rerun merely to alter a displayed count).
- M8 6/6 remains inherited from 0.8.9.4 (disclosed in spec and reports).
