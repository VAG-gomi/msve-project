# MSVE v0.8.4 Schema Consistency Report (Phases C–E)

**Work Order:** 0.8.4 · **Date:** 2026-10-09
**Audit inputs:** see `MSVE_v0.8.4_AUDIT_INPUT_MANIFEST.md`
(candidate spec SHA-256 `9f692585cfe9c4e9322afdb75d2ff52081fcdd55ffbcc59f5a21f5251fa7c003`)

## 1. Principal question and answer

**Question:** Can the `ResultRecord` schema and all 23 normative §E.7
cross-field invariants hold together without making an intended result
state impossible or admitting a semantically contradictory record?

**Answer:** Yes, for the formalizable fragment. All 13 intended scenario
families have witnesses; all 13 targeted contradictory variants are
rejected; the joint constraints are satisfiable. Two caveats bound this
claim (see §4): invariants 3 and 12 are unformalizable as record
constraints, and three invariants (20, 21, 23) formalize only in weakened
form. One new minor finding (F-20) was confirmed.

## 2. What was checked

- **Formal model:** the reconciled formalization
  (`MSVE_v0.8.4_FORMALIZATION_RECONCILIATION.md`), derived independently
  by two reviewers from the candidate bytes and reconciled against the
  normative text. `base_code` is the exact F-01 definition (Z3 string
  theory); the four closure predicates are explicit disjunctions over the
  code lists extracted programmatically from the candidate spec
  (27/3/12/2 — counts match the spec's claims).
- **Solver:** z3 5.1.0, per-scenario `Solver()` with 30 s timeout.
- **Checks:** 46 scenario checks — 33 expected-SAT (joint + 32 scenario
  instances across the 13 families) and 13 expected-UNSAT invalid variants.
  Result: **45/46 behaved as expected.** The single non-conforming check
  is the unconstrained `joint-SAT` query, which returned `unknown`
  (solver search limitation on the heavily quantified unconstrained
  problem — see §4). Joint satisfiability is nevertheless established:
  every valid scenario's SAT model satisfies all encoded invariants, so
  the invariants are jointly satisfiable by entailment.

## 3. Findings

### F-20 (new, minor): invariant 10's packaging condition omits `canonicalization-failure`

Invariant 10's "occurred at packaging" test is `base_code(r) =
"output-not-encodable"` only. But `is_packaging_error` covers
`{output-not-encodable, canonicalization-failure}` (spec line 1097–1098),
and `canonicalization-failure: <detail>` is a specified packaging failure
joint with `output_packaging` per invariant 15b (spec line 1107). A
canonicalization-failure packaging error is therefore outside invariant
10's "semantic_result still recorded" consequent.

**Severity:** minor — a coverage gap in the invariant's protection, not an
inconsistency. Invariant 15b still forces the packaging/execution linkage
for both base codes.

**Proposed minimum correction:** change invariant 10's condition to
`base_code(r) ∈ {output-not-encodable, canonicalization-failure}` (i.e.
`is_packaging_error(r)`). Affected companion documents: the candidate
spec's §E.7 invariant 10 text; no M8 change (M8 does not evaluate this
invariant); the 0.8.3 correction report's F-01 area if re-issued.

### No other new defects

The 15b ⟸-direction concern raised during formalization was resolved
without a spec change: the restricted existential reading is the only one
consistent with NEW-C2, and the solver confirms the joint system is
satisfiable under it. The prose could state the ⟸ direction existentially
in a future pass, but this is editorial, not a defect.

## 4. Limitations and separations

1. **Source interpretation** — the reconciled formalization; two
   independent derivations converged with 8 registered ambiguities.
2. **Formal-model correctness** — this Z3 encoding; validated by the
   13/13 invalid-variant rejections (the constraints have teeth) and by
   reviewer convergence on the interpretation.
3. **Solver result** — 45/46 checks as expected; the `unknown` on the
   unconstrained joint query is a Z3 search artifact, not a spec verdict.
4. **Conclusion about the specification** — the consistency claim holds
   for the *formalized fragment*: invariants 3 and 12 (external
   references) are outside the solver's view, and invariants 20/21/23 are
   checked in weakened form (the "aboutness" of evidence — check property,
   search record, projection linkage — has no schema discriminator).

A SAT result does not prove the formalization faithful to the prose; the
two-reviewer convergence is the evidence for that step. Bounded witnesses
do not prove universal correctness. No formal proof was produced.

## 5. Phase E cross-field check dispositions

| Check | Disposition |
|---|---|
| E1. Invariants reference only defined fields / scoped variables | CONFIRMED (inv-23's vacuous `p` noted as formalization smell, not a field error) |
| E2. Packaging/execution reasons use compatible base-code semantics | PARTIALLY SUPPORTED (F-20: inv-10 omits `canonicalization-failure`) |
| E3. Admission and execution statuses agree | CONFIRMED (inv 1, 2, 10; witnesses S5/S6) |
| E4. Payloads resolve in the correct evidence collection | CONFIRMED for the formalized fragment (`resolves` = hash-membership, interpretation logged) |
| E5. Every §E.2 result type has a valid witness | CONFIRMED (all 11 alternatives, S7) |
| E6. Shortfall agrees with required/achieved | CONFIRMED (S8 × 3; X-shortfall-inconsistent rejected) |
| E7. All summary states representable per precedence | CONFIRMED (S9 × 4 + NOT_RUN) |
| E8. Partial results agree with execution status | CONFIRMED (S10 × 2; X-partial+completed rejected) |
| E9. Evidence-free claims rejected where evidence mandatory | CONFIRMED for the formalized fragment (X12, X-unique-no-evidence rejected; 21/23 weakened caveat) |
| E10. No accidental universal impossibility | CONFIRMED (31 valid scenario instances SAT) |
