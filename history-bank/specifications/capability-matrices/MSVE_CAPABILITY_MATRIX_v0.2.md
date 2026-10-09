# MSVE Capability Matrix v0.2

**Status:** DRAFT FOR REVIEW — NORMATIVE WHEN FROZEN WITH THE DESIGN SPEC
**Version:** 0.2 · **Design spec:** `MSVE_DESIGN_SPEC_v0.2.md`
**Supersedes:** `MSVE_CAPABILITY_MATRIX_v0.1.md` (retained as historical draft)

This matrix is the normative definition of every capability claim MSVE v0 may
make. A capability not listed here is not claimed. A capability listed as
restricted/unsupported must be labelled as such in every release.

**Two independent fields per capability** (Correction G):
- **Target disposition:** SUPPORTED · RESTRICTED · UNSUPPORTED · FUTURE ·
  FORBIDDEN (hard rule — must never be implemented). What the design *intends*.
- **Maturity:** DESIGN_ONLY · IMPLEMENTED · FUNCTIONALLY_VERIFIED ·
  FORMALLY_VERIFIED (where applicable) · INDEPENDENTLY_REPRODUCED · RELEASED.
  What is *demonstrated*. Every v0.2 entry is DESIGN_ONLY — the engine is not
  implemented. A capability does not become implemented or verified because the
  design lists it as supported.

---

## 1. Computation and symbolic mathematics

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| C1 | Exact integer arithmetic (arbitrary precision) | SUPPORTED | DESIGN_ONLY | Bit-exact results; derivation record |
| C2 | Exact rational arithmetic | SUPPORTED | DESIGN_ONLY | Bit-exact results; derivation record |
| C3 | Floating-point evaluation | RESTRICTED | DESIGN_ONLY | Only as explicitly declared approximation with error bounds; never presented as exact |
| C4 | Symbolic expression construction and simplification (SymPy-backed) | SUPPORTED | DESIGN_ONLY | Computed / independently checkable / trusted-tool output distinguished per spec §F.4 |
| C5 | Symbolic solving (equation systems, closed forms) | RESTRICTED | DESIGN_ONLY | Where a solution is substitution-checked; otherwise INCONCLUSIVE with reason |
| C6 | Assumption-aware queries (e.g. "is X positive?") | SUPPORTED | DESIGN_ONLY | Three-valued: true / false / **unknown** (never coerced) |

## 2. Constraint solving and model reasoning

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| M1 | Satisfiability checking, decidable fragments (e.g. QF_LIA) | SUPPORTED | DESIGN_ONLY | Sound and complete *within the fragment*; fragment named in every result |
| M2 | Satisfying-model generation (witnesses) | SUPPORTED | DESIGN_ONLY | Model re-checked against the canonical spec independently of the solver |
| M3 | Unsatisfiable-core extraction | SUPPORTED | DESIGN_ONLY | Diagnostic evidence only — not an independently checked proof (spec §F.5) |
| M4 | Nonlinear / quantified / general SMT | RESTRICTED | DESIGN_ONLY | Attempted only with declared limits; solver `unknown` → INCONCLUSIVE(SOLVER_UNKNOWN) |
| M5 | Uniqueness checking via model-negation re-solve (spec §D) | SUPPORTED | DESIGN_ONLY | Only within decidable fragments; exact canonical projection equality; procedure recorded |
| M6 | Second-model / counterexample search | SUPPORTED | DESIGN_ONLY | Under a declared projection; witnesses returned with differing projected properties |
| M7 | "Meaningfully distinct" judgment | SUPPORTED | DESIGN_ONLY | Per-class projection definitions with exact equality; no tolerance-based equivalence |

