# MSVE Design Specification v0.2

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Supersedes:** `MSVE_DESIGN_SPEC_v0.1.md` (retained as historical draft)
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MUSE WORK ORDER 0.1 · **Review authority:** Project owner
**Version:** 0.2 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

Change summary: v0.2 applies mandatory corrections A–G and review corrections
R1–R5 (see `MSVE_DESIGN_REVIEW_v0.2.md` for the section-by-section ledger).
The principal structural change is the replacement of the flat result-status
taxonomy (§E v0.1) with orthogonal status dimensions (§E v0.2).

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*. Its purpose is to translate formal
specifications into mathematical structures, implementations, and verifiable
results — without silently inventing missing premises and without confusing a
plausible result with an established one.

"General-purpose" means: domain-agnostic *within the formal scope defined by the
input language and the capability matrix* (`MSVE_CAPABILITY_MATRIX_v0.2.md`).
It does not mean universal. Any problem outside the declared scope is
UNSUPPORTED (admission status), not attempted.

### A.2 Intended users and responsibilities

- **Specification authors** (humans): write, review, and freeze formal specifications.
  All domain judgment lives here, explicitly.
- **MSVE (the engine)**: parses, validates, constructs, checks, and records — never
  invents premises, never executes unreviewed natural language.
- **Reviewers** (humans): approve specifications, adjudicate discrepancies, authorize
  capability changes.

### A.3 What MSVE does and does not do

| Activity | MSVE role |
|---|---|
| Mathematical derivation (exact arithmetic, symbolic manipulation) | Performs, within supported classes; see §F.4 for what "computed" means |
| Formal proof checking | Checks proof terms against a small trusted kernel |
| Software construction from a frozen spec | Generates within the restricted v0 generator class (§D/G1); derivation records kept |
| Implementation-contract verification | Checks at three separated levels (§D v0.2: L1/L2/L3) |
| Empirical testing (does it work in reality?) | Does **not** perform; may *record* externally supplied evidence with provenance (§E.6) |
| Scientific interpretation (what does it mean?) | Does **not** perform; labels the boundary |

### A.4 The three judgments (non-eliminable)

1. **Domain judgment** — choosing objectives, axioms, definitions, and what counts as
   desirable. Lives with the specification author. MSVE exposes it; never makes it.
2. **Construction judgment** — choosing algorithms/structures when the specification
   does not uniquely determine them. MSVE reports alternatives or UNDERDETERMINED
   (semantic result); it does not silently prefer one.
3. **Empirical uncertainty** — whether a specified, implemented system behaves as
   intended in reality. Only evidence from the real implementation, under an
   appropriate experimental design, can address this. MSVE never derives it.

### A.5 "All-rounder" — normative definition

In this project, "all-rounder" is a **scope-qualified, version-qualified claim**:

> "All-rounder within declared scope S, capability matrix version X.Y."

- The **capability matrix** is the normative definition of the claim.
- No capability may be advertised merely because a component exists.
- Every public use of the term must carry its scope and version qualifier.
- The staged gates in §J define what each maturity claim requires; the per-capability
  **maturity field** (§G.6, matrix) records what is actually demonstrated.

### A.6 Explicit non-goals

- MSVE will not infer missing historical data (FORBIDDEN — hard rule).
- MSVE will not predict real-world performance from formal correctness alone (OUT OF SCOPE).
- MSVE will not invent objective functions (e.g., "what makes a good chess move") — that
  is domain judgment and belongs in the specification, explicitly.
- MSVE will not replace the project's empirical research process.

---

## B. Formal input language

### B.1 Design rules

1. The language is **minimal and machine-readable**. Unrestricted natural language
   must never drive execution.
2. Every specification carries identity and version; accepted specifications are
   **immutable baselines** (content-hashed).
3. Natural language may be used to *draft candidate specifications* (§B.6). A candidate
   becomes executable only after human review and explicit freeze.

### B.2 Grammar fragment (v0.2, revised per R4)

