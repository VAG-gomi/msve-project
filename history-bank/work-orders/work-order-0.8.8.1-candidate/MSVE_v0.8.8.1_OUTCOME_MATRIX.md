# MSVE v0.8.8.1 — Outcome Compatibility Matrix

**Normative source:** Spec §E.6b `outcome_compatible` definition.
**Model:** `audit_model_0881.py` `_outcome_compatible`.

| claim_kind | Outcome | Allowed conclusion | Normative | Mechanically enforced | Test |
|---|---|---|---|---|---|
| holds | UNSAT | HOLDS | Yes | Yes (O1) | O1 |
| holds | SAT | VIOLATED{witness} | Yes | Partial (SAT allowed, VIOLATED not modeled) | — |
| holds | UNKNOWN | INCONCLUSIVE only | Yes | Yes (O2 rejects) | O2 |
| derive | any | INCONCLUSIVE only (diagnostic) | Yes | Yes (O3 rejects) | O3 |
| prove | any | INCONCLUSIVE only (diagnostic) | Yes | Yes (same as derive) | — |
| (other) | any | False | Yes | Yes (falls through) | — |

**Labels:**
- O1: normatively defined, mechanically enforced, exercised, independently reviewed (pending).
- O2/O3: normatively defined, mechanically enforced, exercised.
- holds+SAT→VIOLATED: normatively defined; witness structure not modeled (attested).
