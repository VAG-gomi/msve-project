# MSVE v0.8.8.1 — Descriptor Completeness Matrix

**Normative:** ClaimDescriptor requires claim_kind, proposition, goal_ref,
inputs_ref, spec_version (assumptions may be []).

| Field | Normative | Model enforcement | Test |
|---|---|---|---|
| claim_id (stored) | Yes | Yes (slot match) | C2 |
| claim_kind | Yes | Yes (`_descriptor_complete` via kind match) | O1 |
| proposition | Yes (mandatory) | Yes (`has_proposition` flag) | D4 |
| goal_ref | Yes (mandatory) | Yes (`has_goal_ref` flag) | D4 |
| inputs_ref | Yes (mandatory) | Yes (`has_inputs_ref` flag) | D4 |
| assumptions | May be [] | Not modeled (always satisfiable) | — |
| spec_version | Yes (mandatory) | Yes (`has_spec_version` + equality) | V5 |

**Rejection cases:**
- Missing descriptor when basis claimed: Yes (C4 in 0.8.8; inv 29).
- Missing mandatory field: Yes (D4).
- Uncomputable identity: Modeled as missing field (sha256 not computed in Z3; presence flags proxy).
- Provenance to different identity: Yes (S9 in 0.8.8).

**Labels:** All normatively defined, mechanically enforced (except assumptions),
exercised by tests, pending independent review.
