# MSVE v0.8 Owner Review Handoff

**Work Order:** 0.8.1 · **Date:** 2026-10-09
**Gate claimed:** READY_FOR_OWNER_REVIEW (lead) · **Owner decision:** pending

This document navigates the evidence bundle. It does not ask you to
accept anything — it shows where the evidence is.

## Artefact locations (relative to `~/workspace/msve-design/`)

**Six design documents (preserved byte-for-byte):**
- `MSVE_DESIGN_SPEC_v0.8.md` — normative specification
- `MSVE_DESIGN_REVIEW_v0.8.md` — review record, verification table, gate decision
- `MSVE_CAPABILITY_MATRIX_v0.8.md` — capability claims C1–C11
- `MSVE_ACCEPTANCE_PLAN_v0.8.md` — acceptance procedure (execution NOT authorised)
- `MSVE_VISUALISATION_PLAN_v0.8.md` — 7 Mermaid diagrams
- `MSVE_REGRESSION_LEDGER_v0.8.md` — D-001–D-033 with full histories

**M8 audit tool:**
- `m8/` — lexer, parser, resolver, type-checker, canonical checker, CLI
- `m8/corpus/` — 46 regression cases + manifest
- `m8/tests/` — canonical and grammar-conformance tests
- `m8/runs/` — build record, Phase-0 probe record

**This bundle (`owner-review/`):**
- `MSVE_v0.8_OWNER_REVIEW_MANIFEST.md` / `.json` — every artefact with SHA-256
- `MSVE_v0.8_READINESS_EVIDENCE_MATRIX.md` — claim-by-claim audit (12 claims)
- `MSVE_v0.8_DEFECT_TRACEABILITY.md` — D-001–D-033 + 24 reviewer findings
- `reviewer-reports/` — original A/B/C/D reports + PROVENANCE.md
- `logs/` — reproduced execution logs and per-case results

## Reproducing the checks

```bash
cd ~/workspace/msve-design
python3 -m m8.cli corpus              # 46 cases; expect "0 failures"
python3 -m m8.cli spec-examples       # 6 valid pass, 5 invalid rejected
python3 -m m8.cli grammar-conformance # expect OK, 48 productions
python3 -m m8.tests.test_canonical    # expect "all assertions hold"
```

Requires Python 3.12+; no third-party dependencies. Runtime captured in
`owner-review/logs/runtime.txt`.

## Most consequential remaining limitations

1. **M8 checks syntax/types, not semantics.** The D-028 contract logic,
   the injectivity argument, and the §B.4b table are paper — verified by
   review, not by execution.
2. **The "next unchecked layer" pattern held again.** The v0.8 correction
   pass itself yielded 24 new defects. Further layers may remain.
3. **No implementation exists.** No conformance or execution claims are made.
4. **Reviewer B's collision sweep** (2,998 values) was not preserved as an
   artefact; spelling-level uniqueness is otherwise covered by
   `test_canonical.py`.
5. **Reviewer independence is procedural.** Reviewers inherited parent
   context at spawn; A and D reports were extracted from session records.

## Evidence that could not be recovered

- Reviewer B's ad-hoc collision-sweep script (EVIDENCE_NOT_AVAILABLE).
- Reviewers' ad-hoc probe scripts beyond the preserved reports.
- Pre-fix gate logs (only the final post-correction state was logged).

## Proposed review order

1. M8 source, grammar mapping, and the reproduced run logs.
2. Design specification and regression ledger.
3. Reviewer findings and their corrections (traceability table).
4. Readiness evidence matrix.
5. Capability matrix, acceptance plan, visualisation plan.
6. Final owner decision.

## What this bundle does not do

It does not declare the design accepted, frozen, or implementation-ready.
Those are separate owner decisions, each requiring explicit authorisation.
