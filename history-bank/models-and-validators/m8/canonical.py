"""M8 canonical-profile checks (msve-canonical-3, v0.8).

Validates the deterministic byte-level rules that the §G canonical profile
requires, beyond what the lexer accepts:

- D-026: binary64 exponent uniqueness — exactly "+0" or sign+nonzero digits;
  no "-0"; Sig="1" requires -1022 <= Exp <= 1023; subnormal form requires
  Exp == -1074; zero is exactly 0x0.0000000000000p+0.
- D-027: JSON string escape determinism — short escapes preferred over
  \\uXXXX; \\uXXXX uses lowercase hex, exactly 4 digits; no unnecessary
  escapes of printable ASCII.
- D-027: rational text grammar — "-"? Nat "/" Nat, denominator > 0,
  lowest terms (gcd == 1).
- D-027: canonical envelope — {"$type": name, ...} with exact field order
  and type-name spellings.

Error category: 'canonical'.
"""
import re, math

class CanonicalError(Exception):
    def __init__(self, msg, where=""):
        super().__init__(f"canonical error{(' at ' + where) if where else ''}: {msg}")
        self.category = "canonical"

_F64 = re.compile(r"^(-?)0x([01])\.([0-9a-fA-F]{13})p(\+0|\+[1-9][0-9]*|-[1-9][0-9]*)$")

def check_f64_canonical(raw, where=""):
    """Validate a hexfloat spelling against msve-canonical-3 §G.2."""
    m = _F64.match(raw)
    if not m:
        if re.match(r"^(-?)0x[01]\.[0-9a-fA-F]{13}p-0$", raw):
            raise CanonicalError("exponent '-0' is not canonical; use '+0' (D-026)", where)
        raise CanonicalError(f"not a canonical binary64 form: {raw!r}", where)
    neg, sig, frac, exp_s = m.group(1) == "-", m.group(2), m.group(3), m.group(4)
    exp = int(exp_s)
    if frac != frac.lower():
        raise CanonicalError("fraction hex digits must be lowercase", where)
    if sig == "0":
        if frac == "0" * 13:
            if raw != "0x0.0000000000000p+0":
                raise CanonicalError("zero must be exactly 0x0.0000000000000p+0", where)
            return 0.0
        if exp != -1074:
            raise CanonicalError(f"subnormal exponent must be exactly -1074, got {exp}", where)
        return ((-1) ** neg) * int(frac, 16) * 2.0 ** -1074
    if not (-1022 <= exp <= 1023):
        raise CanonicalError(f"normal exponent {exp} outside [-1022, 1023]", where)
    return ((-1) ** neg) * (1 + int(frac, 16) / 16 ** 13) * 2.0 ** exp

def canonical_f64(value):
    """Produce the canonical-3 spelling for a finite float."""
    import struct
    bits = struct.unpack("<Q", struct.pack("<d", value))[0]
    sign = "-" if bits >> 63 else ""
    exp = (bits >> 52) & 0x7FF
    mant = bits & ((1 << 52) - 1)
    if exp == 0 and mant == 0:
        return "0x0.0000000000000p+0"
    if exp == 0:
        return f"{sign}0x0.{mant:013x}p-1074"
    e = exp - 1023
    return f"{sign}0x1.{mant:013x}p+{e}" if e >= 0 else f"{sign}0x1.{mant:013x}p{e}"

_SHORT = {'"': '\\"', "\\": "\\\\", "\b": "\\b", "\f": "\\f",
          "\n": "\\n", "\r": "\\r", "\t": "\\t"}

