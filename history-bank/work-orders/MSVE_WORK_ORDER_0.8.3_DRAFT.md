# MUSE WORK ORDER 0.8.3 — DRAFT (prepared by Muse, NOT issued)

MSVE v0.8 — Targeted correction of owner-review residual findings F-01–F-12

**Status:** This text is a draft prepared 2026-10-09 ~12:45 UTC for the owner's
review. It authorizes nothing until the owner issues it, edits it, or dismisses it.

---

## 1. Purpose

Correct the twelve residual findings (F-01–F-12) the owner identified in the final
v0.8 specification and companion documents during substantive owner review on
2026-10-09. The owner's decision: **MSVE v0.8: return for targeted correction.**
This work order is narrowly scoped to those findings and the reconciliation sweep
they imply. It is not a general design revision.

Historical context preserved: findings D-001–D-033 (v0.1–v0.7) and NEW-A/B/C/D
(v0.8 Phase-D review) remain closed in their own ledgers. The twelve F-findings
are new residual defects and cross-document inconsistencies, not reopenings.

---

## 2. Authority and restrictions

- Authorized: document correction of the six v0.8 design documents (new dated
  revisions; every prior version retained unmodified as a historical draft),
  regression-ledger updates, and M8 corpus/test additions **only within M8's
  existing mechanical scope** (audit of the documents — no expansion of M8 into
  the MSVE runtime).
- Treat the `MSVE_v0.8_OWNER_REVIEW_BUNDLE.zip` and the 21 transfer Markdown
  files under `~/workspace/msve-design/transfer/` as read-only historical
  evidence. Do not alter the packaged artefacts to make corrections look complete.
- NOT authorized: MSVE engine implementation; solver or parser integration;
  MSVE acceptance experiments; GrimChess modification or Order 7.2; GitHub
  commits or repository creation; design freeze, acceptance, or any
  implementation authorization. No version-label decision (v0.8-corrected vs
  v0.9) — that is the owner's.
- Do not rewrite history: the correction record must show what was wrong, what
  changed, and what evidence supports the change. Do not silently edit a
  companion document to make a stale claim pass.
- Do not change the specification simply to make the readiness evidence matrix
  pass. A failed or unsupported claim must remain visible; correct the underlying
  defect or narrow the claim.

---

## 3. Input findings (from owner review 2026-10-09; all conceded)

**F-01 — Error-code closure vs detail suffixes (spec §B.9).** The prose promises
that `unbound-identifier: foo` is valid because "the predicate checks the base
code before `": "`", but `is_admission_error` is a disjunction of exact string
equalities (`e == "unbound-identifier"`). Under exact string equality the
suffixed form evaluates to false. Same structural question for
`is_unsupported_reason` and for validation-error codes. Correction: define an
explicit base-code operation, apply it consistently in every predicate and its
prose, or use a data type that separates code from detail. Regression: M8
corpus case(s) exercising base-code extraction and suffixed inputs.

**F-02 — Assurance field names vs result schema (spec §E).** `ResultRecord`
defines `assurance_required`, `assurance_bases`, `assurance_achieved`,
`assurance_shortfall`; the shortfall formula and several §E.7 invariants use
`required`, `bases`, `achieved` with no defined alias, and `required` collides
with `VerificationRecord.required`. Correction: use the actual field paths
consistently, or formally define the shorthand and its scope. Regression:
specification-review (schema coherence), plus a mechanical field-name grep
across the six documents.

**F-03 — NEW-B1 residual rounding statements (spec §B.4b).** Principal NEW-B1
correction is present, but two statements remain literally false: (a) magnitudes
in `[2^-1074, 2^-1022)` "round to subnormals" — e.g. r = 2^-1022 − 2^-1076 lies
above the midpoint (2^-1022 − 2^-1075) between the largest subnormal and the
minimum normal, so round-to-nearest yields the minimum normal; (b) "values
below it round to the maximum finite binary64" — only values in the
maximum-finite rounding interval do. Correction: specify the rounding intervals
precisely, including the subnormal→normal transition midpoint. Regression:
specification-review of the normative wording (paper, but must be exact — this
section is normative text, freeze-blocking if false).