## 3. Proof and formal verification

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| P1 | Proof-term checking via small trusted kernel (Lean) | SUPPORTED | DESIGN_ONLY | Acceptance relative to formal statement, definitions, imports, axioms |
| P2 | Formalization of a frozen spec into the proof assistant's logic | RESTRICTED | DESIGN_ONLY | Human-reviewed step; adequacy recorded as assumption, not derived |
| P3 | Automated tactic-driven proof search | RESTRICTED | DESIGN_ONLY | Discovery only; only kernel-accepted terms count as PROVED |
| P4 | Implementation-contract assurance | SUPPORTED | DESIGN_ONLY | Three separated levels L1/L2/L3 (spec §D.1); L1 proof alone establishes nothing about code |
| P5 | Universal claims from finite test suites alone | UNSUPPORTED | — | A finite suite never establishes a universal claim |

## 4. Construction and implementation generation

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| G1 | Code generation from a frozen specification | RESTRICTED | DESIGN_ONLY | **Narrowed for v0** (Correction D): template-based generation for the declared generator class only (initially: pure total functions over finite enumerable domains, fixed code template; selector class first instance). Each artifact links template instantiations to spec lines. General deterministic generation with complete derivation links: FUTURE |
| G2 | Silent gap-filling during generation | FORBIDDEN | — | Under-specified inputs rejected (INVALID_INPUT), never completed |
| G3 | Natural-language direct execution | FORBIDDEN | — | NL drafts candidate specs only; unreviewed NL assumptions NEVER enter executable specs (spec §B.6) |

## 5. Evidence classification and recording

| # | Capability | Target | Maturity | Guarantee / boundary |
|---|---|---|---|---|
| E1 | Result records with orthogonal status fields (admission / execution / semantic / verification / evidence) | SUPPORTED | DESIGN_ONLY | Per spec §E; completion never presented as success |
| E2 | External experimental evidence handling | SUPPORTED | DESIGN_ONLY | Three-way split: EVIDENCE_RECORDED (ingest only) / RECORD_INTEGRITY assessment / EXTERNAL_ASSESSMENT (spec §E.6). MSVE never promotes a record into a confirmed scientific result |
| E3 | Provenance packaging (hashes, versions, witnesses, seeds) | SUPPORTED | DESIGN_ONLY | Separated claims: identity / integrity-vs-reference / authenticity / correctness (spec §G.1); canonical JSON (§G.2); "tamper-evident relative to a trusted reference", never "tamper-proof" |
| E4 | Re-verification after spec/tool change; supersede marking | SUPPORTED | DESIGN_ONLY | Prior results marked superseded, never deleted |

## 6. Explicitly out of scope / forbidden

| # | Capability | Target | Reason |
|---|---|---|---|
| X1 | Inferring missing historical data | FORBIDDEN | Would manufacture facts; violates the central design principle |
| X2 | Predicting real-world performance from formal correctness | UNSUPPORTED | Category error; requires empirical evidence (judgment 3) |
| X3 | Inventing objective functions ("good chess move") | UNSUPPORTED | Domain judgment; belongs in the specification, explicitly |
| X4 | Arbitrary scientific discovery | UNSUPPORTED | Outside the formal scope by definition |
| X5 | Certifying MSVE by MSVE alone | UNSUPPORTED | Independent checkers required; self-certification never counts |
| X6 | Executing unreviewed specifications | FORBIDDEN | Freeze-and-review gate (spec §H) |
| X7 | Automatic discovery of uniqueness-restoring assumptions | UNSUPPORTED | v0 tests only user-supplied or declared-finite-family candidates (spec §D.5) |

## 7. Maturity staging ("all-rounder" ladder)

An operation advances only when its gate criteria are evidenced. Maturity is
recorded per capability (§G.4); the ladder below defines the shared meaning:

1. **Designed** — contract written, failure behaviour specified, in this matrix.
2. **Implemented** — exists with documented interface.
3. **Functionally verified** — acceptance suite green (normal, boundary, expected-failure cases).
4. **Formally verified** (where applicable) — kernel-checked proofs or sound procedures.
5. **Independently reproduced** — separate party/machine reproduces recorded results.
6. **Released** — scope-qualified release; the claim "all-rounder within scope S,
   matrix vX.Y" is evidenced, never bare.

*End of MSVE_CAPABILITY_MATRIX_v0.2.md (draft for review).*
