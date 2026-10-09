#!/usr/bin/env python3
"""Mechanical check: every nonterminal referenced in the v0.5 EBNF must be defined.
Catches the defect-01 class (e.g. Esc referenced but undefined)."""
import re, sys

path = sys.argv[1]
text = open(path).read()

# Extract the EBNF fenced block(s) between B.3 and B.4 headers
start = text.index("### B.3 Grammar")
end = text.index("### B.4 Type system")
section = text[start:end]
blocks = re.findall(r'```(?:\w*)\n(.*?)```', section, re.S)
block = "\n".join(blocks)

defined = {}
for m in re.finditer(r'^([A-Za-z][A-Za-z0-9_]*)\s*:=', block, re.M):
    lhs = m.group(1)
    # grab the full production (until next production or blank-line + non-indented)
    defined[lhs] = True

lexical = {"Ident", "Slug", "String", "Esc", "Hex", "Nat", "RealLit",
           "SemVer", "Duration", "MemSize", "CheckerID"}

referenced = set()
for m in re.finditer(r'^([A-Za-z][A-Za-z0-9_]*)\s*:=', block, re.M):
    # find end of this production: next production start or end of block
    rest = block[m.end():]
    nxt = re.search(r'^[A-Za-z][A-Za-z0-9_]*\s*:=', rest, re.M)
    rhs = rest[:nxt.start()] if nxt else rest
    # strip quoted literals, [...] char classes, and # comments
    rhs = re.sub(r'"(?:[^"\\]|\\.)*"', ' ', rhs)
    rhs = re.sub(r'\[[^\]]*\]', ' ', rhs)
    rhs = re.sub(r'#.*', ' ', rhs)
    for tok in re.findall(r'[A-Z][A-Za-z0-9_]*', rhs):
        referenced.add(tok)

undefined = sorted(r for r in referenced if r not in defined and r not in lexical)
print(f"defined nonterminals: {len(defined)}")
print(f"referenced nonterminals: {len(referenced)}")
if undefined:
    print("UNDEFINED (referenced but not defined):", undefined)
    sys.exit(1)
print("OK: every referenced nonterminal is defined or lexical.")
