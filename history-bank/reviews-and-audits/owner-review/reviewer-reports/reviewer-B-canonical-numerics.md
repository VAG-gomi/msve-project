All checks are complete. Here is my independent audit report.

---

# Sub-agent B Report: Canonicalisation and Numerical-Semantics Audit of MSVE v0.8

**Scope audited:** `MSVE_DESIGN_SPEC_v0.8.md` §§B.4b, G.2 (+ related §§B.4, E.1, E.7); `m8/canonical.py`; `m8/tests/test_canonical.py`; `m8/runs/2026-10-09-m8-build.md`.
**Method:** read the normative text directly; ran the test suite myself; wrote and ran my own adversarial scripts (collision-construction sweep, boundary arithmetic with exact rationals, checker-vs-spec differential probes). I did not rely on the lead's summaries.

## 0. Test execution (task item 6)

`cd /home/hatch/workspace/msve-design && python3 -m m8.tests.test_canonical` → **PASS** (`test_canonical: all assertions hold`), exit 0. I ran this myself; the run record's claim is reproduced.

## A. Claims that survive adversarial checking

**A1 — Binary64 canonical uniqueness (D-017/D-026): CONFIRMED.** I attempted collision construction three ways: (i) all historically known bad pairs (`0x2.…p+0`, `p+01`, normal-form subnormal `0x1.…p-1074`, the v0.7 survivor `p-0`, uppercase hex, signed zero `-0x0.…p+0`) — every one is rejected by `check_f64_canonical`; (ii) a 2,998-value sweep generating all plausible variant spellings per value (case variants, `p-0`/`p+0`, leading-zero exponents, normal-vs-subnormal forms) — **zero cases** with more than one accepted spelling; (iii) the 2^-1022 normal/subnormal boundary — min normal `0x1.0000000000000p-1022` and max subnormal `0x0.fffffffffffffp-1074` are distinct values with disjoint, unique forms (normal range ≥ 2^-1022, subnormal range < 2^-1022, provable from the exponent bounds). The `-0.0`/`+0.0` identification is consistent with §B.4 rule 3 (Binary64 `==` is equality of canonical forms, so they are the same *value* in MSVE's model — matching IEEE `==` semantics — even though §B.4b distinguishes them operationally, which is also IEEE-consistent).

**A2 — Rational text grammar (D-027): CONFIRMED.** `check_rational_canonical` enforces no-leading-zeros, denominator > 0, gcd = 1, and zero exactly as `0/1` (I verified `6/4`, `1/0`, `-0/5`, `07/3` all fail and `7/3`, `-7/3` pass via the suite I ran).

**A3 — Envelope field order + option omission (D-027): CONFIRMED** via the suite I ran (`$type`-first, exact field lists, `some:false` omits `value`).

**A4 — Packaging boundary for NaN/function values (D-018/D-019/D-030): SUBSTANTIALLY CONFIRMED.** The `output_packaging` field + `Option<Hash>` payloads + invariants 10/15/16 form a coherent design: NaN → `PACKAGING_FAILED(output-not-encodable)` with `semantic_result` preserved, never `INVALID_INPUT`. The B-05 contradiction is resolved at the schema level. (One coherence gap remains — see NEW-B7.)

## B. Defects found

### NEW-B1 — §B.4b underflow/overflow boundary statements are wrong/imprecise (D-032)

**(b)** Source: §B.4b, "Underflow" and "Overflow" bullets.
**(c)** Counterexample (verified with exact rational arithmetic, not floats): the exact mathematical result r = 3/4 × 2^-1074 is nonzero with magnitude < 2^-1074. |r − 0| = 3/4·2^-1074, |r − 2^-1074| = 1/4·2^-1074, so round-to-nearest-even yields the **min subnormal 2^-1074**, not ±0. The spec's sentence "a nonzero exact result with magnitude < 2^-1074 rounds to ±0" is **false**. Separately, the overflow rule "magnitude ≥ 2^1024 becomes ±infinity" misstates the boundary: the true round-to-nearest-even threshold is 2^1024 − 2^970, so e.g. exact result 2^1024 − 2^969 rounds to +∞ despite magnitude < 2^1024. Missing cases: `(+inf) − finite` (only `finite − (±inf)` and `inf − inf` are listed) and `0 / (±inf)` (rule restricted to "finite nonzero x").
**(d)** Expected: exact IEEE-754 boundary behavior. Actual: prose approximations that are false at the boundaries.
**(e)** Root cause: the v0.8 rewrite replaced the "cite IEEE 754" hand-wave with hand-written prose that approximates rather than states the exact thresholds.
**(f)** Proposed correction: state exact thresholds (|r| < 2^-1075 → ±0; |r| = 2^-1075 → ±0 by ties-to-even; 2^-1075 < |r| < 2^-1074 → min subnormal; overflow threshold 2^1024 − 2^970), or define overflow/underflow as consequences of the rounding function over the extended target set rather than as separate rules. Add the two missing rows.
**(g)** Regression: `3/4 × 2^-1074 → min subnormal` (not zero); `2^1024 − 2^969 → +inf`; `(+inf) − 5.0 = +inf`; `0.0 / (+inf) = +0`.
**(h)** Does NOT establish: the NaN/infinity/signed-zero rows, which I checked individually and found correct (`0.0/0.0 = NaN`, `inf−inf = NaN`, `0×inf = NaN`, signed-zero rules all match IEEE).

### NEW-B2 — M8's string-escape checker is more permissive than the spec (D-027)

**(b)** Source: `m8/canonical.py::check_string_canonical` vs §G.2 string policy.
**(c)** Counterexample: `check_string_canonical(r'"\u00a0"')`, `r'"\u20ac"'`, and `r'"\ud83d"'` (lone surrogate) are all **accepted** by M8. Per §G.2, `\uXXXX` is allowed only for codepoints < U+0020 or U+007F–U+009F — U+00A0/U+20AC must be raw UTF-8, and U+D83D is not a Unicode scalar value at all.
**(d)** Expected: M8 rejects non-canonical spellings. Actual: M8 passes spellings the spec forbids, so a non-canonical string literal in a spec example would go undetected.
**(e)** Root cause: the checker only excludes short-escape chars and printable ASCII from `\uXXXX`; it never enforces the spec's allowed codepoint ranges.
**(f)** Proposed correction: reject `\uXXXX` for codepoints outside (< U+0020, U+007F–U+009F); reject surrogate codepoints outright.
**(g)** Regression: `"\u00a0"` and `"\ud83d"` must fail with category `canonical`.
**(h)** Does NOT establish: the spec's escape policy itself, which I verified is deterministic as written (my attempts to find two spec-legal spellings for one string failed).

### NEW-B3 — Canonical type-name grammar contradicts itself (D-027)

**(b)** Source: §G.2, "Canonical type names `<t>`".
**(c)** The productions show `impl(` t ` -> ` t `)` and `(` t (`,` t)* `) -> ` t — containing literal spaces — followed immediately by "**No whitespace** inside type names". `impl(nat -> nat)` both matches the production and violates the no-whitespace rule.
**(d)** Expected: one exact grammar. Actual: two inconsistent statements.
**(e)** Root cause: productions written with readability spacing; the constraint added without reconciling.
**(f)** Proposed correction: pick one — either strip all spaces from the productions (`impl(nat->nat)`, `(nat,nat)->nat`) or state the exact spacing rule normatively.
**(g)** Regression: canonical type-name test vectors, e.g. `impl(nat->nat)` accepted, `impl(nat -> nat)` rejected (or vice versa, per the chosen rule).
**(h)** Does NOT establish: M8 enforces nothing here at all (see NEW-B4) — the spec text is the only artifact affected.

### NEW-B4 — M8 validates envelope field order but not type names or value formats (D-027)

**(b)** Source: `m8/canonical.py::check_envelope`.
**(c)** `check_envelope({"$type":"list","of":"frob","items":[]})`, `"of":"Nat"`, `"of":"nat "`, and `"sig":"(nat)->nat"` are all **accepted** — `of`/`sig` are unchecked strings, and value spellings (nat leading zeros, f64 form, rat form) inside envelopes are never validated.
**(d)** Expected: the "exact" canonical profile is mechanically checked. Actual: only field order and `$type` names are checked; the value-level exactness M8 claims is limited to spec-source literals.
**(e)** Root cause: envelope check implemented as field-order only; no recursion into values or type-name grammar.
**(f)** Proposed correction: validate `of`/`sig` against the (fixed, per NEW-B3) type-name grammar and recurse `check_*` validators into envelope values; document the residual scope in M8's limitations.
**(g)** Regression: envelope corpus with malformed `of`/`sig` and non-canonical `value` strings, all expecting `canonical` failures.
**(h)** Does NOT establish: the spec's envelope rules themselves, which are correct as far as field order/omission go (A3).

### NEW-B5 — NaN has no defined equality/ordering semantics (§B.4 rule 3 vs §B.4b)

**(b)** Source: §B.4 rule 3 ("`Binary64`: equality of canonical forms") combined with §B.4b (NaN producible via `0.0/0.0`).
**(c)** `let x = 0.0/0.0 in x == x` — NaN has no canonical form, so "equality of canonical forms" is undefined for it. Likewise `x < 1.0`, `x != x`. Any constraint over Binary64 can reach this state.
**(d)** Expected: total defined semantics for all operators on all producible values. Actual: a hole exactly where D-032 introduced NaN into the value domain.
**(e)** Root cause: D-032 specified arithmetic *outcomes* producing NaN but not *predicate* outcomes on NaN.
**(f)** Proposed correction: define explicitly (IEEE-style: all comparisons false except `!=`, which is true; or designate NaN comparison an execution error). Note `is_finite` exists so authors can guard, but the operators' semantics must still be total.
**(g)** Regression: `0.0/0.0 == 0.0/0.0`, `0.0/0.0 < 1.0`, `0.0/0.0 != 0.0/0.0` with specified outcomes.
**(h)** Does NOT establish: non-NaN equality/ordering, which is well-defined.

### NEW-B6 — Real/Rat division by zero is undefined (§B.4 rule 2)

**(b)** Source: §B.4 rule 2: "`Real`/`Rat` division is exact rational division" (no zero case), contrasted with the immediately preceding sentence giving Nat/Int division-by-zero an explicit execution error.
**(c)** `(1/3 : Rat) / (0/1 : Rat)` — exact rational division by zero is mathematically undefined; the spec assigns no outcome.
**(d)** Expected: every operator total over its domain or mapped to a named execution error. Actual: silent gap.
**(e)** Root cause: incomplete case analysis when the division rules were written.
**(f)** Proposed correction: execution error (`division-by-zero`), mirroring Nat/Int.
**(g)** Regression: `1/3 / 0/1` → specified execution error, not a type error and not an unspecified result.
**(h)** Does NOT establish: anything about Binary64 division, which is fully specified.

### NEW-B7 — `output_packaging` and `execution` status are not jointly constrained (D-030)

**(b)** Source: §E.1 (`output_packaging` field) + §E.7 invariants 10/15/16 + §G.2 packaging-failure paragraph.
**(c)** No invariant relates the two fields: `execution = COMPLETED ∧ output_packaging = PACKAGING_FAILED(_)`, `execution = INTERNAL_ERROR(output-not-encodable:…) ∧ output_packaging = PACKAGING_OK`, and `execution = INTERNAL_ERROR(…) ∧ output_packaging = PACKAGING_FAILED(_)` are all permitted. §G.2 describes the event as "`execution: INTERNAL_ERROR`" while §E.7 inv. 15 describes it as "`PACKAGING_FAILED(output-not-encodable)`" — two encodings of one event with no rule choosing between them. Additionally, `is_packaging_error` ("covers exactly {output-not-encodable, canonicalization-failure}") does not state whether the `": <detail>"` suffix convention defined in §B.9 for the other three closed types applies (inv. 10's "reason starts with `output-not-encodable`" implies it does, but the predicate definition doesn't say so).
**(d)** Expected: one event, one constrained joint representation. Actual: an unconstrained 2-field state space plus an ambiguous suffix rule.
**(e)** Root cause: D-030 added the `output_packaging` field without retiring or reconciling §G.2's older `INTERNAL_ERROR` wording.
**(f)** Proposed correction: add an invariant (e.g. `output_packaging = PACKAGING_FAILED(r)` ⇔ `execution = INTERNAL_ERROR` with reason extending `r`, or designate one field authoritative); state the detail-suffix rule for `is_packaging_error` explicitly.
**(g)** Regression: a joint-state test — `PACKAGING_FAILED` with `execution = COMPLETED` must either be accepted with a stated meaning or rejected by invariant.
**(h)** Does NOT establish: the core D-030 mechanism (Option<Hash>, preserved semantic_result, never-INVALID_INPUT), which is sound (A4).

## C. Limitations of this audit

- I verified the *spelling-level* uniqueness of the canonical profile, not the injectivity of the full typed encoding (nested records/sets/options) — the structural-induction argument in §G.2 is paper, not machine-checked.
- M8's `canonical_f64` producer was exercised only through the 2,000-value round-trip in the suite I ran plus my 2,998-value sweep — bounded evidence, not a proof.
- I did not audit the M8 parser/typechecker itself beyond `canonical.py`; grammar-conformance claims are outside Sub-agent B's remit.
- All findings are specification/tool-level; no implementation exists, so no conformance claims are made.

**Net assessment:** the v0.8 canonical profile's uniqueness claims hold up under direct collision attack, and the D-030 packaging redesign is coherent. But §B.4b contains a provably false sentence (underflow), M8's canonical checking is weaker than the spec it enforces (NEW-B2, NEW-B4), and NaN's introduction into the value domain was not carried through to predicates (NEW-B5) — the same "next unchecked layer" pattern as previous rounds.