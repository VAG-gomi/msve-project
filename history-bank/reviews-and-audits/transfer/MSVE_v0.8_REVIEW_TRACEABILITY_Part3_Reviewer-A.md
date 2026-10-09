# Report D — Reviewer A Report — Full Text (Part 3/6)

**Work Order:** 0.8.2 · **Source:** `owner-review/reviewer-reports/reviewer-A-grammar-type-system.md` (DIRECT ARTEFACT — transcribed verbatim from the ZIP).

Original findings preserved verbatim. See PROVENANCE note below for execution provenance.

---

I have completed my independent audit. Here is my report.

---

# Sub-agent A Report: Grammar and Type-System Audit of MSVE v0.8

**Auditor:** Sub-agent A (grammar/type-system), operating independently. All findings below were verified by my own inspection of the files and my own test executions — I re-ran every M8 command rather than trusting the build record, and I wrote my own adversarial probes.

**Files examined:** `MSVE_DESIGN_SPEC_v0.8.md` (§B.1–B.13), `m8/grammar.py`, `m8/lexer.py`, `m8/parser.py`, `m8/resolve.py`, `m8/typecheck.py`, `m8/canonical.py`, `m8/cli.py`, `m8/README.md`, `m8/runs/2026-10-09-m8-build.md`, `m8/corpus/manifest.json` (+ sampled corpus files).

## Summary

The v0.8 grammar/type-system work is a genuine improvement over v0.7: the D-025 record-construction production exists and is integrated, the single-source-of-truth claim for §B.3 verifies mechanically, and M8's corpus/spec-examples/grammar-conformance all pass as claimed when I ran them myself. I found **no recurrence of the B-01 class** (every record literal in the normative examples parses under an explicit production, and I reproduced the negative control).

However, I found **10 defects**, most of them the same *shape* of failure as B-01: the spec normatively requires checks that M8 does not perform. The pattern is "normative rule exists in prose, no mechanical enforcement." The six M8-implementation gaps (NEW-A1–A6) are the most consequential for the release gate, because the v0.8 review's evidence claims rest on M8.

## Independent confirmations (each re-run by me)

1. **`python3 -m m8.cli grammar-conformance`** → OK, exit 0: 48 productions, every production has a parser method, and the spec's §B.3 block is byte-identical to `generate_markdown()`. The single-source-of-truth claim (D-025/B-01) holds.
2. **`python3 -m m8.cli corpus`** → 0 failures (36/36 files obtain expected outcomes).
3. **`python3 -m m8.cli spec-examples`** → 6/6 B.11 examples pass; 5/5 B.12 examples rejected with the marked categories.
4. **Keyword agreement:** the §B.2 reserved-keyword set and `m8/lexer.py:KEYWORDS` agree exactly (62/62, empty symmetric difference — verified by script, not by eye).
5. **B-01 negative control reproduced:** with `Parser.parse_record_literal` monkeypatched to raise (simulating the v0.7 grammar), a record example fails with `syntax error ... expected expression, found '{'` — M8 has genuine discriminating power for the B-01 defect class.
6. **B.11 ex3 (selector contract) and ex5 (validator contract):** manually traced. Record literals derive under the D-025 `Atom` alternative; the D-028 `len(d.candidates) == 0` conjunct is present in the contract text; `check validator_contract of validator_impl` satisfies the (In, Out)→Bool / Impl(In→Out) rule; differential+fuzz test items are correctly distinguished per D-024; all quantifier binders, field accesses, and builtin arities check out.
7. **B.12 ex0 (bare quantifier)** → correctly `syntax` (grammar mandates `"::" "(" Proposition ")"`); **B.12 ex4 (`p-0`)** → correctly `lexical` (strict HexFloat regex rejects `-0` exponent; the `_HEXFLOAT_ATTEMPT` guard produces a precise diagnostic).
8. **Axiom/assumption name resolution** (the v0.7-era hole): `axiom bad: frobnicate(1) == 2` is now rejected — the `check_definition` re-resolution path works.
9. **`output` scoping:** rejected in unreferenced constraint groups and in `derive` goals, as §B.5a requires.

## Defects

### NEW-A1 — M8 does not enforce §B.8 resource-limit ranges (M8 gap)

