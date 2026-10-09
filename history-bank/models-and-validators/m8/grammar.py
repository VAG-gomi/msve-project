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