```
Specification  := Header Definitions Constraints Goal Verification ResourceLimits ProvenanceReq
Header         := SpecID Version Scope Authors
SpecID         := string            # globally unique within the MSVE instance
Version        := semver
Scope          := string            # problem-class reference, see capability matrix

Definitions    := Definition*
Definition     := Name ":" Type "=" Expression | "axiom" Proposition

Constraints    := Constraint*
Constraint     := "assume" Proposition    # taken as given; tracked, never checked
               | "require" Predicate      # must hold of the object; checked
               | "forbid" Predicate       # must not hold of the object; checked

Goal           := "derive" Expression
               | "construct" ObjectType "satisfying" Constraints
               | "prove" Proposition "assuming" AssumptionRefs
               | "check" Property "of" Object
               | "compare-models" Constraints "under" Projection    # Projection mandatory

Projection     := "projection" Name "=" ObservableSet

Verification   := ProofRequirement TestRequirement
ProofRequirement := "kernel-checked" CheckerID | "none"
TestRequirement  := ("differential" CheckerID | "property-fuzz" FuzzConfig)* | "none"

ResourceLimits := "timeout" Duration ["memory" Bytes] ["steps" Nat]
ProvenanceReq  := "record" ("spec-hash" | "input-hash" | "tool-versions" | "witness" | "all")
```

### B.3 Semantic roles of assume / require / forbid (R4)

These are not interchangeable merely because all involve Boolean expressions:

- **`assume P`** — P is taken as given. Recorded in the assumption set of every
  result produced under this specification. The engine never checks P; the adequacy
  of assuming P is a human review judgment made at the freeze gate.
- **`require P`** — P must hold of the constructed or checked object. The engine
  must check it. A violated `require` yields VIOLATED (check goals) or NO_SOLUTION
  via CONTRADICTION (construct goals), never silent acceptance.
- **`forbid P`** — P must not hold of the object. Checked; violation handled as for `require`.
- In **`prove`** goals, the proposition is proved *relative to* the `assume`d
  context named in `assuming`. Assumptions are listed in the result; they are not
  proved by the engine.

### B.4 Resource-limit rules (R4)

- `timeout` is **mandatory**. A specification without it is INVALID_INPUT
  ("missing mandatory resource limit").
- `memory` and `steps` are optional and may be combined with `timeout`.
- Degenerate values (`timeout 0`, `steps 0`, negative values) are INVALID_INPUT
  ("degenerate resource limit"), not clamped silently.

### B.5 Type and admission rules

- Every `Expression` is typed; ill-typed specifications are INVALID_INPUT.
- `require`/`forbid` predicates must be decidable within the declared problem
  class, or the specification is UNSUPPORTED (not silently weakened).
- A `compare-models` goal (or any uniqueness-seeking goal) **without** a declared
  `Projection` is INVALID_INPUT ("missing required projection", R3). The engine
  must not guess the intended projection.
- Three admission outcomes are distinct (§E.2):
  1. **Malformed or contractually incomplete** (syntax/type errors, undefined
     identifiers, missing mandatory fields, missing projection where required)
     → **INVALID_INPUT**.
  2. **Valid specification, multiple admissible solutions** → the declared
     model-comparison procedure runs; established non-uniqueness under the
     projection → semantic result **UNDERDETERMINED** (§D).
  3. **Valid specification, conclusion not establishable by the available
     procedure** → semantic result **INCONCLUSIVE** with a reason code (§E.4).

A valid specification need not have a unique solution. Items 1–3 above are
different situations with different evidential meanings; the design must never
merge them.

### B.6 Natural-language handling (hard rule, revised per Correction B)

NL → candidate-specification drafting is a *separate, human-supervised step*.
The engine's executable input is the frozen formal specification only.

**An unreviewed assumption extracted from a natural-language draft must NEVER be
used in an executable specification.** It may be retained as an unreviewed
*proposal* inside a review artifact, clearly labelled. Execution requires explicit
human incorporation and approval of the assumption in the frozen formal
specification. The v0.1 allowance for UNREVIEWED items in output assumption sets
is removed: preferred behaviour is now the only behaviour — rejected until reviewed.

### B.7 Illustrative valid input (selector contract, repaired per Correction E)

```
spec: selector-contract/0.2.0
scope: finite-total-order-selection
define Candidate : { uci: String, rank: Nat, score: Binary64 }
define Binary64  : IEEE-754 binary64, canonicalized (neg-zero -> pos-zero);
                   NaN, +Inf, -Inf rejected at admission
admission: candidates non-empty; uci non-empty strings, pairwise distinct;
           rank : Nat; score finite
require: exists c in candidates. output.uci == c.uci        # existential membership
require: output == maxBy(candidates, key=(score desc, rank asc, uci asc))
           # total order: distinct UCIs guarantee a unique maximum
forbid:  output.uci not in { c.uci | c in candidates }
goal: check(selection-contract, SelectorImplementation)
verify: proof none; test differential(checker=independent-ref-impl-0.2.0),
        property-fuzz(seeds=[…]); timeout 300s
record: all
```

