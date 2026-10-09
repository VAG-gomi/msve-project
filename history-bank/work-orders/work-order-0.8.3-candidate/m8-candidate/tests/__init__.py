"""M8 test package: corpus runner + unit tests.

Run everything with:  python3 -m m8.cli corpus
Run one module with:  python3 -m m8.tests.test_canonical
"""
import os, json, sys

def run_corpus():
    from m8.cli import check_source, DESIGN_DIR
    corpus_dir = os.path.join(DESIGN_DIR, "m8", "corpus")
    manifest = json.load(open(os.path.join(corpus_dir, "manifest.json")))
    failures = 0
    for entry in manifest:
        path = os.path.join(corpus_dir, entry["file"])
        src = open(path).read()
        ok, errors = check_source(src, entry["file"])
        cats = {c for c, _ in errors}
        want = entry["expect"]
        if want == "pass":
            good = ok
        else:
            good = (not ok) and entry.get("category") in cats
        status = "PASS" if good else "FAIL"
        if not good:
            failures += 1
        detail = "" if good else f"  <- want {want}/{entry.get('category')}, got ok={ok} cats={sorted(cats)}"
        print(f"{entry['file']}: {status}{detail}")
        if not good:
            for cat, msg in errors[:3]:
                print(f"    [{cat}] {msg}")
    # unit test modules
    for mod in ("test_canonical", "test_grammar_conformance"):
        print(f"--- {mod} ---")
        __import__(f"m8.tests.{mod}")
        m = sys.modules[f"m8.tests.{mod}"]
        try:
            m.run()
            print(f"{mod}: PASS")
        except AssertionError as e:
            failures += 1
            print(f"{mod}: FAIL: {e}")
    print(f"corpus: {failures} failures")
    return 1 if failures else 0
