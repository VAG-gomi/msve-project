# MSVE v0.8.6 Cross-Document Matrix

**Work Order:** 0.8.6 · **Date:** 2026-10-09
Candidate documents vs. the F-20/F-21 corrections.

| Document | Change in 0.8.6 | Detail |
|---|---|---|
| Design specification | **Normative** | §E.6a new (assurance-evidence linkage definitions); §E.7 invariant 10 corrected (F-20, fully bound variables, `is_packaging_error`); invariants 24–28 new (F-21) |
| Design review | None | Historical ChatGPT review preserved unchanged |
| Capability matrix | None | No capability scope change |
| Acceptance plan | **Checks added** | F-20/F-21 model-level cases; explicit model-vs-engine evidence distinction |
| Visualisation plan | None | No diagram affected (invariants 10, 24–28 are record constraints, not flow changes) |
| Regression ledger | **Entries added** | F-20 (resolved), F-21 (finding + resolution); D-001–D-033 and NEW-A/B/C/D preserved |
| Readiness evidence matrix | None | Readiness claims unchanged; new invariants are additive constraints |
| Defect traceability | **Entries added** | F-20, F-21 traced to §E.7/§E.6a |

## Invariant → document trace

| Invariant | Spec §E.7 | Ledger | Acceptance plan | Matrix |
|---|---|---|---|---|
| 10 (F-20 corrected) | ✓ | F-20 | F-20 cases | — |
| 24 (Level A result) | ✓ | F-21 | F-21 cases | — |
| 25 (proof evidence) | ✓ + §E.6a | F-21 | F-21 cases | — |
| 26 (recompute evidence) | ✓ + §E.6a | F-21 | F-21 cases | — |
| 27 (solver evidence) | ✓ | F-21 | F-21 cases | — |
| 28 (test evidence) | ✓ | F-21 | F-21 cases | — |

## Preservation

D-001–D-033, NEW-A/B/C/D findings, and the F-20/F-21 resolution
histories are preserved without erasure. The 0.8.3 candidate, 0.8.4
audit, 0.8.5 reconciliation, and 0.8.5.2 reports are unchanged.
