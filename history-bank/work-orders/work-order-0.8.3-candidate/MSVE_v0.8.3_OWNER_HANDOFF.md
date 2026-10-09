# MSVE v0.8.3 Owner Handoff

**Work Order:** 0.8.3 · **Date:** 2026-10-09
**Status:** CORRECTION CANDIDATE PREPARED — OWNER REVIEW PENDING

## What this package is

A correction candidate for the v0.8 design documents addressing findings
F-01–F-19 from your review of the Markdown transfer. Originals are
untouched; candidates live in `work-order-0.8.3-candidate/`.

## Documents

- `MSVE_v0.8.3_CORRECTION_REPORT.md` — per-finding dispositions.
- `MSVE_v0.8.3_RESIDUAL_DEFECT_LEDGER.md` — F-01–F-19 ledger (D-001–D-033
  and NEW-A/B/C/D histories preserved).
- `MSVE_v0.8.3_CROSS_DOCUMENT_MATRIX.md` — finding → location →
  correction → evidence → limitation.
- `MSVE_v0.8.3_VERIFICATION_EVIDENCE.md` — commands, exit statuses,
  F-03 derivation, and what remains specification-review-only.
- `MSVE_v0.8.3_PROVENANCE.md` — SHA-256 of all 100 candidate sources;
  F-19 historical limitation recorded.
- Six candidate design documents + candidate readiness matrix +
  candidate M8 (with 2 new corpus cases and 14 new test assertions).

## What was corrected vs not

- **Corrected (19/19 have dispositions):** all F-findings addressed;
  12 verified by executed M8 checks, 7 by specification review.
- **Not reproduced:** B's sweep, pre-fix states (unchanged gaps).
- **Requires your judgement:** F-03 derivation exactness; sufficiency of
  invariant 15b; joint satisfiability of the 23 invariants; whether this
  candidate becomes the new baseline.

## Checks run vs judgements remaining

- **Run:** corpus (48/48), spec-examples (11/11), grammar-conformance,
  both test modules — all green.
- **Judgement (specification-review-only):** F-02, F-03 wording, F-05,
  F-06, F-07, F-10, F-13, F-16, F-18.

No acceptance, freeze, implementation authorisation, or engine-correctness
claim is made by this package.
