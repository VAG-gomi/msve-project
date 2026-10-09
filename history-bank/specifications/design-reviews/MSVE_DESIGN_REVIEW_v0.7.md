# MSVE Design Review v0.7

**Reviewer:** Muse, operating as the MSVE Specification Correction Loop
(self-review — NOT independent) · **Status:** DRAFT
**Scope:** the six-document v0.7 package
**Work order:** v0.7 targeted correction pass (D-016–D-024; D-001–D-015 kept)
**Decision requested:** owner review; this review does not freeze, accept, or
authorize implementation.

**Evidence labels:** SPECIFICATION_REVIEW · MECHANICAL_DOCUMENT_CHECK ·
IMPLEMENTATION_CONFORMANCE · EXECUTED_TEST · FORMAL_PROOF · INCONCLUSIVE.

## 1. What the v0.6 forensic review broke, and what survived

Conceded in full (adjudication recorded 2026-10-09): the v0.6 gate verdict
was premature. Preserved: the three-stage validator architecture, the
quantifier-body grammar rule, the evidence taxonomy, the assurance
vocabulary, the inherited ledger. Repaired: D-016–D-024 below; D-004, D-005,
D-009, D-014, D-015 reopened and re-corrected.

## 2. New-defect coverage (D-016 – D-024)

