# MSVE v0.8.7 — Work 1: Assurance-Basis Coverage Matrix (F-22)

**Adjudication:** Every item in `assurance_bases` is an asserted basis
and must be substantiated, regardless of the achieved level. This is the
preferred reading; it is consistent with §E.6a ("a basis is a claim, not
evidence", not level-restricted) and resolves the F-22 gap where Level B
records could claim strong bases without evidence.

## Coverage matrix

| Basis | LEVEL_A | LEVEL_B | Result-type scope | Evidence (revised invariant) |
|---|---|---|---|---|
| KERNEL_PROOF | Inv 6 requires it (or RECOMPUTE); substantiation required | Allowed; if claimed, substantiation required | Any result with a provable claim | Rev. 25: proof record, method="kernel-checked", property=claim key, artifact hash resolves |
| INDEPENDENT_RECOMPUTE | Inv 6 requires it (or KERNEL_PROOF) for derive goals; substantiation required | Allowed; if claimed, substantiation required | DERIVED_VALUE only (§E.5); non-DERIVED_VALUE + this basis → rejected | Rev. 26: compatibility rule + recompute record with claim linkage |
| SOLVER_BACKED | Not sufficient for Level A (§E.5: no Level A pipeline for solver-backed goals) | Allowed; substantiation required | Any | Rev. 27: solver observation present; outcome-consistency via inv 4/11/22 |
| TEST_BACKED | Not sufficient for Level A (§E.5) | Allowed; substantiation required | Any | Rev. 28: passing test record with property=claim key |

## Prohibited combinations

- `INDEPENDENT_RECOMPUTE ∈ assurance_bases` with `semantic_result`
  not `Some(DERIVED_VALUE{…})` → violates revised invariant 26
  (recomputation is the `derive`-goal Level A path per §E.5; no silent
  extension to other types).
- Any basis in `assurance_bases` without its required substantiation →
  violates the corresponding revised invariant, at any achieved level.

## Unresolved limitations

- Checker independence (recomputation) remains attested via `checker`
  ID, not mechanically derivable (no primary-producer field).
- Whether a specific checker ID is an *authorized* kernel checker is
  not represented in the record schema; `method = "kernel-checked"` is
  the machine-checked condition.
- `INCONCLUSIVE` results have no provable claim; no basis
  substantiation applies (invariant 24 already forbids Level A there).
