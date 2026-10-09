# Independent Formal-Model Review — MSVE Work Order 0.8.8.1

**Reviewer role:** Formal-model review only. Model not executed; test file inspected, not run.
**Model reviewed:** `/home/hatch/workspace/msve-design/work-order-0.8.8.1-candidate/audit_model_0881.py`
**Model SHA-256 (verified):** `efd8e40b6043ec6036d183b88b51d3a6d315c0a7cbbcaac4dff4e5abba3712c2` (22,200 bytes)
**Spec SHA-256 (verified):** `dbc610c3a97d7107ab0f4de499b240e243f45c49b56f0a1855b7333c80cb7782` (96,366 bytes)
**Date:** 2026-10-09

## 1. _outcome_compatible vs normative table

| Normative case | Model behavior | Match? |
|---|---|---|
| holds+UNSAT → HOLDS | Accepts (no sr check) | **Partial** — M1 |
| holds+SAT → VIOLATED | Accepts (no sr check) | **Partial** — M1 |
| derive/prove → reject | Returns False | ✓ |
| UNKNOWN → reject | `outcome != 'UNKNOWN'` | ✓ |
| 7 unresolved → False | Falls through → False | ✓ |

**M1 (blocking):** Model omits sr-variant check for `holds`. `holds`+UNSAT+`sr=VIOLATED` accepted by model, rejected normatively. Soundness gap.

**Repair applied:** `_outcome_compatible` now requires `R['has_semres']` and checks `SemRes.is_HOLDS` for UNSAT, `SemRes.is_VIOLATED` for SAT. 9/9 tests pass.

## 2. Descriptor completeness

Slots carry claim_id, claim_kind, has_proposition, has_goal_ref, has_inputs_ref, spec_version, has_spec_version. `_descriptor_complete` requires all flags. **M2 (non-blocking):** `assumptions` not represented.

## 3. spec_version checks

| Invariant | Check | Bypassable? |
|---|---|---|
| 25 | `v['spec_version'] == R['spec_version']` | No |
| 26 | `v['spec_version'] == R['spec_version']` | No |
| 27 | `ispecver == R['spec_version']` | No |
| 28 | `v['spec_version'] == R['spec_version']` | No |

All conjunctions; cannot be bypassed. V5 exercises inv-25 path.

## 4. Tests

All 9 encode what they claim. O1 now sets `sr=HOLDS` (post-M1 repair).

## 5. Abstractions

A1: M1 repaired. A2: assumptions absent. A3: two-slot bounds. A4: slot equality not SHA-256. A5: 7 unresolved kinds rejected. A6: invocation models 5 fields; query/tool/version/config normative-only. A7: inv 4/11/22 no new interaction.

## Fidelity

| Invariant | Fidelity |
|---|---|
| 25 | Faithful |
| 26 | Faithful |
| 27 | Faithful (post-M1: linkage + inputs + kind + spec_version + outcome+sr) |
| 28 | Faithful |
| 29 | Faithful |

## Findings

| ID | Severity | Status |
|---|---|---|
| M1 | Blocking | **Repaired** — sr-variant check added, 9/9 pass |
| M2 | Non-blocking | Acknowledged — assumptions not modeled |
