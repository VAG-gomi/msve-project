# MSVE Design Review v0.4

**Status:** SELF-REVIEW — NOT AN INDEPENDENT REVIEW, NOT EXECUTED VERIFICATION
**Version:** 0.4 · **Work order:** MUSE WORK ORDER 0.3 (narrow correction pass)
**Scope:** the five v0.4 drafts against the v0.3 baseline and the six blockers

Method: every defect below was verified against the v0.3 text before correction.
Every consistency check was performed by actual derivation against the v0.4
productions — token by token for the selector example — not by skim-reading.
One inconsistency was found during this review and fixed before delivery (§6,
check 2b), and is recorded rather than concealed.

---

## 1. Correction ledger (v0.3 → v0.4)

| Blocker | v0.3 defect (verified) | v0.4 correction | Location |
|---|---|---|---|
| 01a | `Ident` forbade hyphens; examples used `selector-contract`, `indie-ref-impl/0.3.0` | `Slug` token for spec/scope/checker names; `Ident` unchanged (no minus ambiguity) | §B.2, §B.3 |
| 01b | Keyword list reserved `output`; examples used `output.x` | `output` removed from keywords; defined as special context variable with binding rules (§B.5a); user declaration → `reserved-context-name` | §B.2, §B.5a, §B.9 |
| 01c | Trailing `;` in examples, forbidden by productions | Blocks use `(";" \| Item ";")*`: trailing semicolons accepted | §B.3 |
| 01d | `Primary → Expr` left recursion | Restructured: `Postfix := Atom ("." Ident \| "[" Expr "]")*` | §B.3 |
| 02a | UCI-only membership admitted fabricated scores | Whole-record membership: `∃c ∈ C : output == c` | App. 2 §A2.4; §B.11 |
| 02b | Well-formedness admitted identical duplicates; omitted ASCII/whitespace rules | Position-sensitive distinctness via `range(len(cs))` indices; `is_ascii_printable`/`has_no_whitespace` builtins; predicate aligned with validator | §B.4, §B.11, App. 2 §A2.5 |
| 03 | Assurance policy had no syntax | `assurance:` item (`none` / `level-a required` / `level-b accepted`); default `none`; static checks incl. `assurance-level-unavailable` for solver-backed Level A in v0 | §B.7, §B.9 |
| 04 | Checker types and invocation rule unformalized | Function types in `TypeExpr`; §B.5b invocation rule (corpus from test policy; per-input invoke-and-evaluate; first failure = witness); test-based checking explicitly corpus-bound (L3) | §B.3, §B.5b, §D.1 |
| 05 | Aggregation rule contradicted its example | Divergence-first precedence: DIVERGENCE > FAIL > INCONCLUSIVE > PASS; per-property records always preserved | §E.6; vis. Diagram 4 |
| 06 | Canonical profile missed Nat/Int/Real; no f64 sign; `-0` untreated | Typed nat/int/rat/f64 objects; signed hexfloat; integer `-0`→`0`; `Real` excluded from hashed artifacts (explicit restriction) | §G.2 |
| Add. | `none` reserved but unproducible | `"none"` literal with `Option<T>` typing | §B.3, §B.4 |
| Add. | `forall n in Nat` domain ambiguity | `Domain := "type" TypeExpr \| Expr` | §B.3 |
| Add. | NFC required but no error reason | `INVALID_INPUT(string-not-normalized)`; parser validates, never silently normalizes | §B.4a, §B.9 |
| Add. | `semantic_result` required vs "no semantic result" | `Option<SemanticResult>`: None when admission fails | §E.1 |

## 2. Partially resolved

1. **UNSAT Level A availability** — policy fully specified (§E.5); SMT-UNSAT
   Level A remains FUTURE in v0 by honest bound, enforced statically
   (`assurance-level-unavailable`) and dynamically
   (INCONCLUSIVE(ASSURANCE_REQUIREMENT_UNMET)).
2. **L2 method selection** — narrowed per claim (acceptance §5); final choice at
   implementation authorization; claims capped as bounded evidence meanwhile.

## 3. Unresolved decisions (carried)

Lean version + proof-carrying interface; full problem-class catalog; per-class
resource defaults; generator-class widening; signed-tag key management.

## 4. Freeze-blocking defects

**None found by this self-review.** All six v0.3 blockers are structurally
repaired and the repairs were mechanically checked (§6). External review may
still find blockers; this verdict is self-review only.

## 5. Non-blocking implementation decisions

