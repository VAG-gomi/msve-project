# MSVE Design Specification v0.1

**Project:** Mathematical Structure and Verification Engine (MSVE)
**Document status:** DRAFT FOR REVIEW — NOT FROZEN, NOT ACCEPTED
**Implementation status:** NOT AUTHORISED · **Repository status:** NOT AUTHORISED
**Work order:** MUSE WORK ORDER 0 · **Review authority:** Project owner
**Version:** 0.1 (draft)

> Governing principle: *Define, constrain, verify and preserve before constructing.*
> Central design principle: *MSVE must make judgment explicit, traceable and
> challengeable. It must not conceal uncertainty inside a generated formula,
> implementation or explanation.*

This document is a design proposal. Approval of this draft is not approval to
implement. All normative claims (grammar, statuses, guarantees) are provisional
until the specification is reviewed, revised, and explicitly frozen.

---

## A. Purpose, claims and limits

### A.1 Objective

MSVE is a general-purpose mathematical construction and verification instrument
*within an explicitly declared scope*. Its purpose is to translate formal
specifications into mathematical structures, implementations, and verifiable
results — without silently inventing missing premises and without confusing a
plausible result with an established one.

"General-purpose" means: domain-agnostic *within the formal scope defined by the
input language and the capability matrix* (Document 3). It does not mean
universal. Any problem outside the declared scope is UNSUPPORTED, not attempted.

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
| Mathematical derivation (exact arithmetic, symbolic manipulation) | Performs, within supported classes |
| Formal proof checking | Checks proof terms against a small trusted kernel |
| Software construction from a frozen spec | Generates, with derivation records |
| Implementation-contract verification | Checks, via independent checkers and differential testing |
| Empirical testing (does it work in reality?) | Does **not** perform; may *record and classify* externally supplied evidence with provenance |
| Scientific interpretation (what does it mean?) | Does **not** perform; labels the boundary |

### A.4 The three judgments (non-eliminable)

1. **Domain judgment** — choosing objectives, axioms, definitions, and what counts as
   desirable. Lives with the specification author. MSVE exposes it; never makes it.
2. **Construction judgment** — choosing algorithms/structures when the specification
   does not uniquely determine them. MSVE reports alternatives or UNDERDETERMINED;
   it does not silently prefer one.
3. **Empirical uncertainty** — whether a specified, implemented system behaves as
   intended in reality. Only evidence from the real implementation, under an
   appropriate experimental design, can address this. MSVE never derives it.

### A.5 "All-rounder" — normative definition

In this project, "all-rounder" is a **scope-qualified, version-qualified claim**:

> "All-rounder within declared scope S, capability matrix version X.Y."

- The **capability matrix** (Document 3) is the normative definition of the claim.
- No capability may be advertised merely because a component exists.
- Every public use of the term must carry its scope and version qualifier.
- The staged gates in §J define what each maturity claim requires.

### A.6 Explicit non-goals

- MSVE will not infer missing historical data (FORBIDDEN — hard rule, §E).
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
3. Natural language may be used to *draft candidate specifications*. A candidate
   becomes executable only after human review and explicit freeze. Missing
   assumptions must never be inserted silently — the parser must reject
   under-specified inputs with INVALID_INPUT, not complete them.

### B.2 Grammar fragment (illustrative, not final)

```
Specification  := Header Definitions Constraints Goal Verification ProvenanceReq
Header         := SpecID Version Scope Authors
SpecID         := string            # globally unique within the MSVE instance
Version        := semver
Scope          := string            # problem-class reference, see Document 3

Definitions    := Definition*
Definition     := Name ":" Type "=" Expression | "axiom" Proposition

Constraints    := Constraint*
Constraint     := "assume" Expression      # taken as given; tracked as assumption
               | "require" Expression     # must hold; checked
               | "forbid" Expression      # must not hold; checked

Goal           := "construct" ObjectType "satisfying" Constraints
               | "prove" Proposition
               | "check" Property "of" Object
               | "compare-models" Constraints "under" Projection

Verification   := ProofPolicy CheckerPolicy ResourceLimits
ProofPolicy    := "kernel-checked" | "differential-tested" | "property-fuzzed" | "none"
CheckerPolicy  := CheckerID+
ResourceLimits := "timeout" Duration | "memory" Bytes | "steps" Nat

ProvenanceReq  := "record" ("spec-hash" | "input-hash" | "tool-versions" | "witness" | "all")
```

### B.3 Type rules (v0, minimal)

- Every `Expression` is typed; the parser rejects ill-typed specifications (INVALID_INPUT).
- `assume`d expressions are recorded in the assumption set of every output — an
  output's validity is always *relative* to its assumptions.
