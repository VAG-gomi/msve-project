# MSVE Owner Decision Packet — v0.9 synthesis (2026-10-09)

Evidence-linked decision set for the 0.8.8.1 correction candidate. Each
item states the precise question, the options in the surviving records,
the strongest case each way, and the exact choice reserved for the owner.
Ledger IDs refer to `MSVE_BRAINSTORM_DECISION_LEDGER.csv`.

Already-decided matters (DEC-001–DEC-007) are **not** reopened here.

---

## D1. Z3 UNKNOWN and SOLVER_BACKED eligibility (DEC-008)

**Precise question:** May a Z3 `UNKNOWN` observation substantiate a
`SOLVER_BACKED` assurance basis, or is UNKNOWN permanently barred from
supporting any basis?

**Why it matters:** The normative outcome table (§E.5) says
`UNKNOWN → sr = Some(INCONCLUSIVE)` ("never a positive conclusion").
The formal model enforces `outcome ≠ UNKNOWN` for `SOLVER_BACKED`. These
are compatible only if INCONCLUSIVE never carries SOLVER_BACKED — but the
table's UNKNOWN row can be read as permitting the weak chain
UNKNOWN + INCONCLUSIVE + SOLVER_BACKED. The two readings give different
assurance semantics.

**Options:**
- **(A)** UNKNOWN never supports any basis. INCONCLUSIVE stands alone
  (it needs no assurance). The table's UNKNOWN row reads
  `outcome_compatible = False`.
- **(B)** UNKNOWN + INCONCLUSIVE + SOLVER_BACKED is a legitimate weak,
  documented evidence chain. The model is revised to permit it.

**Strongest for (A):** Prevents weak evidence from substantiating an
assurance basis; matches the model's current enforcement; the O2
regression already tests UNKNOWN-rejected-as-solver-backed.

**Strongest for (B):** The normative table as written maps UNKNOWN to a
result rather than to incompatibility; a documented weak chain is more
informative than silence about what the solver did.

**Spec/model constraints:** §E.5 outcome table; model `outcome_compatible`.

**Consequences:** (A) narrows SOLVER_BACKED to SAT/UNSAT-backed results;
(B) widens it to include documented solver-limit cases, weakening the
basis's meaning.

**Smallest exposing test:** A case with `outcome = UNKNOWN`,
`sr = INCONCLUSIVE`, `basis = SOLVER_BACKED` — under (A) the model must
reject; under (B) it must accept.

**Recommendation:** (A). The safer reading; the model already enforces it.

**Owner choice:** Select (A) or (B). If (B), the model needs revision —
that is further design work, not a consequence of this packet.

---

## D2. The seven unresolved claim kinds (DEC-009)

**Precise question:** For `no_solution`, `contradiction`,
`unique_under_projection`, `violated`, `underdetermined`, `disproved`,
`artifact_constructed` — extend the per-kind outcome table, declare them
explicitly unsupported for SOLVER_BACKED in V0, or leave unresolved?

**Why it matters:** Until decided, a solver observation may be recorded
for these kinds but cannot justify SOLVER_BACKED; any claim of formal
closure is blocked.

**Critical dependency — invariants 22/23.** The spec contemplates solver
observations for two of the seven:
- Inv 22: `CONTRADICTION {}` ⇒ `solver_observation = Some({outcome:
  UNSAT, …})` ∨ proof artifact.
- Inv 23: `UNIQUE_UNDER_PROJECTION {projection}` ⇒ `solver_observation
  = Some({outcome: UNSAT, …})` (second-model query) ∨ derivation record.

So these two kinds cannot simply be "excluded": the invariants give them
an evidence role (UNSAT observations). What is missing is which outcomes
*support SOLVER_BACKED* for them — recording ≠ justifying.

**Options:**
- (a) Extend the outcome table with per-kind rules (normative design work).
- (b) Declare the seven explicitly unsupported for SOLVER_BACKED in V0 —
  observations remain recordable per inv 22/23, but the basis is barred.
- (c) Leave marked unresolved (current state).

**Strongest for (a):** Closes the semantics; inv 22/23 already point at
UNSAT as the meaningful outcome for two kinds.

**Strongest for (b):** Honest scoping; avoids inventing semantics under
decision pressure. Cost: inv 22/23 keep their recording role, which must
be stated explicitly so (b) is not misread as deleting them.

**Strongest for (c):** No premature closure. Cost: blocks formal-closure
claims indefinitely.

**Recommendation:** (b), with inv 22/23 preserved as recording
requirements. It is the smallest honest scope cut; (a) can follow later
as new design work.

**Owner choice:** Select (a), (b), or (c). If (a), that is a new
normative work order.

---

## D3. Query and assumption fidelity (DEC-010)

**Precise question:** Is attestation sufficient for V0, or is a
query-audit mechanism required?

**Why it matters:** The model never checks that a solver `query`
faithfully encodes the claimed proposition, and `assumptions` is
normative but unrepresented in the model (M2). A mistaken or adversarial
query breaks the assurance chain silently.

**Options:** (a) Accept attestation for V0 (documented gap);
(b) require a query-audit mechanism design.

