# Report C — M8 Source — Lexer, Grammar, CLI (Part 2/7)

**Work Order:** 0.8.2 · **Evidence:** DIRECT ARTEFACT (complete source text from the ZIP, unmodified).

---



## File: `m8/lexer.py`

```python
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

```


## File: `m8/grammar.py`

```python
"""M8 grammar source of truth (MSVE v0.8).

PRODUCTIONS is the single machine-readable grammar source. The normative
§B.3 presentation in MSVE_DESIGN_SPEC_v0.8.md is GENERATED from it
(see generate_markdown()), and parser.py implements one parse method per
production (checked by tests/test_grammar_conformance.py).

v0.8 changes vs v0.7 (defect-driven):
- D-025: Atom gains record construction:
    "{" (Ident ":" Expr ("," Ident ":" Expr)*)? "}"
- D-026: HexFloat exponent is "+0" or sign+nonzero digits (no "-0").
- Literal gains HexFloat (Binary64 literal).
- Nothing else in the grammar changes; D-031 (cardinality/conflict) is a
  static admission check implemented in typecheck.py, not a grammar rule.
"""
from typing import List, Tuple

M8_VERSION = "0.8.0"
GRAMMAR_VERSION = "0.8.0"

# (production name, EBNF right-hand side)
PRODUCTIONS: List[Tuple[str, str]] = [
    ("Specification",
     'Header Body'),
    ("Header",
     '"spec" Slug "version" SemVer "scope" Slug "authors" "[" (String ("," String)*)? "]"'),
    ("Body",
     'Definition* ConstraintGroup* Projection* Goal Verification ResourceLimits ProvenanceReq'),
    ("Definition",
     'TypeAlias | ValueDef | FunDef | AxiomDecl | AssumptionDecl | ExternalDecl'),
    ("TypeAlias",
     '"type" Ident "=" TypeExpr'),
    ("ValueDef",
     '"define" Ident ":" TypeExpr "=" Expr'),
    ("FunDef",
     '"define" Ident "(" Params ")" ":" TypeExpr "=" Expr'),
    ("Params",
     '(Ident ":" TypeExpr ("," Ident ":" TypeExpr)*)?'),
    ("AxiomDecl",
     '"axiom" Ident ":" Proposition'),
    ("AssumptionDecl",
     '"assume" Ident ":" Proposition'),
    ("ExternalDecl",
     '"define" Ident ":" ImplType "=" "external" "(" String ")"'),
    ("ConstraintGroup",
     '"constraints" Ident "{" (";" | Constraint ";")* "}"'),
    ("Constraint",
     '"require" Ident ":" Predicate | "forbid" Ident ":" Predicate'),
    ("Projection",
     '"projection" Ident "=" "[" ProjPath ("," ProjPath)* "]"'),
    ("ProjPath",
     'Ident ("." Ident)*'),
    ("Goal",
     '"goal" (DeriveGoal | ConstructGoal | ProveGoal | CheckGoal | CompareGoal)'),
    ("DeriveGoal",
     '"derive" Expr'),
    ("ConstructGoal",
     '"construct" TypeExpr "satisfying" "[" Ident ("," Ident)* "]"'),
    ("ProveGoal",
     '"prove" Proposition "assuming" "[" Ident ("," Ident)* "]"'),
    ("CheckGoal",
     '"check" Ident "of" Ident'),
    ("CompareGoal",
     '"compare-models" TypeExpr "satisfying" "[" Ident ("," Ident)* "]" ("under" Ident)?'),
    ("Verification",
     '"verification" "{" (";" | VerifItem ";")* "}"'),
    ("VerifItem",
     'ProofReq | RecomputeReq | TestReq | AssuranceReq'),
    ("ProofReq",
     '"proof" ":" ("none" | "kernel-checked" "by" CheckerID Qualifier)'),
    ("RecomputeReq",
     '"recompute" ":" ("none" | "by" CheckerID Qualifier)'),
    ("TestReq",
     '"test" ":" ("none" | "differential" "by" CheckerID Qualifier | "property-fuzz" FuzzConfig Qualifier)'),
    ("AssuranceReq",
     '"assurance" ":" ("none" | "level-a" "required" | "level-b" "accepted")'),
    ("Qualifier",
     '("required" | "optional")?'),
    ("FuzzConfig",
     '"{" "seeds" ":" "[" Nat ("," Nat)* "]" "," "cases" ":" Nat "}"'),
    ("ResourceLimits",
     '"limits" "{" "timeout" ":" Duration ";" ("memory" ":" MemSize ";")? ("steps" ":" Nat ";")? "}"'),
    ("ProvenanceReq",
     '"record" ":" ("all" | "[" ProvItem ("," ProvItem)* "]")'),
    ("ProvItem",
     '"spec-hash" | "input-hash" | "tool-versions" | "witness" | "outputs"'),
    ("TypeExpr",
     '"String" | "Nat" | "Int" | "Real" | "Rat" | "Binary64" | "Bool" '
     '| "{" (Ident ":" TypeExpr ("," Ident ":" TypeExpr)*)? "}" '
     '| "[" TypeExpr "]" '
     # NEW-A9: "Set" removed from v0 surface syntax (no introduction form;
     # reserved for future use). The canonical "set" envelope is retained.
     '| "Option" "<" TypeExpr ">" | ImplType '
     '| "(" (TypeExpr ("," TypeExpr)*)? ")" "->" TypeExpr | Ident'),
    ("ImplType",
     '"Impl" "(" TypeExpr "->" TypeExpr ")"'),
    ("Expr", 'OrExpr'),
    ("OrExpr", 'AndExpr ("\\\\/" AndExpr)*'),
    ("AndExpr", 'ImplExpr ("/\\\\" ImplExpr)*'),
    ("ImplExpr", 'CmpExpr ("==>" CmpExpr)?'),
    ("CmpExpr", 'AddExpr (("==" | "!=" | "<" | "<=" | ">" | ">=") AddExpr)?'),
    ("AddExpr", 'MulExpr (("+" | "-") MulExpr)*'),
    ("MulExpr", 'Unary (("*" | "/") Unary)*'),
    ("Unary", '("!" | "-")? Postfix'),
    ("Postfix", 'Atom ("." Ident | "[" Expr "]")*'),
    ("Atom",
     'Literal | Ident | Ident "(" (Expr ("," Expr)*)? ")" '
     '| "(" Expr ")" '
     '| "{" (Ident ":" Expr ("," Ident ":" Expr)*)? "}" '
     '| "if" Proposition "then" Expr "else" Expr '
     '| "let" Ident "=" Expr "in" Expr '
     '| "case" Expr "of" "some" "(" Ident ")" "->" Expr "|" "none" "->" Expr '
     '| "some" "(" Expr ")" '
     '| "forall" Ident "in" Domain "::" "(" Proposition ")" '
     '| "exists" Ident "in" Domain "::" "(" Proposition ")"'),
    ("Domain", '"type" TypeExpr | Expr'),
    ("Literal",
     'String | Nat | RealLit | HexFloat | "true" | "false" | "none"'),
    ("Proposition", 'Expr'),
    ("Predicate", 'Expr'),
]

LEXICAL = [
    ("Ident",    r"[A-Za-z_][A-Za-z0-9_]*"),
    ("Slug",     r"[A-Za-z0-9_]+(-[A-Za-z0-9_]+)*"),
    ("String",   r"\" ( [^\"\\\\\\u0000-\\u001F] | Esc )* \""),
    ("Esc",      r"\\\\ ( \"\\\"\" | \"\\\\\" | \"/\" | \"b\" | \"f\" | \"n\" | \"r\" | \"t\" | \"u\" Hex Hex Hex Hex )"),
    ("Hex",      r"[0-9a-fA-F]"),
    ("HexLo",     r"[0-9a-f]"),
    ("Nat",      r"[0-9]+"),
    ("RealLit",  r'Nat "." Nat'),
    ("HexFloat", r'-? "0x" ("0" | "1") "." HexLo{13} "p" ("+0" | ("+" | "-") [1-9] [0-9]*)'),
    ("SemVer",   r'Nat "." Nat "." Nat'),
    ("Duration", r'Nat ("ms" | "s" | "min" | "h")'),
    ("MemSize",  r'Nat ("B" | "KB" | "MB" | "GB")'),
    ("CheckerID", r'Slug "/" SemVer'),
]

PRODUCTION_NAMES = [name for name, _ in PRODUCTIONS]

def generate_markdown() -> str:
    """Emit the normative §B.3 grammar block from this single source."""
    lines = ["```"]
    for name, rhs in PRODUCTIONS:
        lines.append(f"{name:<15} := {rhs}")
    lines.append("```")
    return "\n".join(lines)