def check_string_canonical(raw, where=""):
    """Validate the raw spelling of a string literal against the D-027
    deterministic escape policy (NEW-B2: codepoint ranges enforced)."""
    if not (raw.startswith('"') and raw.endswith('"') and len(raw) >= 2):
        raise CanonicalError("not a string literal", where)
    body = raw[1:-1]
    i = 0
    while i < len(body):
        c = body[i]
        if c != "\\":
            cp = ord(c)
            if 0xD800 <= cp <= 0xDFFF:
                raise CanonicalError(
                    f"lone surrogate U+{cp:04X} is not a Unicode scalar value",
                    where)
            if cp < 0x20 or 0x7F <= cp <= 0x9F:
                raise CanonicalError(
                    f"U+{cp:04X} must be escaped", where)
            i += 1
            continue
        e = body[i + 1] if i + 1 < len(body) else ""
        if e in '"\\/bfnrt':
            # short escape present: check it is the preferred one
            decoded = {"\"": '"', "\\": "\\", "/": "/",
                       "b": "\b", "f": "\f", "n": "\n",
                       "r": "\r", "t": "\t"}[e]
            if decoded in _SHORT and "\\" + e != _SHORT[decoded]:
                raise CanonicalError(
                    f"escape '\\{e}' is not the canonical short form", where)
            i += 2
        elif e == "u":
            hexpart = body[i + 2:i + 6]
            if len(hexpart) != 4 or not re.fullmatch(r"[0-9a-f]{4}", hexpart):
                raise CanonicalError(
                    "\\u escape must use exactly 4 lowercase hex digits", where)
            cp = int(hexpart, 16)
            ch = chr(cp)
            if ch in _SHORT:
                raise CanonicalError(
                    f"U+{cp:04X} must use the short escape {_SHORT[ch]!r}, not \\u{hexpart}", where)
            if 0x20 <= cp <= 0x7E and ch not in ('"', "\\"):
                raise CanonicalError(
                    f"printable ASCII U+{cp:04X} must not be escaped", where)
            if 0xD800 <= cp <= 0xDFFF:
                raise CanonicalError(
                    f"surrogate U+{cp:04X} is not a Unicode scalar value",
                    where)
            # NEW-B2: \uXXXX allowed ONLY for < U+0020 or U+007F-U+009F
            if not (cp < 0x20 or 0x7F <= cp <= 0x9F):
                raise CanonicalError(
                    f"U+{cp:04X} must be raw UTF-8, not \\u{hexpart}", where)
            i += 6
        else:
            raise CanonicalError(f"invalid escape '\\{e}'", where)
    return True

_RAT = re.compile(r"^(-?)([0-9]+)/([0-9]+)$")

def check_rational_canonical(raw, where=""):
    """Validate rational text: -? Nat / Nat, denominator > 0, lowest terms."""
    m = _RAT.match(raw)
    if not m:
        raise CanonicalError(f"not a canonical rational form: {raw!r}", where)
    neg, num_s, den_s = m.groups()
    if len(num_s) > 1 and num_s.startswith("0"):
        raise CanonicalError("numerator must not have leading zeros", where)
    if len(den_s) > 1 and den_s.startswith("0"):
        raise CanonicalError("denominator must not have leading zeros", where)
    num, den = int(num_s), int(den_s)
    if den == 0:
        raise CanonicalError("denominator must be positive", where)
    if num == 0 and neg:
        raise CanonicalError("zero must not carry a sign", where)
    if math.gcd(num, den) != 1:
        raise CanonicalError(f"{num}/{den} is not in lowest terms", where)
    return (-num if neg else num, den)

_NAT = re.compile(r"^(0|[1-9][0-9]*)$")
_INT = re.compile(r"^(-)?(0|[1-9][0-9]*)$")
_HASH = re.compile(r"^[0-9a-f]{64}$")

def check_nat_canonical(raw, where=""):
    if not _NAT.match(raw):
        raise CanonicalError(f"not a canonical nat: {raw!r}", where)
    return True

def check_int_canonical(raw, where=""):
    m = _INT.match(raw)
    if not m or (m.group(1) and m.group(2) == "0"):
        raise CanonicalError(f"not a canonical int: {raw!r}", where)
    return True

def check_hash_canonical(raw, where=""):
    if not _HASH.match(raw):
        raise CanonicalError(f"not a canonical hash: {raw!r}", where)
    return True

def check_bool_canonical(raw, where=""):
    if raw not in ("true", "false"):
        raise CanonicalError(f"not a canonical bool: {raw!r}", where)
    return True

# Canonical type-name grammar (D-027, NEW-B3): no whitespace anywhere.
_TYPENAME_BASE = {"nat", "int", "real", "rat", "f64", "bool", "string", "hash"}
_FIELDNAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def check_typename(s, where=""):
    """Validate a canonical type name against the §G.2 grammar."""
    pos = [0]
    def peek():
        return s[pos[0]] if pos[0] < len(s) else ""
    def expect(c):
        if peek() != c:
            raise CanonicalError(
                f"bad type name {s!r}: expected {c!r} at {pos[0]}", where)
        pos[0] += 1
    def parse_t():
        for base in _TYPENAME_BASE:
            if s.startswith(base, pos[0]):
                pos[0] += len(base)
                return
        if s.startswith("list<", pos[0]) or s.startswith("set<", pos[0]) \
                or s.startswith("option<", pos[0]):
            pos[0] += 5 if s[pos[0]] == 'l' else (4 if s[pos[0]] == 's' else 7)
            parse_t()
            expect(">")
            return
        if s.startswith("record{", pos[0]):
            pos[0] += 7
            parse_field()
            while peek() == ",":
                pos[0] += 1
                parse_field()
            expect("}")
            return
        if s.startswith("impl(", pos[0]):
            pos[0] += 5
            parse_t()
            expect("-"); expect(">")
            parse_t()
            expect(")")
            return
        if peek() == "(":
            pos[0] += 1
            parse_t()
            while peek() == ",":
                pos[0] += 1
                parse_t()
            expect(")")
            expect("-"); expect(">")
            parse_t()
            return
        raise CanonicalError(
            f"bad type name {s!r} at position {pos[0]}", where)
    def parse_field():
        m = _FIELDNAME.match(s, pos[0])
        if not m:
            raise CanonicalError(
                f"bad field name in type name {s!r} at {pos[0]}", where)
        pos[0] = m.end()
        expect(":")
        parse_t()
    parse_t()
    if pos[0] != len(s):
        raise CanonicalError(
            f"trailing characters in type name {s!r}", where)
    return True

