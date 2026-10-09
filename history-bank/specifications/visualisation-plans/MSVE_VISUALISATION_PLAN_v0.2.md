# MSVE Visualisation Plan v0.2

**Status:** DRAFT FOR REVIEW · **Version:** 0.2
**Supersedes:** `MSVE_VISUALISATION_PLAN_v0.1.md` (retained as historical draft)

Generated images are **explanatory aids, not normative specifications**. The
authoritative representation of every diagram below is its Mermaid source
(version-controlled text). Image generation, where used, must not invent
components, connections, or guarantees absent from the written spec
(`MSVE_DESIGN_SPEC_v0.2.md`).

Principal change from v0.1: Diagram 4 (flat result-status state machine) is
**replaced** — the v0.2 status architecture uses orthogonal fields, not one
state machine (Correction A, review R1).

---

## Diagram 1 — System boundary and data flow

**Question it answers:** What crosses MSVE's boundary, in which direction, and
what is never allowed to cross?

```mermaid
flowchart LR
    H[Human: spec author/reviewer] -->|formal spec, frozen| P[Parser / Validator]
    H -->|candidate draft| R[Review & freeze gate]
    R -->|frozen spec| P
    NL[Natural-language request] -.->|drafting aid only| R
    NL -.->|NEVER direct| P
    NLA[NL-extracted assumptions] -.->|proposals only,<br/>NEVER executable| R
    P -->|INVALID_INPUT / UNSUPPORTED| H
    P -->|ACCEPTED| D[Dispatcher]
    D --> S[SymPy layer]
    D --> Z[Z3 layer]
    D --> L[Lean kernel]
    D --> I[Independent checker]
    S & Z & L & I --> PR[Provenance recorder]
    PR --> RP[Result record + evidence bundle]
    RP --> H
```

## Diagram 2 — Specification-to-verification pipeline

**Question it answers:** What are the ordered stages from a specification to a
result record, and where can each stage fail?

```mermaid
flowchart TD
    A[Spec text] --> B{Parse, type-check,<br/>mandatory fields}
    B -->|fail| F1[admission: INVALID_INPUT]
    B -->|pass| C{Scope & support check}
    C -->|outside| F2[admission: UNSUPPORTED]
    C -->|inside| D[Human review & freeze]
    D --> E[Dispatch to layers]
    E --> G{Execute within resource limits}
    G -->|limit hit| F3[execution: TIMEOUT<br/>partial results labelled]
    G -->|interrupted| F3b[execution: INTERRUPTED]
    G -->|done| H{Independent check}
    H -->|disagree| F4[verification: CHECKER_DIVERGENCE]
    H -->|agree| J[Assemble result record]
    J --> K[Orthogonal fields:<br/>admission / execution /<br/>semantic_result /<br/>verification / evidence]
```

## Diagram 3 — Trust boundary, SAT/UNSAT assurance

**Question it answers:** Which components are trusted for what, and what
assurance level attaches to satisfiability vs. unsatisfiability claims?

```mermaid
flowchart TB
    subgraph Trusted [Trusted within documented boundary]
        PK[Parser: syntax, typing,<br/>mandatory fields]
        LK[Lean kernel: proof-term acceptance<br/>relative to formal statement]
    end
    subgraph Checked [Outputs independently re-checked]
        ZM[Z3 models → re-checked<br/>vs canonical spec]
        SY[SymPy results →<br/>substitution-checked where possible]
    end
    subgraph SAT [SAT assurance]
        SM[Model witness +<br/>independent re-check record]
    end
    subgraph UNSAT [UNSAT assurance levels]
        UA[Level A: checkable proof certificate<br/>→ independently established]
        UB[Level B: solver-backed,<br/>pinned solver + config<br/>→ labelled, not 'proved']
        UC[Unsat core: diagnostic only<br/>→ never an independent proof]
    end
    subgraph Independent [Independent of primary path]
        REF[Reference implementation]
        FUZ[Property fuzzer]
    end
    REF & FUZ --> CMP[Differential comparison]
    CMP -->|disagreement| DISC[verification: CHECKER_DIVERGENCE<br/>→ investigation, never silent choice]
```

## Diagram 4 — Result-status architecture (REPLACED per Correction A)

**Question it answers:** How do the orthogonal status fields compose, and which
combinations are forbidden?

*This diagram replaces the v0.1 flat state machine. Statuses are fields of one
result record, not nodes in one machine.*

