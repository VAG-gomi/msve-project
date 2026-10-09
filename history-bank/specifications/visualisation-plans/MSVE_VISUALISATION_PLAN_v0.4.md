# MSVE Visualisation Plan v0.4

**Status:** DRAFT FOR REVIEW · **Version:** 0.4
**Supersedes:** `MSVE_VISUALISATION_PLAN_v0.3.md` (retained as historical draft)

Mermaid source is authoritative; generated images are optional and non-normative.
Only diagrams whose meaning changed are updated. No visual component, connection,
or guarantee absent from `MSVE_DESIGN_SPEC_v0.4.md`.

---

## Diagram 1 — System boundary and data flow (retained from v0.2)

Unchanged in meaning. Reference: v0.2 Diagram 1.

## Diagram 2 — Specification-to-verification pipeline (retained from v0.3)

Unchanged in meaning. Reference: v0.3 Diagram 2. (Admission reasons now include
the v0.4 error catalog; `semantic_result` is absent when admission fails.)

## Diagram 3 — Selector comparator and validation boundary (retained from v0.3)

Unchanged in meaning. Reference: v0.3 Diagram 3. (Membership is now
whole-record equality per App. 2 §A2.4; the diagram's comparator box is unaffected.)

## Diagram 4 — Result record and per-property verification (updated: defect 05)

**Question it answers:** What fields does a result record carry, and in what
precedence is the verification summary computed?

```mermaid
flowchart TB
    subgraph REC [ResultRecord — §E.1]
        ADM[admission]
        EXE[execution]
        SEM[semantic_result: Option<br/>None when admission fails]
        SOL[solver_observation<br/>SAT/UNSAT/UNKNOWN + provenance]
        ASR[assurance_required /<br/>achieved / shortfall]
        VR[verification_records[]<br/>per property, attributable]
        SUM[verification_summary<br/>computed precedence:<br/>DIVERGENCE > FAIL ><br/>INCONCLUSIVE > PASS<br/>empty → NOT_RUN]
        EVI[evidence bundle]
        PRT[partial_results]
        DIS[discrepancies + follow-up]
    end
    VR --> SUM
    FORB[FORBIDDEN: summary hiding<br/>an individual record.<br/>Divergence dominates a lone<br/>FAIL: an untrustworthy check<br/>is the more urgent signal.]
```

The v0.3 ordering (FAIL before DIVERGENCE) contradicted the worked example; the
corrected precedence is divergence-first.

## Diagram 5 — SAT/UNSAT assurance flow (retained from v0.3)

Unchanged in meaning. Reference: v0.3 Diagram 5. (The `assurance: level-b
accepted` syntax in §B.7 is now the explicit mechanism the "LEVEL_B accepted"
branch depends on.)

## Diagram 6 — Generator input-domain boundary (retained from v0.3)

Unchanged in meaning. Reference: v0.3 Diagram 6.

## Diagram 7 — Maturity and release stages (retained from v0.3)

Unchanged in meaning. Reference: v0.3 Diagram 7.

---

## Image-generation prompts (bounded, optional)

**Prompt for Diagram 4 (result record, corrected precedence):**
> "Technical diagram, flat vector style, white background. Title: 'MSVE Result
> Record — Verification Precedence'. Boxes for the record fields: admission,
> execution, semantic_result (Option: absent when admission fails),
> solver_observation, assurance required/achieved/shortfall,
> verification_records[] (per property, attributable), verification_summary,
> evidence bundle, partial_results, discrepancies. A precedence list:
> 'DIVERGENCE > FAIL > INCONCLUSIVE > PASS; empty → NOT_RUN'. Note:
> 'Divergence dominates: an untrustworthy check is the more urgent signal.
> Per-property records are always preserved.' No extra elements."

*End of MSVE_VISUALISATION_PLAN_v0.4.md (draft for review).*
