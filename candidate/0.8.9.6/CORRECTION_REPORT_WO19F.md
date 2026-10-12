# MSVE-WO-1.9F Correction Report — Candidate 0.8.9.6

**Work order:** MSVE-WO-1.9F (Provenance, Audit Reproducibility and Schema Closure)
**Base:** Candidate 0.8.9.5
**Date:** 2026-10-12
**Status:** CORRECTION CANDIDATE — NOT APPROVED, NOT FROZEN, NOT RELEASED

## Summary

Candidate 0.8.9.6 addresses the three blocking findings (P1) and metadata
issues from the owner's source review of 0.8.9.5. All changes are within the
approved design (D1–D9, A1/A2/A4/A5/A6, D3 Option A). No new owner decisions.

## Blocking findings corrected

### P1. Formal audit self-contained

**Finding:** `run_audit_0895.py` hard-coded `/home/hatch/workspace/msve-wo19d/archival/candidate/0.8.9.4`
as the import path, loaded `/tmp/m8test/codelists.json`, and wrote output to
a 0.8.9.4 path. The reported 31/31 was not demonstrably bound to 0.8.9.5.

**Correction:**
- `run_audit_0896.py` uses `os.path.dirname(__file__)` for the candidate directory.
- `audit_model_0896.py` loads `codelists.json` from the candidate directory (now tracked).
- Outputs write to `candidate/0.8.9.6/outputs/`.
- No hardcoded `/home/hatch`, `/tmp/m8test`, or `0.8.9.4` paths remain (verified by assertion).
- Added scenario C2d: duplicate invocation IDs rejected (negative control for Inv 27c).

**Verification:** 32/32 checks pass from the candidate directory with no external dependencies.

### P1. Execution nonce uniqueness

**Finding:** `str(int(time.time() * 1000000))` is a timestamp, not a unique-per-execution
mechanism. Concurrent calls can collide.

**Correction:**
- Replaced with `str(uuid.uuid4())` (cryptographically random UUID4).
- Normative spec updated: timestamp nonces explicitly insufficient; UUID4 or CSPRNG required.
- Added `_check_invocation_uniqueness()` enforcing bundle-level duplicate-ID rejection (INVALID_INPUT).
- Tests: distinct nonces → distinct IDs; 100 UUIDs unique; duplicate IDs rejected.

### P1. Invocation reference types and solver-observation fields

**Finding:** Three mismatches:
1. `SolverInvocation.inputs_ref: Hash` (required) but pipeline copied nullable `claim.inputs_ref`.
2. Encoder used `inputs_ref or ""`, collapsing None and "".
3. Solver returned `invocation_id`, normative wanted `provenance_ref`; solver didn't return `config`.

**Correction:**
1. **Normative:** `verification_inputs_ref` derivation defined:
   - If claim has `Some(h)` (valid hash) → use `h`.
   - If claim has `None` → `sha256(canonical_query_bytes)`.
   - Null NEVER becomes empty string.
2. **Prototype `pipeline.py`:**
   - Computes `_verif_inputs_ref` per the normative derivation.
   - Validates present hashes strictly (64-char hex) via `_validate_hash()`.
   - Encoder distinguishes None (0x00), "" (0x01+len(0)), valid (0x01+len+bytes).
   - Removed `inputs_ref or ""`.
3. **Prototype `decode.py`:** Strict hash validation at input boundary.
   Present `goal_ref`/`inputs_ref` must be 64-char lowercase hex or null.
   Malformed values → MALFORMED_INPUT (no exploratory gap).
4. **Solver interface:**
   - `solver.run()` now accepts `config` parameter and records it in the observation.
   - Pipeline passes `config` to solver and asserts observation config matches invocation config.
   - Pipeline maps `invocation_id` → `provenance_ref` per normative ("provenance_ref IS the invocation_id").
5. **Normative `SolverObs`:** Added clarification that `provenance_ref` is the invocation ID and `config` must be the actually-applied configuration.

**Tests updated:** Existing tests using `"inputs-1"`, `"i"`, `"g"` replaced with `None` (valid per Option<Hash>). Experiment input fixed.

## Metadata reconciliation

- Removed stale `Implementation status: NOT AUTHORISED` line; marked Work Order 0.8 header as historical.
- D3 schema title: "Candidate 0.8.9.6".
- Spec footer: `MSVE_DESIGN_SPEC_v0.8.9.6.md`.
- Spec header: 0.8.9.6 / WO-1.9F.

## Verification

### Prototype
- **159/159 passed** (153 existing + 6 new adversarial)
- Environment: Python 3.12.3, z3-solver 5.1.0.0, pytest 9.1.1
- New tests cover: distinct nonces, UUID uniqueness, duplicate-ID rejection, null vs empty distinguishability, invalid hash rejection, provenance_ref mapping.

### Formal model
- **32/32 checks** (31 existing + C2d duplicate-ID negative control)
- Self-contained: no external path dependencies.

### M8
- **6/6 preserved** from 0.8.9.4 (grammar/examples unchanged).
- Distinguished as inherited evidence in this report.

## Adversarial coverage (7 required cases)

1. ✅ Same metadata with distinct nonces → different IDs (`test_96_distinct_nonces`)
2. ✅ Repeated/concurrent execution without duplicates (`test_96_uuid_nonce_uniqueness`)
3. ✅ Duplicate IDs in bundle rejected (`test_96_duplicate_id_rejected`, C2d)
4. ✅ Null inputs_ref ≠ empty string (`test_96_null_not_empty_string`)
5. ✅ Invalid SHA-256 rejected (`test_96_invalid_hash_rejected`)
6. ✅ Mismatched invocation/observation metadata → assertion failure (config assert in pipeline)
7. ✅ Clean-clone audit loads 0.8.9.6 model (path assertions, no hardcoded refs)

## Limitations

1. The formal model checks Inv 27c as a state constraint (IDs differ); it does not prove SHA-256 injectivity or that the implementation's encoding is correct. Implementation tests cover the encoding.
2. M8 6/6 is inherited from 0.8.9.4, not re-executed (grammar unchanged).
3. UUID4 collision resistance relies on the cryptographic properties of UUID4, not proven in the model.

## Commits

(To be filled after push)
