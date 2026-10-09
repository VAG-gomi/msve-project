# MSVE Design Review v0.8

**Status:** DRAFT FOR REVIEW · **Version:** 0.8
**Supersedes:** `MSVE_DESIGN_REVIEW_v0.7.md` (historical draft)
**Normative companion:** `MSVE_DESIGN_SPEC_v0.8.md`

## 1. Review mandate

This document records the v0.8 review: the v0.7 adversarial findings, the
v0.8 correction pass, the M8 audit tool, the Phase D independent
sub-agent reviews, the lead's adjudication, and the release-gate decision.

## 2. v0.7 review outcome (carried)

The v0.7 external adversarial review produced five critical blockers
(B-01–B-05) and reopened D-025–D-033 areas. The v0.7 gate was **BLOCKED**.
The v0.7 documents remain historical drafts, unmodified.

**B-01 – B-05 → v0.8 disposition:**

| Finding | v0.8 correction | Ledger |
|---|---|---|
| B-01 (record literals ungrammatical) | D-025: bare-brace record literal as `Atom` alternative (F-11: not a separate `RecordLit` production), R13, M8 corpus | D-025 |
| B-02 (canonical form gaps) | D-026 (`-0` rejected), D-027 (escapes, rationals, envelopes) | D-026, D-027 |
| B-03 (decoder invariant) | D-028: contract false-branch conjunct | D-028 |
| B-04 (error model) | D-029: three closed types | D-029 |
| B-05 (packaging/schema) | D-030: `output_packaging`, refs, invariants 15–22 | D-030 |

## 3. M8 audit tool (Phase B)

M8 (`m8/`) is a real lexer/parser/name-resolver/type-checker for the MSVE
surface language, built from the v0.8 grammar. It is an audit tool under
test, not an oracle. See `m8/README.md` and `m8/runs/2026-10-09-m8-build.md`
for the implementation record, the twelve corrected tool defects, and the
B-01 negative control.

**Executed results (2026-10-09, on the final v0.8 package):**

| Check | Result |
|---|---|
| `python3 -m m8.cli corpus` | 0 failures (46 cases at gate; 48 in the 0.8.3 candidate) |
| `python3 -m m8.cli spec-examples` | 0 failures (6/6 valid pass; 5/5 invalid rejected in marked categories) |
| `python3 -m m8.cli grammar-conformance` | OK (48 productions; spec §B.3 byte-identical to generated) |
| `python3 -m m8.tests.test_canonical` | all assertions hold |
| `python3 -m m8.tests.test_grammar_conformance` | production/method coverage holds |

**What M8 does not establish:** contract satisfiability (the D-028
contract logic is hand-verified, SPECIFICATION_REVIEW); injectivity as a
machine-checked proof (structural-induction sketch); implementation
conformance (no engine exists); execution (no tests executed).

## 4. Phase D independent reviews

Four sub-agent reviewers were dispatched after a verified Phase-0
capability probe (SHA-256 `2ecd5df3…0d75b7` matched). Reviewers were
instructed to base findings on the document text and their own checks,
not on the lead's summaries. Findings were not shared between reviewers
before their initial submissions.

### 4.1 Agent A — grammar and type-system audit

**Report received 2026-10-09.** Agent A re-ran all M8 commands,
verified keyword agreement (62/62), reproduced the B-01 negative
control, and traced the §B.11 examples manually. Confirmed: D-025
integrated, §B.3 single-source-of-truth holds, no B-01 recurrence.

**Findings — all ten conceded by the lead after verification:**

| ID | Defect | Disposition |
|---|---|---|
| NEW-A1 | M8 `check_limits` stub (§B.8 unenforced) | Range + `steps:0` enforced |
| NEW-A2 | M8 missed level-a exclusion (§B.7) | `else` branch added |
| NEW-A3 | M8 never validated projection paths (§B.5a) | `check_proj_paths` implemented |
| NEW-A4 | Cyclic aliases crashed M8 | `CheckError` + cycle detection |
| NEW-A5 | Unbound type names silent (§B.5) | Name-resolution error |
| NEW-A6 | Builtin shadowing accepted (§B.5) | Rejected in `collect` |
| NEW-A7 | HexFloat `-?` tokenization ambiguity | `-?` removed; unary minus |
| NEW-A8 | Function-typed locals uncallable | `check_call` extended |
| NEW-A9 | `Set<T>` no introduction form | Removed from v0 `TypeExpr` |
| NEW-A10 | Option as quantifier domain | Restricted to list/set |