- `require`/`forbid` expressions must be decidable within the declared problem
  class, or the specification is UNSUPPORTED (not silently weakened).

### B.4 Illustrative valid input (selector contract, sketch)

```
spec: selector-contract/0.1.0
scope: finite-total-order-selection
define Candidate : { uci: String, rank: Nat, probability: Real }
require: forall c in input. output.uci == c.uci for some c      # membership
require: output == argmax(probability, tie -> (rank, uci))       # declared order
forbid:  output.uci not in { c.uci | c in input }                # no invention
goal: check(selection-contract, SelectorImplementation)
verify: differential-tested(checker=independent-ref-impl-0.1.0),
        property-fuzzed(seeds=[…]), timeout(300s)
record: all
```

### B.5 Illustrative invalid inputs (must be rejected, not repaired)

- A specification with no `Goal` → INVALID_INPUT ("missing objective").
- A `require` referencing an undefined name → INVALID_INPUT ("unbound identifier"),
  never auto-completed.
- A natural-language paragraph submitted as a specification → INVALID_INPUT
  ("not a formal specification; submit a candidate draft for review").
- A `Goal: prove` over an undecidable fragment without a `ProofPolicy` →
  UNSUPPORTED or INVALID_INPUT, never attempted blindly.

### B.6 Natural-language handling (hard rule)

NL → candidate-specification drafting is a *separate, human-supervised step*.
The engine's executable input is the frozen formal specification only. Any
assumption present in the NL draft but absent from the frozen spec must be
listed in the output's assumption set as UNREVIEWED if used at all — preferred:
rejected until reviewed.

---

## C. Supported problem classes

The **capability matrix** (Document 3: `MSVE_CAPABILITY_MATRIX_v0.1.md`) is
normative. Summary for v0:

| Class | v0 disposition |
|---|---|
| Exact integer/rational arithmetic | Supported |
| Symbolic expression manipulation (SymPy-backed) | Supported within SymPy's capabilities |
| Finite constraint systems, decidable fragments (e.g. QF_LIA via Z3) | Supported |
| General/nonlinear constraint solving | Restricted — may return unknown; reported as limitation, never as false uniqueness |
| Model construction and witness generation | Supported where the solver provides models |
| Uniqueness checking | Supported only via the negation procedure (§D) within decidable fragments |
| Proof checking (Lean kernel) | Supported for propositions formalized in Lean; the formalization step is human-reviewed |
| Implementation-contract verification (finite, total-order properties) | Supported via differential testing + property fuzzing; formal proof where feasible |
| Inferring missing historical data | **FORBIDDEN** |
| Predicting real-world performance from formal correctness | OUT OF SCOPE |
| Inventing objective functions | OUT OF SCOPE |

**Decidability rule:** no claim of decidability or completeness without naming the
problem class and the precise guarantees of the chosen procedure. A solver
returning `unknown`, or an interrupted computation, must never be presented as a
proof of inconsistency or of underdetermination.

---

## D. Underdetermination, uniqueness and distinctness

### D.1 Decision procedure (per supported class)

For a well-formed specification with a `compare-models` or uniqueness-requiring goal:

1. **Satisfiability:** check whether the specification is satisfiable.
   - If no model exists → **CONTRADICTION** (with unsatisfiable core where the
     solver supports it).
2. **Projection:** define the projection onto the *observable properties relevant
   to the requested objective* (declared in the spec; see §D.2).
3. **Second-model search:** assert the negation of the first model *under the
   projection* and re-solve.
   - If a second, projection-distinct model exists → **UNDERDETERMINED**: return
     both witnesses and identify which properties differ under the projection.
4. **Uniqueness claim:** only if the procedure's completeness guarantee covers the
   problem class → report uniqueness *with the procedure and its guarantees recorded*.