def generate_lexical_markdown() -> str:
    lines = ["```"]
    for name, rhs in LEXICAL:
        lines.append(f"{name:<10} := {rhs}")
    lines.append("```")
    return "\n".join(lines)

```


## File: `m8/cli.py`

```python
"""M8 command-line interface.

Usage:
  python3 -m m8.cli check <file.msve>      parse + resolve + type-check one file
  python3 -m m8.cli corpus                  run the full regression corpus
  python3 -m m8.cli grammar-conformance     check grammar.py <-> spec <-> parser
  python3 -m m8.cli spec-examples           check every formal example in the v0.8 spec

Exit code 0 iff all checks pass. Every failure carries a category:
lexical | syntax | name-resolution | type | admission | canonical.
"""
import sys, os, json, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from m8.lexer import lex, LexError
from m8.parser import parse, ParseError, check_production_coverage
from m8.resolve import resolve, ResolveError
from m8.typecheck import typecheck
from m8.grammar import (PRODUCTIONS, PRODUCTION_NAMES, M8_VERSION,
                        GRAMMAR_VERSION, generate_markdown)
from m8.canonical import check_canonical_tree

DESIGN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_source(source, label="<input>"):
    """Run the full M8 pipeline. Returns (ok, [errors])."""
    errors = []
    try:
        toks = lex(source)
    except LexError as e:
        return False, [("lexical", str(e))]
    try:
        tree = parse(source)
    except ParseError as e:
        return False, [("syntax", str(e))]
    resolver, rerrs = resolve(tree)
    errors += [("name-resolution", str(e)) for e in rerrs]
    terrs, _checker = typecheck(tree, resolver)
    errors += [(e.category, str(e)) for e in terrs]
    cerrs = check_canonical_tree(tree)
    errors += [("canonical", str(e)) for e in cerrs]
    return (len(errors) == 0), errors

