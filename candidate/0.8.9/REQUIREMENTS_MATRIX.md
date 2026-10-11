# Requirements → Model → Code → Test Matrix — D1–D9 (Candidate 0.8.9)

Each row traces an owner ruling through the normative requirement, the
formal model, the prototype implementation, and the verifying tests.

| Ruling | Normative requirement (0.8.9) | Formal model | Prototype code | Tests |
|---|---|---|---|---|
| D1 | §E.5: UNKNOWN+INCONCLUSIVE → weak SOLVER_BACKED; never positive; bound to claim/query/specver (A1) | Inv 30: WEAK_SOLVER_BACKED → UNKNOWN ∧ INCONCLUSIVE ∧ ¬HOLDS ∧ ¬VIOLATED | `assurance.py::award()` (weak chain); `pipeline.py` (observation binding) | Model W1/W2; `test_wo19_amendments.py::test_a1_*`; `test_unknown_experiment.py` |
| D2 | §E.5: seven kinds barred from SOLVER_BACKED (weak or strong), before D1 (A2) | Inv 31: seven kinds → ¬SOLVER_BACKED ∧ ¬WEAK | `admission.py:48`; `assurance.py:23,74` | Model W3/W3b; `test_wo13_hardening.py` (14) |
| D3 | §E.4a + `D3_SOLVER_FRAGMENT_SCHEMA.md`: msve-arith-v1 schema; assumptions non-semantic metadata; claim_query_link UNVERIFIED | Inv 32: solver-backed → query_language = msve-arith-v1 | `queries.py` (grammar/types/denotation); `result.py:22` | Model W4; `test_wo19_amendments.py::test_d3_*`; `test_solver.py` |
| D4 | §E.6a: independent checker core; disclosed sharing; lineage; witness for SAT; no-witness → INCONCLUSIVE (A4) | Inv 33: INDEPENDENT_RECOMPUTE → checker_independent ∧ witness_checkable | `checker.py` (0 z3 refs); `DEPENDENCIES.md` | Model W5; `test_checker.py`; `experiments/checker_xval/` |
| D5 | §B.8a: capacity params, defaults, ranges, precedence, INVALID_INPUT, explicit overflow failure (A5) | Inv 34: 1 ≤ records ≤ 1M; 1 ≤ descriptors ≤ 100k | `capacity.py`; `config/default.json` | Model W6; `test_wo19_amendments.py::test_a5_*` (5) |
| D6 | §E.6b: msve-descriptor-1 (tags, u32be, count, sort, NFC, version binding) (A6) | Inv 35: claim_id → encoding = msve-descriptor-1 | `identity.py`; `ENCODING.md` | Model W7; `test_wo19_amendments.py::test_a6_*` (5); 16 vectors |
| D7 | Gates per WO-1.8 (unchanged by this WO) | — (governance, not modelable) | — | WO-1.8 report |
| D8 | All outputs experimental:true (unchanged) | — | `result.py:11` | `test_pipeline.py::test_experimental_flag` |
| D9 | Two-repo separation (unchanged) | — | repo layout | WO-1.7/1.8 audits |

**Amendment decisions:** DEC-027 (A1), DEC-028 (A2), DEC-029 (A4),
DEC-030 (A5), DEC-031 (A6), DEC-032 (D3 scope A) — all ACCEPTED-BY-OWNER.
