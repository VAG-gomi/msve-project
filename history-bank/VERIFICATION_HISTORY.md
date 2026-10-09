# VERIFICATION_HISTORY.md

Historical verification claims and the evidence behind them. This work order
(MSVE-HISTORY-001) did **not** re-execute any model or test suite. File
enumeration, hashing, and integrity checks were performed; application code
was not executed.

## Claim 1 — 0.8.8.1 final regression: 9/9 pass

- **Status:** REPORTED, with surviving raw log.
- **Evidence:** `candidate/0.8.8.1/run_audit_0881_raw.log` (852 bytes,
  `525cd406…`), recorded 2026-10-09T14:52:51Z, Python 3.12.3, Z3 5.1.0,
  exit 0. Tests: R1, C2, C3, O1, O2, O3, D4, V5, D6.
- **Limitation:** `sat_models_0881.json` stores truncated model strings, not
  complete assignments. Execution evidence for the identified files, not
  evidence of real-world mathematical correctness.
- **Attribution:** work order 0.8.8.1-FINAL. Not independently reproduced here.

## Claim 2 — 0.8.4 invariant audit: 45/46 checks as expected

- **Status:** REPORTED, with surviving scripts and partial outputs.
- **Evidence:** `work-orders/work-order-0.8.4-audit/` — model, driver,
  raw stdout excerpts, witness catalog; reconciliation in 0.8.5 records
  (31 SAT, 14 expected-UNSAT, 1 joint-query `unknown` honestly preserved).
- **Limitation:** invariants 3/12 unformalizable (external refs);
  20/21/23 weakened; the joint `unknown` is a solver search limit, not a
  result.

## Claim 3 — 0.8.7: 18/18 pass

- **Status:** REPORTED with a chronological caveat.
- **Evidence:** `work-orders/work-order-0.8.7-candidate/run_audit_087_raw.log`
  (14:05:48Z).
- **Limitation (CONFLICTING with any claim it verifies the final 0.8.7
  bytes):** the log predates the final R1-driven model change (~14:08Z).
  It cannot verify the final 0.8.7 model bytes. The post-change full stdout
  was not preserved (UNAVAILABLE).

## Claim 4 — M8 corpus: 46/46 + spec examples

- **Status:** REPORTED.
- **Evidence:** `models-and-validators/m8/` (tool, corpus of 65 cases,
  tests), run records in `m8/runs/`, logs in
  `reviews-and-audits/owner-review/logs/`.
- **Limitation:** not re-executed here.

## Claim 5 — Four independent reviewers (A–D) on v0.8

- **Status:** ORIGINAL-PRESERVED (full reports).
- **Evidence:** `reviews-and-audits/owner-review/reviewer-reports/`
  (reviewer-A through D plus PROVENANCE.md).
- **Limitation:** reviewer reports do not record the exact spec hashes they
  inspected; interleaving with later corrections is not cryptographically
  anchorable (documented in the 0.8.3 correction report).

## Claim 6 — 0.8.8 / 0.8.8.1 independent normative + model reviews

- **Status:** ORIGINAL-PRESERVED (full reports in work-order directories).
- **Evidence:** `MSVE_v0.8.8_NORMATIVE_REVIEW.md`,
  `MSVE_v0.8.8_MODEL_REVIEW.md`, `MSVE_v0.8.8.1_NORMATIVE_REVIEW.md`,
  `MSVE_v0.8.8.1_MODEL_REVIEW.md`, reconciliation records.
- **Note:** the 0.8.8.1 model re-inspection was performed on the final hash
  (`fc6eb49f…`) — the strongest verification linkage in the project.

## Claims NOT made

- No claim that any Z3 result establishes real-world mathematical truth
  about an engine (no engine exists).
- No claim that a passing test at one layer verifies another layer.
- No claim that reported results were independently reproduced during
  archival.
