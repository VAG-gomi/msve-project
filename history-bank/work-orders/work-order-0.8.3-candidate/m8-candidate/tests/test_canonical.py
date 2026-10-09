"""Unit tests for m8/canonical.py (D-026, D-027 regression)."""
from m8.canonical import (check_f64_canonical, canonical_f64,
                          check_string_canonical, check_rational_canonical,
                          check_envelope, check_typename, CanonicalError)

def expect_ok(fn, *args):
    fn(*args)

def expect_fail(fn, *args):
    try:
        fn(*args)
    except CanonicalError:
        return
    raise AssertionError(f"expected CanonicalError for {args}")

def run():
    # D-026: exponent uniqueness
    expect_ok(check_f64_canonical, "0x1.0000000000000p+0")
    expect_ok(check_f64_canonical, "0x1.0000000000000p+1")
    expect_ok(check_f64_canonical, "0x1.0000000000000p-1")
    expect_ok(check_f64_canonical, "0x0.0000000000001p-1074")
    expect_ok(check_f64_canonical, "0x0.0000000000000p+0")
    expect_fail(check_f64_canonical, "0x1.0000000000000p-0")   # the v0.7 survivor
    expect_fail(check_f64_canonical, "0x2.0000000000000p+0")   # bad leading digit
    expect_fail(check_f64_canonical, "0x1.0000000000000p+01")  # leading-zero exp
    expect_fail(check_f64_canonical, "0x1.0000000000000p-1074")  # normal-form subnormal
    expect_fail(check_f64_canonical, "0x1.000000000000AP+0")   # upper hex
    expect_fail(check_f64_canonical, "0x0.0000000000001p-1022")  # subnormal wrong exp
    # canonical_f64 round-trips through the validator
    import struct, random
    random.seed(7)
    for _ in range(2000):
        bits = random.getrandbits(64)
        f = struct.unpack("<d", struct.pack("<Q", bits))[0]
        if f != f or f in (float("inf"), float("-inf")):
            continue
        c = canonical_f64(f)
        back = check_f64_canonical(c)
        bf = struct.unpack("<Q", struct.pack("<d", back))[0]
        want = struct.unpack("<Q", struct.pack("<d", 0.0 if f == 0.0 else f))[0]
        assert bf == want, (f, c)
    # D-027: string escapes
    expect_ok(check_string_canonical, r'"a\nB"')
    expect_ok(check_string_canonical, r'"\u001a"')
    expect_fail(check_string_canonical, r'"\u001A"')   # must be lowercase
    expect_fail(check_string_canonical, r'"\u000a"')   # must use \n
    expect_fail(check_string_canonical, r'"\u0041"')  # printable ASCII must not be escaped
    # D-027: rationals
    assert check_rational_canonical("7/3") == (7, 3)
    assert check_rational_canonical("-7/3") == (-7, 3)
    expect_fail(check_rational_canonical, "6/4")    # not lowest terms
    expect_fail(check_rational_canonical, "1/0")    # zero denominator
    expect_fail(check_rational_canonical, "-0/5")   # signed zero
    expect_fail(check_rational_canonical, "07/3")   # leading zeros
    # D-027: envelope
    expect_ok(check_envelope, {"$type": "nat", "value": "1"})
    expect_ok(check_envelope, {"$type": "f64", "value": "0x1.0000000000000p+0"})
    expect_ok(check_envelope, {"$type": "list", "of": "nat", "items": []})
    expect_ok(check_envelope, {"$type": "option", "of": "nat", "some": False})
    expect_ok(check_envelope, {"$type": "option", "of": "nat", "some": True, "value": {"$type": "nat", "value": "1"}})
    expect_ok(check_envelope, {"$type": "impl", "sig": "(nat)->nat", "value": "ext/1.0.0"})
    expect_fail(check_envelope, {"$type": "nat", "value": "1", "extra": 0})
    expect_fail(check_envelope, {"value": "1", "$type": "nat"})  # order
    expect_fail(check_envelope, {"$type": "frob"})
    expect_fail(check_envelope, {"$type": "binary64", "value": "0x1.0000000000000p+0"})  # tag is f64
    expect_fail(check_envelope, {"$type": "list", "items": []})  # missing "of"
    # NEW-B2: string escape codepoint ranges
    expect_fail(check_string_canonical, r'"\u00a0"')  # must be raw UTF-8
    expect_fail(check_string_canonical, r'"\ud83d"')  # lone surrogate
    expect_ok(check_string_canonical, r'"\u001f"')
    expect_ok(check_string_canonical, r'"\u0085"')
    # NEW-B3/B4: type-name grammar + envelope value checking
    expect_ok(check_typename, "impl(nat->nat)")
    expect_fail(check_typename, "impl(nat -> nat)")
    expect_ok(check_typename, "record{a:nat,b:list<f64>}")
    expect_fail(check_typename, "list<nat> ")
    expect_fail(check_envelope, {"$type": "list", "of": "frob", "items": []})
    expect_fail(check_envelope, {"$type": "list", "of": "Nat", "items": []})
    expect_fail(check_envelope, {"$type": "nat", "value": "007"})
    expect_fail(check_envelope, {"$type": "f64", "value": "0x1.0000000000000p-0"})
    expect_ok(check_envelope, {"$type": "list", "of": "nat",
                               "items": [{"$type": "nat", "value": "3"}]})
    expect_fail(check_envelope, {"$type": "option", "of": "nat", "some": True,
                                  "value": {"$type": "nat", "value": "01"}})
    # F-12: empty record and zero-arg function type names are legal
    expect_ok(check_typename, "record{}")
    expect_ok(check_typename, "()->nat")
    expect_ok(check_typename, "record{a:()->bool}")
    expect_fail(check_typename, "record{")
    expect_fail(check_typename, "()->")
    # F-14: string escape policy — raw UTF-8 for other scalar values,
    # surrogates forbidden, lowercase hex, short-escape preference
    expect_fail(check_string_canonical, '"\\u20ac"')  # printable non-ASCII must be raw
    expect_fail(check_string_canonical, '"\\u001A"')  # uppercase hex
    expect_fail(check_string_canonical, '"\\u000a"')  # short escape exists
    expect_fail(check_string_canonical, '"\\ud800"')  # surrogate
    expect_ok(check_string_canonical, '"caf\u00e9"')  # raw UTF-8 non-ASCII ok
    expect_ok(check_string_canonical, '"\\u0000"')
    expect_ok(check_string_canonical, '"a\\nb"')
    # F-15: blob digests are lowercase hex, like Hash
    expect_ok(check_envelope, {"$type": "blob", "sha256": "a" * 64, "bytes": "3"})
    expect_fail(check_envelope, {"$type": "blob", "sha256": "A" * 64, "bytes": "3"})
    expect_fail(check_envelope, {"$type": "blob", "sha256": "a" * 63, "bytes": "3"})
    print("test_canonical: all assertions hold")

if __name__ == "__main__":
    run()
    print("PASS")