**F-04 — `is_nan` missing from builtin inventory (spec §B.4).** Rule 3 references
`is_nan` for NaN guards; rule 11's complete inventory declares `is_finite` but
not `is_nan`. Under name resolution, `is_nan` has no listed builtin to resolve
to. Correction: add `is_nan: Binary64 -> Bool` with defined semantics, or remove
the unsupported reference. Regression: M8 corpus case calling `is_nan`.

**F-05 — Set quantification vs no set introduction form (spec §B.4.8).**
Quantifier domains may be "list/set expressions", but v0 `TypeExpr` has no `Set`
(removed per NEW-A9) and no set introduction form exists. Correction: restrict
the v0 domain to lists, or define a set construction mechanism and its
semantics. Regression: specification-review of §B.4.8 against the v0 `TypeExpr`
grammar.

**F-06 — Closure-predicate enforcement at the result-record boundary (open
question).** `is_admission_error` and `is_unsupported_reason` are defined
(NEW-C1 corrected) but `is_admission_error(` is never invoked outside its own
definition; §E.7 shows no invariant requiring `INVALID_INPUT(reason)` to satisfy
`is_admission_error(reason)` or `UNSUPPORTED(reason)` to satisfy
`is_unsupported_reason(reason)`. Resolve: add an explicit refinement or
invariant at the point a result record is accepted, checked, or packaged — or
demonstrate where the enforcement already exists. The claim that the domains are
"enforced" must not exceed the shown rules.

**F-07 — Verification-input evidence resolution (narrowed NEW-C5).** Invariants
9 and 15 now name `evidence.derivation_records` / `evidence.constructed_artifacts`
(corrected), but invariant 20 still requires `VerificationRecord.inputs_ref` to
"resolve in the evidence bundle" while `EvidenceBundle` declares only
`verification_inputs_ref: Hash` with no resolution rule. Resolve: state whether
`inputs_ref` must equal that hash, point to an artifact elsewhere, or resolve by
another mechanism.

**F-08 — Error counts, change summary vs §B.9 (spec internal).** Opening change
summary says 15 admission codes and 2 unsupported reasons; final §B.9 defines 27
and 3 (12 validation errors agree). Correction: reconcile the change summary
with the final definitions (owner's evidence: the detailed lists are the
intended ones).

**F-09 — Corpus count, 36 vs 46.** Change summary, design review, and
capability matrix say 36-case corpus; transfer record and rerun logs report 46
cases (36 + 10 NEW-A regression cases added during the correction pass).
Correction: reconcile every count against the actual corpus manifest — **after**
confirming precisely which files the CLI runs from the manifest and whether
other `.msve` files are intentionally excluded. Do not edit counts until the
CLI manifest-selection logic is pinned down and documented.

**F-10 — Packaging outcome, invariant 15b vs acceptance plan and Diagram 2.**
Spec invariant 15b is a biconditional (PACKAGING_FAILED ⇔ INTERNAL_ERROR with
matching base code); acceptance-plan §9 says INTERNAL_ERROR applies only if the
packaging failure itself is the outcome; Diagram 2 shows the execution error
without the paired packaging status. Correction: make the acceptance plan and
diagram agree with the normative joint-status rule.

**F-11 — D-025 correction description (design review B-01 table).** The review
table refers to a `RecordLit` production; the actual grammar uses a bare-brace
alternative under `Atom`. Correction: bring the review table into line with the
grammar that was actually built (the same misdescription class was already
corrected in the regression ledger — apply it here too).

**F-12 — Canonical type-name grammar coverage (spec §B.3 / canonical profile).**
Surface grammar permits an empty record type `{}` and zero-argument function
type `() -> T`; the canonical type-name grammar requires ≥1 record field and ≥1
function argument. The canonical profile separately encodes `Impl` signatures —
if those forms are legal there, the profile cannot express their type names.
Resolve: either extend the canonical grammar to cover the permitted types or
explicitly exclude the unsupported forms from the v0 language. This needs an
explicit design decision, not a silent assumption.

---

## 4. Required deliverables

