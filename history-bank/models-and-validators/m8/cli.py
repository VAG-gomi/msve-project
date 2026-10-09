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
