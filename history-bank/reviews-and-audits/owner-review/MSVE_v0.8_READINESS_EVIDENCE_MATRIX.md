# MSVE v0.8 Readiness Evidence Matrix

**Work Order:** 0.8.1 · **Date:** 2026-10-09
**Method:** each claim traced to artefacts; checks reproduced where safe.

Evidence categories: SPECIFICATION_REVIEW · MECHANICAL_DOCUMENT_CHECK ·
IMPLEMENTATION_CONFORMANCE · EXECUTED_TEST · FORMAL_PROOF · INCONCLUSIVE.

Dispositions: SUPPORTED · PARTIALLY_SUPPORTED · UNSUPPORTED · INCONCLUSIVE.

---

### CLM-01 — Phase 0 capability probe verified

- **Source:** completion report; `m8/runs/phase0-capability-probe.md`
- **Evidence:** `m8/runs/phase0-capability-probe.md` (sha256 `49e820fca06a3ff2…`)
- **Method:** sub-agent computed SHA-256 of `m8-probe-0.8`; lead recomputed locally; match.
- **Outcome:** `2ecd5df35df647d1f04d7fa8c4113cc3ddd326001ebffe8d1883dd8b8d0d75b7` both sides.
- **Category:** EXECUTED_TEST (of sub-agent dispatch, not of MSVE).
- **Reproduction:** the hash comparison is reproducible (`echo -n 'm8-probe-0.8' | sha256sum`).
- **Limitation:** establishes that a child agent can be spawned and return a value — not review quality, independence of judgment, or any MSVE property.
- **Disposition:** SUPPORTED (for the narrow claim: probe verified).

### CLM-02 — M8 was built

- **Source:** completion report; design review §3
- **Evidence:** `m8/*.py` (8 modules), `m8/tests/`, `m8/README.md`, `m8/runs/2026-10-09-m8-build.md` — see manifest.
- **Method:** source inspection; the tool runs (`python3 -m m8.cli …`).
- **Outcome:** M8 lexes, parses, resolves, type-checks, and canonical-checks MSVE surface syntax.
- **Category:** EXECUTED_TEST (the tool executes).
- **Reproduction:** reproduced 2026-10-09; instructions in handoff.
- **Limitation:** M8 is an audit tool under test (12+10 implementation defects found and fixed during construction/review). It is not verified against an independent oracle.
- **Disposition:** SUPPORTED.

### CLM-03 — The 46-case corpus passed

- **Source:** completion report ("46 cases, 0 failures")
- **Evidence:** `owner-review/logs/corpus.log` (`ec4ac2624e57e80e…`), `owner-review/logs/corpus-per-case.json`; `m8/corpus/manifest.json`; the 46 `.msve` files.
- **Method:** `python3 -m m8.cli corpus` reproduced 2026-10-09; per-case verdicts parsed from the log.
- **Outcome:** 46/46 verdicts PASS; final line `corpus: 0 failures`; exit 0.
- **Category:** EXECUTED_TEST.
- **Reproduction:** reproduced; per-case JSON lets a reviewer inspect each expectation.
- **Limitation:** "PASS" means the case behaved as the manifest expected. The manifest expectations were authored by the same party that built M8. Corpus coverage is bounded; M8's *implemented* checks only (Agent A's warning stands).
- **Disposition:** SUPPORTED (for the narrow claim: the corpus passed as defined).

### CLM-04 — Six valid examples passed

- **Source:** completion report; design review §3
- **Evidence:** `owner-review/logs/spec-examples.log` (`71198002aec6944f…`); `m8/corpus/v08/v08-ex0.msve` … `v08-ex5.msve`.
- **Method:** `python3 -m m8.cli spec-examples` reproduced; log shows B.11 examples 0–5 PASS.
- **Outcome:** 6/6 pass (parse + name-resolution + type-check).
- **Category:** EXECUTED_TEST.
- **Reproduction:** reproduced.
- **Limitation:** establishes syntax/types only — not contract satisfiability, not semantic correctness.
- **Disposition:** SUPPORTED.

### CLM-05 — Five invalid examples were rejected correctly

- **Source:** completion report; design review §3
- **Evidence:** `owner-review/logs/spec-examples.log`; `m8/corpus/v08/inv-*.msve` (5 files).
- **Method:** reproduced; log shows B.12 examples 0–4 PASS with categories syntax, type, name-resolution, admission, lexical.
- **Outcome:** 5/5 rejected in the marked categories.
- **Category:** EXECUTED_TEST.
- **Reproduction:** reproduced.
- **Limitation:** the categories were assigned by the same party that wrote the cases.
- **Disposition:** SUPPORTED.

### CLM-06 — Grammar conformance passed

- **Source:** completion report; design review §3
- **Evidence:** `owner-review/logs/grammar-conformance.log` (`e8a81a50f38b57ed…`); `m8/grammar.py`; spec §B.3.
- **Method:** `python3 -m m8.cli grammar-conformance` reproduced. Checks: every production has a parser method; spec §B.3 block byte-identical to `generate_markdown()`.
- **Outcome:** `OK (48 productions, parser methods present, spec §B.3 matches generated)`; exit 0.
- **Category:** EXECUTED_TEST + MECHANICAL_DOCUMENT_CHECK.
- **Reproduction:** reproduced.
- **Limitation:** byte-identity is between the spec block and the generator — both authored by the same party. It does not establish the grammar is *correct*, only single-sourced.
- **Disposition:** SUPPORTED (for the narrow claim: conformance passed).

### CLM-07 — Canonicalisation tests passed

