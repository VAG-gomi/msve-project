# Independent Normative Review — MSVE Work Order 0.8.8

**Reviewer role:** normative text only. No model code executed.
**Spec reviewed:** `/home/hatch/workspace/msve-design/work-order-0.8.8-candidate/MSVE_DESIGN_SPEC_v0.8.md`
**Spec SHA-256:** `d194537c2f15755023ca00e3503de9283d84a7e7b9201e35f351c666e96ad169` (94,563 bytes)
**Review completed:** 2026-10-09T14:41:14Z

---

## Q1. §E.6b — ClaimDescriptor completeness (lines 1318–1356)

**Finding: structurally complete, with one field-definition gap (see N-2).**
- All six descriptor fields defined with types (lines 1166–1168): `claim_kind, proposition, goal_ref, inputs_ref, assumptions, spec_version`.
- Mandatory-fields-per-kind: explicit — "All six descriptor fields are mandatory. `assumptions` may be `[]`." (lines 1328–1329). Incomplete descriptor → no identity; basis rejected. No sentinel fallback.
- Identity policy: explicit and syntactic — "distinct goal/proposition/inputs yield distinct identities even if outputs coincide" (lines 1326–1327), with the owner decision recorded: "syntactic identity selected as the working direction; semantic equivalence is not attempted" (lines 1327–1328).
- Payload-free variants: addressed — `HOLDS`, `NO_SOLUTION`, `CONTRADICTION`, `UNIQUE_UNDER_PROJECTION` use descriptors with check property/search problem as `proposition` and goal as `goal_ref`; "identity does not depend on an output hash" (lines 1331–1334).

**Objective met:** Yes, subject to N-2.

## Q2. Revised invariants 25–28 — claim_id linkage (lines 1462–1497)

**Finding: linkage present; invariant 27 references an undefined function (see N-1).**
- Inv 25 (proof): requires `vr.claim_id = cid` + descriptor presence (`∃ d ∈ claim_descriptors: d.claim_id = cid`). Well-formed.
- Inv 26 (recompute): requires `vr.claim_id = cid` + `DERIVED_VALUE` compatibility + descriptor presence. Well-formed.
- Inv 27 (solver): requires `provenance_ref` → invocation with `i.claim_id = cid` + `i.inputs_ref` match + `outcome_compatible(i, obs, r.semantic_result)`. **The `outcome_compatible` function is never defined** (see N-1).
- Inv 28 (test): requires `vr.claim_id = cid` + `inputs_ref` match + descriptor presence. Well-formed. (Note: 0.8.8 adds the `inputs_ref` check that 0.8.7 lacked — improvement.)

**Objective met:** Partially — blocked by N-1 for invariant 27.

## Q3. Type definitions — ClaimDescriptor and SolverInvocation (lines 1166–1183)

**Finding: complete except the `claim_id` field/method ambiguity (see N-2).**
- `ClaimDescriptor`: six fields typed; `claim_kind` enumeration listed; canonical encoding specified (`"|"`-joined); `claim_id = sha256(canonical_encoding)` described in a comment.
- `SolverInvocation`: eight fields including `claim_id: Hash` and `invocation_id: Hash` as explicit stored fields.
- `EvidenceBundle`: both new collections present (`claim_descriptors`, `solver_invocations`, line 1162).
- `ResultRecord.claim_id: Option<Hash>` (line 1078); `VerificationRecord.claim_id: Hash` (line 1150, with normative comment lines 1151–1152).

## Q4. Sentinel removal and remaining undefined identity

**Finding: sentinel gone; one new evasion path (see N-3).**
- `__no_claim_key__`: absent from the spec. ✓
- Old `claim_key` function: absent. ✓
- **N-3 (blocking):** No invariant encodes the §E.6b prose requirement (line 1321) that "every result that carries an assurance basis must have `claim_id = Some(h)`." Invariants 25–28 all place `r.claim_id = Some(cid)` in the *antecedent*; a record with `claim_id = None` and e.g. `KERNEL_PROOF ∈ bases` satisfies every invariant vacuously. The central requirement is evadable by omitting the claim_id.

## Q5. The five identity tests

The spec prose addresses each (lines 1323–1326, 1331–1334):
1. derive 2+2 vs 8/2: distinguished by `goal_ref`/`proposition`. ✓
2. Different propositions, same artefact hash: distinguished by `proposition`. ✓
3. Different projections: distinguished by `assumptions`. ✓
4. Different inputs: distinguished by `inputs_ref`. ✓
5. Payload-free variants: descriptor-based, no output hash. ✓
Whether the regression suite exercises these is outside normative remit (model reviewer's scope).

---

## Findings

| ID | Issue | Lines | Severity |
|---|---|---|---|
| N-1 | `outcome_compatible(i, obs, sr)` used in inv 27 but never defined; §E.6b gives only a prose table | 1487 | **Blocking** |
| N-2 | `d.claim_id` field-access in inv 25/26/28, but `ClaimDescriptor` has no `claim_id` field — only a derived-value comment; inconsistent with `SolverInvocation.claim_id` which is a stored field | 1166–1174, 1467, 1479, 1495 | **Blocking** |
| N-3 | No invariant requires `bases ≠ [] ⇒ claim_id = Some(_)`; `claim_id = None` + any basis satisfies inv 25–28 vacuously, evading the central requirement stated in §E.6b prose | 1321, 1462–1497 | **Blocking** |

**N-1 detail:** Same defect class as R1-2 (0.8.7). A formal invariant cannot reference an undefined function symbol. The prose interpretation table (lines 1348–1353) is not a definition.

**N-2 detail:** Either add `claim_id: Hash` as a stored field on `ClaimDescriptor` (with a well-formedness invariant tying it to the hash of the canonical encoding), or define `claim_id(d: ClaimDescriptor): Hash` as a function and use function-application syntax in the invariants. The current text is ambiguous.

**N-3 detail:** Add an invariant such as `r.assurance_bases ≠ [] ⇒ ∃ cid: Hash. r.claim_id = Some(cid)`, or fold the requirement into each of 25–28 by making `claim_id = None` with a claimed basis an explicit violation.

## Objective assessment

| 0.8.8 objective | Met? |
|---|---|
| R1-1: claim identity for payload-free variants | **Yes in prose** (descriptor-based); blocked by N-2/N-3 for formal force |
| Solver linkage: observation tied to exact claim | **Partially** — invocation binding present; blocked by N-1 (undefined compatibility fn) |
| `provenance_ref` target and resolution | **Yes** — defined as `invocation_id` in `solver_invocations` (lines 1341–1347) |
| Sentinel removed | **Yes** |
| Claim-key coverage for all variants | Superseded by descriptor design; N-3 leaves an evasion path |

**Verdict:** The Option A design is sound and the prose is explicit, but three blocking formal gaps (N-1, N-2, N-3) prevent the normative text from mechanically expressing its own central requirement. These are drafting repairs, not owner decisions. The candidate should not be presented as formally complete until N-1–N-3 are repaired.
