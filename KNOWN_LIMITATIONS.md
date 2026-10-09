# KNOWN_LIMITATIONS.md

Disclosed limits of the 0.8.8.1 candidate. Keep the epistemic categories
distinct: verified claims, reviewer judgements, attestations, and unresolved
items are not interchangeable.

## Attested / not mechanically verifiable

- **Checker independence:** that a recomputation checker is independent of
  the producer is attested via `vr.checker`, not established by the schema.
- **Checker authorisation:** that a checker string names an authorized
  kernel is attested, not checked.
- **Query fidelity:** that a solver `query` faithfully encodes the claimed
  proposition is attested; the outcome table does not bind outcome to query
  interpretation.
- **Solver execution:** that the solver actually ran the recorded query is
  attested; the model sees only the recorded observation.

## Partially modelled

- **Canonical identity:** `claim_id = sha256(canonical_encoding)` is
  normative; the model uses slot equality as a proxy and does not recompute
  the hash. The 9/9 result does not demonstrate mechanical verification of
  canonical identity.
- **Assumptions:** the descriptor's `assumptions` field is normative but not
  represented in the model (M2). Two claims differing only in assumptions
  are not shown distinct by the model.
- **Serialization:** the canonical encoding `kind|proposition|goal_ref|inputs_ref|assumptions|spec_version`
  lacks a precise escaping rule for arbitrary proposition/assumption content.

## Bounded

- Two verification records, two descriptor slots, two solver invocations per
  result record. A third of any is unrepresentable in the model.

## Unresolved (see OPEN_DECISIONS.md)

- Seven claim kinds without defined outcome interpretation.
- UNKNOWN outcome policy divergence.

## What the evidence does establish

- 9/9 regression tests pass on the final file hashes (reported verification,
  raw log preserved).
- All blocking independent-review findings were repaired and re-verified,
  including model re-inspection on the final hash.
- Historical defect trace from v0.8 through 0.8.8.1 is documented in
  `records/continuity-export-01/`.