# Canonical envelope: {"$type": name, ...} — exact field order per §G.2.
# ("option" with some=false omits "value"; handled in check_envelope.)
_ENVELOPE_FIELDS = {
    "string": ["$type", "value"],
    "nat": ["$type", "value"],
    "int": ["$type", "value"],
    "real": ["$type", "value"],
    "rat": ["$type", "value"],
    "f64": ["$type", "value"],
    "bool": ["$type", "value"],
    "list": ["$type", "of", "items"],
    "set": ["$type", "of", "items"],
    "option": ["$type", "of", "some", "value"],
    "record": ["$type", "fields"],
    "impl": ["$type", "sig", "value"],
    "hash": ["$type", "value"],
    "blob": ["$type", "sha256", "bytes"],
}

def check_envelope(obj, where=""):
    """Validate a canonical envelope dict: exact $type tag, exact field
    order, known type names."""
    if not isinstance(obj, dict):
        raise CanonicalError("envelope must be a JSON object", where)
    keys = list(obj.keys())
    if not keys or keys[0] != "$type":
        raise CanonicalError("$type must be the first field", where)
    tname = obj["$type"]
    if tname not in _ENVELOPE_FIELDS:
        raise CanonicalError(f"unknown canonical type name {tname!r}", where)
    want = _ENVELOPE_FIELDS[tname]
    if tname == "option" and obj.get("some") is False:
        want = ["$type", "of", "some"]
    if keys != want:
        raise CanonicalError(
            f"type {tname!r}: fields must be exactly {want}, got {keys}",
            where)
    # NEW-B4: validate type-name fields and recurse into values.
    if "of" in obj:
        check_typename(obj["of"], where + " of")
    if "sig" in obj:
        check_typename(obj["sig"], where + " sig")
    if "value" in obj:
        v = obj["value"]
        sub = where + " value"
        if tname in ("real", "rat"):
            check_rational_canonical(v, sub)
        elif tname == "f64":
            check_f64_canonical(v, sub)
        elif tname == "nat":
            check_nat_canonical(v, sub)
        elif tname == "int":
            check_int_canonical(v, sub)
        elif tname == "bool":
            check_bool_canonical(v, sub)
        elif tname == "hash":
            check_hash_canonical(v, sub)
        elif tname == "string":
            check_string_canonical(v, sub)
        elif tname == "option":
            if not isinstance(obj.get("some"), bool):
                raise CanonicalError("'some' must be a bool", sub)
            if obj["some"]:
                check_envelope(v, sub)
        elif tname == "impl":
            if not isinstance(v, str):
                raise CanonicalError("impl value must be a string", sub)
    if "items" in obj:
        if not isinstance(obj["items"], list):
            raise CanonicalError("'items' must be a list", where)
        for i, item in enumerate(obj["items"]):
            check_envelope(item, f"{where} items[{i}]")
    if "fields" in obj:
        if not isinstance(obj["fields"], dict):
            raise CanonicalError("'fields' must be an object", where)
        for fname, fval in obj["fields"].items():
            check_envelope(fval, f"{where} fields.{fname}")
    return True

def check_canonical_tree(spec):
    """Walk the AST; validate every HexFloat and String literal's raw
    spelling against the canonical profile. Returns [CanonicalError]."""
    errors = []
    def visit(node):
        if isinstance(node, dict):
            for v in node.values():
                visit(v)
            return
        if isinstance(node, (list, tuple)):
            for v in node:
                visit(v)
            return
        kind = getattr(node, "kind", None)
        if kind is None:
            return
        if kind == "Literal":
            lit = node.fields.get("lit")
            raw = node.fields.get("raw", "")
            where = f"{node.line}:{node.col}"
            try:
                if lit == "HEXFLOAT":
                    check_f64_canonical(raw, where)
                elif lit == "STRING":
                    check_string_canonical(raw, where)
            except CanonicalError as e:
                errors.append(e)
        for v in node.fields.values():
            visit(v)
    visit(spec)
    return errors