5. **Otherwise:** report the limitation honestly — **TIMEOUT** (resource limit),
   or a bounded statement ("no second model found within procedure P; uniqueness
   not established").

### D.2 "Meaningfully distinct" — per-class definitions (v0)

Distinctness is always **relative to a declared projection**. v0 defines:

- **Selection projection** (selector case): two models are distinct iff they select
  different `uci` values. Models differing only in probability values but agreeing
  on the selected move are *equivalent* under this projection.
- **Probability-output projection** (selector case): two models are distinct iff
  their probability vectors differ (beyond a declared numerical tolerance).
- **Constraint-satisfaction projection** (general): distinct iff they differ on a
  declared observable variable set.

Conflating these equivalence relations is a design error. The specification must
declare which projection the uniqueness question is asked under.

### D.3 Restoring uniqueness

When UNDERDETERMINED, the engine should identify *which additional assumption
would restore uniqueness* (e.g., "fixing the tie-break to lexical-UCI yields a
unique model under the selection projection"). It must preserve the distinction
between:
- a **mathematically sufficient** assumption (restores uniqueness formally), and
- an **empirically justified** assumption (has evidence behind it).
The engine supplies the first; only the specification author (human) may assert
the second, and it is recorded as an assumption, not a derivation.

---

## E. Output contract and failure taxonomy

### E.1 Result statuses — semantics, preconditions, evidential requirements

| Status | Meaning | Precondition | Evidential requirement |
|---|---|---|---|
| DERIVED | Result follows from the spec by exact computation | Supported problem class; spec valid | Derivation record; input/output hashes |
| PROVED | Proposition established | Proof term accepted by the trusted kernel | Proof artifact + kernel acceptance record |
| CONSTRUCTED | Implementation generated from frozen spec | Spec frozen; generation deterministic | Generated code + derivation record + spec hash |
| VERIFIED | Property checked against implementation | Independent checker run | Checker identity/version, inputs, outcome |
| EXPERIMENTALLY_CONFIRMED | External empirical evidence recorded | Evidence supplied *with provenance*; MSVE never establishes this itself | Experiment identity, raw data refs, hashes; kept distinct from DERIVED/PROVED |
| UNDERDETERMINED | Multiple projection-distinct models demonstrated, or non-uniqueness established by a complete procedure | §D procedure followed | Both witnesses + differing properties |
| CONTRADICTION | Constraints inconsistent | Solver establishes unsatisfiability | Unsat core where supported |
| TIMEOUT | Resource limit reached before result established | Limit declared in spec | Which limit; partial state if any |
| CHECKER_DIVERGENCE | Independent checkers disagree, or a cross-check fails | ≥2 checkers run | Both results; discrepancy recorded, investigated, never silently resolved |
| UNSUPPORTED | Problem outside supported language/guarantees | Detected at parse or dispatch | Which boundary was hit |
| INVALID_INPUT | Spec fails syntax/typing/contract validation | Detected at parse | Precise validation errors |

### E.2 Anti-conflation rules (hard)

- A solver `unknown`, an interruption, or a timeout must **never** be reported as
  CONTRADICTION or UNDERDETERMINED.
- A passed finite test suite is **not** a universal proof; universal claims require
  a suitable formal argument or sound checking procedure (§4 of the work order).
- A generated implementation is **not** automatically VERIFIED; a VERIFIED
  implementation is **not** automatically experimentally successful.
- Failed runs and changed specifications must remain distinguishable from
  successful runs in the provenance record.

---

## F. Trust base and verification architecture

### F.1 Architecture (orchestration, not a new solver)

```
spec text → [Parser/Validator] → frozen spec → [Dispatcher]
    → [SymPy layer]   (exact arithmetic, symbolic manipulation)
    → [Z3 layer]      (constraint solving, model generation, unsat cores)
    → [Lean layer]    (proof-term checking via small trusted kernel)
    → [Independent checker] (differential testing, property fuzzing, reference impls)
    → [Provenance recorder] → versioned result package
```

v0 is an **orchestration and verification pipeline over established components**.
Building a new solver requires separate evidence and authorization.

### F.2 Component evaluation (against requirements, not reputation)

| Component | Role | What it establishes | Outside its guarantee |
|---|---|---|---|
| Specification parser/validator (MSVE-owned, v0) | Rejects ill-formed/under-specified inputs | Syntactic/typing validity | Semantic adequacy of the spec (human review) |
| SymPy (pinned version) | Exact/symbolic computation | Correctness of derivations *within its algorithms* | Undecidable queries (returns None — preserved as unknown, per §C) |
| Z3 (pinned version) | SMT solving, models, unsat cores | Satisfiability within decidable fragments; model witnesses | `unknown` results; heuristic internal search (results independently checkable) |
| Lean kernel (pinned version) | Proof-term checking | Theorem *relative to its formal statement, definitions, imports, axioms* | Whether the formal statement says what the researcher intended |
| Independent checker (per acceptance case) | Differential/property testing | Behavioural agreement on tested inputs | Universal claims (bounded by test/fuzz coverage) |
| Provenance recorder (MSVE-owned) | Hashing, versioning, packaging | Tamper-evident record linkage | Correctness of the recorded content itself |

### F.3 What "trusted" means here

"Trusted" = relied upon without re-verification *within a stated boundary*, with
the boundary documented. The parser is trusted for syntax, not semantics. The
Lean kernel is trusted for proof-term acceptance, not for formalization adequacy.
Z3 is trusted for models *within decidable fragments*; its outputs are
independently re-checked against the spec regardless.

---

## G. Provenance and archival discipline

Every MSVE output is a **versioned result package** containing:

1. Specification identity, version, and content hash (frozen baseline reference).
2. Input hashes (all inputs, canonicalized).
3. Exact tool/solver/checker versions and configuration (solver flags, seeds,
   resource limits).
4. Derivation records, model witnesses, proof artifacts (where applicable).
5. Test inputs, random seeds, and reproducible fuzzing conditions.
6. Output hashes.
7. Verification outcome per claimed property, with checker identity.
8. Assumption set (including UNREVIEWED items, if any — preferred: none).
9. Failure records and unresolved issues, preserved alongside successes.

**Rules:**
- Distinguish the *identity* of an artifact (what it is, hash) from *evidence
  about its correctness* (what was checked, by whom, with what result).
- Preserve failed attempts and specification revisions as traceable history.
  Never overwrite evidence to make the final record cleaner.
- Re-verification is required after any specification or tool-version change;
  prior results are marked superseded, not deleted.

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

*Summary. Normative detail: Document 4 (`MSVE_ACCEPTANCE_PLAN_v0.1.md`).*

- **First application (proposed):** the published GrimChess Order 7 PM-E0
  selector contract, using the 75-position empirical baseline as the comparison point.
- **Baseline preserved as reported:** PM-E0 selected candidate[0] in 75/75 under the
  documented empty-prior condition — empirical evidence over the panel, not a
  universal theorem.
- **The plan must cover:** candidate membership; ranking and deterministic
  tie-breaking; invalid-input handling (**to be executed** — Order 7 implemented
  the rejection logic but the malformed-input cases were never run; the plan must
  not claim they passed); universal vs. bounded properties; agreement/disagreement
  with an independently implemented reference selector; reproducible property-based
  and fuzz tests; limits of finite testing; provenance and independent reproduction.
- **Marginal value test:** the acceptance case must state what formal verification
  adds over the empirical baseline — specifically, which guarantees generalize
  beyond the 75 recorded positions and which remain bounded to tested examples.
- The vertical slice itself remains **proposed until separately authorized**.

---

## J. Release and completion criteria

Measurable gates. An operation is complete only when **all** applicable criteria hold.

| Gate | Measurable criterion |
|---|---|
| 1. Designed | Frozen spec (genesis commit); input language, output contract, failure taxonomy, scope defined; reviewed |
| 2. Implemented | Every claimed operation exists with a documented interface; no phantom components |
| 3. Functionally verified | Executable acceptance suite: normal cases, boundary cases, expected failures (incl. CONTRADICTION, UNDERDETERMINED, TIMEOUT, UNSUPPORTED, INVALID_INPUT); all green |
| 4. Formally verified (where applicable) | Claimed universal properties backed by kernel-checked proofs or sound procedures; proof artifacts preserved |
| 5. Integrated and reproducible | Operations compose; versions pinned; independent re-runs reproduce recorded results bit-for-bit (modulo declared non-determinism such as timing) |
| 6. Scope-qualified release | Full declared capability matrix passes acceptance; limitations and unsupported operations documented; "all-rounder within scope S, matrix vX.Y" claim evidenced |

**Completion rule (frozen):** MSVE shall not be declared complete merely because
planned components exist. Every advertised operation needs an explicit contract,
acceptance tests, documented failure behaviour, and appropriate evidence.
Unsupported, unproven, or untested capabilities remain explicitly labelled in the
release matrix. A failed operation stays visible; it is not removed to clean the record.

---

## Appendix 1. Glossary (v0.1 draft)

- **Specification:** a formal, versioned, content-hashed document in the input language.
- **Frozen specification:** a specification reviewed and baselined; immutable thereafter.
- **Projection:** the declared observable properties under which model distinctness is judged.
- **Witness:** a concrete model, counterexample, or proof artifact produced as evidence.
- **Trusted component:** relied upon without re-verification within a documented boundary.
- **Result package:** the versioned, hashed bundle defined in §G.

## Appendix 2. Unresolved design decisions (carried, not hidden)

1. Exact Lean version selection and the proof-carrying interface format — deferred to
   implementation authorization; does not block design freeze.
2. Full v0 problem-class catalog beyond the initial matrix — the matrix (Document 3)
   is authoritative; extensions need their own review.
3. Whether the fuzzer's random seeds should be centrally registered or per-run
   recorded — per-run recording is specified (§G.5); central registry deferred.
4. Precise timeout/memory defaults per problem class — to be set at implementation
   authorization, documented per release.

*End of MSVE_DESIGN_SPEC_v0.1.md (draft for review).*