Note the v0.1 error corrected here: membership is existential
(∃c ∈ C: output.uci = c.uci), not the universal-quantifier formulation of v0.1 §B.4.

### B.8 Illustrative invalid inputs (rejected, not repaired)

- No `Goal` → INVALID_INPUT ("missing objective").
- Unbound identifier → INVALID_INPUT ("unbound identifier").
- Natural-language paragraph as specification → INVALID_INPUT ("not a formal
  specification; submit a candidate draft for review").
- `compare-models` without `Projection` → INVALID_INPUT ("missing required projection").
- Missing `timeout` → INVALID_INPUT ("missing mandatory resource limit").

---

## C. Supported problem classes

The **capability matrix** (`MSVE_CAPABILITY_MATRIX_v0.2.md`) is normative.
Summary for v0 (target dispositions; all currently at maturity DESIGN_ONLY):

| Class | v0 disposition |
|---|---|
| Exact integer/rational arithmetic | Supported |
| Symbolic expression manipulation (SymPy-backed) | Supported within stated limits (§F.4) |
| Finite constraint systems, decidable fragments (e.g. QF_LIA via Z3) | Supported |
| General/nonlinear constraint solving | Restricted — solver `unknown` → INCONCLUSIVE(SOLVER_UNKNOWN), never false uniqueness |
| Model construction and witness generation | Supported where the solver provides models |
| Uniqueness checking | Supported only via the negation procedure (§D) within decidable fragments |
| Proof checking (Lean kernel) | Supported for propositions formalized in Lean; formalization is human-reviewed |
| Implementation-contract verification | Three separated levels L1/L2/L3 (§D v0.2) |
| Code generation | Restricted to the v0 generator class (§D/G1) |
| Inferring missing historical data | **FORBIDDEN** |
| Predicting real-world performance from formal correctness | OUT OF SCOPE |
| Inventing objective functions | OUT OF SCOPE |

**Decidability rule:** no claim of decidability or completeness without naming the
problem class and the precise guarantees of the chosen procedure.

---

## D. Underdetermination, uniqueness and distinctness

### D.1 Three assurance levels for the acceptance case (Correction D)

The first acceptance plan — and any implementation-assurance claim — must
distinguish:

- **Level 1 — Mathematical model.** Properties of the *abstract algorithm* proved
  or established under explicit assumptions (e.g., "the abstract selector returns
  the unique maximum of a total order").
- **Level 2 — Implementation conformance.** Evidence that the *actual
  implementation or generated code* conforms to the mathematical model. Method must
  be named: checked refinement proof, translation validation, static analysis, or
  another suitably limited verification method. L1 proof alone establishes nothing
  about generated code.
- **Level 3 — Tested behaviour.** Regression tests, independent-reference
  comparisons, property-based tests and fuzzing over executed inputs. Bounded to
  tested inputs; never a universal proof on its own.

Where v0 cannot provide an assurance method for a promised guarantee, the
guarantee is narrowed, the capability marked RESTRICTED, or the method identified
as future work. The acceptance report must keep L1/L2/L3 visibly separate and
state the marginal value against the empirical baseline in those terms.

### D.2 Decision procedure (per supported class)

For a well-formed specification with a `compare-models` or uniqueness-requiring goal:

1. **Satisfiability:** check whether the specification is satisfiable.
   - If no model exists → semantic result **CONTRADICTION** (unsat core as
     diagnostic where the solver supports it; assurance per §F.5).
2. **Projection:** use the spec-declared projection onto the observable properties
   relevant to the objective (§D.3). Absent projection → INVALID_INPUT (R3), never guessed.
3. **Second-model search:** construct the query "π(m₂) ≠ π(m₁)" — the disjunction
   over projected components of exact inequality (§D.4) — assert it, and re-solve.
   - If a second, projection-distinct model exists → **UNDERDETERMINED**: return
     both witnesses and identify the differing projected properties.
4. **Uniqueness claim:** only if (a) the second-model query is UNSAT **and**
   (b) the decision procedure's completeness guarantee covers the problem class →
   report **UNIQUE_UNDER_PROJECTION** with procedure and guarantees recorded.
5. **Otherwise:** semantic result **INCONCLUSIVE** with reason code —
   SOLVER_UNKNOWN, PROCEDURE_INCOMPLETE, RESOURCE_EXHAUSTED, or
   EXECUTION_INTERRUPTED (§E.4). Uniqueness is **not** established.

### D.3 "Meaningfully distinct" — exact comparison rules (Correction F, R5)

Distinctness is relative to a declared projection. v0.2 replaces the v0.1
tolerance-based rule (which could fail transitivity) with **exact canonical equality**:

- **Selection projection** (selector case): π(m) = selected `uci` string.
  Distinct iff the strings differ (exact equality — transitive).
- **Probability-output projection** (selector case): π(m) = the sequence of
  canonicalized binary64 scores (neg-zero normalized, non-finite rejected at
  admission). Distinct iff the sequences differ bitwise in any component
  (exact equality on canonical forms — transitive).
- **Constraint-satisfaction projection** (general): π(m) = values of the declared
  observable variable set in canonical form. Distinct iff any differ exactly.

No threshold-based "approximate distinctness" may be described as an equivalence
relation. If a future application needs tolerance-based comparison, it must be
specified as a separate, explicitly non-transitive witness-comparison method —
not as the projection equality used by the uniqueness procedure.

### D.4 Second-model query construction

Given first model m₁ and projection π with components π₁…πₖ, the engine asserts:

```
(π₁(m₂) ≠ π₁(m₁)) ∨ (π₂(m₂) ≠ π₂(m₁)) ∨ … ∨ (πₖ(m₂) ≠ πₖ(m₁))
```

with ≠ as exact inequality on canonical forms, then re-solves. The query is
well-defined precisely because projection equality is exact (§D.3).

### D.5 Assumptions that restore uniqueness (Correction F)

The v0.1 promise that MSVE could "identify which additional assumption would
restore uniqueness" is **removed** as a general capability. For v0:

- MSVE may test candidate assumptions that are **explicitly supplied by the user**
  or drawn from a **declared finite candidate family** in the specification.
- It reports which candidates restore uniqueness under the specified procedure.
- A **mathematically sufficient** assumption (restores uniqueness formally) must
  not be presented as **scientifically justified** merely because it solves the
  formal problem. Only the specification author (human) may assert empirical
  justification, recorded as an assumption.

### D.6 Code generation scope (Correction D, matrix G1)

v0.1 §G1 promised general deterministic code generation with complete derivation
links. That promise is narrowed: v0 generation is restricted to **template-based
generation for the declared generator class** (initially: pure total functions
over finite enumerable domains with a fixed code template — the selector class
being the first instance). Each generated artifact links template instantiations
to spec lines. General deterministic generation with complete derivation links is
FUTURE work, not a v0 claim.

---

## E. Result-status architecture (redesigned per Correction A)

### E.1 Why the flat taxonomy was wrong

v0.1 §E treated TIMEOUT, UNDERDETERMINED, PROVED and CONSTRUCTED as mutually
exclusive terminal states. They are not the same kind of thing: a timeout is an
*execution* event, underdetermination is a *semantic* outcome, proof is a
*semantic* outcome of a specific goal type, and construction is an *artifact*
event. Forcing them into one state machine produced category errors — e.g., no
clean way to say "execution timed out, but a first model was already
independently established." v0.2 replaces the flat taxonomy with a **result
record of orthogonal fields**.

### E.2 The result record

Every MSVE run produces a result record with these independent fields:

| Field | Values | Notes |
|---|---|---|
| `admission` | ACCEPTED · INVALID_INPUT · UNSUPPORTED | Determined at parse/scope-check; see §B.5 |
| `execution` | NOT_STARTED · RUNNING · COMPLETED · TIMEOUT · INTERRUPTED · INTERNAL_ERROR | Execution lifecycle only |
| `semantic_result` | Per goal type (see §E.3) | What the mathematics established |
| `verification` | NOT_RUN · PASS · FAIL · INCONCLUSIVE · CHECKER_DIVERGENCE | Outcome of the independent checking step |
| `evidence` | Artifact bundle (§E.6, §G) | Records, witnesses, provenance |

### E.3 Semantic results per goal type

| Goal | Semantic result values |
|---|---|
| `derive` | DERIVED_VALUE · INCONCLUSIVE(reason) |
| `construct` | ARTIFACT_CONSTRUCTED · NO_SOLUTION (sub-reason: CONTRADICTION) · INCONCLUSIVE(reason) |
| `prove` | PROVED · DISPROVED · INCONCLUSIVE(reason) |
| `check` | HOLDS · VIOLATED (with counterexample witness) · INCONCLUSIVE(reason) |
| `compare-models` | UNIQUE_UNDER_PROJECTION · UNDERDETERMINED (with witnesses) · CONTRADICTION · INCONCLUSIVE(reason) |

### E.4 INCONCLUSIVE reason codes (Correction C)

INCONCLUSIVE is always qualified:

- **SOLVER_UNKNOWN** — the solver returned `unknown`; nothing about
  satisfiability, uniqueness, or inconsistency may be inferred.
- **PROCEDURE_INCOMPLETE** — the available procedure lacks the completeness
  guarantee the question requires.
- **RESOURCE_EXHAUSTED** — a declared limit (timeout/memory/steps) was reached.
- **EXECUTION_INTERRUPTED** — the run was stopped externally.

These have different evidential meanings and must never be merged. In particular:
solver `unknown` ≠ timeout ≠ interruption ≠ unsupported class ≠ established
unsatisfiability ≠ established non-uniqueness.

### E.5 Required semantics (the six rules)

1. **ARTIFACT_CONSTRUCTED does not mean verified.** Construction and verification
   are separate fields; a constructed artifact with `verification: NOT_RUN` is
   exactly that — constructed, not verified.
2. **PROVED identifies the precise proposition and its formal assumptions.**
   A PROVED result names the proposition, the assumption context, the kernel,
   and the proof artifact. "Proved" without these is not a well-formed result.
3. **Verification identifies property, method, and artifact.** A PASS names the
   property checked, the checking method, the checker identity/version, and the
   artifact checked.
4. **Timeouts preserve established results.** If execution ends in TIMEOUT but a
   semantic result (e.g., a first model, re-checked) was already independently
   established, the record keeps it, labelled with how far execution had
   progressed. Partial results are explicitly labelled partial.
5. **Completion is not success.** `execution: COMPLETED` with
   `semantic_result: INCONCLUSIVE(...)` is a completed run that established
   nothing — it must never be presented as a verification success.
6. **Recording is not confirming.** External evidence ingestion (§E.6) never
   becomes a scientific conclusion by MSVE's hand.

### E.6 External experimental evidence (Correction A, experimental-evidence rule)

The unqualified v0.1 status EXPERIMENTALLY_CONFIRMED is removed. v0.2
distinguishes three things:

1. **EVIDENCE_RECORDED** — external experimental evidence ingested with full
   provenance (experiment identity, method, raw-data references, hashes).
   MSVE asserts nothing about the evidence's truth; it records that the evidence
   was supplied and what was supplied.
2. **RECORD_INTEGRITY assessment** — a verification procedure assesses the
   *record's* integrity/consistency (hashes match manifest, schema valid,
   provenance chain complete), yielding PASS/FAIL. This assesses the record, not
   the scientific claim.
3. **Scientific conclusion** — recorded only as EXTERNAL_ASSESSMENT with its own
   provenance (who concluded, on what basis, when). MSVE never promotes a record
   into a confirmed scientific result.

### E.7 Anti-conflation rules (hard, retained and extended)

- A solver `unknown`, an interruption, or a timeout must **never** be reported as
  CONTRADICTION or UNDERDETERMINED.
- A passed finite test suite is **not** a universal proof (see §R2 note below on
  why enumeration cannot establish universal properties over unbounded classes).
- A generated implementation is **not** automatically verified; a verified
  implementation is **not** automatically experimentally successful.
- Failed runs and changed specifications remain distinguishable from successful
  runs in the provenance record.

---

## F. Trust base and verification architecture

### F.1 Architecture (orchestration, not a new solver)

```
spec text → [Parser/Validator] → admission check → [Review & freeze gate] → [Dispatcher]
    → [SymPy layer]   (exact arithmetic, symbolic computation)
    → [Z3 layer]      (constraint solving, model generation, unsat diagnostics)
    → [Lean layer]    (proof-term checking via small trusted kernel)
    → [Independent checker] (differential testing, property fuzzing, reference impls)
    → [Provenance recorder] → versioned result package (result record + evidence bundle)
```

v0 is an **orchestration and verification pipeline over established components**.
Building a new solver requires separate evidence and authorization.

### F.2 Component evaluation (against requirements, not reputation)

| Component | Role | What it establishes | Outside its guarantee |
|---|---|---|---|
| Specification parser/validator (MSVE-owned, v0) | Admission: syntax, typing, mandatory fields | Syntactic/typing validity | Semantic adequacy of the spec (human review) |
| SymPy (pinned version) | Exact/symbolic computation | See §F.4 | Undecidable queries (None preserved as unknown) |
| Z3 (pinned version) | SMT solving, models, unsat diagnostics | Satisfiability within decidable fragments; model witnesses (re-checked) | `unknown` results; heuristic internal search |
| Lean kernel (pinned version) | Proof-term checking | Theorem *relative to its formal statement, definitions, imports, axioms* | Whether the formal statement says what was intended |
| Independent checker (per acceptance case) | Differential/property testing | Behavioural agreement on tested inputs (L3) | Universal claims |
| Provenance recorder (MSVE-owned) | Hashing, versioning, packaging | Content identity + integrity relative to a trusted reference (§G) | Origin without a defined authenticity mechanism; correctness of content |

### F.3 What "trusted" means here

"Trusted" = relied upon without re-verification *within a stated boundary*, with
the boundary documented. The parser is trusted for syntax, not semantics. The
Lean kernel is trusted for proof-term acceptance, not for formalization adequacy.
Z3 is trusted for models *within decidable fragments*; its outputs are
independently re-checked against the canonical spec regardless.

### F.4 Symbolic computation: computed, checkable, trusted (Correction C)

The v0.1 description ("correctness of derivations within its algorithms") is
replaced with an explicit three-way split for SymPy-backed results:

- **Computed:** the library produced a value (e.g., exact integer arithmetic,
  expression simplification, solved forms). Recorded with library version and inputs.
- **Independently checkable:** results the engine re-verifies by an independent
  path — e.g., a claimed solution substituted back into the original equations;
  an arithmetic result recomputed by a second implementation. Where checkable,
  the check is run and recorded.
- **Trusted-tool output:** results with no independent check in v0 (e.g., the
  internal choices of a simplification routine). Labelled as relying on the
  pinned library version within the stated trust boundary — **not** described as
  formally verified derivations.

A symbolic result from a version-pinned library is not automatically a formally
verified derivation. The result record states which of the three applies.

### F.5 SAT and UNSAT assurance (Correction C)

The v0.1 asymmetry (detailed model rechecking, thin unsatisfiability treatment)
is corrected:

**Satisfying models:**
- Recheck the witness against the *canonical* formal specification (not a
  transformed copy), independently of the solver.
- Record the checker and its version; preserve the model and relevant input hashes.

**Unsatisfiability — assurance levels:**
- **Level A (independently checkable):** a proof certificate in a checkable
  format (where the solver stack supports one) is verified by an independent
  checker. May be described as independently established.
- **Level B (solver-backed):** the result relies on the pinned solver and
  configuration within the stated trust boundary. A solver-generated
  unsatisfiable core is useful *diagnostic* evidence but is **not** an
  independently checked proof of unsatisfiability and must not be described as one.

**Refusal rule:** if the request's declared assurance requirement (in
Verification) demands Level A and only Level B is available, the engine reports
the shortfall — it refuses the stronger claim rather than silently lowering the
standard. The result record shows `semantic_result: CONTRADICTION` with
`assurance: LEVEL_B_SOLVER_BACKED` and the unmet requirement flagged.

