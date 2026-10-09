# MSVE v0.8.4 Owner Handoff

**Work Order 0.8.4 — Result-Schema Consistency and Invariant Satisfiability Audit**
**Date:** 2026-10-09 · **Status:** CONSISTENCY AUDIT COMPLETE — OWNER REVIEW REQUIRED

This is not acceptance, freeze, or implementation authorization.

## Decision

**CONSISTENCY EVIDENCE SUPPORTS OWNER REVIEW.**

All 13 intended scenario families have witnesses under the joint
constraints; all 13 targeted contradictions are rejected; no material
formalization ambiguity remains unresolved (8 ambiguities registered, all
dispositioned in the reconciliation). The joint constraint system is
satisfiable.

## What was established

1. Two reviewers independently formalized all 23 §E.7 invariants from the
   candidate bytes (spec SHA-256 `9f692585…7c003`) and converged; the
   reconciliation records every disagreement and its resolution.
2. Z3 5.1.0: 45/46 scenario checks behaved as expected — 31 valid scenario
   instances SAT (incl. all 11 `SemanticResult` alternatives per §E.2, all
   5 verification summaries, F-01 detailed error codes), 13 invalid
   variants UNSAT for identifiable reasons.
3. The highest-value open item from 0.8.3 — joint satisfiability of the
   §E.7 invariants — is now demonstrated for the formalizable fragment.
4. Phase A corrected the 0.8.3 report's truncated ZIP checksum; the full
   value is `1d04b8989a7c4b647dc2fdf772316220dc06649329ce0e7964bf13b62d24c850`.

## What remains uncertain / outside the audit

- Invariants 3 ("the check corpus was non-empty") and 12 ("the frozen spec
  contains `assurance: level-b accepted`") reference objects outside the
  record and cannot be checked as record constraints.
- Invariants 20/21/23 check only evidence *existence*, not *aboutness*
  (no schema discriminator for "the check property", "search record", or
  projection linkage).
- The unconstrained joint Z3 query returned `unknown` (solver search
  limit); satisfiability is established by entailment from the witnesses.
- No claim about MSVE-engine behavior or implementation conformance.

## New finding: F-20 (minor)

Invariant 10's "occurred at packaging" test covers only
`base_code(r) = "output-not-encodable"`, but `canonicalization-failure`
is also a packaging base code (joint with `output_packaging` per 15b).
Proposed minimum correction: test `is_packaging_error(r)` instead.
Affects the candidate spec's invariant 10 text only.

**Is a new correction work order required?** F-20 is minor and editorially
scoped (one predicate in one invariant). It does not block the consistency
conclusion. Whether to fold it into a future correction pass is the
owner's decision; no new work order is required by this audit's result.

## Artefacts (all in `~/workspace/msve-design/work-order-0.8.4-audit/`)

- `MSVE_v0.8.4_AUDIT_INPUT_MANIFEST.md` (Phase A, incl. checksum correction)
- `MSVE_v0.8.4_INVARIANT_FORMALIZATION_A.md` / `…_B.md` (independent)
- `MSVE_v0.8.4_FORMALIZATION_RECONCILIATION.md`
- `MSVE_v0.8.4_SCHEMA_CONSISTENCY_REPORT.md`
- `MSVE_v0.8.4_WITNESS_AND_COUNTERMODEL_CATALOG.md`
- `MSVE_v0.8.4_VERIFICATION_EVIDENCE.md`
- `MSVE_v0.8.4_OWNER_HANDOFF.md` (this file)
- `audit_model.py`, `run_audit.py`, `dump_witnesses.py` (audit tool)
- `MSVE_v0.8.4_AUDIT_MANIFEST.json` (SHA-256 of all audit artefacts)

The v0.8.3 candidate artefacts were not modified.