10 new corpus cases added (46 total, 0 failures). Agent A's warning —
"M8's *implemented* checks have run" — is adopted as a standing rule.

### 4.2 Agent B — canonicalisation and numerical-semantics audit

**Report received 2026-10-09 ~11:37 UTC.** Agent B ran the canonical
test suite independently (PASS reproduced), ran a 2,998-value
collision-construction sweep (zero duplicate spellings accepted), and
verified the 2^-1022 boundary by hand. Confirmed: binary64 uniqueness
(A1), rational grammar (A2), envelope field order (A3), packaging
coherence (A4).

**Findings — all seven conceded by the lead after verification:**

| ID | Defect | Disposition |
|---|---|---|
| NEW-B1 | §B.4b underflow/overflow prose false at boundaries; missing rows | Corrected: exact thresholds; added `(+inf)−finite`, `0/(±inf)` |
| NEW-B2 | M8 string-escape checker more permissive than spec | Corrected in `canonical.py`; regression cases added |
| NEW-B3 | Type-name grammar contradicted "no whitespace" | Corrected to spaceless forms |
| NEW-B4 | M8 envelope skipped type-name/value validation | Corrected: `check_typename` + recursive validation |
| NEW-B5 | NaN comparisons undefined | Corrected: IEEE-style predicate rules |
| NEW-B6 | Real/Rat division by zero undefined | Corrected: `division-by-zero` execution error |
| NEW-B7 | `output_packaging`/`execution` jointly unconstrained | Corrected: invariant 15b; suffix rule stated |

Agent B's net assessment notes the pattern: "the same 'next unchecked
layer' pattern as previous rounds" — NaN entered the value domain in
D-032 but predicates were not carried through. The lead accepts this
characterization; it is recorded as a standing methodological warning.

### 4.3 Agent C — validator and result-contract audit

**Report received 2026-10-09 ~11:37 UTC.** Agent C ran M8 on the
validator example (PASS reproduced), hand-derived the D-028
counterexample through the contract (contract = `false`; the v0.7 form
re-derived to `true`), verified both invariant directions, and ran four
D-031 cases through M8 (all per §B.7).

**Confirmed:** D-028 fixed (tight oracle); D-029 domain partition
coherent; D-031 operational; D-033 sufficient for inv. 14.

**Findings — conceded by the lead:**

| ID | Defect | Disposition |
|---|---|---|
| NEW-C1 | `is_admission_error`/`is_unsupported_reason` never defined | Both `define` predicates written; M8-verified |
| NEW-C2 | `INTERNAL_ERROR` reasons unbounded (fourth domain) | Normative open-domain statement + 4 specified reasons |
| NEW-C3 | `execution`/`output_packaging` underdetermined | Duplicate of NEW-B7; fixed by inv. 15b |
| NEW-C4 | `UNIQUE_UNDER_PROJECTION` evidence-free | Invariant 23 added |
| NEW-C5 | "Evidence bundle" vague; no value-artifact list | Inv. 9/15 name the lists |

### 4.4 Agent D — regression and cross-document audit

**Report received 2026-10-09.** Agent D verified all M8 gates green,
confirmed the 7-diagram plan, the B→D mapping, the D-028 acceptance
case, and matrix claims. Found three copy-forward defects, all conceded:

| ID | Defect | Disposition |
|---|---|---|
| NEW-D1 | 3 normative links pointed to v0.7 files | Updated to v0.8 |
| NEW-D2 | Ledger D-025 misdescribed the as-built grammar | Corrected to bare-brace form |
| NEW-D3 | Diagram 3 showed the retired `is_error_code` contract | Updated to v0.8 contract |