---

## G. Provenance and archival discipline

### G.1 Separated provenance claims (Correction G)

Hashing alone establishes content identity. v0.2 separates four claims that v0.1
blurred:

1. **Content identity** — SHA-256 over the canonical form (§G.2) identifies the
   recorded content. Anyone with the content can recompute the hash.
2. **Integrity relative to a trusted reference** — comparison against an
   *independently preserved* manifest or anchor (e.g., the frozen spec's published
   hash, a release manifest held outside the result store) can reveal substitution
   of a package together with its manifest.
3. **Authenticity** — a claim about *origin*, supported only by a defined
   mechanism. v0 mechanism: project-owner signed release tags, verified
   out-of-band. Without it, no origin claim is made.
4. **Correctness** — established only by verification procedures (§E, §F), never
   by hashing.

The phrase "tamper-proof" is not used. The accurate claim is **"tamper-evident
relative to a trusted reference"**: altering content without access to the
reference breaks the hash link detectably; the mechanism does not prevent
alteration and does not authenticate origin by itself.

### G.2 Canonicalization rules

All hashed inputs, outputs, manifests, and specifications use **canonical JSON**:
UTF-8 encoding, lexicographically sorted object keys, no insignificant
whitespace, numbers in canonical form (integers as decimal strings without
exponent; binary64 values as exact decimal expansions or hexfloat — fixed per
release and documented). Canonicalization rules are versioned with the release;
changing them requires re-hashing with both rules recorded during transition.