- (b) Spec §B.8: "`timeout` mandatory… range 1s…24h (outside → INVALID_INPUT(timeout-out-of-range)). `steps: 0` → INVALID_INPUT(degenerate-resource-limit)." Tool: `m8/typecheck.py:Checker.check_limits` is literally `return  # durations/memory lexed; no further static rules`.
- (c) Counterexample: `limits { timeout: 9999h; }` → **M8: PASS** (ran myself). `limits { timeout: 10s; steps: 0; }` → **M8: PASS** (ran myself).
- (d) Expected: admission failures with the §B.8 codes. Actual: silent acceptance.
- (e) Root cause: `check_limits` was left as a stub; the normative rule exists only in prose.
- (f) Proposed correction: implement the range check (parse the Duration value, compare against 1s…24h) and the `steps: 0` / `cases: 0`-analogous rejections in `check_limits` (`cases: 0` is already handled in `check_verification`; extend the same treatment).
- (g) Regression case: corpus files `limits-timeout-range.msve` (expect fail/admission) and `limits-steps-zero.msve` (expect fail/admission).
- (h) Does NOT establish that the spec's §B.8 is wrong — the spec is correct; M8 is incomplete. Does not affect any other check's validity.

### NEW-A2 — M8 does not reject `level-a required` on construct/check/compare-models goals (M8 gap)

- (b) Spec §B.7: "`construct` / `compare-models` / `check` + `level-a required` → INVALID_INPUT(assurance-level-unavailable)." Tool: `m8/typecheck.py:check_verification` — the `if mode == "level-a":` block handles only `ProveGoal` and `DeriveGoal`; there is no `else` branch.
- (c) Counterexample: construct goal with `assurance: level-a required` → **M8: PASS** (ran myself).
- (d) Expected: `INVALID_INPUT(assurance-level-unavailable)`. Actual: acceptance.
- (e) Root cause: the positive admission requirements (prove→kernel proof, derive→proof-or-recompute) were implemented but the negative exclusion for the other three goal kinds was omitted.
- (f) Proposed correction: add the `else` branch emitting `assurance-level-unavailable` for ConstructGoal/CheckGoal/CompareGoal with `level-a`.
- (g) Regression case: corpus file `verif-assurance-level-a-unavailable.msve` (construct + level-a → fail/admission).
- (h) Does NOT establish the assurance policy itself is unsound — only that M8 under-enforces it.

### NEW-A3 — M8 never validates projection paths against the model type (M8 gap)