## 5. Lead adjudication

Every material finding from Agents A–D was verified against the primary
sources before disposition:

- **Challenge method:** for each finding I located the exact spec
  section and tool code cited, reproduced the counterexample where one
  was given (or constructed it), and confirmed the expected-vs-actual
  gap before conceding.
- **Concessions:** all 24 findings (A1–A10, B1–B7, C1–C5 with C3≡B7,
  D1–D3) were conceded. No finding was rejected. Two were duplicates
  (C3 of B7), which strengthens rather than weakens the case for the fix.
- **Corrections:** each concession produced a spec or tool change plus
  a regression case. The M8 corpus grew from 36 to 46 cases; the
  canonical test suite gained 14 assertions; §B.2, §B.3, §B.4, §B.4b,
  §B.5, §B.7, §B.8, §B.9, §E.7, §G.2 were all amended.
- **Disagreements:** none required reconciliation by vote. Where agents
  overlapped (B7/C3), both derivations were checked independently.
- **What was not challenged:** the reviewers' confirmations (e.g.,
  C's D-028 derivation, B's collision sweep) were spot-checked, not
  fully re-derived — noted as a limitation below.

## 6. Verification table

| Object | Method | Result | Evidence | Limitation |
|---|---|---|---|---|
| §B.3 grammar vs `m8/grammar.py` | `grammar-conformance` (mechanical) | OK, 48 productions, byte-identical | EXECUTED_TEST | — |
| All §B.11 examples parse+type-check | `spec-examples` (mechanical) | 6/6 pass | EXECUTED_TEST | Syntax/types only |
| All §B.12 invalid examples rejected | `spec-examples` (mechanical) | 5/5 in marked categories | EXECUTED_TEST | — |
| 46-case regression corpus | `corpus` (mechanical) | 0 failures | EXECUTED_TEST | Bounded; M8's implemented checks only |
| Canonical f64/string/rational/envelope | `test_canonical` (mechanical) | All assertions hold | EXECUTED_TEST | Bounded corpus |
| B-01 negative control | Disabled record-literal branch (mechanical) | Exact v0.7 failure reproduced | EXECUTED_TEST | Monkeypatched, not historical v0.7 |
| D-028 contract logic | C's hand-derivation (both branches) | Contract rejects the counterexample | SPECIFICATION_REVIEW | Not machine-checked |
| Binary64 uniqueness | B's 2,998-value collision sweep | Zero duplicate spellings | EXECUTED_TEST | Bounded; spelling-level only |
| D-025–D-033 corrections | Spec inspection vs ledger | All present as claimed | SPECIFICATION_REVIEW | — |
| Cross-document consistency | D's audit + lead greps | 3 defects found and fixed | MECHANICAL_DOCUMENT_CHECK | Textual/structural |
| Injectivity (§G.2) | Structural-induction sketch | Argument given | SPECIFICATION_REVIEW | Not machine-checked |
| Implementation conformance | — | No engine exists | NOT_CHECKED | Out of scope (Work Order 0.8) |
| Execution of acceptance tests | — | Not authorized | NOT_CHECKED | Requires separate authorization |

## 7. Release-gate decision

**Gate: READY_FOR_OWNER_REVIEW.**

Basis: the five v0.7 blockers (B-01–B-05) are corrected under D-025–
D-033 with regression cases; the 24 Phase-D findings are all corrected
with regression cases; all mechanical gates are green; the six
documents are cross-consistent; every limitation is stated explicitly.

This decision means: the package is coherent enough for the owner's
review. It does **not** mean owner acceptance, design freeze, or
implementation authorization — each requires a separate explicit
decision.

Residual risks honestly held: (1) M8 verifies syntax/types, not
contract satisfiability or implementation conformance; (2) the
"next unchecked layer" pattern held again in v0.8 (24 new defects),
so further layers may remain; (3) the injectivity argument and the
D-028 derivation are paper, not machine-checked.

*End of MSVE_DESIGN_REVIEW_v0.8.md.*
