# MSVE Visualisation Plan v0.1

**Status:** DRAFT FOR REVIEW · **Version:** 0.1

Generated images are **explanatory aids, not normative specifications**. The
authoritative representation of every diagram below is its Mermaid source
(version-controlled text). Image generation, where used, must not invent
components, connections, or guarantees absent from the written spec.

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
    P -->|INVALID_INPUT on ill-formed| H
    P --> D[Dispatcher]
    D --> S[SymPy layer]
    D --> Z[Z3 layer]
    D --> L[Lean kernel]
    D --> I[Independent checker]
    S & Z & L & I --> PR[Provenance recorder]
    PR --> RP[Versioned result package]
    RP --> H
```

## Diagram 2 — Specification-to-verification pipeline

**Question it answers:** What are the ordered stages from a specification to a
verifiable result, and where can each stage fail?

```mermaid
flowchart TD
    A[Spec text] --> B{Parse & type-check}
    B -->|fail| F1[INVALID_INPUT]
    B -->|pass| C{Scope & support check}
    C -->|outside| F2[UNSUPPORTED]
    C -->|inside| D[Human review & freeze]
    D --> E[Dispatch to layers]
    E --> G{Execute within resource limits}
    G -->|limit hit| F3[TIMEOUT]
    G -->|done| H{Independent check}
    H -->|disagree| F4[CHECKER_DIVERGENCE]
    H -->|agree| J[Provenance packaging]
    J --> K[Result: DERIVED / PROVED / CONSTRUCTED / VERIFIED / UNDERDETERMINED / CONTRADICTION]
```

## Diagram 3 — Trust boundary and independent checking

**Question it answers:** Which components are trusted for what, and where does
independent checking sit?

```mermaid
flowchart TB
    subgraph Trusted [Trusted within documented boundary]
        PK[Parser: syntax & typing]
        LK[Lean kernel: proof-term acceptance]
    end
    subgraph Checked [Outputs independently re-checked]
        ZM[Z3 models → re-checked vs spec]
        SY[SymPy derivations → substitution-checked]
    end
    subgraph Independent [Independent of primary path]
        REF[Reference implementation]
        FUZ[Property fuzzer]
    end
    REF & FUZ --> CMP[Differential comparison]
    CMP -->|disagreement| DISC[Recorded discrepancy → investigation]
```

Labels on trust: the parser is trusted for syntax, not semantics; the kernel for
proof-term acceptance, not formalization adequacy; Z3 models are *checked*, not
trusted.

## Diagram 4 — Result-status state machine

**Question it answers:** Which statuses can an MSVE run end in, and which
transitions are forbidden?

```mermaid
stateDiagram-v2
    [*] --> Running
    Running --> DERIVED
    Running --> PROVED
    Running --> CONSTRUCTED
    Running --> VERIFIED
    Running --> UNDERDETERMINED : second model found
    Running --> CONTRADICTION : unsat established
    Running --> TIMEOUT : limit reached
    Running --> CHECKER_DIVERGENCE : checkers disagree
    Running --> UNSUPPORTED : boundary hit
    Running --> INVALID_INPUT : validation failed
    note right of TIMEOUT : TIMEOUT never transitions to UNDERDETERMINED or CONTRADICTION
    note right of UNDERDETERMINED : requires witnesses, not a solver 'unknown'
    DERIVED & PROVED & CONSTRUCTED & VERIFIED & UNDERDETERMINED & CONTRADICTION --> [*]
    TIMEOUT & CHECKER_DIVERGENCE & UNSUPPORTED & INVALID_INPUT --> [*]
```

## Diagram 5 — Provenance and evidence flow

**Question it answers:** What evidence attaches to a result, and how is it
linked tamper-evidently?

```mermaid
flowchart LR
    SPEC[Frozen spec<br/>hash] --> PKG[Result package]
    IN[Inputs<br/>hashes] --> PKG
    TOOL[Tool / solver / checker<br/>versions + config] --> PKG
    WIT[Witnesses / proofs<br/>derivation records] --> PKG
    SEED[Seeds / fuzz corpus] --> PKG
    OUT[Outputs<br/>hashes] --> PKG
    PKG --> VER{Re-verification<br/>after change}
    VER -->|spec/tool changed| SUP[Prior package: SUPERSEDED<br/>preserved, not deleted]
    VER -->|unchanged| REP[Independent reproduction]
```

---

## Image-generation prompts (bounded, optional)

Use only if a presentation context needs rendered figures. Each prompt must
reproduce exactly the entities and relations of the corresponding Mermaid
diagram — no additions.

**Prompt for Diagram 1 (system boundary):**
> "Technical architecture diagram, flat vector style, white background. Title:
> 'MSVE System Boundary'. Boxes: 'Human (spec author/reviewer)', 'Review &
> freeze gate', 'Parser / Validator', 'Dispatcher', 'SymPy layer', 'Z3 layer',
> 'Lean kernel', 'Independent checker', 'Provenance recorder', 'Versioned result
> package', and a dashed box 'Natural-language request (drafting aid only)'.
> Solid arrows: Human → Parser (label 'formal spec, frozen'); Review gate →
> Parser ('frozen spec'); Parser → Dispatcher; Dispatcher → each layer;
> layers → Provenance recorder → result package → Human. Dashed arrows:
> natural-language box → Review gate ('drafting aid only'), and a crossed-out
> dashed arrow from the natural-language box to the Parser labeled 'NEVER
> direct'. No extra components, no decorative elements, no invented labels."

**Prompt for Diagram 4 (status state machine):**
> "Technical state diagram, flat vector style, white background. Title: 'MSVE
> Result Statuses'. One start node labeled 'Running' with arrows to eleven
> terminal states: DERIVED, PROVED, CONSTRUCTED, VERIFIED, UNDERDETERMINED,
> CONTRADICTION, TIMEOUT, CHECKER_DIVERGENCE, UNSUPPORTED, INVALID_INPUT, plus
> a note box: 'TIMEOUT never becomes UNDERDETERMINED or CONTRADICTION' and a
> note box: 'UNDERDETERMINED requires witnesses, not solver unknown'. No extra
> states, no decorative elements."

Do not generate decorative imagery. If a precise diagram or a few sentences
communicate more reliably, prefer them.

*End of MSVE_VISUALISATION_PLAN_v0.1.md (draft for review).*
