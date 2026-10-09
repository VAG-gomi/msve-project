# Report C — M8 Corpus Cases (Part 7/7)

**Work Order:** 0.8.2 · **Evidence:** DIRECT ARTEFACT (case inputs from the ZIP) + RECORDED OUTPUT (verdicts from the 0.8.1 reproduction log).

46 cases. Verdict PASS means the case behaved as the manifest expected.

---



## Case 1/46: `record-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec record_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
type Pair = { x: Nat, y: Nat }
define p : Pair = { x: 1, y: 2 }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 2/46: `record-nested.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec record_nested
version 0.8.0
scope m8-corpus
authors ["m8"]
type Inner = { a: Bool }
type Outer = { inner: Inner, n: Nat }
define o : Outer = { inner: { a: true }, n: 3 }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 3/46: `record-dup-field.msve`

- Manifest expected: `fail` / category `type`
- Recorded verdict: `PASS` (match: True)

```
spec record_dup_field
version 0.8.0
scope m8-corpus
authors ["m8"]
type Pair = { x: Nat, y: Nat }
define p : Pair = { x: 1, x: 2 }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 4/46: `record-unknown-field.msve`

- Manifest expected: `fail` / category `type`
- Recorded verdict: `PASS` (match: True)

```
spec record_unknown_field
version 0.8.0
scope m8-corpus
authors ["m8"]
type Pair = { x: Nat, y: Nat }
define p : Pair = { x: 1, y: 2, z: 3 }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 5/46: `record-missing-field.msve`

- Manifest expected: `fail` / category `type`
- Recorded verdict: `PASS` (match: True)

```
spec record_missing_field
version 0.8.0
scope m8-corpus
authors ["m8"]
type Pair = { x: Nat, y: Nat }
define p : Pair = { x: 1 }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 6/46: `record-field-type-mismatch.msve`

- Manifest expected: `fail` / category `type`
- Recorded verdict: `PASS` (match: True)

```
spec record_field_type_mismatch
version 0.8.0
scope m8-corpus
authors ["m8"]
type Pair = { x: Nat, y: Nat }
define p : Pair = { x: 1, y: true }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 7/46: `record-infer.msve`

- Manifest expected: `fail` / category `syntax`
- Recorded verdict: `PASS` (match: True)

```
spec record_infer
version 0.8.0
scope m8-corpus
authors ["m8"]
define p = { x: 1, y: true }
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 8/46: `quant-parens-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec quant_parens_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define p : Bool = forall x in type Nat :: (x >= 0)
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 9/46: `quant-nested-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec quant_nested_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define p : Bool = forall x in type Nat :: ((forall y in type Nat :: (x <= x + y)))
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 10/46: `bare-quantifier.msve`

- Manifest expected: `fail` / category `syntax`
- Recorded verdict: `PASS` (match: True)

```
spec bare_quantifier
version 0.8.0
scope m8-corpus
authors ["m8"]
define p : Bool = forall x in type Nat :: x >= 0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 11/46: `arith-neg3-plus2.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec arith_neg3_plus2
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Int = -3 + 2
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 12/46: `arith-mixed-real-nat.msve`

- Manifest expected: `fail` / category `type`
- Recorded verdict: `PASS` (match: True)

```
spec arith_mixed_real_nat
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Real = 1.5 + 2
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 13/46: `arith-nat-int-embed.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec arith_nat_int_embed
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Int = 5 + -3
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 14/46: `arith-unary-minus-nat.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec arith_unary_minus_nat
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Int = -5
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 15/46: `arith-div-int-exact.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec arith_div_int_exact
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Nat = 6 / 3
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 16/46: `is_some-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec is_some_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define b : Bool = is_some(some(1))
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 17/46: `unbound-ident.msve`

- Manifest expected: `fail` / category `name-resolution`
- Recorded verdict: `PASS` (match: True)

```
spec unbound_ident
version 0.8.0
scope m8-corpus
authors ["m8"]
define b : Bool = frobnicate(1)
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 18/46: `to_rat-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec to_rat_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define r : Rat = to_rat(1.5)
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 19/46: `range-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec range_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define xs : [Nat] = range(3)
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 20/46: `f64-valid.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec f64_valid
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Binary64 = 0x1.0000000000000p+0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 21/46: `f64-neg-zero-exp.msve`

- Manifest expected: `fail` / category `lexical`
- Recorded verdict: `PASS` (match: True)

```
spec f64_neg_zero_exp
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Binary64 = 0x1.0000000000000p-0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 22/46: `f64-upper-hex.msve`

- Manifest expected: `fail` / category `lexical`
- Recorded verdict: `PASS` (match: True)

```
spec f64_upper_hex
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Binary64 = 0x1.000000000000Ap+0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 23/46: `f64-normal-form-subnormal.msve`

- Manifest expected: `fail` / category `canonical`
- Recorded verdict: `PASS` (match: True)

```
spec f64_normal_form_subnormal
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Binary64 = 0x1.0000000000000p-1074
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 24/46: `string-escape-upper.msve`

- Manifest expected: `fail` / category `canonical`
- Recorded verdict: `PASS` (match: True)

```
spec string_escape_upper
version 0.8.0
scope m8-corpus
authors ["m8"]
define s : String = "\u001A"
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 25/46: `string-escape-not-short.msve`

- Manifest expected: `fail` / category `canonical`
- Recorded verdict: `PASS` (match: True)

```
spec string_escape_not_short
version 0.8.0
scope m8-corpus
authors ["m8"]
define s : String = "\u000a"
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 26/46: `string-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec string_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define s : String = "a\nB"
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 27/46: `case-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec case_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define f : Nat = case some(1) of some(x) -> x + 1 | none -> 0
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 28/46: `let-ok.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec let_ok
version 0.8.0
scope m8-corpus
authors ["m8"]
define v : Nat = let x = 2 in x * 3
goal derive 1
verification {
  proof: none;
}
limits { timeout: 10s; }
record: all

```


