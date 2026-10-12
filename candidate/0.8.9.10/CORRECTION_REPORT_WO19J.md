# MSVE-WO-1.9J Correction Report — Candidate 0.8.9.10

**Work order:** MSVE-WO-1.9J (Candidate Identity and Evidence Closure)
**Base:** Candidate 0.8.9.9
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN, NOT RELEASED

## Objective

Bind the manifest to verified repository commits, complete artefact hashes,
add `run_text()` end-to-end duplicate-key coverage, and reconcile metadata.

## 1. Repository identities corrected

All SHAs are full 40-character values verified via `git rev-parse` /
`git ls-remote`:

- **Archival candidate content:** `3e0c87c42533be95c3976e6016a3d9a4f7d658ee`
  (contains `candidate/0.8.9.10/` with spec, D3, vectors, model, runner, outputs)
- **Archival final:** includes PROJECT_STATE update (see manifest)
- **Prototype:** `a89f473275b4cf97bec92106e17d533a0442f574`
  (contains the WO-1.9I duplicate-aware decoder and WO-1.9J `run_text()` tests —
  verified by cloning and checking file presence)

The manifest distinguishes candidate-content from final commits.

## 2. Evidence manifest completed

SHA-256 recorded for every key artefact, verified against the exact published
files:
- Spec, D3 schema, invocation vectors, query-ID vectors
- Formal model, audit runner, codelists.json
- Test output (`outputs/pytest_08910.txt`, 178 passed)
- Audit output (`outputs/audit_08910.txt`, 32/32)
- Prototype: decoder, pipeline, solver, queries, test file

No artefact is labelled "verified" on presence alone; hashes are computed
from the published revisions.

## 3. run_text() end-to-end duplicate-key test

**New tests:**
- `test_910_run_text_duplicate_key_rejected`: submits duplicate-key raw JSON
  through `run_text()` (the raw-JSON entry point). Asserts `MALFORMED_INPUT`
  with "duplicate" in the message. Installs a solver sentinel that raises
  `AssertionError` if called; asserts the sentinel was never triggered —
  proving rejection occurs before solver invocation.
- `test_910_run_text_valid_still_works`: valid raw JSON through `run_text()`
  still produces a solver observation.

**Clarification:** `run_text()` is the raw-JSON entry point applying
duplicate-aware decoding. Direct `run(dict)` invocation is already-parsed
input; duplicate-key history cannot be recovered from a dictionary.

Existing raw-JSON tests for top-level, declaration, and nested keys preserved.

## 4. Specification metadata reconciled

- Footer: `MSVE_DESIGN_SPEC_v0.8.9.10.md`
- Header: 0.8.9.10 / WO-1.9J
- M8 inherited-evidence range: 0.8.9.5–0.8.9.9 (origin: 0.8.9.4, 2026-10-12)
- Added explicit `run_text()` raw-entry-point documentation
- Correction report and manifest use consistent version, commits, counts

## Verification

- **Prototype:** 178/178 passed (output retained in candidate)
- **Formal model:** 32/32 checks (output retained in candidate)
- **M8:** 6/6 inherited from 0.8.9.4

## Limitations

1. Counts are reported from assistant execution, not independently reproduced.
2. M8 inherited, not re-executed (grammar unchanged).
3. The formal model does not cover JSON decoding.

## Findings-to-evidence table

| Finding | Fix | Evidence |
|---------|-----|----------|
| Manifest SHAs incomplete | Full 40-char SHAs + SHA-256 for all artefacts | CANDIDATE_MANIFEST_08910.md |
| No run_text() e2e test | Sentinel test through raw entry point | test_910_run_text_duplicate_key_rejected |
| M8 stops at 0.8.9.7 | Extended to 0.8.9.9 | spec paragraph |
| Footer 0.8.9.9 | Updated to 0.8.9.10 | spec footer |