def cmd_check(path):
    with open(path) as f:
        src = f.read()
    ok, errors = check_source(src, path)
    for cat, msg in errors:
        print(f"[{cat}] {msg}")
    print("M8: PASS" if ok else "M8: FAIL")
    return 0 if ok else 1

def cmd_corpus():
    from m8.tests import run_corpus
    return run_corpus()

def cmd_grammar_conformance():
    spec_path = os.path.join(DESIGN_DIR, "MSVE_DESIGN_SPEC_v0.8.md")
    problems = []
    # 1. every production has a parser method
    missing, extra = check_production_coverage()
    if missing:
        problems.append(f"productions without parser method: {missing}")
    if extra:
        problems.append(f"parser methods without production: {extra}")
    # 2. the spec's §B.3 block must equal the generated block
    try:
        text = open(spec_path).read()
    except FileNotFoundError:
        print("grammar-conformance: v0.8 spec not present yet — SKIPPED")
        return 2
    m = re.search(r"### B\.3 Grammar.*?\n(```\n.*?\n```)", text, re.S)
    if not m:
        problems.append("no §B.3 grammar block found in spec")
    elif m.group(1).strip() != generate_markdown().strip():
        problems.append("spec §B.3 differs from m8/grammar.py generated block")
    if problems:
        for p in problems:
            print("CONFORMANCE PROBLEM:", p)
        return 1
    print(f"grammar-conformance: OK "
          f"({len(PRODUCTIONS)} productions, parser methods present, spec §B.3 matches generated)")
    return 0

def cmd_spec_examples():
    spec_path = os.path.join(DESIGN_DIR, "MSVE_DESIGN_SPEC_v0.8.md")
    try:
        text = open(spec_path).read()
    except FileNotFoundError:
        print("spec-examples: v0.8 spec not present yet — SKIPPED")
        return 2
    # valid examples: §B.11 fences; invalid: §B.12 fences (marked INVALID:)
    def fences_between(start, end):
        sec = text[text.index(start):text.index(end)]
        return re.findall(r"```\n(.*?)```", sec, re.S)
    try:
        valid = fences_between("### B.11 Valid examples", "### B.12 Invalid examples")
        invalid_sec = text[text.index("### B.12 Invalid examples"):]
        # cut at the next top-level section
        m2 = re.search(r"\n## ", invalid_sec[10:])
        if m2:
            invalid_sec = invalid_sec[:10 + m2.start()]
        invalid = re.findall(r"```\n(.*?)```", invalid_sec, re.S)
    except ValueError as e:
        print("spec-examples: section markers missing:", e)
        return 2
    failures = 0
    for i, src in enumerate(valid):
        ok, errors = check_source(src, f"B.11 example {i}")
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
            print(f"B.11 example {i}: {status}")
            for cat, msg in errors[:5]:
                print(f"    [{cat}] {msg}")
        else:
            print(f"B.11 example {i}: {status}")
    for i, src in enumerate(invalid):
        first = src.strip().split("\n", 1)[0]
        m = re.match(r"//\s*INVALID:\s*(\S+)", first)
        if not m:
            print(f"B.12 example {i}: no INVALID marker — SKIPPED (not a machine case)")
            continue
        want = m.group(1)
        ok, errors = check_source(src, f"B.12 example {i}")
        cats = {c for c, _ in errors}
        if ok:
            print(f"B.12 example {i}: FAIL (expected rejection [{want}], but passed)")
            failures += 1
        elif want not in cats:
            print(f"B.12 example {i}: FAIL (expected [{want}], got {sorted(cats)})")
            for cat, msg in errors[:3]:
                print(f"    [{cat}] {msg}")
            failures += 1
        else:
            print(f"B.12 example {i}: PASS (rejected [{want}])")
    print(f"spec-examples: {failures} failures")
    return 1 if failures else 0

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "check":
        return cmd_check(argv[2])
    if cmd == "corpus":
        return cmd_corpus()
    if cmd == "grammar-conformance":
        return cmd_grammar_conformance()
    if cmd == "spec-examples":
        return cmd_spec_examples()
    print(f"unknown command {cmd}")
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))

```