## Case 29/46: `verif-diff-plus-fuzz.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec verif_diff_plus_fuzz
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  test: differential by indie-fuzz/1.0.0 required;
  test: property-fuzz { seeds: [1], cases: 10 } required;
}
limits { timeout: 10s; }
record: all

```


## Case 30/46: `verif-duplicate-test.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif_duplicate_test
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  test: differential by indie-fuzz/1.0.0 required;
  test: differential by indie-fuzz/1.0.0 required;
}
limits { timeout: 10s; }
record: all

```


## Case 31/46: `verif-proof-conflict.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif_proof_conflict
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  proof: kernel-checked by lean-kernel/4.9.0 required;
}
limits { timeout: 10s; }
record: all

```


## Case 32/46: `verif-recompute-conflict.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif_recompute_conflict
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  recompute: none;
  recompute: by recompute-checker/1.0.0 required;
}
limits { timeout: 10s; }
record: all

```


## Case 33/46: `verif-test-none-conflict.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif_test_none_conflict
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  test: none;
  test: differential by indie-fuzz/1.0.0 required;
}
limits { timeout: 10s; }
record: all

```


## Case 34/46: `verif-qualifier-default.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec verif_qualifier_default
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: kernel-checked by lean-kernel/4.9.0;
}
limits { timeout: 10s; }
record: all

```


## Case 35/46: `verif-cases-zero.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif_cases_zero
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  test: property-fuzz { seeds: [1], cases: 0 } required;
}
limits { timeout: 10s; }
record: all

```


## Case 36/46: `verif-assurance-level-a-needs-proof.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif_assurance_level_a_needs_proof
version 0.8.0
scope m8-corpus
authors ["m8"]
goal derive 1
verification {
  proof: none;
  assurance: level-a required;
}
limits { timeout: 10s; }
record: all

```


## Case 37/46: `limits-timeout-range.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec limits-timeout-range
version 0.8.0
scope exact-arithmetic
authors ["t"]
goal derive 1
verification { proof: none; }
limits { timeout: 9999h; }
record: all

```


## Case 38/46: `limits-steps-zero.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec limits-steps-zero
version 0.8.0
scope exact-arithmetic
authors ["t"]
goal derive 1
verification { proof: none; }
limits { timeout: 10s; steps: 0; }
record: all

```


## Case 39/46: `verif-assurance-level-a-unavailable.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec verif-assurance-level-a-unavailable
version 0.8.0
scope exact-arithmetic
authors ["t"]
type Pair = { x: Nat, y: Nat }
constraints positive {
  require px: output.x > 0;
  require py: output.y > 0;
}
goal construct Pair satisfying [positive]
verification { proof: none; assurance: level-a required; }
limits { timeout: 10s; }
record: all

```


## Case 40/46: `type-cyclic-alias.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec type-cyclic-alias
version 0.8.0
scope exact-arithmetic
authors ["t"]
type A = B
type B = A
goal derive 1
verification { proof: none; }
limits { timeout: 10s; }
record: all

```


## Case 41/46: `type-unbound-name.msve`

- Manifest expected: `fail` / category `name-resolution`
- Recorded verdict: `PASS` (match: True)

```
spec type-unbound-name
version 0.8.0
scope exact-arithmetic
authors ["t"]
define f(x: Ghost): Nat = 1
goal derive 1
verification { proof: none; }
limits { timeout: 10s; }
record: all

```


## Case 42/46: `define-shadow-builtin.msve`

- Manifest expected: `fail` / category `name-resolution`
- Recorded verdict: `PASS` (match: True)

```
spec define-shadow-builtin
version 0.8.0
scope exact-arithmetic
authors ["t"]
define len: Nat = 3
goal derive 1
verification { proof: none; }
limits { timeout: 10s; }
record: all

```


## Case 43/46: `f64-subtraction-no-spaces.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec f64-subtraction-no-spaces
version 0.8.0
scope exact-arithmetic
authors ["t"]
define v: Binary64 = 0x1.0000000000000p+0-0x1.0000000000000p+0
goal derive v
verification { proof: none; }
limits { timeout: 10s; }
record: all

```


## Case 44/46: `call-local-fn.msve`

- Manifest expected: `pass`
- Recorded verdict: `PASS` (match: True)

```
spec call-local-fn
version 0.8.0
scope exact-arithmetic
authors ["t"]
define inc(x: Nat): Nat = x + 1
define apply(f: (Nat) -> Nat, x: Nat): Nat = f(x)
goal derive apply(inc, 1)
verification { proof: none; }
limits { timeout: 10s; }
record: all

```


## Case 45/46: `quant-option-domain.msve`

- Manifest expected: `fail` / category `type`
- Recorded verdict: `PASS` (match: True)

```
spec quant-option-domain
version 0.8.0
scope exact-arithmetic
authors ["t"]
define o: Option<Nat> = some(1)
define p: Bool = forall x in o :: (x > 0)
goal derive 1
verification { proof: none; }
limits { timeout: 10s; }
record: all

```


## Case 46/46: `proj-path-unresolvable.msve`

- Manifest expected: `fail` / category `admission`
- Recorded verdict: `PASS` (match: True)

```
spec proj-path-unresolvable
version 0.8.0
scope exact-arithmetic
authors ["t"]
type M = { x: Nat }
projection bad = [output.zzz]
constraints c {
  require r1: output.x == 1;
}
goal compare-models M satisfying [c] under bad
verification { proof: none; }
limits { timeout: 10s; }
record: all

```
