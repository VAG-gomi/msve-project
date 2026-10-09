# Report D — Reviewer D Report — Full Text (Part 6/6)

**Work Order:** 0.8.2 · **Source:** `owner-review/reviewer-reports/reviewer-D-cross-document.md` (DIRECT ARTEFACT — transcribed verbatim from the ZIP).

Original findings preserved verbatim. See PROVENANCE note below for execution provenance.

---

All checks complete. Compiling the final report.

---

# Sub-agent D Report: Regression and Cross-Document Audit of MSVE v0.8

**Scope audited:** All six v0.8 documents + `m8/` under `/home/hatch/workspace/msve-design/`.
**Method:** Direct file inspection; greps across all documents; ran the three M8 CLI commands myself; cross-checked ledger claims against spec text. I did not rely on the lead's summaries.

## 0. M8 execution (task item 6) — all green, verified by me

```
python3 -m m8.cli corpus              → corpus: 0 failures
python3 -m m8.cli spec-examples       → spec-examples: 0 failures
python3 -m m8.cli grammar-conformance → OK (48 productions, parser methods present, spec §B.3 matches generated)
```

## A. Confirmed consistent

- **A1 — Visualisation plan completeness:** exactly 7 ` ```mermaid ` blocks; 7 diagram sections (system boundary, spec-to-verification pipeline, validator pipeline, result record, SAT/UNSAT assurance, generator boundary, maturity stages). D-023 satisfied.
- **A2 — Review §2 B-table vs ledger mapping:** the review's B-01–B-05 → D-025–D-030 table matches the ledger's §"B-01 – B-05 → D-number mapping" exactly (B-01→D-025, B-02→D-026/D-027, B-03→D-028, B-04→D-029, B-05→D-030).
- **A3 — Acceptance plan §8.4 D-028 case:** states "a decoder returning `{ok:false, candidates:[c], error:some("malformed-json")}` with `out = rejected("malformed-json")` → contract **false** (the `len(d.candidates) == 0` conjunct)" — matches the spec's §B.11 contract (spec line 761) and §B.13 invariant (spec lines 354–360).
- **A4 — Capability matrix C1–C11:** claims are consistent with the spec (C1 grammar-from-`m8/grammar.py`, C11 M8 Implemented, others Designed). No overclaim detected at the matrix level.
- **A5 — D-028/D-029/D-031 substance verified in spec:** the contract conjunct, the three closed-type predicates (`is_validation_error` defined at spec line 395, `is_admission_error` at 568), and the Qualifier default ("omitted `required`/`optional` means `required`", spec lines 546–547) are all present as the ledger claims.
- **A6 — No renamed-defect leakage in v0.8 normative text:** `ErrorCode`/`is_error_code`/`minimal escaping` hits in v0.8 files are all historical references (change summaries, "the v0.7 X is retired") — except NEW-D3 below. The `"binary64"` string in M8 is a negative test case, correctly rejected.

## B. Defects found

### NEW-D1 — Three normative links in the v0.8 spec point to v0.7 documents

**(a)** ID: NEW-D1 (cross-document; relates to D-023 self-containment).
**(b)** Locations: `MSVE_DESIGN_SPEC_v0.8.md` line 89 ("capability matrix (`MSVE_CAPABILITY_MATRIX_v0.7.md`)"), line 894 ("Matrix (`MSVE_CAPABILITY_MATRIX_v0.7.md`) normative"), line 1379 ("Normative: `MSVE_ACCEPTANCE_PLAN_v0.7.md`").
**(c)** Counterexample: a reader following the spec's normative scope definition lands on the superseded v0.7 matrix, whose error model (single `ErrorCode`) contradicts the v0.8 spec's D-029 three-type model.
**(d)** Expected: normative companions referenced as v0.8. Actual: three normative references name v0.7 files.
**(e)** Root cause: the v0.7→v0.8 copy retained old filenames in normative (not historical) positions.
**(f)** Proposed correction: change all three to `MSVE_CAPABILITY_MATRIX_v0.8.md` / `MSVE_ACCEPTANCE_PLAN_v0.8.md`.
**(g)** Regression: grep for `v0\.7\.md` in normative (non-historical) positions across all v0.8 docs must return empty.
**(h)** Does NOT establish: any defect in the v0.8 companion documents themselves, which exist and are consistent (A4).

### NEW-D2 — Ledger's D-025 correction description does not match the actual grammar

**(a)** ID: NEW-D2 (ledger accuracy; relates to D-025).
**(b)** Location: `MSVE_REGRESSION_LEDGER_v0.8.md`, D-025 "Correction (v0.8)" — claims "`Atom := … | RecordLit`, `RecordLit := TypeName "{" Fields "}"`" and "constructor functions re-lexed as `Ctor`".
**(c)** Counterexample: the spec's actual §B.3 `Atom` production (spec line 224) is `"{" (Ident ":" Expr ("," Ident ":" Expr)*)? "}"` — bare braces, **no `TypeName` prefix**. No `Ctor` token exists in `m8/grammar.py`, `m8/lexer.py`, `m8/parser.py`, or the spec (verified by grep). The v0.8 examples use bare-brace literals (`{ accepted: false, … }`, corpus file `v08-ex5.msve` line 32), not `TypeName{…}`.
**(d)** Expected: ledger describes the correction that was made. Actual: ledger describes a `TypeName`-prefixed record syntax that was never implemented.
**(e)** Root cause: the ledger entry was written from the intended design rather than the as-built grammar.
**(f)** Proposed correction: rewrite the D-025 correction line to match the as-built form (bare-brace `Atom` alternative; `expect_field_name` policy; R13 typing). Remove the `Ctor` claim or record it as superseded-during-construction.
**(g)** Regression: ledger correction text must quote the actual generated production.
**(h)** Does NOT establish: any defect in the grammar itself — the as-built form parses all examples and the B-01 negative control holds (substance of D-025 is sound).

### NEW-D3 — Visualisation plan v0.8 shows the retired v0.7 validator contract

**(a)** ID: NEW-D3 (cross-document; relates to D-028/D-029).
**(b)** Locations: `MSVE_VISUALISATION_PLAN_v0.8.md` line 69 (Diagram 3 contract box: "out == rejected(e), is_error_code(e) or out == validate(decoded)") and lines 142–144 (image prompt: "as v0.6, with the contract box reading … is_error_code(e)").
**(c)** Counterexample: the v0.8 contract (spec §B.11) is `out == rejected(e)` with `is_validation_error(e)` **and** `len(d.candidates) == 0` — the diagram shows the retired predicate and omits the D-028 conjunct entirely.
**(d)** Expected: the v0.8 diagram reflects the v0.8 contract. Actual: the diagram and its generation prompt reproduce the v0.7/v0.6 contract verbatim.
**(e)** Root cause: the v0.8 visualisation plan was produced by version-string substitution on the v0.7 file without updating diagram contents.
**(f)** Proposed correction: update the Diagram 3 contract box to the v0.8 form (`is_validation_error(e)` + `len(d.candidates) == 0`); rewrite the image prompt to describe the v0.8 contract, not "as v0.6".
**(g)** Regression: no occurrence of `is_error_code` in any v0.8 document outside historical/retirement mentions.
**(h)** Does NOT establish: any defect in the spec's contract itself, which is correct (A3).

## C. Limitations of this audit

- I verified 4 of the 9 new D-numbers in depth against the spec (D-025 substance, D-028, D-029, D-031); D-026/D-027/D-030/D-032/D-033 were spot-checked only for presence, not exhaustively re-derived.
- I did not audit M8's internals beyond executing the CLI; grammar/type-checker correctness claims are outside Sub-agent D's remit.
- Cross-document checks are textual and structural; I did not re-verify every semantic claim (e.g., each acceptance-plan corpus row) against the spec.
- All findings are document/tool-level; no implementation exists, so no conformance claims are made.

**Net assessment:** the six-document package is structurally complete and the M8 gates are green, but the v0.8 pass inherited three copy-forward defects of its own (NEW-D1 stale normative links, NEW-D2 ledger misdescription, NEW-D3 stale diagram) — the same "correction pass introduces its own layer" pattern. None of the three affects the spec's normative substance, but all three should be fixed before any release-gate decision, since a gate decision taken on documents that misdescribe each other is not evidence-based.

---

**Provenance (from `owner-review/reviewer-reports/PROVENANCE.md`, transcribed):**

# Reviewer Report Provenance

All four reviewers were genuine sub-agents spawned by the lead agent under
MSVE Work Order 0.8, Phase D, after a verified Phase-0 capability probe.

- **Reviewer A** (grammar/type-system): agent_id 9152704e-b63e-4b37-a4f0-c1c97f0c5b8b.
  Spawned 2026-10-09 ~11:34 UTC, completed ~11:37 UTC. The runtime handoff
  did not arrive in the lead's context; the report was extracted verbatim
  from the agent's session record at
  `/home/hatch/agents/agent-9152704e-b63e-4b37-a4f0-c1c97f0c5b8b/sessions/`.
- **Reviewer B** (canonicalisation/numerics): agent_id 95c2a762-4d26-42d7-938c-1ebf9bd18a66.
  Delivered via runtime handoff 2026-10-09 ~11:37 UTC; cross-checked
  against the session record. Identical text.
- **Reviewer C** (validator/contracts): agent_id 1504052d-5d7b-49a0-aff7-0f468e75ce46.
  Delivered via runtime handoff 2026-10-09 ~11:37 UTC; cross-checked
  against the session record. Identical text.
- **Reviewer D** (cross-document): agent_id 52e3a6a9-ff90-40a1-b9e6-44783086fc2d.
  Spawned after A/B/C reported. The runtime handoff did not arrive in the
  lead's context; the report was extracted verbatim from the agent's
  session record at
  `/home/hatch/agents/agent-52e3a6a9-ff90-40a1-b9e6-44783086fc2d/sessions/`.

Each report file below is the reviewer's final response verbatim, with
only the leading conversational sentence retained as received. No
findings were added, removed, or reworded.

Independence note: reviewers were spawned as separate child agents with
separate execution records. They inherited the parent's context at spawn
(context independence is procedural, not absolute). They were instructed
not to rely on the lead's summaries and to verify claims against the
files directly. Reviewer D was spawned after A/B/C completed but was not
shown their findings before its initial submission.