### G.3 Result package contents

Every MSVE output is a versioned result package containing the result record
(§E.2) plus:

1. Specification identity, version, content hash (frozen baseline reference).
2. Input hashes (canonicalized).
3. Exact tool/solver/checker versions and configuration.
4. Derivation records, model witnesses, proof artifacts (where applicable).
5. Test inputs, random seeds, reproducible fuzzing conditions.
6. Output hashes.
7. Assumption set (human-reviewed only — §B.6).
8. Failure records and unresolved issues, preserved alongside successes.
9. Supersession records: what this package supersedes and why.

**Rules:** preserve failed attempts and specification revisions as traceable
history — never overwrite evidence to clean the record. Re-verification is
required after any specification or tool-version change; prior results are marked
superseded, not deleted.

### G.4 Capability maturity (Correction G)

The v0.1 matrix used SUPPORTED while the engine is unimplemented — inviting
confusion between intended support and demonstrated capability. v0.2 keeps the
**target disposition** (SUPPORTED / RESTRICTED / UNSUPPORTED / FUTURE /
FORBIDDEN) and adds a separate **maturity** field per capability:

`DESIGN_ONLY` · `IMPLEMENTED` · `FUNCTIONALLY_VERIFIED` ·
`FORMALLY_VERIFIED` (where applicable) · `INDEPENDENTLY_REPRODUCED` · `RELEASED`

