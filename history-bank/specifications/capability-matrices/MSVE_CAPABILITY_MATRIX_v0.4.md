# MSVE Capability Matrix v0.4

**Status:** DRAFT FOR REVIEW — NORMATIVE WHEN FROZEN WITH THE DESIGN SPEC
**Version:** 0.4 · **Design spec:** `MSVE_DESIGN_SPEC_v0.4.md`
**Supersedes:** `MSVE_CAPABILITY_MATRIX_v0.3.md` (retained as historical draft)

Two independent fields per capability:
- **Target disposition:** SUPPORTED · RESTRICTED · UNSUPPORTED · FUTURE · FORBIDDEN.
- **Maturity:** Designed · Implemented · Functionally verified · Formally verified
  (or N/A with reason) · Integrated and reproducible · Independently reproduced ·
  Released. Every v0.4 entry is at **Designed** — the engine is not implemented.

---

## 1. Computation and symbolic mathematics

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| C1 | Exact integer arithmetic (arbitrary precision) | SUPPORTED | Designed | Bit-exact; derivation record; Level A eligible via independent recomputation |
| C2 | Exact rational arithmetic | SUPPORTED | Designed | As C1 |
| C3 | Floating-point evaluation | RESTRICTED | Designed | Only as declared approximation with error bounds; never exact |
| C4 | Symbolic expression construction/simplification (SymPy-backed) | SUPPORTED | Designed | Computed / checkable / trusted-tool output distinguished (spec §F) |
| C5 | Symbolic solving | RESTRICTED | Designed | Where substitution-checked; else INCONCLUSIVE with reason |
| C6 | Assumption-aware queries | SUPPORTED | Designed | Three-valued: true / false / unknown (never coerced) |

## 2. Constraint solving and model reasoning

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| M1 | Satisfiability checking, decidable fragments (e.g. QF_LIA) | SUPPORTED | Designed | Sound+complete within the named fragment |
| M2 | Satisfying-model generation (witnesses) | SUPPORTED | Designed | Re-checked vs canonical spec independently of solver |
| M3 | Unsatisfiable-core extraction | SUPPORTED | Designed | Diagnostic only — never an independent proof |
| M4 | Nonlinear / quantified / general SMT | RESTRICTED | Designed | Declared limits; unknown → INCONCLUSIVE(SOLVER_UNKNOWN) |
| M5 | Uniqueness checking via model-negation re-solve | SUPPORTED | Designed | Decidable fragments; exact canonical projection equality; Level B in v0 |
| M6 | Second-model / counterexample search | SUPPORTED | Designed | Declared projection; witnesses with differing projected properties |
| M7 | Projection-relative distinctness | SUPPORTED | Designed | Exact equality on canonical forms; no tolerance equivalence |

## 3. Proof and formal verification

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| P1 | Proof-term checking via small trusted kernel (Lean) | SUPPORTED | Designed | Level A eligible; acceptance relative to formal statement/definitions/imports/axioms |
| P2 | Formalization of frozen spec into prover logic | RESTRICTED | Designed | Human-reviewed; adequacy recorded as assumption |
| P3 | Tactic-driven proof search | RESTRICTED | Designed | Discovery only; kernel-accepted terms count as PROVED |
| P4 | Implementation-contract assurance | SUPPORTED | Designed | L1/L2/L3 separated; L1 alone proves nothing about code; `check` goals are corpus-bound L3 (spec §B.5b) |
| P5 | Universal claims from finite suites alone | UNSUPPORTED | — | Never a universal proof |

## 4. Construction and implementation generation

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| G1 | Template-based code generation | RESTRICTED | Designed | Structural-recursion templates over finite lists/collections (spec §D.5); comparator/total-order obligations discharged at L1; output re-checked (L2). Finite collection ≠ finite domain ≠ unbounded class of finite collections. General generation: FUTURE |
| G2 | Silent gap-filling during generation | FORBIDDEN | — | Under-specified inputs rejected, never completed |
| G3 | Natural-language direct execution | FORBIDDEN | — | Unreviewed NL assumptions NEVER enter executable specs |

## 5. Evidence classification and recording

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| E1 | Result records per the typed schema | SUPPORTED | Designed | `semantic_result` optional (absent when admission fails); solver observations; assurance triple; per-property records with divergence-first aggregation (§E.6) |
| E2 | External experimental evidence handling | SUPPORTED | Designed | EVIDENCE_RECORDED / RECORD_INTEGRITY / EXTERNAL_ASSESSMENT; never promoted by MSVE |
| E3 | Provenance packaging | SUPPORTED | Designed | Identity / integrity-vs-reference / authenticity / correctness separated; `msve-canonical-1`: no bare JSON numbers; typed nat/int/rat/f64 objects; Real excluded from hashed artifacts; "tamper-evident relative to a trusted reference" |
| E4 | Re-verification; supersede marking | SUPPORTED | Designed | Prior results superseded, never deleted |

## 6. Explicitly out of scope / forbidden

| # | Capability | Target | Reason |
|---|---|---|---|
| X1 | Inferring missing historical data | FORBIDDEN | Would manufacture facts |
| X2 | Predicting real-world performance from formal correctness | UNSUPPORTED | Category error; needs empirical evidence |
| X3 | Inventing objective functions | UNSUPPORTED | Domain judgment; belongs in the spec |
| X4 | Arbitrary scientific discovery | UNSUPPORTED | Outside formal scope |
| X5 | Certifying MSVE by MSVE alone | UNSUPPORTED | Independent checkers required |
| X6 | Executing unreviewed specifications | FORBIDDEN | Freeze-and-review gate |
| X7 | Automatic discovery of uniqueness-restoring assumptions | UNSUPPORTED | Only user-supplied / declared-finite-family candidates |

## 7. Maturity ladder (unified vocabulary)

1. **Designed** — contract written; failure behaviour specified; in this matrix.
2. **Implemented** — exists with documented interface; versioned.
3. **Functionally verified** — acceptance suite (normal, boundary, expected-failure) green and recorded.
4. **Formally verified** — kernel-checked proof or sound procedure + artifacts;
   or **N/A with recorded reason** — never misleadingly labelled.
5. **Integrated and reproducible** — composes with declared components; versions
   pinned; re-runs reproduce.
6. **Independently reproduced** — separate party/machine reproduces from the
   package alone. (Distinct from 5: composition vs independent confirmation.)
7. **Released** — matrix entries at claimed maturity; limitations documented;
   scope+version-qualified claims evidenced.

Stages 1–3, 5 sequential; 4 may be N/A (recorded); 6 requires 5; 7 requires all
applicable prior stages. "All-rounder within scope S, matrix vX.Y" is earned
only at stage 7 with evidence — never bare.

*End of MSVE_CAPABILITY_MATRIX_v0.4.md (draft for review).*