```mermaid
flowchart TB
    subgraph REC [Result record — orthogonal fields]
        ADM[admission:<br/>ACCEPTED<br/>INVALID_INPUT<br/>UNSUPPORTED]
        EXE[execution:<br/>NOT_STARTED · RUNNING · COMPLETED<br/>TIMEOUT · INTERRUPTED · INTERNAL_ERROR]
        SEM[semantic_result per goal:<br/>prove → PROVED / DISPROVED / INCONCLUSIVE<br/>check → HOLDS / VIOLATED / INCONCLUSIVE<br/>construct → ARTIFACT_CONSTRUCTED /<br/>NO_SOLUTION / INCONCLUSIVE<br/>compare-models → UNIQUE_UNDER_PROJECTION /<br/>UNDERDETERMINED / CONTRADICTION /<br/>INCONCLUSIVE]
        VER[verification:<br/>NOT_RUN · PASS · FAIL<br/>INCONCLUSIVE · CHECKER_DIVERGENCE]
        EVI[evidence: derivation records,<br/>proof artifacts, witnesses,<br/>verification records,<br/>external evidence records]
    end
    FORB1[FORBIDDEN: execution COMPLETED<br/>presented as verification PASS]
    FORB2[FORBIDDEN: TIMEOUT →<br/>CONTRADICTION or UNDERDETERMINED]
    FORB3[FORBIDDEN: ARTIFACT_CONSTRUCTED<br/>read as verified]
    FORB4[FORBIDDEN: EVIDENCE_RECORDED<br/>read as scientific confirmation]
    REC -.-> FORB1 & FORB2 & FORB3 & FORB4
```

Accompanying table (example legal combinations):

| admission | execution | semantic_result | verification | Reading |
|---|---|---|---|---|
| ACCEPTED | COMPLETED | PROVED | PASS | Proposition proved; independent check passed |
| ACCEPTED | COMPLETED | INCONCLUSIVE(SOLVER_UNKNOWN) | NOT_RUN | Completed run; nothing established |
| ACCEPTED | TIMEOUT | INCONCLUSIVE(RESOURCE_EXHAUSTED) | NOT_RUN | Partial results labelled separately |
| ACCEPTED | COMPLETED | UNDERDETERMINED | PASS | Two witnesses; non-uniqueness verified |
| INVALID_INPUT | NOT_STARTED | — | NOT_RUN | Rejected before execution |
| ACCEPTED | COMPLETED | CONTRADICTION (Level B) | PASS | Unsat established solver-backed; assurance labelled |

## Diagram 5 — Provenance: separated claims

**Question it answers:** Which provenance claim does each mechanism actually support?

```mermaid
flowchart LR
    HASH[SHA-256 over<br/>canonical JSON] --> ID[Content identity:<br/>recomputable by anyone]
    REF[Independently preserved<br/>manifest / anchor] --> INT[Integrity vs reference:<br/>substitution detectable]
    SIG[Project-owner signed<br/>release tag] --> AUTH[Authenticity:<br/>origin claim]
    CHECK[Verification procedures<br/>§E/§F] --> CORR[Correctness:<br/>stated properties only]
    ID & INT & AUTH & CORR --> NOTE[No single mechanism gives all four.<br/>Never 'tamper-proof' —<br/>'tamper-evident relative to<br/>a trusted reference'.]
```

---

## Image-generation prompts (bounded, optional)

**Prompt for Diagram 4 (result-status architecture):**
> "Technical diagram, flat vector style, white background. Title: 'MSVE Result
> Record — Orthogonal Status Fields'. Five labeled boxes in a row: 'admission:
> ACCEPTED / INVALID_INPUT / UNSUPPORTED', 'execution: NOT_STARTED / RUNNING /
> COMPLETED / TIMEOUT / INTERRUPTED / INTERNAL_ERROR', 'semantic_result (per
> goal): PROVED / DISPROVED / HOLDS / VIOLATED / ARTIFACT_CONSTRUCTED /
> UNIQUE_UNDER_PROJECTION / UNDERDETERMINED / CONTRADICTION /
> INCONCLUSIVE(reason)', 'verification: NOT_RUN / PASS / FAIL / INCONCLUSIVE /
> CHECKER_DIVERGENCE', 'evidence: derivation, proof, witness, verification,
> external-evidence records'. Below, four red 'FORBIDDEN' note boxes:
> 'COMPLETED presented as PASS', 'TIMEOUT reported as CONTRADICTION or
> UNDERDETERMINED', 'ARTIFACT_CONSTRUCTED read as verified',
> 'EVIDENCE_RECORDED read as scientific confirmation'. No extra boxes, no
> decorative elements, no invented labels."

**Prompt for Diagram 3 (trust boundary, SAT/UNSAT):**
> "Technical diagram, flat vector style, white background. Title: 'MSVE Trust
> Boundary and Assurance Levels'. Grouped boxes: 'Trusted (documented
> boundary)': parser, Lean kernel. 'Checked': Z3 models re-checked, SymPy
> substitution-checked. 'UNSAT assurance': Level A (checkable certificate,
> independently established), Level B (solver-backed, labelled not proved),
> unsat core (diagnostic only). 'Independent': reference implementation,
> fuzzer, differential comparison. No extra components, no decorative elements."

Do not generate decorative imagery. If a precise diagram or a few sentences
communicate more reliably, prefer them.

*End of MSVE_VISUALISATION_PLAN_v0.2.md (draft for review).*