Every v0.2 capability is at maturity **DESIGN_ONLY**. A capability does not
become implemented or verified because the design lists it as supported. The
matrix (§7-equivalent) records both fields for every entry.

---

## H. Governance and capability authorisation

### H.1 Authority

| Decision | Authority |
|---|---|
| Approve / revise / reject this design | Project owner |
| Freeze a specification (making it an immutable baseline) | Project owner (or delegated reviewer, recorded) |
| Authorize repository creation | Project owner, after design freeze |
| Authorize implementation (vertical slice or beyond) | Project owner, separate explicit authorization |
| Declare a release complete (per §J gates) | Project owner, on evidence |

### H.2 Capability track separation

- MSVE is a **separate capability track** from existing research projects and
  from àfi_adaptive (formal construction/verification vs. adaptive behaviour —
  architecturally distinct, never silently folded together).
- MSVE may be *used as a tool* against a separately authorized research task.
  Use grants no permission to modify that task's frozen artifacts, branches, or
  evidence. Tool use is read-only unless the task's own authorization says otherwise.

### H.3 Repository genesis rule

If a repository is subsequently authorized, its **genesis commit must be the
reviewed and frozen design specification** — not an empty placeholder followed
by undocumented changes. The "Designed" gate (§J) is satisfied by that commit.

