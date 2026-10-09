"""M8 name resolution (v0.8).

Two passes over the parsed AST:
 1. Collect top-level definitions (type aliases, values, functions, axioms,
    assumptions, externals). Duplicate definition names are an error
    (admission: duplicate-definition).
 2. Resolve every variable/call reference to: a builtin, a local binding
    (param / let / case-binder / quantifier binder), a top-level definition,
    or the special `output` variable (in scope only where §B.5a allows).

Annotations are written into node.fields['resolved']. Errors carry the
category 'name-resolution'.
"""
from .lexer import KEYWORDS

BUILTINS = {
    "len", "range", "is_finite", "is_nan", "base_code", "is_ascii_printable", "has_no_whitespace",
    "is_some", "to_rat", "decode_candidates",
}

# contextual type names must not be treated as value references
TYPE_NAMES = {"String", "Nat", "Int", "Real", "Rat", "Binary64", "Bool",
              "Set", "Option", "Impl"}

class ResolveError(Exception):
    def __init__(self, msg, line, col):
        super().__init__(f"name-resolution error at {line}:{col}: {msg}")
        self.line, self.col = line, col
        self.category = "name-resolution"

class Resolver:
    def __init__(self):
        self.defs = {}          # name -> definition Node
        self.type_aliases = {}  # name -> TypeAlias Node
        self.errors = []

    def err(self, msg, node):
        self.errors.append(ResolveError(msg, node.line, node.col))

    # ---- pass 1: collect ----
    def collect(self, spec):
        body = spec.fields["body"]
        for d in body.fields["definitions"]:
            name = d.fields.get("name")
            if not name:
                continue
            if name in self.defs or name in self.type_aliases:
                self.err(f"duplicate definition '{name}'", d)
                continue
            # NEW-A6: the flat namespace includes builtins (§B.5).
            if name in BUILTINS:
                self.err(f"duplicate definition '{name}' (shadows a builtin)",
                         d)
                continue
            if d.kind == "TypeAlias":
                self.type_aliases[name] = d
            else:
                self.defs[name] = d
            if name == "output":
                self.err("'output' is a reserved context name and cannot be defined", d)

    # ---- pass 2: resolve ----
    def resolve(self, spec):
        body = spec.fields["body"]
        # goal determines `output` scope for referenced constraint groups
        goal = body.fields["goal"]
        output_groups = set()
        if goal.kind == "ConstructGoal":
            output_groups = set(goal.fields["refs"])
        if goal.kind == "CompareGoal":
            output_groups = set(goal.fields["refs"])
        for grp in body.fields["constraint_groups"]:
            in_scope = dict()
            if grp.fields["name"] in output_groups:
                in_scope["output"] = "output"
            for c in grp.fields["items"]:
                self.resolve_expr(c.fields["pred"], in_scope, allow_output=bool(in_scope))
        for d in body.fields["definitions"]:
            self.resolve_definition(d)
        self.resolve_goal(goal)
        # projections: paths resolve against model type (checked in typecheck)
        return self.errors

    def resolve_definition(self, d):
        if d.kind in ("AxiomDecl", "AssumptionDecl"):
            return  # propositions over builtins/globals only; no locals
        if d.kind == "TypeAlias":
            return
        if d.kind == "ExternalDecl":
            return
        scope = {}
        if d.kind == "FunDef":
            for p in d.fields["params"]:
                scope[p.fields["name"]] = "param"
        self.resolve_expr(d.fields["body"], dict(scope), allow_output=False)

    def resolve_goal(self, goal):
        if goal.kind == "DeriveGoal":
            self.resolve_expr(goal.fields["expr"], {}, allow_output=False)
        elif goal.kind == "ProveGoal":
            self.resolve_expr(goal.fields["prop"], {}, allow_output=False)
        # other goal kinds carry no expressions (refs checked in typecheck)

    def resolve_expr(self, e, scope, allow_output):
        k = e.kind
        if k == "Var":
            name = e.fields["name"]
            if name in scope:
                e.fields["resolved"] = ("local", name)
            elif name == "output" and allow_output:
                e.fields["resolved"] = ("output",)
            elif name in BUILTINS:
                e.fields["resolved"] = ("builtin", name)
            elif name in self.defs:
                e.fields["resolved"] = ("define", name)
            elif name in TYPE_NAMES:
                self.err(f"type name '{name}' used as a value", e)
            else:
                self.err(f"unbound identifier '{name}'", e)
            return
        if k == "Call":
            name = e.fields["fun"]
            if name in scope:
                e.fields["resolved"] = ("local", name)
            elif name in BUILTINS:
                e.fields["resolved"] = ("builtin", name)
            elif name in self.defs:
                e.fields["resolved"] = ("define", name)
            else:
                self.err(f"unbound identifier '{name}'", e)
            for a in e.fields["args"]:
                self.resolve_expr(a, scope, allow_output)
            return
        if k == "Let":
            self.resolve_expr(e.fields["value"], scope, allow_output)
            s2 = dict(scope); s2[e.fields["name"]] = "let"
            self.resolve_expr(e.fields["body"], s2, allow_output)
            return
        if k == "Case":
            self.resolve_expr(e.fields["scrut"], scope, allow_output)
            s2 = dict(scope); s2[e.fields["binder"]] = "case"
            self.resolve_expr(e.fields["some"], s2, allow_output)
            self.resolve_expr(e.fields["none"], scope, allow_output)
            return
        if k in ("Forall", "Exists"):
            dom = e.fields["domain"]
            if dom.kind == "ExprDomain":
                self.resolve_expr(dom.fields["expr"], scope, allow_output)
            s2 = dict(scope); s2[e.fields["var"]] = "quant"
            self.resolve_expr(e.fields["body"], s2, allow_output)
            return
        if k == "If":
            for f in ("cond", "then", "else"):
                self.resolve_expr(e.fields[f], scope, allow_output)
            return
        if k == "BinOp":
            self.resolve_expr(e.fields["left"], scope, allow_output)
            self.resolve_expr(e.fields["right"], scope, allow_output)
            return
        if k == "UnOp":
            self.resolve_expr(e.fields["operand"], scope, allow_output)
            return
        if k == "FieldAccess":
            self.resolve_expr(e.fields["base"], scope, allow_output)
            return
        if k == "Index":
            self.resolve_expr(e.fields["base"], scope, allow_output)
            self.resolve_expr(e.fields["index"], scope, allow_output)
            return
        if k == "Some":
            self.resolve_expr(e.fields["expr"], scope, allow_output)
            return
        if k == "RecordLit":
            for _, fe in e.fields["fields"]:
                self.resolve_expr(fe, scope, allow_output)
            return
        if k == "Literal":
            return
        self.err(f"resolve: unhandled node kind {k}", e)


def resolve(spec):
    r = Resolver()
    r.collect(spec)
    errors = r.resolve(spec)
    return r, errors