- (b) Spec §B.5a: "projection paths type-check against that type." Tool: `m8/resolve.py` says "projections: paths resolve against model type (checked in typecheck)" — but `typecheck.py` contains no projection-path check at all (verified by reading the full file; `check_goal`'s CompareGoal branch checks `refs` and `under` but never the paths).
- (c) Counterexample: `projection bad = [output.zzz]` with model type `{ x: Nat }` under a compare-models goal → **M8: PASS** (ran myself).
- (d) Expected: rejection (unresolvable path). Actual: acceptance — a dangling comment in resolve.py claims a check that does not exist.
- (e) Root cause: the check was deferred between the two passes and never implemented in either.
- (f) Proposed correction: in `check_goal`'s CompareGoal branch, walk each projection's paths against the resolved model record type (first segment must be `output`, subsequent segments must be fields of the current record type).
- (g) Regression case: corpus file `proj-path-unresolvable.msve` (expect fail/admission or type).
- (h) Does NOT establish anything about projection semantics beyond path resolution.

### NEW-A4 — Cyclic type aliases crash M8 instead of producing a diagnostic (M8 bug)

- (b) Tool: `m8/typecheck.py:_resolve_alias` raises bare `ValueError(f"cyclic type alias {t}")`; no caller catches `ValueError` (callers catch only `CheckError`).
- (c) Counterexample: `type A = B` / `type B = A` → **uncaught traceback, tool crash** (ran myself; exit via exception, not a categorized error).
- (d) Expected: a categorized diagnostic (e.g. admission/type error). Actual: Python traceback — M8's "every failure carries a category" contract (cli.py docstring) is violated.
- (e) Root cause: the occurs/cycle guard uses the wrong exception type for the tool's error protocol.
- (f) Proposed correction: raise `CheckError` (or catch `ValueError` at the `check_source` boundary and map it to a category).
- (g) Regression case: corpus file `type-cyclic-alias.msve` (expect fail with a clean category, no traceback).
- (h) Does NOT establish that recursive types should be legal — only that the rejection must be a diagnostic, not a crash.

### NEW-A5 — Unbound type names pass silently when unconstrained (M8 gap)

- (b) Tool: `m8/typecheck.py:type_of_texpr` returns unknown `NamedType`s verbatim ("allow forward refs: record now, resolve at use") — but nothing ever resolves them.
- (c) Counterexample: `define f(x: Ghost): Nat = 1` → **M8: PASS** (ran myself). A downstream use gives only a confusing message: `type T = { x: Ghost }` + `define v: T = { x: 1 }` → "type error: literal has type Nat, expected Ghost" (never "unknown type").
- (d) Expected: `INVALID_INPUT(unbound-identifier: Ghost)` per §B.5, or at minimum an "unknown type" diagnostic at the declaration. Actual: silent acceptance / misleading message.
- (e) Root cause: all type aliases are collected in pass 1, so forward references are unnecessary — the leniency serves no purpose and creates the hole.
- (f) Proposed correction: in `type_of_texpr`, resolve `NamedType` against `self.aliases`/`self.r.type_aliases` at the point of use and raise a name-resolution error for unknown names.
- (g) Regression case: corpus file `type-unbound-name.msve` (expect fail/name-resolution).
- (h) Does NOT establish that any currently-passing normative example relies on the leniency (all 6 B.11 examples declare types before use — verified by the passing spec-examples run).

### NEW-A6 — Builtin shadowing not rejected (M8 gap)

- (b) Spec §B.5: "Flat namespace per specification (types, definitions, axioms, assumptions, constraint groups, projections, external handles, builtins per §B.4 rule 11). Duplicates → INVALID_INPUT(duplicate-definition: name)."
- (c) Counterexample: `define len: Nat = 3` → **M8: PASS** (ran myself); the definition is then silently unusable (`len` as a call resolves to the builtin; as a value it errors "builtin used as a value").
- (d) Expected: `INVALID_INPUT(duplicate-definition: len)`. Actual: acceptance of a definition that can never be referenced.
- (e) Root cause: `resolve.py:collect` checks duplicates only against user definitions, never against `BUILTINS`.
- (f) Proposed correction: in `collect`, reject definition names that collide with `BUILTINS` (and the contextual type names) as `duplicate-definition`.
- (g) Regression case: corpus file `define-shadow-builtin.msve` (expect fail/name-resolution or admission).
- (h) Does NOT establish that shadowing would be semantically harmful — only that the spec's flat-namespace rule is unenforced.

### NEW-A7 — HexFloat `-?` creates a tokenization ambiguity with binary minus (spec lexical wart)

- (b) Spec §B.2: `HexFloat := "-"? "0x" ("0" | "1") "." HexLo{13} "p" …`. The spec states no tokenization disambiguation rule (maximal munch is assumed, never stated).
- (c) Counterexample: `define v: Binary64 = 0x1.0000000000000p+0-0x1.0000000000000p+0` (subtraction, no spaces) → the lexer gloms `-0x1.0000000000000p+0` as one HEXFLOAT token (maximal munch) → `syntax error ... found '-0x1.0000000000000p+0'` (ran myself). The identical expression with spaces parses.
- (d) Expected: either consistent tokenization (subtraction works without spaces, as it does for `1-2`) or an explicit rule. Actual: whitespace-sensitive lexing for exactly one literal kind.
- (e) Root cause: embedding the sign in the numeric token — a design most languages avoid (unary minus is normally a separate operator; the grammar already has `Unary := ("!" | "-")? Postfix`).
- (f) Proposed correction: drop `-?` from the HexFloat token and rely on unary minus (canonical spellings like `-0x1…p+0` remain byte-identical source text; canonicalization operates on values), or state maximal munch normatively in §B.2.
- (g) Regression case: corpus file `f64-subtraction-no-spaces.msve` documenting whichever behavior is chosen.
- (h) Does NOT establish any semantic unsoundness — both readings denote the same value; it is a lexical robustness wart.

### NEW-A8 — Function-typed parameters cannot be called (M8/spec inconsistency)

- (b) Grammar permits `Params := (Ident ":" TypeExpr …)` where TypeExpr includes function types; §B.4 rule 10 ("Application: exact argument-type match") does not restrict application to top-level functions. Tool: `m8/typecheck.py:check_call` raises "calling a local variable 'f' (not a function)" for `tag == "local"`.
- (c) Counterexample: `define apply(f: (Nat) -> Nat, x: Nat): Nat = f(x)` → **rejected** (ran myself), although `f` as a *value* type-checks fine — first-class function values exist but cannot be applied.
- (d) Expected: either callable (spec permits the type) or function-typed params banned. Actual: the type is admitted and the call is rejected — the two rules disagree.
- (f) Proposed correction: decide normatively — either allow application of locals whose type is a function type (extend `check_call`), or add a static rule rejecting function-typed parameter/let types. Do not leave the contradiction.
- (g) Regression case: corpus file documenting the chosen behavior.
- (h) Does NOT establish that higher-order functions are needed for the selector slice — only that the current combination of rules is incoherent.

### NEW-A9 — `Set<T>` has no introduction form (spec completeness gap)

- (b) `TypeExpr` includes `"Set" "<" TypeExpr ">"`; §B.4 rule 3 defines set equality; but no production constructs a set value (no literal, no builtin — the builtin inventory in §B.4 rule 11 has no set constructor).
- (c) Counterexample: there is no expression of the form `define s: Set<Nat> = …` that can be written — the type is uninhabitable in surface syntax.
- (d) Expected: every type former has an introduction form, or `Set` is marked reserved-for-future-use. Actual: dead type former with defined equality semantics.
- (e) Root cause: the type system was extended with sets without a corresponding expression production.
- (f) Proposed correction: either add a set-literal production (e.g. `set{…}`) with typing/evaluation rules, or remove `Set` from the v0 type former list.
- (g) Regression case: a corpus case asserting the chosen status (parse or clean rejection).
- (h) Does NOT affect any normative example (none uses sets) — it is a latent inconsistency.

### NEW-A10 — Option accepted as a quantifier domain without defined semantics (M8/spec looseness)

- (b) Spec §B.4 rule 8: "domain is `type T` or a collection expression". Tool: `m8/typecheck.py:check_quant` accepts `("list", "set", "option")` as `ExprDomain`.
- (c) Counterexample: `define o: Option<Nat> = some(1)` then `forall x in o :: (x > 0)` → **M8: PASS** (ran myself).
- (d) Expected: either iteration-over-Option defined in the execution semantics or rejection. Actual: accepted with no specified meaning.
- (e) Root cause: "collection" was implemented as list/set/option without checking that the spec defines iteration for all three.
- (f) Proposed correction: restrict `ExprDomain` to list/set (or define Option iteration normatively).
- (g) Regression case: corpus file `quant-option-domain.msve` with the chosen expectation.
- (h) Does NOT establish that Option iteration is meaningless — only that it is currently unspecified.

## Limitations of this audit (what my findings do NOT establish)

- I audited the grammar, type system, name resolution, and M8's implementation thereof. I did **not** audit semantic contract correctness (validator extensional equality, decode-table fidelity), canonical injectivity beyond the f64/string/rational checks I ran, or the assurance policy — those belong to Sub-agents B, C, D.
- A finding that M8 under-enforces a rule does not impugn the rule itself; NEW-A1–A6 are tool gaps, and the spec text is correct in each case.
- My negative-control reproduction used a monkeypatched parser, not the actual v0.7 grammar — it confirms M8's discriminating power for the B-01 *class*, not the historical v0.7 event.
- I did not verify the lead agent's other v0.8 claims (ledger completeness, matrix, acceptance plan) — out of scope for Sub-agent A.

## Bottom line for the gate

M8 is a real, working audit tool whose headline claims check out — but its coverage is thinner than the v0.8 review's evidence language implies. Six normative rules (§B.5 flat namespace, §B.7 level-a exclusion, §B.8 ranges, §B.5a projection paths, plus crash-safety and type-name resolution) have **no mechanical enforcement**. Until NEW-A1–A6 are fixed and their regression cases are in the corpus, "M8's checks have actually run" should be read as "M8's *implemented* checks have run" — the unimplemented ones are exactly where the next B-01-class defect will hide.

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
