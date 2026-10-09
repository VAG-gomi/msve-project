# MSVE Visualisation Plan v0.6

**Status:** DRAFT FOR REVIEW · **Version:** 0.6
**Supersedes:** `MSVE_VISUALISATION_PLAN_v0.5.md` (retained as historical draft)

Mermaid source is authoritative; generated images are optional and non-normative.
Nothing absent from `MSVE_DESIGN_SPEC_v0.6.md`.

---

## Diagram 1 — System boundary and data flow (retained)

Unchanged in meaning.

## Diagram 2 — Specification-to-verification pipeline (retained from v0.5)

Unchanged in meaning (corpus rule: empty → INCONCLUSIVE(NO_TEST_CORPUS)).

## Diagram 3 — Validator pipeline: decode → validate → typed outcome (revised)

**Question it answers:** How does raw input become a validated candidate set,
with every rejection named and accepted data bound to the input?

```mermaid
flowchart LR
    RAW[RawInput: String] --> DEC[Decode<br/>decode_candidates<br/>§B.13 table, 10 rows<br/>deterministic priority]
    DEC -->|ok=false + error code| REJ1[rejected<br/>decoder error code]
    DEC -->|ok=true| VAL[Validate<br/>validate<br/>empty → uci → dup-uci<br/>fixed priority]
    VAL -->|rejected| REJ2[rejected<br/>semantic error code]
    VAL -->|accepted| ACC[accepted<br/>EXACTLY the decoded<br/>candidates, same order]
    CON[validator_contract:<br/>out == rejected(decode error)<br/>or out == validate(decoded)]
    INV[Malformed inputs] -.->|tested against| DEC
    NOTE[Three separate claims:<br/>(a) abstract pipeline correct<br/>(conditional on §B.13)<br/>(b) implementation conforms<br/>(c) bounded tests found<br/>no failures in cases tested]
```

## Diagram 4 — Result record and per-property verification (retained)

Unchanged in meaning (divergence-first precedence). Reference: v0.5 Diagram 4.

**v0.6 note:** the assurance block now shows three fields —
`assurance_required` (NONE | LEVEL_A | LEVEL_B),
`assurance_bases` (list: KERNEL_PROOF | INDEPENDENT_RECOMPUTE |
SOLVER_BACKED | TEST_BACKED), `assurance_achieved` (NONE | LEVEL_A | LEVEL_B) —
with `assurance_shortfall` computed by the normative rule. A diagram must
show all three plus the shortfall, never a single "assurance" badge.

## Diagram 5 — SAT/UNSAT assurance flow (retained)

Unchanged in meaning. (The `assurance:` syntax in §B.7 is the explicit mechanism.)

## Diagram 6 — Generator input-domain boundary (retained)

Unchanged in meaning.

## Diagram 7 — Maturity and release stages (retained)

Unchanged in meaning.

---

## Image-generation prompts (bounded, optional)

**Prompt for Diagram 3 (validator pipeline):**
> "Technical diagram, flat vector style, white background. Title: 'MSVE:
> Validator Pipeline (decode → validate → outcome)'. Left to right: box
> 'RawInput (String)' → box 'Decode: decode_candidates — §B.13 table, 10
> rows, deterministic priority' with two outgoing arrows: down to
> 'rejected (decoder error code)' and right to box 'Validate: validate —
> empty → uci-shape → duplicate-uci, fixed priority', which splits down to
> 'rejected (semantic error code)' and right to 'accepted: EXACTLY the
> decoded candidates, same order (no fabrication/omission/reordering)'.
> Below: box 'validator_contract: out == rejected(decode error) OR out ==
> validate(decoded candidates)'. A dashed box 'Malformed inputs' with a
> solid arrow to Decode labeled 'tested against'. A note box: 'Three
> separate claims: (a) abstract pipeline correct, conditional on §B.13;
> (b) implementation conforms; (c) bounded tests found no failures in
> cases tested.' No extra elements."

*End of MSVE_VISUALISATION_PLAN_v0.6.md (draft for review).*
