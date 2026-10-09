# MSVE Visualisation Plan v0.5

**Status:** DRAFT FOR REVIEW · **Version:** 0.5
**Supersedes:** `MSVE_VISUALISATION_PLAN_v0.4.md` (retained as historical draft)

Mermaid source is authoritative; generated images are optional and non-normative.
Only diagrams whose meaning changed are updated. Nothing absent from
`MSVE_DESIGN_SPEC_v0.5.md`.

---

## Diagram 1 — System boundary and data flow (retained from v0.2)

Unchanged in meaning.

## Diagram 2 — Specification-to-verification pipeline (updated: corpus rule)

```mermaid
flowchart TD
    A[Spec text] --> B{Parse, type-check,<br/>mandatory fields}
    B -->|fail| F1[admission: INVALID_INPUT<br/>execution: NOT_STARTED<br/>semantic_result: None]
    B -->|pass| C{Scope & support check}
    C -->|outside| F2[admission: UNSUPPORTED]
    C -->|inside| D[Human review & freeze]
    D --> E[Dispatch to layers]
    E --> G{Execute within resource limits}
    G -->|limit hit| F3[execution: TIMEOUT<br/>partial_results labelled]
    G -->|done| S[solver_observation:<br/>SAT / UNSAT / UNKNOWN]
    S --> R[semantic_result under<br/>assurance policy]
    R --> H{Corpus check<br/>for check goals}
    H -->|empty corpus| F5[INCONCLUSIVE<br/>(NO_TEST_CORPUS)<br/>never vacuous HOLDS]
    H -->|non-empty| T{Independent check}
    T -->|disagree| F4[verification: CHECKER_DIVERGENCE<br/>per-property records kept]
    T -->|agree| J[Assemble result record:<br/>§E.1 typed schema]
```

## Diagram 3 — Selector, validator, and input routing (updated: defect 03)

**Question it answers:** Which inputs go to the selector, which to the validator,
and what does each contract cover?

```mermaid
flowchart LR
    RAW[RawInput: String<br/>serialized candidate set] --> VAL[Abstract validator<br/>RawInput -> Option(CandidateSet)<br/>App.2 §A2.5 + §A2.9]
    VAL -->|None + defect named| REJ[Rejected]
    VAL -->|Some(cs)| WF[Well-formed CandidateSet]
    WF --> SEL[Abstract selector<br/>CandidateSet -> Candidate<br/>prefers comparator]
    SEL --> OUT[Unique maximal candidate<br/>whole-record member]
    INV[Malformed inputs] -.->|tested against| VAL
    INV -.->|NEVER routed to| SEL
    NOTE[Three separate claims:<br/>(a) abstract model correct<br/>(b) implementation conforms<br/>(c) bounded tests found<br/>no failures in cases tested]
```

## Diagram 4 — Result record and per-property verification (retained from v0.4)

Unchanged in meaning (divergence-first precedence). Reference: v0.4 Diagram 4.

## Diagram 5 — SAT/UNSAT assurance flow (retained from v0.3)

Unchanged in meaning. (The `assurance:` syntax in §B.7 is the explicit mechanism.)

## Diagram 6 — Generator input-domain boundary (retained from v0.3)

Unchanged in meaning.

## Diagram 7 — Maturity and release stages (retained from v0.3)

Unchanged in meaning.

---

## Image-generation prompts (bounded, optional)

**Prompt for Diagram 3 (selector, validator, routing):**
> "Technical diagram, flat vector style, white background. Title: 'MSVE:
> Validator and Selector Routing'. Left to right: box 'RawInput (String,
> serialized candidate set)' → box 'Abstract validator: RawInput →
> Option(CandidateSet), contract App.2 §A2.5+§A2.9' with two outgoing arrows:
> down to 'Rejected (None, defect named)' and right to 'Well-formed
> CandidateSet' → box 'Abstract selector: CandidateSet → Candidate (prefers
> comparator)' → box 'Unique maximal candidate (whole-record member)'. A dashed
> box 'Malformed inputs' with a solid arrow to the validator labeled 'tested
> against' and a crossed-out dashed arrow to the selector labeled 'NEVER routed
> here'. A note box: 'Three separate claims: (a) abstract model correct; (b)
> implementation conforms; (c) bounded tests found no failures in cases
> tested.' No extra elements."

*End of MSVE_VISUALISATION_PLAN_v0.5.md (draft for review).*