**Strongest for (a):** V0 is an evidence-validation layer; full query
semantics is a research problem, not a V0 deliverable.

**Strongest for (b):** Without it, SOLVER_BACKED rests on an unchecked
premise — the chain's weakest link is structural, not incidental.

**Recommendation:** (a) for V0, explicitly documented — with the gap
named in the acceptance criteria so it cannot be forgotten later.

**Owner choice:** Accept the attested gap or commission mechanism design.

---

## D4. Checker independence and authorisation (DEC-011)

**Precise question:** Define an attestation schema for checker
authorisation and recompute-checker independence, or accept the gap?

**Why it matters:** `checker ≠ ""` is enforced, but that the checker
names an authorized kernel — and that a recompute checker is independent
of the producer — are format-free attestations. A producer self-recompute
is undetectable.

**Options:** (a) Design a normative attestation schema;
(b) accept the documented gap for V0.

**Recommendation:** (a) is cheap relative to its value — a schema for
"who may check" and "independence from whom" — but it is new design work.

**Owner choice:** Commission the schema or document acceptance of the gap.

---

## D5. Two-slot bounds (DEC-012)

**Precise question:** Is the model's bound (2 verification records, 2
descriptors, 2 solver invocations per result) an acceptable V0 bound, or
must the schema support arbitrary counts?

**Why it matters:** A third of any is unrepresentable. If real V0
results need more, the model cannot encode them.

**Options:** (a) Accept as a V0 bound; (b) extend the schema.

**Recommendation:** (a), unless a concrete V0 use case needs three — no
such case is in the records.

**Owner choice:** Accept the bound or require the extension.

---

## D6. Canonical claim-identity encoding and escaping (DEC-013)

**Precise question:** Specify the exact escaping rule for the canonical
encoding `kind|proposition|goal_ref|inputs_ref|assumptions|spec_version`,
or accept the model's slot-equality proxy?

**Why it matters:** `claim_id = sha256(canonical_encoding)` is normative,
but without an escaping rule, adversarial proposition/assumption content
could produce ambiguous encodings. The model does not recompute the hash.

**Options:** (a) Specify escaping normatively; (b) accept the proxy as a
V0 limitation.

**Recommendation:** (a) — this is a small, closable specification task,
and identity is load-bearing (DEC-001/DEC-002).

**Owner choice:** Commission the escaping rule or accept the limitation.

---

## D7. Approval boundary and freeze criteria (DEC-014)

**Precise question:** Approve, modify, or reject the five proposed
baseline-acceptance criteria?

**Why it matters:** No freeze, baseline, implementation, or experiment is
authorised. The criteria are the gate to all of them.

**Proposed criteria (not binding):**
1. All UNRESOLVED items above decided by the owner.
2. Fresh independent reviews on the exact final hashes, no blocking
   findings open.
3. Regression suite covering every normative rule claimed as mechanically
   enforced.
4. The 7-kind outcome table extended or explicitly scoped.
5. Explicit owner statement authorising freeze.

**Note on criterion 2:** the normative re-review of the final spec hash
`dbc610c3…` is currently undocumented (DEC-024). Criterion 2 cannot be
met without it.

**Owner choice:** Approve the criteria as binding, modify them, or
replace them. Then apply them.

---

## D8. V0 scope: validation layer vs construction engine (DEC-015)

**Precise question:** Is the first implementation slice an
evidence-validation layer over established tools, or does it include
autonomous construction of new mathematical structures?

**Why it matters:** The acceptance plan scopes generation out of the
initial vertical slice, but the spec includes construction result types
(e.g. `ARTIFACT_CONSTRUCTED`). The boundary determines what the first
build must demonstrate.

**Options:** (a) Validation-layer first: the slice checks that claimed
results are properly supported. (b) Include constrained construction:
additionally specify how candidate constructions are generated,
represented, and distinguished from merely-permitted ones.

**Recommendation:** (a) — it matches the acceptance plan and is the
smaller verifiable deliverable. (b) is a separate design effort.

**Owner choice:** Fix the initial capability boundary.

---

## D9. §H governance clarification (DEC-016 / DEC-025)

**Precise question:** Confirm that spec §H ("repo creation after freeze;
frozen spec is the genesis commit") governs the *future implementation
repository*, while the existing public `msve-project` is the *archival
project bank* — so the archive's existence does not violate §H.

**Why it matters:** Read literally, §H could be taken to forbid the
repository that already exists. The distinction dissolves the tension.

**Owner choice:** Confirm the distinction (proposed recording location:
`PROJECT_STATE.md` or `OPEN_DECISIONS.md`), or state the alternative
reading.

---

## Already decided — do not reopen

DEC-001–DEC-007 (claim descriptor Option A, syntactic identity,
solver_invocations, claim-linked provenance, per-goal outcomes, PUBLIC
visibility, candidate-not-frozen status). No new contradictory evidence
has been identified.

## What happens after the owner rules

Decisions here do not change the candidate. Each ruling maps to a
follow-on: (A)/(B) on D1 → model or table edit; D2 → table extension or
scoping edit; D6 → escaping rule; D7 approval → freeze review against the
criteria. Those are separate work orders, each requiring its own
authorization. Nothing in this packet authorises them.
