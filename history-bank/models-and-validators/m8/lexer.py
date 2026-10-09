"""M8 lexer for the MSVE formal language (v0.8).

Tokenises the surface language. Canonical-profile validation (escape
case, exponent uniqueness, rational reduction) is NOT done here — see
m8/canonical.py. The lexer accepts the general lexical shapes and records
raw spellings so later passes can diagnose precisely.
"""
import re

# Exactly the v0.7 reserved-keyword list (§B.2). Type names (String, Nat,
# ...), builtin names (len, is_some, ...) and `output` are NOT reserved;
# they lex as IDENT and are matched contextually by the parser.
KEYWORDS = {
    "spec", "version", "scope", "authors", "type", "define", "axiom", "assume",
    "constraints", "require", "forbid", "projection", "goal", "derive",
    "construct", "satisfying", "prove", "assuming", "check", "of",
    "compare-models", "under", "verification", "proof", "recompute", "test",
    "none", "kernel-checked", "by", "differential", "property-fuzz", "seeds",
    "cases", "required", "optional", "assurance", "level-a", "level-b",
    "accepted", "limits", "timeout", "memory", "steps", "record", "all",
    "external", "spec-hash", "input-hash", "tool-versions", "witness",
    "outputs", "true", "false", "if", "then", "else", "forall", "exists",
    "in", "let", "case", "of", "some",
}

# multi-char operators, longest first
OPERATORS = ["==>", "\\/", "/\\", "==", "!=", "<=", ">=", "->", "::"]

SINGLE = set("{}[](),:;.=< >+-*/!|\"'")

class LexError(Exception):
    def __init__(self, msg, line, col):
        super().__init__(f"lexical error at {line}:{col}: {msg}")
        self.line, self.col = line, col

class Token:
    __slots__ = ("kind", "value", "raw", "line", "col")
    def __init__(self, kind, value, raw, line, col):
        self.kind, self.value, self.raw = kind, value, raw
        self.line, self.col = line, col
    def __repr__(self):
        return f"Tok({self.kind},{self.raw!r},{self.line}:{self.col})"

_TOKEN_SPEC = [
    ("COMMENT",   r"//[^\n]*"),
    ("WS",        r"[ \t\r\n]+"),
    ("STRING",    r'"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"'),
    ("BADSTRING", r'"(?:[^"\n\\]|\\.)*"?'),
    # Hyphenated reserved keywords lex as single tokens (§B.2).
    ("HYPHENKW",  r"compare-models|kernel-checked|property-fuzz|level-a|level-b|"
                  r"spec-hash|input-hash|tool-versions"),
    # Strict surface HexFloat = the canonical-3 form (§B.2, D-026):
    # lowercase hex, lowercase p, exponent "+0" or sign+nonzero digits.
    # NEW-A7: no leading "-?" — negation is unary minus (avoids the
    # maximal-munch ambiguity with binary minus).
    ("HEXFLOAT",  r"0x[01]\.[0-9a-f]{13}p(?:\+0|[+-][1-9][0-9]*)"),
    ("SEMVER",    r"[0-9]+\.[0-9]+\.[0-9]+"),
    ("REALLIT",   r"[0-9]+\.[0-9]+"),
    ("DURATION",  r"[0-9]+(?:ms|s|min|h)\b"),
    ("MEMSIZE",   r"[0-9]+(?:KB|MB|GB|B)\b"),
    ("NAT",       r"[0-9]+"),
    ("IDENT",     r"[A-Za-z_][A-Za-z0-9_]*"),
    ("PUNCT",     r"[{}()\[\],:;.=<>\+\-\*/!|]"),
]
_MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in _TOKEN_SPEC))

# A "-?0x" prefix that fails the strict HexFloat rule is a lexical error
# with a precise diagnostic (not a confusing token cascade).
_HEXFLOAT_ATTEMPT = re.compile(r"-?0x")
_HEXFLOAT_STRICT = re.compile(r"0x[01]\.[0-9a-f]{13}p(?:\+0|[+-][1-9][0-9]*)")

def _decode_string(raw, line, col):
    body = raw[1:-1]
    out = []
    i = 0
    while i < len(body):
        c = body[i]
        if c != "\\":
            out.append(c); i += 1; continue
        e = body[i + 1]
        simple = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f",
                  "n": "\n", "r": "\r", "t": "\t"}
        if e in simple:
            out.append(simple[e]); i += 2
        elif e == "u":
            out.append(chr(int(body[i + 2:i + 6], 16))); i += 6
        else:
            raise LexError(f"bad escape '\\{e}'", line, col)
    return "".join(out)

def lex(source):
    tokens = []
    pos, line, col = 0, 1, 1
    while pos < len(source):
        # NEW-A7: the "-?" is not part of the HexFloat token (negation is
        # unary minus). If we see "-" followed by a valid hexfloat, it's
        # unary minus + literal — do not raise. Only raise for a "-?0x"
        # attempt that is not a valid literal in either position.
        if _HEXFLOAT_ATTEMPT.match(source, pos) \
           and not _HEXFLOAT_STRICT.match(source, pos):
            if not (source[pos] == "-"
                    and _HEXFLOAT_STRICT.match(source, pos + 1)):
                raise LexError(
                    "malformed Binary64 literal: expected "
                    "0x(0|1).<13 lowercase hex digits>p(+0|[+-][1-9][0-9]*) "
                    "(D-026: no '-0' exponent, lowercase hex; negation is unary '-')",
                    line, col)
        for op in OPERATORS:
            if source.startswith(op, pos):
                tokens.append(Token("OP", op, op, line, col))
                pos += len(op); col += len(op)
                break
        else:
            m = _MASTER.match(source, pos)
            if not m:
                raise LexError(f"unexpected character {source[pos]!r}", line, col)
            kind = m.lastgroup
            raw = m.group()
            nline = line + raw.count("\n")
            if kind in ("WS", "COMMENT"):
                pass
            elif kind == "BADSTRING":
                raise LexError("unterminated or invalid string literal", line, col)
            elif kind == "STRING":
                tokens.append(Token("STRING", _decode_string(raw, line, col), raw, line, col))
            elif kind == "IDENT" and raw in KEYWORDS:
                tokens.append(Token("KEYWORD", raw, raw, line, col))
            elif kind == "HYPHENKW":
                tokens.append(Token("KEYWORD", raw, raw, line, col))
            elif kind == "NAT":
                tokens.append(Token("NAT", int(raw), raw, line, col))
            elif kind == "PUNCT":
                tokens.append(Token("OP", raw, raw, line, col))
            else:
                tokens.append(Token(kind, raw, raw, line, col))
            if "\n" in raw:
                col = len(raw) - raw.rindex("\n")
            else:
                col += len(raw)
            line = nline
            pos = m.end()
            continue
        # operator branch line/col already advanced; loop continues
    tokens.append(Token("EOF", "", "", line, col))
    return tokens