| ID | v0.7 correction | Evidence | Status |
|---|---|---|---|
| D-016 | `is_some` in builtins; `range(n)=[0..n-1]`; recursive structural equality (§B.4 rules 3, 11) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (M5: all identifiers in all 6 examples resolve) | Corrected at spec level |
| D-017 | Unique binary64 grammar: leading `1` + `-1022≤Exp≤1023` for normals; one subnormal form (`p-1074`); zero exactly `0x0.0000000000000p+0`; no leading-zero exponents | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (M6: v0.6 collision pairs rejected; 19,451-value round-trip) | Corrected at spec level |
| D-018 | Function values not encodable (named reason); `Impl` carries `sig`; ±inf encodable; NaN → packaging failure | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (every TypeExpr kind audited) | Corrected at spec level |
| D-019 | `Real` exact rational payloads; `to_rat` total; `real-not-encodable` removed; packaging failures → INTERNAL_ERROR(output-not-encodable), semantic result preserved (§E.7 inv. 10) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-020 | `is_error_code` closure predicate + contract conjunct; `DecodeOutcome` invariant normative | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK (M7: 12 codes, table ∪ validate == disjuncts) | Corrected at spec level |
| D-021 | `recompute:` separate VerifItem; `proof:` kernel-only; §B.12 ex.18 rejects old syntax | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-022 | Payload-carrying SemanticResult + binding rules; 14 exhaustive §E.7 invariants; `involved_records`/`recorded_at` defined; Level B ⇒ spec-acceptance (inv. 12) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |
| D-023 | All seven Mermaid sources reproduced in the visualisation plan | MECHANICAL_DOCUMENT_CHECK (7 fenced sources present) | Corrected |
| D-024 | Duplicate rule: same kind + same method (checker IDs don't distinguish); differential+fuzz legal (§B.12 ex.17) | SPECIFICATION_REVIEW + MECHANICAL_DOCUMENT_CHECK | Corrected at spec level |

## 3. Reopened inherited defects

D-004 (canonical-3, impl signatures, non-finite/function rules); D-005
(unique binary64 per D-017); D-009 (exact Real payloads per D-019); D-014
(`recompute:` separation per D-021); D-015 (closure per D-020/D-022). Each
re-entry preserves its original ID, failure mode, and version history —
reopening is recorded, not rewritten.

## 4. The strengthened method — applied, with a catch to show for it

Three new checks were committed after the v0.6 failure and run during v0.7
drafting:

- **M5 (identifier resolution):** every identifier in every §B.11 example
  resolves to a keyword, type name, builtin, defined name, bound variable,
  field, or the special variable. Result: all resolve — the v0.6 `is_some`
  class of defect is now mechanically detectable.
- **M6 (collision construction):** for the binary64 uniqueness claim —
  the old collision pairs must be rejected, and 19,451 values (incl.
  subnormals, ±0, extremes) must round-trip. **This check caught a real
  hole in the v0.7 draft**: the first revision omitted the exponent-range
  bound, admitting `0x1.0000000000000p-1074` for the minimum subnormal.
  Fixed before delivery (`-1022 ≤ Exp ≤ 1023`); recorded in the ledger.
- **M7 (enumeration membership):** the 12 `is_error_code` disjuncts equal
  the §B.13 table codes ∪ the validate-stage codes, exactly.

M1–M4 re-run: nonterminal closure 47/55/0; 100 grammar literals accounted,
0 unused keywords; all section references resolve across 6 documents;
per-token derivation of the validator contract re-done under the v0.7
grammar (with `is_some` now defined and the closure conjunct).

## 5. Adversarial challenge — performed

1. `"[]"` → decode-ok → `validate` → `rejected("empty-candidate-set")` ✓
2. Swapped/fabricated candidates → contract false ✓
3. v0.6 binary64 collision pairs → rejected under canonical-3 ✓
4. Bare quantifier body → syntax error; nested quantifiers derive ✓
5. Validator contract re-derived per-token; all identifiers resolve (M5) ✓
6. Test-backed Level B, NaN-at-packaging, shortfall, divergence — all
   representable; §E.7 exhaustive ✓
7. Shortfall computed; bases recorded; §D.6 caps each method ✓
8. Cross-document consistency: §6 below ✓
9. All 24 defects in the ledger; none renamed or dropped ✓
10. Falsifier retained: any input whose required outcome the rules don't
    entail reopens the gate ✓

## 6. Cross-document consistency report

- **Spec ↔ ledger:** D-001–D-024 each map to normative text; reopenings
  recorded with history.
- **Spec ↔ matrix:** C2 (`to_rat` total), E1 (payloads/invariants), E3
  (canonical-3), P4 (`recompute:` separation) aligned.
- **Spec ↔ acceptance plan:** contracts, regression cases, discrepancy
  protocol (incl. packaging failure), entry conditions aligned.
- **Spec ↔ visualisation:** all 7 sources reproduced; Diagram 3 shows the
  closure conjunct; Diagram 4 shows required/bases/achieved + shortfall.
- **Terminology/version:** v0.7 / `0.7.0` / `msve-canonical-3` consistent;
  `msve-canonical-2` mentioned only as superseded-before-use.

## 7. Evidence obtained vs not obtained

**Obtained:** M1–M7 as listed in §4 (MECHANICAL_DOCUMENT_CHECK);
per-token derivations and the 10 adversarial questions
(SPECIFICATION_REVIEW); the M6 draft-stage catch with its fix.

**Not obtained (disclosed):** no implementation → no
IMPLEMENTATION_CONFORMANCE, no EXECUTED_TEST; L1 sketches (U1–U4, V1–V3,
C1) are proposed methods, not FORMAL_PROOFs; L2 methods proposed, not
executed; the injectivity induction is paper, not machine-checked.
No OWNER_DECISION_REQUIRED arose.

## 8. Release-gate decision

**READY_FOR_OWNER_REVIEW.**

Reasons: D-016–D-024 each have a corrected normative rule, an invariant,
regression cases, and specification-level plus mechanical evidence (§2).
The five reopened inherited defects are re-corrected with history
preserved (§3). The strengthened method demonstrably caught a defect in
this draft (M6, §4). All required specification-level checks were
evaluated; §7 discloses what was not checked.

This status is **not** owner approval, acceptance, freeze, or
implementation authorisation. It means the package is fit for the owner's
review — and for the next adversarial round, which remains the honest
test of the loop.

*End of MSVE_DESIGN_REVIEW_v0.7.md (draft).*
