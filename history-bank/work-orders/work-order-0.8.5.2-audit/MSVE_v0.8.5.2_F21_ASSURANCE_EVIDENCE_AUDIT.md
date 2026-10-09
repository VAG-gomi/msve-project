# MSVE v0.8.5.2 F-21 Assurance Evidence Audit

**Work Order:** 0.8.5.2 · **Date:** 2026-10-09
**Artefacts inspected:** `s1_assignment.json`, `audit_model.py`,
`MSVE_v0.8.4_FORMALIZATION_RECONCILIATION.md`,
`MSVE_v0.8.4_WITNESS_AND_COUNTERMODEL_CATALOG.md`,
candidate spec `MSVE_DESIGN_SPEC_v0.8.md` (§D.6, §E.1, §E.4–§E.7),
the S1 scenario constraints in `run_audit.py`.

## The S1 model's assurance claim (from `s1_assignment.json`)

- `assurance_required = LEVEL_A`, `assurance_achieved = LEVEL_A`,
  bases = {`KERNEL_PROOF`}.
- Evidence present: `derivation_ref` resolves in `derivation_records`
  (invariant 9); `value_ref` resolves in `constructed_artifacts`
  (invariant 15).
- Evidence **absent**: no `resolves` fact for `proof_artifacts`;
  `verification_records` empty; `verification_summary = NOT_RUN`;
  no solver observation.

The S1 description in the transferred records is accurate: the JSON was
not mis-summarized.

## Normative requirements (candidate spec)

- §E.5: `derive` goals at Level A require "kernel-checked proof OR
  independent recomputation with agreement (evidential meaning: §D.6)".
- §E.1: "`KERNEL_PROOF` from `proof: kernel-checked …`" — the basis is
  derived from the input specification's `proof:` field.
- §E.7 invariant 6 (the only assurance-basis invariant):
  `assurance_achieved = LEVEL_A ⟹ KERNEL_PROOF ∈ assurance_bases ∨
  INDEPENDENT_RECOMPUTE ∈ assurance_bases`. It constrains the *claimed*
  basis, not its substantiation.
- No invariant links `KERNEL_PROOF ∈ assurance_bases` to
  `evidence.proof_artifacts`, to any `VerificationRecord`, or to the
  `verification_summary`. Invariant 17 (`PROVED` ⟹ proof artifact
  resolves) applies only to the `PROVED` alternative, not to
  `DERIVED_VALUE` with a `KERNEL_PROOF` basis.

## Solver tests (z3 5.1.0, 30 s each; `f21_assurance_tests.py`, exit 0)

| Case | Result |
|---|---|
| F21-1: Level A + KERNEL_PROOF + proof artifact + PASS record | sat |
| F21-2: Level A + KERNEL_PROOF, **no** proof artifact, **no** verification records, NOT_RUN | **sat** |
| F21-3: Level A via INDEPENDENT_RECOMPUTE + recompute PASS record | sat |
| F21-3b: Level A via INDEPENDENT_RECOMPUTE, **no** agreement evidence | **sat** |
| F21-4: Level A required, LEVEL_B achieved, shortfall recorded | sat |
| F21-5: LEVEL_A achieved + KERNEL_PROOF basis + **INCONCLUSIVE** semantic result | **sat** |

## Adjudication

**F-21 is a genuine specification gap, not a formalization error.**
Invariant 6 is formalized exactly as written; the formalization is
faithful. What is missing is normative content the specification never
states: no invariant requires that an achieved assurance level be
substantiated by corresponding evidence in the record. The schema therefore
admits:

- (a) a `KERNEL_PROOF` basis with no proof artifact and no verification
  record (F21-2);
- (b) an `INDEPENDENT_RECOMPUTE` basis with no agreement evidence
  (F21-3b) — the schema has no agreement-evidence field at all;
- (c) `LEVEL_A` achieved on an `INCONCLUSIVE` (or absent) semantic result
  (F21-5) — the strongest assurance claim attached to no result.

On (c): the spec's own shortfall pattern (invariant 11) pairs
`INCONCLUSIVE{ASSURANCE_REQUIREMENT_UNMET}` with *unachieved* Level A.
Achieved Level A on an inconclusive result is semantically incoherent
under §E.5, yet no invariant forbids it.

On `verification_summary = NOT_RUN` with `LEVEL_A`: this alone is **not**
a violation. Verification records (§E.6) are a per-property checking
mechanism distinct from the assurance basis; no normative text links the
summary to the achieved level. F-21's substance is the missing
basis→evidence linkage, not the NOT_RUN summary.

## Proposed finding F-21 (for owner decision; not applied)

**F-21:** The §E.7 invariants do not require that an achieved assurance
level be substantiated by evidence in the record. A record may claim
`assurance_achieved = LEVEL_A` with a `KERNEL_PROOF` (or
`INDEPENDENT_RECOMPUTE`) basis while containing no proof artifact, no
supporting verification record, and — in the extreme — no semantic result
at all.

**Smallest defensible normative corrections** (proposals; each adds
content the spec does not currently state):

1. `assurance_achieved = LEVEL_A ⟹ semantic_result = Some(sr) ∧ sr is not
   INCONCLUSIVE{...}` — achieved Level A requires an actual result.
   (Closes F21-5; consistent with invariant 11's shortfall pattern.)
2. `KERNEL_PROOF ∈ assurance_bases ⟹ ∃ vr ∈ verification_records.
   (vr.source_item = "proof" ∧ vr.result = PASS)` — the kernel-proof
   basis must be backed by a passing proof verification item. (Grounded
   in the D-033 `source_item` vocabulary, which lists `"proof"`; the
   linkage itself is new normative content.)

Both require owner judgement: they restrict records the current spec
permits, and (2) in particular interprets `source_item = "proof"` as the
canonical evidence locus, which the spec implies but does not state.

## Answers to the completion criteria

- Does S1 satisfy the complete intended assurance requirements, not just
  the encoded cross-field invariants? **No.** It satisfies every encoded
  invariant, but §E.5's "kernel-checked proof" requirement has no
  record-level evidence counterpart, and S1 contains none.
- Does the current formal model admit an evidence-free Level A claim?
  **Yes** (F21-2, F21-3b, F21-5 — all sat).
- The S1 witness remains a valid witness *of the formalized fragment*;
  it is not valid evidence that the *intended* assurance requirements
  are met. The 0.8.4/0.8.5 consistency claim must be read with this
  limitation.