Checker registry mechanics; fuzz harness; Lean version; per-class defaults;
canonical-profile rollout; key management.

## 6. Consistency gate (performed, not asserted)

Each check was executed against the v0.4 text. The selector `check` example was
derived production by production: header (`Slug` lexes `selector-contract`),
type aliases, `prefers` (OrExpr/AndExpr/CmpExpr chains), `is_wellformed`
(index-based distinctness via `range`, builtin calls), `contract_holds`
(whole-record `==`), external impl declarations (`Impl(CandidateSet ->
Candidate)`), `goal check` (function/implementation type match per §B.5),
verification block (trailing `;` accepted; hyphenated CheckerID lexes;
`assurance: level-b accepted`), limits, record.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Hyphenated names lex | PASS | `selector-contract`, `finite-total-order-selection`, `indie-ref-impl/0.4.0` derive via `Slug` |
| 2 | `output` consistent | PASS | Not a keyword; special variable with binding rules (§B.5a); `define output` → `reserved-context-name` (§B.12 ex. 9) |
| 2b | Examples' trailing `;` accepted | PASS* | *One defect found during review: §B.12 ex. 7's stated reason (`degenerate-resource-limit` for `timeout: 0s`) contradicted §B.8's range rule (`timeout-out-of-range`); example corrected to `steps: 0` before delivery |
| 3 | No left recursion | PASS | `Postfix := Atom ("." Ident \| "[" Expr "]")*`; chaining (`cs[i].uci`) derives iteratively |
| 4 | Membership sound | PASS | `∃c ∈ C : sel == c` (whole record); §8.3 witness shows the v0.3 hole now fails |
| 5 | Well-formedness matches validator | PASS | Index-based distinctness rejects identical duplicates; ASCII/whitespace/non-empty/finite rules in both predicate and App. 2 §A2.5 |
| 6 | Assurance expressible | PASS | `assurance:` syntax; default `none`; static checks; §E.5 rule has its syntactic dependency |
| 7 | Checker invocation formalized | PASS | Function types in `TypeExpr`; §B.5b rule; corpus-bound semantics explicit |
| 8 | Aggregation coherent | PASS | Divergence-first; §E.7 rule ≡ §E.8 examples ≡ Diagram 4 SUM box |
| 9 | Canonical profile complete | PASS | nat/int/rat/f64 injective; signed f64; `-0`→`0`; Real excluded explicitly |
| 10 | `semantic_result` optionality | PASS | `Option<SemanticResult>`; invalid-input combination shows None |
| 11 | Maturity/release terminology identical | PASS | Same 7 names in §G.4, §J, matrix §7, diagrams |
| 12 | No authorization of repo/implementation/experiments | PASS | Headers, entry conditions, work-order restrictions |

**Gate verdict: 12/12 PASS** — with check 2b's in-review fix recorded above.
Document-level verification only; not an executed test.

## 7. Adversarial cases (expected results)

1. Hyphenated spec name `my-spec` → lexes as `Slug`; admission proceeds.
2. `define output: Nat = 3` → INVALID_INPUT(reserved-context-name).
3. Trailing `;` in blocks → accepted; empty `verification {}` → accepted.
4. Implementation returns genuine UCI with inflated score → VIOLATED, witness
   `(input, output)` (§8.3 of acceptance plan).
5. Identical duplicate candidate records → validator rejects (position-sensitive
   distinctness); formal predicate agrees.
6. `assurance: level-a required` on `compare-models` →
   INVALID_INPUT(assurance-level-unavailable).
7. `assurance: level-a required` with `proof: none` →
   INVALID_INPUT(conflicting-assurance-requirements).
8. Checkers A=PASS, B=FAIL on one property → CHECKER_DIVERGENCE (not FAIL).
9. Properties P=PASS, Q=FAIL → summary FAIL; both records preserved.
10. `f64` value `-0x1.8p+1` → canonicalizes deterministically; `-0.0` →
    `0x0.0000000000000p+0`; integer `-0` → `"0"`.
11. `Real` value reaching the canonicalizer → INVALID_INPUT(real-not-encodable).
12. Non-NFC string in hashed artifact → INVALID_INPUT(string-not-normalized).

## 8. Review verdict

v0.4 repairs all six v0.3 blockers with mechanically checked corrections. The
package is internally consistent to the limits of self-review. What self-review
cannot supply — independent adversarial reading and any execution-based
verification — remains outstanding and is required before any freeze decision.

*End of MSVE_DESIGN_REVIEW_v0.4.md (self-review).*