- **Source:** completion report; design review §3
- **Evidence:** `owner-review/logs/test-canonical.log` (`3e169d871d00846c…`); `m8/tests/test_canonical.py`; `m8/canonical.py`.
- **Method:** `python3 -m m8.tests.test_canonical` reproduced.
- **Outcome:** `test_canonical: all assertions hold`; exit 0.
- **Category:** EXECUTED_TEST.
- **Reproduction:** reproduced.
- **Limitation:** bounded assertions (f64 forms, escapes, rationals, envelopes). The 2,998-value collision sweep was Reviewer B's ad-hoc script, not preserved as an artefact — EVIDENCE_NOT_AVAILABLE for the sweep itself. Injectivity remains a proof sketch.
- **Disposition:** PARTIALLY_SUPPORTED (the preserved test module passed; the sweep is not preserved).

### CLM-08 — 24 defects were found by reviewers A–D

- **Source:** completion report
- **Evidence:** `owner-review/reviewer-reports/reviewer-*.md` (4 files) + `PROVENANCE.md`.
- **Method:** inspected each report; counted findings: A1–A10 (10), B1–B7 (7), C1–C5 (5), D1–D3 (3) = 25; C3 duplicates B7 → 24 unique.
- **Outcome:** 24 unique findings documented.
- **Category:** SPECIFICATION_REVIEW (the findings are review outputs).
- **Reproduction:** the reports are preserved; the reviewers' ad-hoc probe scripts were not preserved.
- **Limitation:** "independent" is procedural — reviewers inherited parent context at spawn. A and D reports were extracted from session records (handoff did not arrive); text verified identical to session source.
- **Disposition:** SUPPORTED (24 unique findings; 25 with the duplicate counted).

### CLM-09 — All findings were corrected

- **Source:** completion report; design review §5; ledger §§NEW-A/B/C/D
- **Evidence:** corrected spec text (see traceability); 10 new corpus cases; 14 new canonical assertions; `owner-review/logs/*` (post-correction runs green).
- **Method:** for each finding, located the correction in the spec/tool and the regression case; re-ran the gates after all corrections.
- **Outcome:** every finding has a linked correction and regression case; all gates green after correction.
- **Category:** EXECUTED_TEST (tool fixes + corpus) + SPECIFICATION_REVIEW (spec fixes).
- **Reproduction:** the final state was reproduced; the intermediate pre-fix states were not preserved as separate artefacts.
- **Limitation:** correctness of each fix rests on the lead's adjudication, not on a second independent review of the fixes.
- **Disposition:** SUPPORTED (with the stated limitation).

### CLM-10 — All M8 gates remain green

- **Source:** completion report
- **Evidence:** `owner-review/logs/corpus.log`, `spec-examples.log`, `grammar-conformance.log`, `test-canonical.log`, `test-grammar-conformance.log`.
- **Method:** all five commands reproduced 2026-10-09 after the final corrections.
- **Outcome:** corpus 0 failures; spec-examples 0 failures; grammar-conformance OK; test_canonical PASS; test_grammar_conformance PASS.
- **Category:** EXECUTED_TEST.
- **Reproduction:** reproduced.
- **Limitation:** gates test the final state; they do not test the corrections' necessity (no pre-fix gate logs preserved).
- **Disposition:** SUPPORTED.

### CLM-11 — Cross-document consistency was established

- **Source:** completion report; design review §4.4
- **Evidence:** Reviewer D report; lead's follow-up greps (NEW-D1 regression check).
- **Method:** D's textual/structural audit; 3 defects found and fixed; re-grep confirms no normative v0.7 links remain.
- **Outcome:** consistent after correction.
- **Category:** MECHANICAL_DOCUMENT_CHECK + SPECIFICATION_REVIEW.
- **Reproduction:** the grep checks are reproducible; D's full audit is preserved as a report.
- **Limitation:** textual/structural only; D did not re-verify every semantic claim.
- **Disposition:** SUPPORTED (with the stated limitation).

### CLM-12 — v0.8 is ready for owner review

- **Source:** design review §7 (gate decision)
- **Evidence:** this matrix (CLM-01–CLM-11); the six documents; the traceability table.
- **Method:** consolidated assessment.
- **Outcome:** 10 SUPPORTED, 1 PARTIALLY_SUPPORTED (CLM-07), 0 UNSUPPORTED, 0 INCONCLUSIVE.
- **Category:** SPECIFICATION_REVIEW (judgment, not measurement).
- **Reproduction:** the underlying evidence is preserved and reproducible; the judgment itself is the lead's.
- **Limitation:** "ready for owner review" is a threshold judgment — it asserts the package is coherent enough to review, not that it is correct. The "next unchecked layer" pattern (24 defects found in the correction pass) implies further defects may remain. No implementation exists; no conformance or execution claims are made.
- **Disposition:** SUPPORTED as a *review-readiness* claim; the owner must still perform the review.

---

## Summary

| Disposition | Count | Claims |
|---|---|---|
| SUPPORTED | 10 | CLM-01, 02, 03, 04, 05, 06, 08, 09, 10, 11 |
| PARTIALLY_SUPPORTED | 1 | CLM-07 (collision sweep not preserved) |
| UNSUPPORTED | 0 | — |
| INCONCLUSIVE | 0 | — |

No claim required manufacturing evidence. One evidence gap identified: Reviewer B's 2,998-value collision sweep script was not preserved (EVIDENCE_NOT_AVAILABLE); the claim it supported (spelling-level uniqueness) is otherwise covered by the preserved `test_canonical.py` assertions.
