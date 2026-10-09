# MSVE Capability Matrix v0.5

**Status:** DRAFT FOR REVIEW — NORMATIVE WHEN FROZEN WITH THE DESIGN SPEC
**Version:** 0.5 · **Design spec:** `MSVE_DESIGN_SPEC_v0.5.md`
**Supersedes:** `MSVE_CAPABILITY_MATRIX_v0.4.md` (retained as historical draft)

Two independent fields per capability:
- **Target disposition:** SUPPORTED · RESTRICTED · UNSUPPORTED · FUTURE · FORBIDDEN.
- **Maturity:** Designed · Implemented · Functionally verified · Formally verified
  (or N/A with reason) · Integrated and reproducible · Independently reproduced ·
  Released. Every v0.5 entry is at **Designed**.

---

## 1. Computation and symbolic mathematics

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| C1 | Exact integer arithmetic (arbitrary precision) | SUPPORTED | Designed | Bit-exact; derivation record; Level A via independent recomputation |
| C2 | Exact rational arithmetic | SUPPORTED | Designed | As C1; `RealLit` exact decimals |
| C3 | Floating-point evaluation | RESTRICTED | Designed | Declared approximation with error bounds only; no `Binary64` literals in v0 |
| C4 | Symbolic computation (SymPy-backed) | SUPPORTED | Designed | Computed / checkable / trusted-tool output distinguished |
| C5 | Symbolic solving | RESTRICTED | Designed | Where substitution-checked; else INCONCLUSIVE with reason |
| C6 | Assumption-aware queries | SUPPORTED | Designed | Three-valued: true / false / unknown |

## 2. Constraint solving and model reasoning

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| M1 | Satisfiability, decidable fragments | SUPPORTED | Designed | Sound+complete within the named fragment |
| M2 | Model generation (witnesses) | SUPPORTED | Designed | Re-checked vs canonical spec |
| M3 | Unsat-core extraction | SUPPORTED | Designed | Diagnostic only |
| M4 | Nonlinear / quantified / general SMT | RESTRICTED | Designed | Declared limits; unknown → INCONCLUSIVE(SOLVER_UNKNOWN) |
| M5 | Uniqueness via model-negation re-solve | SUPPORTED | Designed | Explicit model type; exact canonical projection equality; Level B in v0 |
| M6 | Second-model / counterexample search | SUPPORTED | Designed | Declared projection on explicit model type |
| M7 | Projection-relative distinctness | SUPPORTED | Designed | Exact equality; no tolerance equivalence |

## 3. Proof and formal verification

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| P1 | Proof-term checking (Lean kernel) | SUPPORTED | Designed | Level A eligible; relative to formal statement/definitions/imports/axioms |
| P2 | Formalization of frozen spec | RESTRICTED | Designed | Human-reviewed; adequacy as assumption |
| P3 | Tactic-driven proof search | RESTRICTED | Designed | Discovery only |
| P4 | Implementation-contract assurance | SUPPORTED | Designed | L1/L2/L3; `check` goals corpus-bound (empty corpus → INCONCLUSIVE(NO_TEST_CORPUS)); universal impl claims need L2 |
| P5 | Universal claims from finite suites alone | UNSUPPORTED | — | Never a universal proof |

## 4. Construction and implementation generation

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| G1 | Template-based code generation | RESTRICTED | Designed | Structural-recursion templates (spec §D.5); L1 obligations; L2 re-check. Out of scope for first slice |
| G2 | Silent gap-filling | FORBIDDEN | — | Rejected, never completed |
| G3 | Natural-language direct execution | FORBIDDEN | — | Unreviewed NL assumptions NEVER executable |

## 5. Evidence classification and recording

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| E1 | Result records per the typed schema | SUPPORTED | Designed | All schema types structurally defined (§E.1): ErrorCode, SemanticResult (Option), ReasonCode (+NO_TEST_CORPUS), SolverObs, VerificationRecord, EvidenceBundle, ArtifactRef, ExternalEvidence, PartialResult, Discrepancy; divergence-first aggregation |
| E2 | External experimental evidence | SUPPORTED | Designed | EVIDENCE_RECORDED / RECORD_INTEGRITY / EXTERNAL_ASSESSMENT |
| E3 | Provenance packaging | SUPPORTED | Designed | Four claims separated; `msve-canonical-1`: no bare JSON numbers; nat/int/rat/f64 + records/lists/sets/options/bools/strings/impl/blob encodings; `Real` excluded from hashed artifacts (explicit); "tamper-evident relative to a trusted reference" |
| E4 | Re-verification; supersede marking | SUPPORTED | Designed | Superseded, never deleted |

## 6. Explicitly out of scope / forbidden

| # | Capability | Target | Reason |
|---|---|---|---|
| X1 | Inferring missing historical data | FORBIDDEN | Would manufacture facts |
| X2 | Predicting real-world performance from formal correctness | UNSUPPORTED | Category error |
| X3 | Inventing objective functions | UNSUPPORTED | Domain judgment |
| X4 | Arbitrary scientific discovery | UNSUPPORTED | Outside formal scope |
| X5 | Certifying MSVE by MSVE alone | UNSUPPORTED | Independent checkers required |
| X6 | Executing unreviewed specifications | FORBIDDEN | Freeze-and-review gate |
| X7 | Automatic discovery of uniqueness-restoring assumptions | UNSUPPORTED | User-supplied / finite-family only |

## 7. Maturity ladder (unified vocabulary)

1. **Designed** · 2. **Implemented** · 3. **Functionally verified** ·
4. **Formally verified** (or N/A with recorded reason) ·
5. **Integrated and reproducible** · 6. **Independently reproduced** ·
7. **Released**. Sequential 1–3, 5; 4 may be N/A; 6 requires 5; 7 requires all
applicable prior stages. "All-rounder within scope S, matrix vX.Y" earned only
at stage 7 with evidence.

*End of MSVE_CAPABILITY_MATRIX_v0.5.md (draft for review).*