---

## I. Acceptance plan and initial vertical slice

*Summary. Normative detail: `MSVE_ACCEPTANCE_PLAN_v0.2.md`.*

- **First application (proposed):** the published GrimChess Order 7 PM-E0
  selector contract, using the 75-position empirical baseline as the comparison point.
- **Three assurance levels** (§D.1): L1 mathematical model, L2 implementation
  conformance, L3 tested behaviour — kept visibly separate in the acceptance report.
- **Baseline preserved as reported:** PM-E0 selected candidate[0] in 75/75 under the
  documented empty-prior condition — empirical evidence over the panel, not a
  universal theorem.
- **Binding correction:** malformed-input rejection was implemented but never
  executed in Order 7; the plan executes those cases and must not claim they passed.
- **Marginal value** is stated in L1/L2/L3 terms: which guarantees generalize beyond
  the 75 positions, which are conformance evidence, which are bounded to tested inputs.
- The vertical slice remains **proposed until separately authorized**.

---

## J. Release and completion criteria

Measurable gates. An operation is complete only when **all** applicable criteria hold.

| Gate | Measurable criterion |
|---|---|
| 1. Designed | Frozen spec (genesis commit); input language, output contract, failure taxonomy, scope defined; reviewed |
| 2. Implemented | Every claimed operation exists with a documented interface; no phantom components |
| 3. Functionally verified | Executable acceptance suite: normal, boundary, and expected-failure cases (incl. CONTRADICTION, UNDERDETERMINED, INCONCLUSIVE, UNSUPPORTED, INVALID_INPUT); all green |
| 4. Formally verified (where applicable) | Claimed universal properties backed by kernel-checked proofs or sound procedures; proof artifacts preserved |
| 5. Integrated and reproducible | Operations compose; versions pinned; independent re-runs reproduce recorded results (modulo declared non-determinism such as timing) |
| 6. Scope-qualified release | Full declared capability matrix passes acceptance at the claimed maturity; limitations and unsupported operations documented; "all-rounder within scope S, matrix vX.Y" claim evidenced |

**Completion rule:** MSVE shall not be declared complete merely because planned
components exist. Every advertised operation needs an explicit contract,
acceptance tests, documented failure behaviour, and appropriate evidence.
Unsupported, unproven, or untested capabilities remain explicitly labelled in the
release matrix. A failed operation stays visible; it is not removed to clean the record.

