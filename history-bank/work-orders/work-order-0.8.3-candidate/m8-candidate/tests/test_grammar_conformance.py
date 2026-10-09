"""Grammar-conformance test: grammar.py <-> parser.py <-> spec §B.3."""
import re, os

def run():
    from m8.grammar import PRODUCTIONS, PRODUCTION_NAMES, generate_markdown
    from m8.parser import check_production_coverage, Parser
    # 1. production <-> parser method
    missing, extra = check_production_coverage()
    assert not missing, f"productions without parser method: {missing}"
    assert not extra, f"parser methods without production: {extra}"
    # 2. no duplicate production names
    assert len(set(PRODUCTION_NAMES)) == len(PRODUCTION_NAMES), "duplicate productions"
    # 3. spec §B.3 matches the generated block (when the spec exists)
    design = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    spec = os.path.join(design, "MSVE_DESIGN_SPEC_v0.8.md")
    if not os.path.exists(spec):
        print("test_grammar_conformance: v0.8 spec absent — parts 1-2 only")
        return
    text = open(spec).read()
    m = re.search(r"### B\.3 Grammar.*?\n(```\n.*?\n```)", text, re.S)
    assert m, "no §B.3 grammar block in spec"
    assert m.group(1).strip() == generate_markdown().strip(), \
        "spec §B.3 differs from m8/grammar.py"
    print(f"test_grammar_conformance: {len(PRODUCTIONS)} productions OK")

if __name__ == "__main__":
    run()
    print("PASS")
