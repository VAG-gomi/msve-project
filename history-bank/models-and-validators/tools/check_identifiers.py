#!/usr/bin/env python3
"""M5: every identifier in §B.11 examples must resolve.
Resolves to: keyword | type name | builtin | defined name | bound variable |
field name | special variable | header slug parts."""
import re, sys

path = sys.argv[1]
text = open(path).read()

kwsec = text[text.index("Keywords (reserved):"):text.index("`output` is not a keyword")]
keywords = set()
for m in re.finditer(r'`([^`]*)`', kwsec):
    keywords.update(m.group(1).split())

type_names = {"String", "Nat", "Int", "Real", "Rat", "Binary64", "Bool",
              "Set", "Option", "Impl"}
builtins = {"len", "range", "is_finite", "is_ascii_printable",
            "has_no_whitespace", "is_some", "to_rat", "decode_candidates"}
special = {"output"}

sec = text[text.index("### B.11 Valid examples"):text.index("### B.12 Invalid examples")]
fences = re.findall(r'```\n(.*?)```', sec, re.S)

ok = True
for idx, fence in enumerate(fences):
    defined, bound, fields = set(), set(), set()
    for m in re.finditer(r'^(?:define|type|axiom|assume)\s+([A-Za-z_][A-Za-z0-9_]*)', fence, re.M):
        defined.add(m.group(1))
    # constraint group names, constraint names, projection names
    defined.update(re.findall(r'^\s*constraints\s+([A-Za-z_][A-Za-z0-9_]*)', fence, re.M))
    defined.update(re.findall(r'^\s*projection\s+([A-Za-z_][A-Za-z0-9_]*)', fence, re.M))
    defined.update(re.findall(r'\b(?:require|forbid)\s+([A-Za-z_][A-Za-z0-9_]*)\s*:', fence))
    # record field definitions: any `name:` inside braces
    for m in re.finditer(r'([A-Za-z_][A-Za-z0-9_]*)\s*:', fence):
        fields.add(m.group(1))
    # function params
    for m in re.finditer(r'define\s+[A-Za-z_]+\s*\(([^)]*)\)', fence):
        for p in m.group(1).split(','):
            p = p.strip()
            if p:
                bound.add(p.split(':')[0].strip())
    bound.update(re.findall(r'\blet\s+([A-Za-z_][A-Za-z0-9_]*)', fence))
    bound.update(re.findall(r'\bcase\b.*?\bof\s+some\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)', fence))
    bound.update(re.findall(r'\b(?:forall|exists)\s+([A-Za-z_][A-Za-z0-9_]*)', fence))

    code = fence
    code = re.sub(r'"(?:[^"\\]|\\.)*"', ' ', code)          # strings
    code = re.sub(r'//.*', ' ', code)                        # comments
    # header lines: spec/scope/version/authors/checker ids — collect slug parts as allowed
    allowed_extra = set()
    for m in re.finditer(r'^(?:spec|scope|authors|version)\s+(.*)$', code, re.M):
        allowed_extra.update(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', m.group(1)))
    code = re.sub(r'^(?:spec|scope|authors|version)\s+.*$', ' ', code, flags=re.M)
    code = re.sub(r'[A-Za-z_][A-Za-z0-9_-]*/\d+\.\d+\.\d+', ' ', code)  # CheckerID
    code = re.sub(r'\b\d+\s*(?:ms|s|min|h|B|KB|MB|GB)\b', ' ', code)    # Duration/MemSize
    code = re.sub(r'\.\s*[A-Za-z_][A-Za-z0-9_]*', ' ', code)            # field access
    code = re.sub(r'\b(?:level-[ab]|kernel-checked|property-fuzz|compare-models|independent-recompute)\b', ' ', code)

    resolvable = keywords | type_names | builtins | special | defined | bound | fields | allowed_extra
    unresolved = set()
    for m in re.finditer(r'[A-Za-z_][A-Za-z0-9_]*', code):
        if m.group(0) not in resolvable:
            unresolved.add(m.group(0))
    if unresolved:
        ok = False
        print(f"example {idx}: UNRESOLVED: {sorted(unresolved)}")
    else:
        print(f"example {idx}: all identifiers resolve")
sys.exit(0 if ok else 1)
