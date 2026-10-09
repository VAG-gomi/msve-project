# VERSION_LINEAGE.md

How MSVE artifacts relate across versions. Superseded versions are preserved,
not deleted. "Supersedes" means the later version was produced as a correction
or revision of the earlier; it does not mean the earlier was wrong in every
respect.

## Specification lineage

```
v0.1 → v0.2 → v0.3 → v0.4 → v0.5 → v0.6 → v0.7 → v0.8 (top-level, 377e106e…)
                                                              │
                              ┌───────────────────────────────┘
                              ▼
              0.8.3 candidate spec (F-01–F-19 corrections)
                              │
              0.8.6 candidate spec (F-20 + F-21: invariant 10 fix, §E.6a, invariants 24–28)
                              │
              0.8.7 candidate spec (F-22–F-27; R1-1 claim-key repair)
                              │
              0.8.8 candidate spec (Option A: ClaimDescriptor, stored claim_id,
                                    solver_invocations, invariant 29)
                              │
              0.8.8.1 candidate spec (claim_kind, spec_version, outcome_compatible,
                                      unresolved-kind handling) = dbc610c3… ← CURRENT CANDIDATE
```

- The top-level `MSVE_DESIGN_SPEC_v0.8.md` (`377e106e…`) is the pre-0.8.3
  document. It is a distinct original, not a copy of the candidate.
- Each candidate spec lives inside its work-order directory; the current
  candidate is additionally archived at `candidate/0.8.8.1/`.

## Model lineage

| File | Location | Relation |
|---|---|---|
| `audit_model.py` | work-order-0.8.4-audit/ | First Z3 formalization of §E.7 invariants (23 invariants) |
| `audit_model_086.py` | work-order-0.8.6 / 0.8.7 | Extended model (31 constraints; invariants 24–28) |
| `audit_model_087.py` | work-order-0.8.7-candidate/ | R1-1 repair (claim key for payload-free variants) |
| `audit_model_088.py` | work-order-0.8.8-candidate/ | Option A (ClaimDescriptor, stored claim_id) |
| `audit_model_0881.py` | work-order-0.8.8.1 + `candidate/0.8.8.1/` | Final: claim_kind, spec_version, outcome_compatible (`fc6eb49f…`) |

Companion drivers `run_audit*.py` / `f20_adjudication.py` /
`f21_assurance_tests.py` / `dump_*.py` are preserved alongside their models.

## Document-set lineage

Each version v0.1–v0.8 produced a consistent document set: design spec,
capability matrix, acceptance plan, visualisation plan, design review
(v0.6+ also: regression ledger). All sets are preserved under
`specifications/`. The v0.8 set was additionally revised inside the
0.8.3 and 0.8.6 candidate directories.

## Review lineage

- v0.1–v0.5: self-reviews + ChatGPT external text reviews (summaries only).
- v0.6/v0.7: ChatGPT forensic/adversarial reviews → gate BLOCKED (summaries only).
- v0.8: four independent reviewers A–D, full reports preserved
  (`reviews-and-audits/owner-review/reviewer-reports/`).
- 0.8.8 / 0.8.8.1: independent normative + formal-model reviews, full
  reports preserved in the respective work-order directories.

## Known defect → repair mapping (summary)

D-001–D-033 (v0.6/v0.7 rounds) → repaired across 0.8/0.8.3;
F-01–F-19 (owner findings) → 0.8.3; F-20 (packaging) → 0.8.6;
F-21 (assurance linkage) → 0.8.6; F-22–F-27 → 0.8.7;
R1-1 (claim key) → 0.8.7; N-1/2/3, F1/F2 → 0.8.8;
N-0.8.8.1-1/2/3, M1 → 0.8.8.1. Full detail in the continuity export
(`records/continuity-export-01/02_FINDING_AND_CORRECTION_LEDGER.md`).
