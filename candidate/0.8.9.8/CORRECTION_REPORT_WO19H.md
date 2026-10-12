# MSVE-WO-1.9H Correction Report — Candidate 0.8.9.8

**Work order:** MSVE-WO-1.9H (Query Schema Closure and Invocation Evidence Reproducibility)
**Base:** Candidate 0.8.9.7
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN, NOT RELEASED

## Summary

Candidate 0.8.9.8 closes two P1 findings and three P2 issues from the owner's
review of 0.8.9.7. All changes are within the approved design.

## P1 findings corrected

### 1. Exact query-object field enforcement

**Finding:** The D3 validator accepted unknown top-level and declaration fields,
while the normative schema requires exactly `language`, `declarations`,
`assertions` (and `name`, `sort` for declarations).

**Correction:** `queries.validate()` now:
- Rejects unknown top-level keys with `MALFORMED_INPUT`.
- Rejects unknown declaration keys with `MALFORMED_INPUT`.
- Preserves the malformed-vs-unsupported language distinction.

**Tests:** `test_98_unknown_top_level_key_rejected`,
`test_98_unknown_declaration_key_rejected`,
`test_98_unsupported_language_still_unsupported`.

### 2. Self-contained invocation vectors

**Finding:** `INVOCATION_VECTORS.md` said query_canon "(see below)" with no
actual query shown. The vector could not be independently reproduced.

**Correction:** Rewrote `INVOCATION_VECTORS.md` with:
- Complete query object (JSON).
- Exact canonical query JSON text.
- Expected `query_id` with verification note (SHA-256 of canonical bytes).
- All invocation field values.
- Complete preimage bytes in hex.
- Expected invocation ID.
- Encoding rule, field order, and reference implementation notes.
- Nonce labelled as FIXED TEST FIXTURE (production uses UUID4).

**Tests:**
- `test_98_vector_query_id_reproducible`: canonical bytes → expected query_id.
- `test_98_vector_invocation_id_reproducible`: full vector → expected invocation ID.
Both stages verified independently, not just the final hash.

## P2 corrections

### 3. SolverInvocation query types

**Finding:** Normative said `query: String`; prototype stored an object.

**Correction:** Normative now declares `query: QueryObject` (structured) and
`query_payload: String` (canonical JSON). Consistency required:
- `query_payload = canonical_json(query)`
- `query_id = SHA256(UTF8(query_payload))`
- Mismatch → `INVALID_INPUT`, blocks solver-backed assurance.

Prototype adds `_check_query_consistency()` enforcing this at invocation time.

**Tests:** `test_98_mismatched_query_payload_rejected`,
`test_98_qid_payload_mismatch_rejected`.

### 4. D3 schema header

Updated to "Candidate 0.8.9.8".

### 5. Manifest hashes

`INVOCATION_VECTORS.md` SHA-256 now recorded in the manifest (see below).

## Verification

- **Prototype:** 170/170 passed
- **Formal model:** 32/32 checks, self-contained
- **M8:** 6/6 inherited from 0.8.9.4 (grammar unchanged; provenance in spec)

## Adversarial coverage (8 required)

1. ✅ Unknown top-level key rejected
2. ✅ Unknown declaration key rejected
3. ✅ Unsupported language remains UNSUPPORTED
4. ✅ Canonical bytes reproduce vector query_id
5. ✅ Vector reproduces preimage and expected ID
6. ✅ Mismatched query/payload rejected
7. ✅ Payload/qid mismatch rejected (blocks assurance)
8. ✅ Manifest hashes (below, git-verified)

## Limitations

1. The formal model does not verify the runtime encoding; vectors provide
   implementation evidence.
2. M8 inherited, not re-executed.
3. Only `msve-arith-v1` is implemented; other languages are UNSUPPORTED by design.

## Findings-to-evidence table

| Finding | Fix | Test |
|---------|-----|------|
| Unknown query keys accepted | `queries.py` key validation | `test_98_unknown_top_level_key_rejected` |
| Unknown decl keys accepted | `queries.py` decl validation | `test_98_unknown_declaration_key_rejected` |
| Vector not reproducible | `INVOCATION_VECTORS.md` rewritten | `test_98_vector_*_reproducible` |
| query: String vs object | Normative `QueryObject` + consistency | `test_98_mismatched_*_rejected` |
| D3 header 0.8.9.6 | Updated to 0.8.9.8 | — |
| Manifest missing vector hash | Added (see manifest) | — |
