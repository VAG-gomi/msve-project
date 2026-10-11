# Consistency and Verification Report — Candidate 0.8.9 (WO-1.9)

## Specification ↔ model agreement

| Scope item | Spec | Model | Agreement |
|---|---|---|---|
| D1 weak chain | §E.5 (A1) | Inv 30 | Yes — model W1/W2 |
| D2 bar before D1 | §E.5 (A2) | Inv 31 | Yes — model W3/W3b |
| D3 fragment scope | §E.4a + schema doc | Inv 32 | Yes — model W4 |
| D4 checker constraints | §E.6a (A4) | Inv 33 | Yes — model W5 |
| D5 capacity | §B.8a (A5) | Inv 34 | Yes — model W6 |
| D6 identity | §E.6b (A6) | Inv 35 (version only) | Partial — byte framing verified by Python vectors, not Z3 (documented limit) |

**Properties the model cannot express:** byte-level framing details of
`msve-descriptor-1` (verified instead by 16 golden vectors + 15 identity
tests); the `claim_query_link: UNVERIFIED` semantic boundary (a negative
claim about correspondence, verified by code inspection + contract).

## Formal validation results

- Driver: `run_audit_0889.py`; **17/17 checks behaved as expected**
  (9 retained 0.8.8.1 + 8 new W1–W7).
- Log: `model_audit_0889.log` (this directory).
- Z3 5.1.0; per-scenario timeout 30s.

## Prototype verification results

- Full suite: **128/128 passed** (114 pre-existing + 14 new), 8.3s.
- Genuine UNKNOWN experiment: reproduced (UNKNOWN/timeout →
  INCONCLUSIVE + weak SOLVER_BACKED).
- 16/16 golden vectors match under `msve-descriptor-1`.
- No test success manufactured; no expected outputs altered to hide
  discrepancies (the 7 recomputed vectors changed because the encoding
  changed — documented as the A6 transition, not a fix-up).

## Contract ↔ runtime agreement

- Error codes: contract and runtime both use `INVALID_INPUT` (A5
  reconciliation complete; `INVALID_CONFIG` retired everywhere).
- Capacity values: contract, `config/default.json`, and `capacity.py`
  agree (10000/1000).
- Encoding: contract, `ENCODING.md`, and `identity.py` agree
  (`msve-descriptor-1`).
- D3: contract §3/§10 and `D3_SOLVER_FRAGMENT_SCHEMA.md` agree
  (assumptions non-semantic metadata; link UNVERIFIED).

## What was not verified

- Universal collision resistance of `msve-descriptor-1` (finite vectors
  only; not claimed).
- Portability of timeout-induced UNKNOWN across Z3 versions/platforms.
- Common-mode failure elimination by checker independence (trust
  boundary, disclosed).
