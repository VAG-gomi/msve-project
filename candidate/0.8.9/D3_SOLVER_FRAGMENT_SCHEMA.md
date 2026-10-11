# D3 Solver-Fragment Schema — `msve-arith-v1` (Normative, Candidate 0.8.9)

**Status:** candidate for owner review. **Scope:** solver-fragment first
(D3 scope ruling, Option A). Schemas for other claim kinds are explicitly
deferred until their semantics are designed. This document does not expand
the DSL beyond what is implemented and verified.

## 1. Input schema and permitted fields

A query is a JSON object with exactly these fields:

```
query := {
  "language":     "msve-arith-v1",          # required, exact string
  "declarations": [decl*],                  # optional, default []
  "assertions":   [expr+]                   # required, non-empty list
}
decl := { "name": <non-empty string, first char alphabetic>,
          "sort": "Int" | "Bool" }
```

No other fields are permitted at the top level of the query object.
Unknown fields are rejected as `MALFORMED_INPUT`.

## 2. Variable declarations, types, name binding

- Two sorts: `Int` (mathematical integers, unbounded) and `Bool`.
- Each declaration binds a name to a sort. Names must be unique within a
  query; duplicates are rejected. A name's first character must be
  alphabetic (this excludes numeric literals from the name space).
- Name resolution is lexical and flat: there are no scopes, binders, or
  shadowing. An unbound name is rejected (`unbound-identifier`).

## 3. Expression operators and semantics

```
expr := <int literal> | <bool literal> | <declared name>
      | ["+", expr, expr] | ["-", expr, expr] | ["*", expr, expr]
      | ["=", expr, expr]
      | ["<", expr, expr] | ["<=", expr, expr]
      | [">", expr, expr] | [">=", expr, expr]
      | ["and", expr+] | ["or", expr+] | ["not", expr]
      | ["ite", expr, expr, expr]
```

Semantics are the standard mathematical meanings over integers and
Booleans: `+,-,*` are integer arithmetic; comparators are integer order
(`=` is sort-polymorphic equality); `and/or/not` are Boolean connectives;
`ite(c, t, e)` is if-then-else. There is no division, no modulus, no
quantifiers, no uninterpreted functions.

## 4. Typing rules

- Integer literals and `+,-,*` over `Int` yield `Int`.
- Comparators over `Int` yield `Bool`; `=` requires both sides to have
  the same sort and yields `Bool`.
- `and`/`or` require ≥1 `Bool` arguments and yield `Bool`;
  `not` requires exactly one `Bool` argument.
- `ite` requires a `Bool` condition and two branches of the same sort;
  it yields that sort.
- Any ill-typed expression is rejected as `MALFORMED_INPUT`. Typing is
  decidable and total over the grammar: every closed expression has
  exactly one sort or is rejected.

## 5. Top-level assertion requirements

Every element of `assertions` must have sort `Bool`. The query denotes
the **conjunction** of its assertions. An empty assertion list is
rejected: a query must say something.

## 6. Query interpretation and claim-kind/outcome mappings

The solver checks satisfiability of the asserted conjunction.

| Claim kind | Query content | UNSAT | SAT | UNKNOWN |
|---|---|---|---|---|
| `holds` | **negation** of the claimed property | `HOLDS` | `VIOLATED` (witness = counterexample) | `INCONCLUSIVE` (+ weak `SOLVER_BACKED` per A1) |
| `derive`, `prove` | diagnostic query | `INCONCLUSIVE` (diagnostic only) | `INCONCLUSIVE` (diagnostic only) | `INCONCLUSIVE` (+ weak `SOLVER_BACKED` per A1) |
| seven unresolved kinds | any | `INCONCLUSIVE`, no basis (A2 bar) | `INCONCLUSIVE`, no basis (A2 bar) | `INCONCLUSIVE`, no basis (A2 bar) |

For `holds`, the caller supplies the negated property: UNSAT means no
counterexample exists within the solver's reasoning, hence the property
holds relative to the query as stated. Solver results are observations
about the formal query, never proofs of the natural-language proposition.

## 7. Assumption representation and semantic role

**Normative rule:** in `msve-arith-v1`, assumptions are **non-semantic
metadata**. They are recorded strings, preserved byte-for-byte in the
claim identity (`msve-descriptor-1`), and reported in results — but they
are **not** incorporated into the solver query and do **not** participate
in solver reasoning.

Consequences:

- Assurance attaches to the formal query **as stated**, never to
  "the proposition under the assumptions."
- A claim whose truth depends on assumptions not encoded in the query
  is **underspecified** for assurance purposes. The engine must not
  grant assurance that depends on formally unrepresented assumptions.
- Callers that need assumption-like premises in reasoning must encode
  them as assertions **inside the query**. The schema provides no
  separate assumption-to-premise channel, by design: silently promoting
  a preserved string to a logical premise would be inventing semantics.

This preserves the existing `claim_query_link: UNVERIFIED` boundary and
the D3 prohibition on accepting dependent claims without a formal schema.

## 8. Admission, rejection, unsupported, underspecified

- **Admitted:** well-formed `msve-arith-v1` queries for kinds
  `holds`, `derive`, `prove`.
- **Rejected** (`MALFORMED_INPUT`): unknown language, bad declarations,
  unbound/duplicate names, ill-typed expressions, non-Boolean assertions,
  empty assertion list, non-string operators, unknown operators.
- **Unsupported** (`UNSUPPORTED`): any other `language` value; the seven
  unresolved kinds for assurance purposes (recording permitted).
- **Underspecified** (`UNDERSPECIFIED`): claims whose assurance would
  depend on assumptions not represented in the query.

## 9. Query identity, canonical identity, provenance

- `query_id = sha256` over canonical JSON (sorted keys, no whitespace,
  UTF-8) of the query object.
- The claim's `claim_id` uses `msve-descriptor-1` (A6), which covers the
  claim fields including the assumption strings — but **not** the query
  object itself. Query and claim identities are linked in the result
  record (`query_id` field); the link `claim_query_link` remains
  `UNVERIFIED` (see §10).
- Solver observations bind claim, query, and spec version (A1).

## 10. Solver conclusions vs natural-language prose

Solving the supplied query establishes a result **about that formal
query under the semantics defined above**. It does not establish that
the free-text `proposition` expresses the same mathematical claim, that
the query faithfully formalizes the proposition, or that the
declarations model the intended domain. That correspondence is
unverified by the engine and must be established — if at all — outside
it. No output, report, or assurance path may imply otherwise.

---

**Deferred:** schemas for all other claim kinds; assumption-as-premise
channels; richer sorts and theories. Each requires its own semantics
design and owner decision before any dependent claim is accepted (D3).
