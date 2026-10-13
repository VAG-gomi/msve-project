# D3 Solver-Fragment Schema — `msve-arith-v1` (Normative, Candidate 0.8.9.14)

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
| `holds` | **negation** of the claimed property | `HOLDS` (solver-backed; see §10a) | `VIOLATED` (witness = counterexample) | `INCONCLUSIVE` (+ weak `SOLVER_BACKED` per A1) |
| `derive`, `prove` | diagnostic query | `INCONCLUSIVE` (diagnostic only) | `INCONCLUSIVE` (diagnostic only) | `INCONCLUSIVE` (+ weak `SOLVER_BACKED` per A1) |
| seven unresolved kinds | any | `INCONCLUSIVE`, no basis (A2 bar) | `INCONCLUSIVE`, no basis (A2 bar) | `INCONCLUSIVE`, no basis (A2 bar) |

## 10a. Solver-backed HOLDS vs corpus-based HOLDS (0.8.9.11, Blocker 2)

A `HOLDS` result from a `holds` claim via UNSAT of the negation is
**solver-backed**, NOT corpus-based. The evidence requirements differ:

- **Solver-backed HOLDS**: requires an actual UNSAT solver observation with
  provenance binding (query_id, claim_id, spec_version per Invariant 3).
  Does NOT require a check corpus or verification record. The solver's
  reasoning is the evidence.
- **Corpus-based HOLDS**: requires non-empty check corpus AND passing
  verification record (Invariants 3, 20). The corpus is the evidence.

Neither path permits vacuous HOLDS. A solver timeout, UNKNOWN, or missing
observation cannot produce HOLDS. An empty corpus cannot produce
corpus-based HOLDS.

**Boundary preserved**: When `claim_query_link` is `UNVERIFIED`, the
solver-backed HOLDS applies to the formal query only. The natural-language
proposition remains unverified.

For `holds`, the caller supplies the negated property: UNSAT means no
counterexample exists within the solver's reasoning, hence the property
holds relative to the query as stated. Solver results are observations
about the formal query, never proofs of the natural-language proposition.

## 7. Assumption representation and semantic role

**Normative rule:** in `msve-arith-v1`, assumptions are **non-semantic
metadata**. They are recorded strings, preserved byte-for-byte **as
recorded values**, and reported in results — but they are **not**
incorporated into the solver query and do **not** participate
in solver reasoning. For the **claim identity** (`msve-descriptor-1`),
assumptions contribute their **NFC-normalized** UTF-8 encoding (§E.6b);
canonically equivalent assumption strings therefore yield the same
`claim_id` even though the recorded values differ byte-for-byte.

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
- **Rejected** (`MALFORMED_INPUT`): missing, non-string, or structurally
  malformed `language` field; duplicate JSON object keys at any level
  (0.8.9.9: detected during parsing via duplicate-aware decoding, before
  dictionary construction); bad declarations, unbound/duplicate names,
  ill-typed expressions, non-Boolean assertions, empty assertion list,
  non-string operators, unknown operators, unknown top-level or declaration
  fields (0.8.9.8).
  (Correction 0.8.9.5, Finding 5: an unknown *value* that is a well-formed
  string is NOT malformed — see UNSUPPORTED below.)
- **Unsupported** (`UNSUPPORTED`): a well-formed `language` string naming
  a language not implemented by this candidate (e.g. `"msve-arith-v2"`);
  the seven unresolved kinds for assurance purposes (recording permitted).
- **Underspecified** (`UNDERSPECIFIED`): claims whose assurance would
  depend on assumptions not represented in the query.
  (0.8.9.11: normatively maps to `admission: ACCEPTED` +
  `semantic_result: INCONCLUSIVE{reason: UNDERSPECIFIED_ASSUMPTIONS}` —
  see spec §E.3a. The query is well-formed; the limitation is in the
  claim's assurance requirements, not the query syntax.)

## 9. Query identity, canonical identity, provenance

### 9.1 Canonical query encoding (Correction 0.8.9.2)

`query_id` is the SHA-256 (64-char lowercase hex) of the **canonical
byte encoding** of the query object, defined as follows. The encoding
must be fully deterministic; no serializer discretion is permitted.

1. **Input:** a query object conforming to the `msve-arith-v1` schema.
   Duplicate object keys are rejected at admission (`INVALID_INPUT`);
   they are never silently resolved.
2. **JSON serialization** with exactly these rules:
   - Object keys sorted by Unicode codepoint, ascending. (Sorting is by
     codepoint value, applied before any escaping.)
   - No whitespace: object/array separators are `,` and `:` with nothing
     around them.
   - ASCII-only output (`ensure_ascii`): every non-ASCII character is
     escaped as `\uXXXX` with lowercase hex digits, exactly 4 digits.
     Characters outside the Basic Multilingual Plane are encoded as UTF-16
     surrogate pairs (`\uHHHH\uLLLL`, lowercase hex).
   - String escaping per RFC 8259: `"` → `\"`, `\` → `\\`, control
     characters → `\b` `\f` `\n` `\r` `\t` or `\u00XX` (lowercase hex).
     `/` is NOT escaped.
   - Integers: decimal representation, no leading zeros, no `+` sign,
     no exponent, no decimal point. (`-0` is not permitted; use `0`.)
     The schema permits only integers; non-integer numbers are rejected.
   - Booleans: `true` / `false`. Null: `null`.
   - Arrays preserve element order: `[` elements separated by `,` `]`.
3. **Bytes:** the UTF-8 encoding of the ASCII-only JSON text from step 2.
   (Since the text is ASCII-only, this is the byte sequence of the text.)
4. **Hash:** `query_id = SHA-256(bytes)` rendered as 64-char lowercase hex.

Rationale: the rules above pin every byte. Two implementations that
follow them produce identical `query_id` values for the same query
object. Golden vectors are provided in `QUERY_ID_VECTORS.md`.

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
