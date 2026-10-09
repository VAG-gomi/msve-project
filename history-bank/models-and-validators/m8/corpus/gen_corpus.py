#!/usr/bin/env python3
"""Generate the M8 regression corpus files (deterministic).

Each entry: (filename, definitions_block, verification_block, expect, category)
The generated .msve files are the stable corpus artifacts; this script
documents how they were produced.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = HERE

TEMPLATE = """spec {name}
version 0.8.0
scope m8-corpus
authors ["m8"]
{definitions}goal derive 1
verification {{
{verification}}}
limits {{ timeout: 10s; }}
record: all
"""

DEFAULT_VERIF = "  proof: none;\n"

CASES = [
    # --- D-025: record construction ---
    ("record-ok",
     'type Pair = { x: Nat, y: Nat }\n'
     'define p : Pair = { x: 1, y: 2 }\n',
     DEFAULT_VERIF, "pass", None),
    ("record-nested",
     'type Inner = { a: Bool }\n'
     'type Outer = { inner: Inner, n: Nat }\n'
     'define o : Outer = { inner: { a: true }, n: 3 }\n',
     DEFAULT_VERIF, "pass", None),
    ("record-dup-field",
     'type Pair = { x: Nat, y: Nat }\n'
     'define p : Pair = { x: 1, x: 2 }\n',
     DEFAULT_VERIF, "fail", "type"),
    ("record-unknown-field",
     'type Pair = { x: Nat, y: Nat }\n'
     'define p : Pair = { x: 1, y: 2, z: 3 }\n',
     DEFAULT_VERIF, "fail", "type"),
    ("record-missing-field",
     'type Pair = { x: Nat, y: Nat }\n'
     'define p : Pair = { x: 1 }\n',
     DEFAULT_VERIF, "fail", "type"),
    ("record-field-type-mismatch",
     'type Pair = { x: Nat, y: Nat }\n'
     'define p : Pair = { x: 1, y: true }\n',
     DEFAULT_VERIF, "fail", "type"),
    ("record-infer",
     'define p = { x: 1, y: true }\n',
     DEFAULT_VERIF, "fail", "syntax"),  # define requires ": TypeExpr"
    # --- quantifier parens (D-005 area) ---
    ("quant-parens-ok",
     'define p : Bool = forall x in type Nat :: (x >= 0)\n',
     DEFAULT_VERIF, "pass", None),
    ("quant-nested-ok",
     'define p : Bool = forall x in type Nat :: ((forall y in type Nat :: (x <= x + y)))\n',
     DEFAULT_VERIF, "pass", None),
    ("bare-quantifier",
     'define p : Bool = forall x in type Nat :: x >= 0\n',
     DEFAULT_VERIF, "fail", "syntax"),
    # --- arithmetic typing (D-007/D-008) ---
    ("arith-neg3-plus2",
     'define v : Int = -3 + 2\n',
     DEFAULT_VERIF, "pass", None),
    ("arith-mixed-real-nat",
     'define v : Real = 1.5 + 2\n',
     DEFAULT_VERIF, "fail", "type"),
    ("arith-nat-int-embed",
     'define v : Int = 5 + -3\n',
     DEFAULT_VERIF, "pass", None),
    ("arith-unary-minus-nat",
     'define v : Int = -5\n',
     DEFAULT_VERIF, "pass", None),
    ("arith-div-int-exact",
     'define v : Nat = 6 / 3\n',
     DEFAULT_VERIF, "pass", None),
    # --- identifiers / builtins (D-016) ---
    ("is_some-ok",
     'define b : Bool = is_some(some(1))\n',
     DEFAULT_VERIF, "pass", None),
    ("unbound-ident",
     'define b : Bool = frobnicate(1)\n',
     DEFAULT_VERIF, "fail", "name-resolution"),
    ("to_rat-ok",
     'define r : Rat = to_rat(1.5)\n',
     DEFAULT_VERIF, "pass", None),
    ("range-ok",
     'define xs : [Nat] = range(3)\n',
     DEFAULT_VERIF, "pass", None),
    # --- canonical forms (D-026/D-027) ---
    ("f64-valid",
     'define v : Binary64 = 0x1.0000000000000p+0\n',
     DEFAULT_VERIF, "pass", None),
    ("f64-neg-zero-exp",
     'define v : Binary64 = 0x1.0000000000000p-0\n',
     DEFAULT_VERIF, "fail", "lexical"),
    ("f64-upper-hex",
     'define v : Binary64 = 0x1.000000000000Ap+0\n',
     DEFAULT_VERIF, "fail", "lexical"),
    ("f64-normal-form-subnormal",
     'define v : Binary64 = 0x1.0000000000000p-1074\n',
     DEFAULT_VERIF, "fail", "canonical"),
    ("string-escape-upper",
     'define s : String = "\\u001A"\n',
     DEFAULT_VERIF, "fail", "canonical"),
    ("string-escape-not-short",
     'define s : String = "\\u000a"\n',
     DEFAULT_VERIF, "fail", "canonical"),
    ("string-ok",
     'define s : String = "a\\nB"\n',
     DEFAULT_VERIF, "pass", None),
    # --- options / case (totality) ---
    ("case-ok",
     'define f : Nat = case some(1) of some(x) -> x + 1 | none -> 0\n',
     DEFAULT_VERIF, "pass", None),
    ("let-ok",
     'define v : Nat = let x = 2 in x * 3\n',
     DEFAULT_VERIF, "pass", None),
    # --- D-031: verification items ---
    ("verif-diff-plus-fuzz",
     '',
     '  proof: none;\n'
     '  test: differential by indie-fuzz/1.0.0 required;\n'
     '  test: property-fuzz { seeds: [1], cases: 10 } required;\n',
     "pass", None),
    ("verif-duplicate-test",
     '',
     '  proof: none;\n'
     '  test: differential by indie-fuzz/1.0.0 required;\n'
     '  test: differential by indie-fuzz/1.0.0 required;\n',
     "fail", "admission"),
    ("verif-proof-conflict",
     '',
     '  proof: none;\n'
     '  proof: kernel-checked by lean-kernel/4.9.0 required;\n',
     "fail", "admission"),
    ("verif-recompute-conflict",
     '',
     '  recompute: none;\n'
     '  recompute: by recompute-checker/1.0.0 required;\n',
     "fail", "admission"),
    ("verif-test-none-conflict",
     '',
     '  proof: none;\n'
     '  test: none;\n'
     '  test: differential by indie-fuzz/1.0.0 required;\n',
     "fail", "admission"),
    ("verif-qualifier-default",
     '',
     '  proof: kernel-checked by lean-kernel/4.9.0;\n',
     "pass", None),
    ("verif-cases-zero",
     '',
     '  proof: none;\n'
     '  test: property-fuzz { seeds: [1], cases: 0 } required;\n',
     "fail", "admission"),
    ("verif-assurance-level-a-needs-proof",
     '',
     '  proof: none;\n'
     '  assurance: level-a required;\n',
     "pass", None),  # goal is derive; derive allows recompute OR proof... neither present -> fail?
]

def main():
    # fix: derive goal with assurance level-a and no proof/recompute must FAIL admission
    cases = []
    for name, defs, verif, expect, cat in CASES:
        if name == "verif-assurance-level-a-needs-proof":
            expect, cat = "fail", "admission"
        cases.append((name, defs, verif, expect, cat))
    manifest = []
    for name, defs, verif, expect, cat in cases:
        src = TEMPLATE.format(name=name.replace("-", "_"), definitions=defs,
                              verification=verif)
        path = os.path.join(CORPUS, name + ".msve")
        with open(path, "w") as f:
            f.write(src)
        entry = {"file": name + ".msve", "expect": expect}
        if cat:
            entry["category"] = cat
        manifest.append(entry)
    with open(os.path.join(CORPUS, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"wrote {len(cases)} corpus files + manifest")

if __name__ == "__main__":
    main()