---

## Appendix 1. Glossary (v0.2, revised)

- **Specification:** a formal, versioned, content-hashed document in the input language.
- **Frozen specification:** a specification reviewed and baselined; immutable thereafter.
- **Admission status:** ACCEPTED / INVALID_INPUT / UNSUPPORTED — whether the
  specification was well-formed and within scope (§E.2).
- **Semantic result:** what the mathematics established for the goal type
  (e.g., PROVED, UNDERDETERMINED, CONTRADICTION, INCONCLUSIVE) — independent of
  execution and verification outcomes (§E.3).
- **Verification outcome:** NOT_RUN / PASS / FAIL / INCONCLUSIVE /
  CHECKER_DIVERGENCE — what independent checking established (§E.2).
- **Projection:** the declared observable properties under which model
  distinctness is judged; equality on projections is exact over canonical forms (§D.3).
- **Witness:** a concrete model, counterexample, or proof artifact produced as evidence.
- **Trusted component:** relied upon without re-verification within a documented boundary.
- **Result record:** the orthogonal-field record defined in §E.2.
- **Result package:** the result record plus the evidence bundle defined in §G.3.
- **Maturity:** the demonstrated-evidence level of a capability, separate from its
  target disposition (§G.4).
- **EVIDENCE_RECORDED:** external experimental evidence ingested with provenance;
  MSVE asserts nothing about its truth (§E.6).

## Appendix 2. Formal selector contract v0.2 (Correction E)

*Normative for the acceptance plan. Proposed — to be frozen before any execution.*

**A2.1 Types.**
`Candidate := { uci: String, rank: Nat, score: Binary64 }`, where Binary64 is
IEEE-754 binary64, canonicalized: −0.0 normalized to +0.0; NaN, +∞, −∞ are not
representable in a well-formed candidate.

**A2.2 Admission (well-formedness).** The candidate set C must satisfy: C
non-empty; every `uci` a non-empty string; UCIs pairwise distinct (duplicates →
INVALID_INPUT, "duplicate candidate identity"); every `rank` a Nat; every
`score` finite. Violation → INVALID_INPUT with the specific defect named.

**A2.3 Membership.** `∃c ∈ C : output.uci = c.uci.` (Existential — the v0.1
universal-quantifier formulation was an error, corrected.)

**A2.4 Ranking (total order).** Define the key
`K(c) := (score(c), −rank(c), uci(c))` compared lexicographically:
higher score preferred; equal scores → lower rank preferred; remaining ties →
lexicographically smaller UCI preferred. `output` is the unique maximizer of K
over C. Because UCIs are pairwise distinct, the order is total and the maximum
is unique for non-empty C.

**A2.5 Numeric semantics.** Scores are compared as canonicalized binary64 values
with exact comparison — bitwise equality of canonical forms is the equality
rule; no tolerance is defined or used. Non-finite values are rejected at
admission (§A2.2), so comparison is a total order on well-formed inputs.
Signed zero is normalized; there is no separate −0.0 case in the ordering.

**A2.6 No calibration claim.** Scores are used for ranking only. The contract
asserts nothing about probability calibration, and no probability-sum or
normalization constraint is imposed unless a specification declares one.

**A2.7 Determinism.** Selection is a pure function of C: identical inputs yield
identical outputs.

**A2.8 Assessed semantics and mismatch report.** The proposed semantics
(score desc, rank asc, lexical-UCI asc) were compared against the preserved
Order 7 record: PM-E0 selected candidate[0] in 75/75; the 11 exact-probability
ties were resolved by (rank, lexical UCI); softmax is monotonic in the engine's
ordering. **No mismatch on observed behaviour.** The edge-case rules are new
explicit decisions, not historical claims: non-finite rejection, −0.0
normalization, duplicate-UCI rejection, and the existential membership
formulation go beyond what Order 7 recorded and are proposed contract terms for
review — they must not be presented as historical facts.

## Appendix 3. Unresolved design decisions (carried, not hidden)

1. Exact Lean version selection and the proof-carrying interface format — deferred to
   implementation authorization; does not block design freeze.
2. Full v0 problem-class catalog beyond the initial matrix — the matrix is
   authoritative; extensions need their own review.
3. Precise timeout/memory defaults per problem class — to be set at implementation
   authorization, documented per release.
4. The v0 generator class is initially scoped to template-based generation for
   pure total functions over finite enumerable domains; widening the class needs
   its own design review.

*End of MSVE_DESIGN_SPEC_v0.2.md (draft for review — not frozen).*
