# MSVE Capability Matrix v0.1

**Status:** DRAFT FOR REVIEW — NORMATIVE WHEN FROZEN WITH THE DESIGN SPEC
**Version:** 0.1 · **Design spec:** `MSVE_DESIGN_SPEC_v0.1.md`

This matrix is the normative definition of every capability claim MSVE v0 may
make. A capability not listed here is not claimed. A capability listed as
restricted/unsupported must be labelled as such in every release.

Dispositions: **SUPPORTED** · **RESTRICTED** · **UNSUPPORTED** · **FUTURE** ·
**FORBIDDEN** (hard rule — must never be implemented).

---

## 1. Computation and symbolic mathematics

| # | Capability | Disposition | Guarantee / boundary |
|---|---|---|---|
| C1 | Exact integer arithmetic (arbitrary precision) | SUPPORTED | Bit-exact results; derivation record |
| C2 | Exact rational arithmetic | SUPPORTED | Bit-exact results; derivation record |
| C3 | Floating-point evaluation | RESTRICTED | Allowed only as explicitly declared approximation with error bounds; never presented as exact |
| C4 | Symbolic expression construction and simplification (SymPy-backed) | SUPPORTED | Within SymPy's algorithms; simplification steps recorded |
| C5 | Symbolic solving (equation systems, closed forms) | RESTRICTED | Where SymPy returns a verified solution (substitution-checked); otherwise reported as limitation |
| C6 | Assumption-aware queries (e.g. "is X positive?") | SUPPORTED | Three-valued: true / false / **unknown** (SymPy's `None` preserved as unknown, never coerced) |

## 2. Constraint solving and model reasoning

| # | Capability | Disposition | Guarantee / boundary |
|---|---|---|---|
| M1 | Satisfiability checking, decidable fragments (e.g. QF_LIA) | SUPPORTED | Sound and complete *within the fragment*; fragment named in every result |
| M2 | Satisfying-model generation (witnesses) | SUPPORTED | Model re-checked against the spec independently of the solver |
| M3 | Unsatisfiable-core extraction | SUPPORTED | Where the solver provides it; otherwise CONTRADICTION reported without core |
| M4 | Nonlinear / quantified / general SMT | RESTRICTED | Attempted only with declared limits; solver `unknown` → reported as limitation (never as CONTRADICTION or UNDERDETERMINED) |
| M5 | Uniqueness checking via model-negation re-solve (§D of design spec) | SUPPORTED | Only within decidable fragments; procedure and fragment recorded with the claim |
| M6 | Second-model / counterexample search | SUPPORTED | Under a declared projection (§D.2); witnesses returned with differing properties |
| M7 | "Meaningfully distinct" judgment | SUPPORTED | Per-class projection definitions; no global notion of distinctness |

## 3. Proof and formal verification

| # | Capability | Disposition | Guarantee / boundary |
|---|---|---|---|
| P1 | Proof-term checking via small trusted kernel (Lean) | SUPPORTED | Acceptance is *relative to the formal statement, definitions, imports, axioms* — does not establish the statement says what was intended |
| P2 | Formalization of a frozen spec into the proof assistant's logic | RESTRICTED | Human-reviewed step; the formalization adequacy judgment is recorded as an assumption, not derived |
| P3 | Automated tactic-driven proof search | RESTRICTED | Permitted as discovery; only kernel-accepted terms count as PROVED |
| P4 | Implementation-contract verification, finite total-order properties | SUPPORTED | Via differential testing + property fuzzing (§4 of work order); formal proof where feasible |
| P5 | Universal claims from finite test suites alone | UNSUPPORTED | A finite suite never establishes a universal claim; §E anti-conflation rule |

## 4. Construction and implementation generation

| # | Capability | Disposition | Guarantee / boundary |
|---|---|---|---|
| G1 | Code generation from a frozen specification | SUPPORTED | Deterministic; derivation record links every generated artifact to spec lines |
| G2 | Silent gap-filling during generation | FORBIDDEN | Under-specified inputs rejected (INVALID_INPUT), never completed |
| G3 | Natural-language direct execution | FORBIDDEN | NL drafts candidate specs only; execution requires a frozen formal spec |

## 5. Evidence classification and recording

| # | Capability | Disposition | Guarantee / boundary |
|---|---|---|---|
| E1 | Classify results as DERIVED / PROVED / CONSTRUCTED / VERIFIED | SUPPORTED | Per §E evidential requirements |
| E2 | Record externally supplied empirical evidence as EXPERIMENTALLY_CONFIRMED | SUPPORTED | Records only; MSVE never establishes this status itself; requires experiment identity + data provenance |
| E3 | Provenance packaging (hashes, versions, witnesses, seeds) | SUPPORTED | Per §G of design spec |
| E4 | Re-verification after spec/tool change; supersede marking | SUPPORTED | Prior results marked superseded, never deleted |

## 6. Explicitly out of scope / forbidden

| # | Capability | Disposition | Reason |
|---|---|---|---|
| X1 | Inferring missing historical data | FORBIDDEN | Would manufacture facts; violates the central design principle |
| X2 | Predicting real-world performance from formal correctness | UNSUPPORTED | Category error; requires empirical evidence (judgment 3) |
| X3 | Inventing objective functions ("good chess move") | UNSUPPORTED | Domain judgment; belongs in the specification, explicitly |
| X4 | Arbitrary scientific discovery | UNSUPPORTED | Outside the formal scope by definition |
| X5 | Certifying MSVE by MSVE alone | UNSUPPORTED | Independent checkers required (§4 of work order); self-certification never counts |
| X6 | Executing unreviewed specifications | FORBIDDEN | Freeze-and-review gate (§H) |

## 7. Maturity staging ("all-rounder" ladder)

An operation advances only when its gate criteria are evidenced:

1. **Designed** — contract written, failure behaviour specified, in this matrix.
2. **Implemented** — exists with documented interface.
3. **Functionally verified** — acceptance suite green (normal, boundary, expected-failure cases).
4. **Formally verified** (where applicable) — kernel-checked proofs or sound procedures.
5. **Integrated and reproducible** — composes; pinned versions; independent re-runs reproduce.
6. **Scope-qualified release** — matrix passes acceptance; the claim
   "all-rounder within scope S, matrix vX.Y" is evidenced, never bare.

*End of MSVE_CAPABILITY_MATRIX_v0.1.md (draft for review).*
