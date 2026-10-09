#!/usr/bin/env python3
"""M6: challenge the canonical-3 binary64 uniqueness claim.
1. Attempt the v0.6 collision pairs under the new grammar (must reject/distinguish).
2. Round-trip random binary64 values through the canonical-3 rules."""
import re, struct, random, sys

def canonical(f):
    """canonical-3 f64 value string per §G.2. Returns None if not encodable."""
    import math
    if math.isnan(f):
        return None
    if math.isinf(f):
        return ("-" if f < 0 else "") + "inf-special"  # handled by tag rule
    bits = struct.unpack('<Q', struct.pack('<d', f))[0]
    sign = '-' if bits >> 63 else ''
    exp = (bits >> 52) & 0x7FF
    mant = bits & ((1 << 52) - 1)
    if exp == 0 and mant == 0:
        return "0x0.0000000000000p+0"  # -0.0 normalizes here
    if exp == 0:  # subnormal
        return f"{sign}0x0.{mant:013x}p-1074"
    e = exp - 1023
    es = f"+{e}" if e >= 0 else f"{e}"
    return f"{sign}0x1.{mant:013x}p{es}"

def parse_canonical(s):
    """Parse a canonical-3 finite form back to float. Raises on non-canonical."""
    m = re.fullmatch(r'(-?)0x([01])\.([0-9a-f]{13})p([+-]?(?:0|[1-9][0-9]*))', s)
    assert m, f"grammar reject: {s}"
    neg, sig, frac, exp = m.group(1) == '-', m.group(2), m.group(3), int(m.group(4))
    if sig == '0':
        assert frac != '0' * 13 or (s == "0x0.0000000000000p+0" and not neg), f"zero form: {s}"
        if frac == '0' * 13:
            return -0.0 if neg else 0.0
        assert exp == -1074, f"subnormal exp: {s}"
        return ((-1) ** neg) * int(frac, 16) * 2.0 ** -1074
    assert -1022 <= exp <= 1023, f"normal exp range: {s}"
    return ((-1) ** neg) * (1 + int(frac, 16) / 16 ** 13) * 2.0 ** exp

fails = []
# 1. v0.6 collision pairs must not both be accepted as canonical for the same value
for bad, good, val in [
    ("0x2.0000000000000p+0", "0x1.0000000000000p+1", 2.0),
    ("0x1.0000000000000p-1074", "0x0.0000000000001p-1074", 5e-324),
    ("0x1.0000000000000p+01", "0x1.0000000000000p+1", 2.0),
]:
    try:
        parse_canonical(bad)
        fails.append(f"collision form accepted: {bad}")
    except AssertionError:
        pass
    assert parse_canonical(good) == val, f"good form failed: {good}"
    assert canonical(val) == good, f"canonical({val}) = {canonical(val)}, want {good}"
print("collision pairs: old ambiguous forms rejected, unique forms accepted")

# 2. round-trip fuzz
random.seed(20261009)
tested = 0
for _ in range(20000):
    kind = random.random()
    if kind < 0.1:
        f = random.choice([0.0, -0.0, 5e-324, 2.2250738585072014e-308,
                           1.7976931348623157e308, float('inf'), float('-inf')])
    elif kind < 0.2:
        bits = random.getrandbits(64)
        f = struct.unpack('<d', struct.pack('<Q', bits))[0]
        if f != f:
            continue  # NaN: not encodable, skip (packaging failure by design)
    else:
        f = random.uniform(-1e300, 1e300)
    c = canonical(f)
    if c is None or c.endswith('inf-special'):
        continue
    back = parse_canonical(c)
    bf = struct.unpack('<Q', struct.pack('<d', back))[0]
    of = struct.unpack('<Q', struct.pack('<d', 0.0 if f == 0.0 else f))[0]
    # -0.0 normalizes to +0.0
    if f == 0.0:
        assert bf == struct.unpack('<Q', struct.pack('<d', 0.0))[0], f"zero: {c}"
    else:
        assert bf == of, f"round-trip mismatch: {f} -> {c} -> {back}"
    tested += 1
print(f"round-trip: {tested} values OK (incl. subnormals, ±0, extremes)")
print("M6: OK" if not fails else f"M6 FAILURES: {fails}")
sys.exit(1 if fails else 0)