**D-1 — Corrected design documents.** New dated revisions of the six v0.8
documents incorporating the F-01–F-12 resolutions. Every prior version retained
unmodified. Each correction cites the finding ID and the exact changed location.
Version label at the owner's discretion — do not publish a new "v0.9".

**D-2 — Residual-defect ledger F-001–F-012.** New ledger preserving the full
D-001–D-033 and NEW-A/B/C/D histories verbatim. For each F-finding: original
failure mode, correction, normative location, regression evidence type
(EXECUTED_TEST / SPECIFICATION_REVIEW / MECHANICAL_DOCUMENT_CHECK), and the
evidence record. New findings must not be mislabeled as already resolved, and
historical findings must not be reopened by this pass.

**D-3 — Cross-document reconciliation report (explicit deliverable).** Because
the 0.8 correction pass systematically left stale claims in companion documents
(F-08, F-09, F-11), this order requires a dedicated reconciliation sweep:
every count, code inventory, corpus count, corpus-selection rule, normative
reference, and diagram must be checked across all six documents, and every
discrepancy listed with its resolution. The sweep must be executed by a reviewer
internal to the pass but **different from the agent(s) that authored the
corrections**.

**D-4 — 23-invariant joint-satisfiability analysis.** The highest-value check:
for each result event class, either demonstrate that the §E.7 invariant set
admits exactly one recording, or produce the counterexample (a conforming
record that should be nonconforming, or two mutually inconsistent conforming
records — as Reviewer C constructed against the old set). Frame the deliverable
as "the counterexample or the demonstration", not a prose claim. Paper
adversarial construction is acceptable; mechanical checking is not required at
this stage.

**D-5 — Regression evidence.** For each mechanically checkable correction
(F-01, F-04, F-12 if grammar-extended, F-02 field-name grep, F-09 CLI selection
rule): actual rerun logs with commands, exit statuses, and per-case outcomes.
For prose corrections: a specification-review record naming the exact text
checked. Preserve the 0.8.2 evidence categories:
DIRECT ARTEFACT / RECORDED OUTPUT / REPRODUCED OUTPUT / REPORT CLAIM /
INFERENCE / EVIDENCE NOT AVAILABLE.

**D-6 — Completion report.** Per-finding disposition, corrected paths, actual
checks rerun and their results, missing or unavailable evidence, unresolved
defects, and the exact remaining limits of verification. No acceptance, freeze,
or implementation claim.

---

## 5. Evidence discipline (standing, from 0.8.2)

- Label every test claim's source evidence; never reconstruct absent command
  outputs from memory.
- Keep quoted original material distinct from commentary.
- No PASS without a recorded refutation attempt (standing lesson from the v0.4
  round). A "hand-derived" claim means mechanically per-token/per-line checked,
  not skimmed (standing lesson from the v0.3 round).

---

## 6. Quality-control checks before handoff

- All 12 F-findings have one and only one disposition, and any summary
  arithmetic is mechanically reconciled against the individual dispositions
  (the CLM-12 error must not recur).
- Every F-correction links finding → proposed change → resulting artefact →
  supporting evidence, and states the chain's strength honestly
  (EXECUTED_TEST vs SPECIFICATION_REVIEW).
- The reconciliation report (D-3) lists zero unresolved cross-document
  discrepancies, or names each one explicitly.
- No historical artefact (ZIP, transfer reports, prior drafts, prior ledgers)
  was modified.
- The NEW-C1 chronology question is settled in the record: predicates defined
  after Reviewer C's inspection; reviewer reports record no spec hash, so
  interleaving remains unanchored — state this as a known limitation, do not
  paper it over.

---

## 7. Stopping rule and final status

Stop when the corrected revisions exist, every F-finding has a dispositioned
correction with linked evidence, the reconciliation sweep is complete, the
invariant analysis is delivered as counterexample-or-demonstration, and the
completion report is honest about remaining gaps.

Final status must read: **TARGETED CORRECTION COMPLETE — OWNER REVIEW OF
CORRECTIONS STILL PENDING.** Do not claim design acceptance, freeze, or
implementation authorization.
