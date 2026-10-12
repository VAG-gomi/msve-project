# MSVE-WO-1.9I Correction Report — Candidate 0.8.9.9

**Work order:** MSVE-WO-1.9I (Duplicate-Key Rejection and Evidence Manifest Closure)
**Base:** Candidate 0.8.9.8
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN, NOT RELEASED

## Summary

Candidate 0.8.9.9 closes the P1 duplicate-JSON-key enforcement gap and
completes the evidence manifest. All changes are within the approved design.

## P1 finding corrected

### Duplicate JSON object keys rejected at parse time

**Finding:** `decode.py` used ordinary `json.loads()`, which collapses duplicate
keys (last wins) before validation. The D3 schema requires duplicate keys to be
rejected as `MALFORMED_INPUT`.

**Correction:** Added `_reject_duplicates()` as `object_pairs_hook` to
`json.loads()` in `decode()`. Any repeated key at any nesting level raises
`MSVEError("MALFORMED_INPUT", "duplicate object key: ...")` before dictionary
construction. Rejected input cannot proceed to solver execution or assurance.

**Normative:** D3 schema's MALFORMED_INPUT list now explicitly includes
"duplicate JSON object keys at any level (0.8.9.9: detected during parsing
via duplicate-aware decoding, before dictionary construction)".

**Tests (raw JSON text, not Python dicts):**
- `test_99_duplicate_top_level_key`
- `test_99_duplicate_declaration_name_key`
- `test_99_duplicate_declaration_sort_key`
- `test_99_duplicate_nested_query_key`
- `test_99_valid_json_still_works`
- `test_99_duplicate_cannot_reach_solver`

## P2 corrections

### Complete manifest

The manifest now records:
- Full 40-char Git SHAs for archival (content + final) and prototype,
  verified via `git rev-parse` and `git ls-remote`.
- SHA-256 for: specification, D3 schema, invocation vectors, formal model,
  audit runner, `codelists.json`.
- Test command and environment.
- Explicit "reported, not independently reproduced" label for test counts.

### M8 provenance through 0.8.9.8

The spec's inherited-evidence statement now reads "0.8.9.5–0.8.9.8"
(previously stopped at 0.8.9.7). Origin preserved: 6/6 verified 2026-10-12
on 0.8.9.4; grammar/examples unchanged.

## Verification

- **Prototype:** 176/176 passed
- **Formal model:** 32/32 checks, self-contained
- **M8:** 6/6 inherited from 0.8.9.4

## Limitations

1. Test counts are reported from assistant execution, not independently reproduced.
2. The formal model does not verify the JSON decoder; duplicate-key tests are
   implementation-level.
3. M8 inherited, not re-executed.

## Findings-to-evidence table

| Finding | Fix | Test |
|---------|-----|------|
| Duplicate keys collapsed | `decode.py` object_pairs_hook | `test_99_duplicate_*` (6 tests) |
| Manifest incomplete | Full SHAs recorded | git-verified |
| M8 stops at 0.8.9.7 | Spec updated to 0.8.9.8 | — |
