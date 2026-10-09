# Report C — M8 Source — Parser (Part 3/7)

**Work Order:** 0.8.2 · **Evidence:** DIRECT ARTEFACT (complete source text from the ZIP, unmodified).

---



## File: `m8/parser.py`

```python
"""M8 recursive-descent parser for the MSVE formal language (v0.8).

One parse method per production in m8/grammar.py (checked by
tests/test_grammar_conformance.py). Produces AST Nodes with source
locations. Raises ParseError (syntax failure) with location.
"""
from .lexer import lex, Token
from .grammar import PRODUCTION_NAMES

class ParseError(Exception):
    def __init__(self, msg, line, col):
        super().__init__(f"syntax error at {line}:{col}: {msg}")
        self.line, self.col = line, col

class Node:
    __slots__ = ("kind", "fields", "line", "col")
    def __init__(self, kind, fields=None, line=0, col=0):
        self.kind = kind
        self.fields = fields or {}
        self.line, self.col = line, col
    def __repr__(self):
        return f"Node({self.kind}@{self.line}:{self.col})"

class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.pos = 0

    # ---- low-level ----
    def peek(self):
        return self.toks[self.pos]

    def at(self, kind=None, value=None):
        t = self.peek()
        return (kind is None or t.kind == kind) and (value is None or t.value == value)

    def next(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t

    def expect_kw(self, kw):
        t = self.peek()
        if t.kind == "KEYWORD" and t.value == kw:
            return self.next()
        raise ParseError(f"expected keyword '{kw}', found {t.raw!r}", t.line, t.col)

    def expect_op(self, op):
        t = self.peek()
        if t.kind == "OP" and t.value == op:
            return self.next()
        raise ParseError(f"expected '{op}', found {t.raw!r}", t.line, t.col)

    def expect_ident(self):
        t = self.peek()
        if t.kind == "IDENT":
            return self.next()
        raise ParseError(f"expected identifier, found {t.raw!r}", t.line, t.col)

    def expect_field_name(self):
        """Record field names may be reserved keywords (e.g. `accepted`,
        `seeds`, `timeout` are used as field names in normative examples);
        the position is unambiguous."""
        t = self.peek()
        if t.kind in ("IDENT", "KEYWORD"):
            return self.next()
        raise ParseError(f"expected field name, found {t.raw!r}", t.line, t.col)

    def accept_kw(self, kw):
        if self.at("KEYWORD", kw):
            return self.next()
        return None

    def at_ctx(self, name):
        """Contextual keyword: an IDENT token with the given text (type names
        and builtin names are not reserved; §B.2)."""
        t = self.peek()
        return t.kind == "IDENT" and t.value == name

    def accept_ctx(self, name):
        if self.at_ctx(name):
            return self.next()
        return None

    def expect_ctx(self, name):
        t = self.peek()
        if self.at_ctx(name):
            return self.next()
        raise ParseError(f"expected '{name}', found {t.raw!r}", t.line, t.col)

    def accept_op(self, op):
        if self.at("OP", op):
            return self.next()
        return None

    def node(self, kind, fields, tok):
        return Node(kind, fields, tok.line, tok.col)

    # ---- Specification ----
    def parse_specification(self):
        t = self.peek()
        header = self.parse_header()
        body = self.parse_body()
        if not self.at("EOF"):
            t = self.peek()
            raise ParseError(f"unexpected trailing input {t.raw!r}", t.line, t.col)
        return self.node("Specification", {"header": header, "body": body}, t)

    def parse_header(self):
        t = self.expect_kw("spec")
        slug = self.parse_slug()
        self.expect_kw("version")
        semver = self.parse_semver()
        self.expect_kw("scope")
        scope = self.parse_slug()
        self.expect_kw("authors")
        self.expect_op("[")
        authors = []
        if not self.at("OP", "]"):
            authors.append(self.expect_string())
            while self.accept_op(","):
                authors.append(self.expect_string())
        self.expect_op("]")
        return self.node("Header", {"name": slug, "version": semver,
                                    "scope": scope, "authors": authors}, t)

    def parse_slug(self):
        # Slug parts may themselves be keywords (e.g. recompute-checker);
        # the Slug lexical rule does not exclude them.
        t = self.peek()
        if t.kind not in ("IDENT", "KEYWORD"):
            raise ParseError(f"expected identifier, found {t.raw!r}", t.line, t.col)
        self.next()
        parts = [t.value]
        while self.at("OP", "-"):
            self.next()
            t2 = self.peek()
            if t2.kind not in ("IDENT", "KEYWORD"):
                raise ParseError(f"expected identifier, found {t2.raw!r}",
                                 t2.line, t2.col)
            self.next()
            parts.append(t2.value)
        return self.node("Slug", {"parts": parts}, t)

    def parse_semver(self):
        t = self.peek()
        if t.kind != "SEMVER":
            raise ParseError(f"expected version a.b.c, found {t.raw!r}", t.line, t.col)
        return self.node("SemVer", {"value": t.value}, self.next())

    def expect_string(self):
        t = self.peek()
        if t.kind != "STRING":
            raise ParseError(f"expected string, found {t.raw!r}", t.line, t.col)
        return self.node("StringLit", {"value": t.value, "raw": t.raw}, self.next())

    def parse_body(self):
        t = self.peek()
        defs, cgroups, projs = [], [], []
        while True:
            if self.at("KEYWORD", "type") or self.at("KEYWORD", "define") \
               or self.at("KEYWORD", "axiom") or self.at("KEYWORD", "assume"):
                defs.append(self.parse_definition())
            elif self.at("KEYWORD", "constraints"):
                cgroups.append(self.parse_constraint_group())
            elif self.at("KEYWORD", "projection"):
                projs.append(self.parse_projection())
            else:
                break
        goal = self.parse_goal()
        verif = self.parse_verification()
        limits = self.parse_resource_limits()
        prov = self.parse_provenance_req()
        return self.node("Body", {"definitions": defs, "constraint_groups": cgroups,
                                  "projections": projs, "goal": goal,
                                  "verification": verif, "limits": limits,
                                  "provenance": prov}, t)

    def parse_definition(self):
        if self.at("KEYWORD", "type"):
            return self.parse_type_alias()
        if self.at("KEYWORD", "axiom"):
            t = self.next()
            name = self.expect_ident()
            self.expect_op(":")
            prop = self.parse_proposition()
            return self.node("AxiomDecl", {"name": name.value, "prop": prop}, t)
        if self.at("KEYWORD", "assume"):
            t = self.next()
            name = self.expect_ident()
            self.expect_op(":")
            prop = self.parse_proposition()
            return self.node("AssumptionDecl", {"name": name.value, "prop": prop}, t)
        # define ...
        t = self.expect_kw("define")
        name = self.expect_ident()
        if self.at("OP", "("):
            self.next()
            params = self.parse_params()
            self.expect_op(")")
            self.expect_op(":")
            rtype = self.parse_type_expr()
            self.expect_op("=")
            body = self.parse_expr()
            return self.node("FunDef", {"name": name.value, "params": params,
                                        "rtype": rtype, "body": body}, t)
        self.expect_op(":")
        # ValueDef vs ExternalDecl: lookahead for ImplType then "external"
        texpr = self.parse_type_expr()
        self.expect_op("=")
        if self.at("KEYWORD", "external"):
            if texpr.kind != "ImplType":
                raise ParseError("external declaration requires an Impl type",
                                 t.line, t.col)
            self.next()
            self.expect_op("(")
            desc = self.expect_string()
            self.expect_op(")")
            return self.node("ExternalDecl", {"name": name.value, "type": texpr,
                                              "descriptor": desc}, t)
        body = self.parse_expr()
        return self.node("ValueDef", {"name": name.value, "type": texpr,
                                      "body": body}, t)

    def parse_type_alias(self):
        t = self.expect_kw("type")
        name = self.expect_ident()
        self.expect_op("=")
        texpr = self.parse_type_expr()
        return self.node("TypeAlias", {"name": name.value, "type": texpr}, t)

    def parse_params(self):
        params = []
        if not self.at("OP", ")"):
            t = self.expect_ident()
            self.expect_op(":")
            ty = self.parse_type_expr()
            params.append(self.node("Param", {"name": t.value, "type": ty}, t))
            while self.accept_op(","):
                t = self.expect_ident()
                self.expect_op(":")
                ty = self.parse_type_expr()
                params.append(self.node("Param", {"name": t.value, "type": ty}, t))
        return params

    def parse_constraint_group(self):
        t = self.expect_kw("constraints")
        name = self.expect_ident()
        self.expect_op("{")
        items = []
        while not self.at("OP", "}"):
            if self.at("OP", ";"):
                self.next(); continue
            ct = self.peek()
            if self.accept_kw("require"):
                kind = "require"
            elif self.accept_kw("forbid"):
                kind = "forbid"
            else:
                raise ParseError(f"expected 'require' or 'forbid', found {ct.raw!r}",
                                 ct.line, ct.col)
            cname = self.expect_ident()
            self.expect_op(":")
            pred = self.parse_predicate()
            self.expect_op(";")
            items.append(self.node("Constraint", {"kind": kind, "name": cname.value,
                                                  "pred": pred}, ct))
        self.expect_op("}")
        return self.node("ConstraintGroup", {"name": name.value, "items": items}, t)

    def parse_projection(self):
        t = self.expect_kw("projection")
        name = self.expect_ident()
        self.expect_op("=")
        self.expect_op("[")
        paths = [self.parse_proj_path()]
        while self.accept_op(","):
            paths.append(self.parse_proj_path())
        self.expect_op("]")
        return self.node("Projection", {"name": name.value, "paths": paths}, t)

    def parse_proj_path(self):
        t = self.expect_field_name()
        parts = [t.value]
        while self.at("OP", "."):
            self.next()
            parts.append(self.expect_field_name().value)
        return self.node("ProjPath", {"parts": parts}, t)

    def parse_goal(self):
        t = self.expect_kw("goal")
        if self.at("KEYWORD", "derive"):
            self.next()
            return self.node("DeriveGoal", {"expr": self.parse_expr()}, t)
        if self.at("KEYWORD", "construct"):
            self.next()
            ty = self.parse_type_expr()
            self.expect_kw("satisfying")
            refs = self.parse_ident_list()
            return self.node("ConstructGoal", {"type": ty, "refs": refs}, t)
        if self.at("KEYWORD", "prove"):
            self.next()
            prop = self.parse_proposition()
            self.expect_kw("assuming")
            refs = self.parse_ident_list()
            return self.node("ProveGoal", {"prop": prop, "refs": refs}, t)
        if self.at("KEYWORD", "check"):
            self.next()
            f = self.expect_ident(); self.expect_kw("of"); h = self.expect_ident()
            return self.node("CheckGoal", {"fun": f.value, "impl": h.value}, t)
        if self.at("KEYWORD", "compare-models"):
            self.next()
            ty = self.parse_type_expr()
            self.expect_kw("satisfying")
            refs = self.parse_ident_list()
            under = None
            if self.accept_kw("under"):
                under = self.expect_ident().value
            return self.node("CompareGoal", {"type": ty, "refs": refs, "under": under}, t)
        c = self.peek()
        raise ParseError(f"expected goal kind, found {c.raw!r}", c.line, c.col)

    def parse_ident_list(self):
        self.expect_op("[")
        names = []
        if not self.at("OP", "]"):
            names.append(self.expect_ident().value)
            while self.accept_op(","):
                names.append(self.expect_ident().value)
        self.expect_op("]")
        return names

    def parse_verification(self):
        t = self.expect_kw("verification")
        self.expect_op("{")
        items = []
        while not self.at("OP", "}"):
            if self.at("OP", ";"):
                self.next(); continue
            items.append(self.parse_verif_item())
            self.expect_op(";")
        self.expect_op("}")
        return self.node("Verification", {"items": items}, t)

    def parse_verif_item(self):
        t = self.peek()
        if self.at("KEYWORD", "proof"):
            self.next(); self.expect_op(":")
            if self.accept_kw("none"):
                return self.node("ProofReq", {"mode": "none"}, t)
            self.expect_kw("kernel-checked"); self.expect_kw("by")
            cid = self.parse_checker_id()
            q = self.parse_qualifier()
            return self.node("ProofReq", {"mode": "kernel-checked",
                                          "checker": cid, "qualifier": q}, t)
        if self.at("KEYWORD", "recompute"):
            self.next(); self.expect_op(":")
            if self.accept_kw("none"):
                return self.node("RecomputeReq", {"mode": "none"}, t)
            self.expect_kw("by")
            cid = self.parse_checker_id()
            q = self.parse_qualifier()
            return self.node("RecomputeReq", {"mode": "by", "checker": cid,
                                              "qualifier": q}, t)
        if self.at("KEYWORD", "test"):
            self.next(); self.expect_op(":")
            if self.accept_kw("none"):
                return self.node("TestReq", {"mode": "none"}, t)
            if self.accept_kw("differential"):
                self.expect_kw("by")
                cid = self.parse_checker_id()
                q = self.parse_qualifier()
                return self.node("TestReq", {"mode": "differential",
                                             "checker": cid, "qualifier": q}, t)
            self.expect_kw("property-fuzz")
            cfg = self.parse_fuzz_config()
            q = self.parse_qualifier()
            return self.node("TestReq", {"mode": "property-fuzz",
                                         "config": cfg, "qualifier": q}, t)
        if self.at("KEYWORD", "assurance"):
            self.next(); self.expect_op(":")
            if self.accept_kw("none"):
                return self.node("AssuranceReq", {"mode": "none"}, t)
            if self.accept_kw("level-a"):
                self.expect_kw("required")
                return self.node("AssuranceReq", {"mode": "level-a"}, t)
            self.expect_kw("level-b"); self.expect_kw("accepted")
            return self.node("AssuranceReq", {"mode": "level-b"}, t)
        raise ParseError(f"expected verification item, found {t.raw!r}", t.line, t.col)

    def parse_checker_id(self):
        slug = self.parse_slug()
        self.expect_op("/")
        t = self.peek()
        if t.kind != "SEMVER":
            raise ParseError(f"expected version, found {t.raw!r}", t.line, t.col)
        self.next()
        return self.node("CheckerID", {"slug": slug, "version": t.value},
                         slug)

    def parse_qualifier(self):
        if self.accept_kw("required"):
            return "required"
        if self.accept_kw("optional"):
            return "optional"
        return None  # default applied in typecheck (D-031): required

    def parse_fuzz_config(self):
        t = self.expect_op("{")
        # reconstruct token for location
        self.expect_kw("seeds"); self.expect_op(":"); self.expect_op("[")
        seeds = [self.expect_nat()]
        while self.accept_op(","):
            seeds.append(self.expect_nat())
        self.expect_op("]"); self.expect_op(",")
        self.expect_kw("cases"); self.expect_op(":")
        cases = self.expect_nat()
        self.expect_op("}")
        return {"seeds": seeds, "cases": cases}

    def expect_nat(self):
        t = self.peek()
        if t.kind != "NAT":
            raise ParseError(f"expected natural number, found {t.raw!r}", t.line, t.col)
        self.next()
        return t.value

    def parse_resource_limits(self):
        t = self.expect_kw("limits")
        self.expect_op("{")
        self.expect_kw("timeout"); self.expect_op(":")
        dt = self.peek()
        if dt.kind != "DURATION":
            raise ParseError(f"expected duration, found {dt.raw!r}", dt.line, dt.col)
        self.next()
        timeout = dt.value
        self.expect_op(";")
        memory = steps = None
        if self.accept_kw("memory"):
            self.expect_op(":")
            mt = self.peek()
            if mt.kind != "MEMSIZE":
                raise ParseError(f"expected memory size, found {mt.raw!r}", mt.line, mt.col)
            self.next(); memory = mt.value; self.expect_op(";")
        if self.accept_kw("steps"):
            self.expect_op(":")
            steps = self.expect_nat(); self.expect_op(";")
        self.expect_op("}")
        return self.node("ResourceLimits", {"timeout": timeout, "memory": memory,
                                            "steps": steps}, t)

    def parse_provenance_req(self):
        t = self.expect_kw("record")
        self.expect_op(":")
        if self.accept_kw("all"):
            return self.node("ProvenanceReq", {"mode": "all"}, t)
        self.expect_op("[")
        items = []
        for kw in ("spec-hash", "input-hash", "tool-versions", "witness", "outputs"):
            pass
        items.append(self.parse_prov_item())
        while self.accept_op(","):
            items.append(self.parse_prov_item())
        self.expect_op("]")
        return self.node("ProvenanceReq", {"mode": "list", "items": items}, t)

    def parse_prov_item(self):
        t = self.peek()
        if t.kind == "KEYWORD" and t.value in ("spec-hash", "input-hash",
                                               "tool-versions", "witness", "outputs"):
            self.next()
            return t.value
        raise ParseError(f"expected provenance item, found {t.raw!r}", t.line, t.col)

    # ---- TypeExpr ----
    _BASE_TYPES = ("String", "Nat", "Int", "Real", "Rat", "Binary64", "Bool")

    def parse_type_expr(self):
        t = self.peek()
        # NEW-A9: "Set" removed from v0 surface syntax (reserved).
        if self.at_ctx("Set"):
            raise ParseError("'Set' is reserved for future use in v0 (no introduction form)",
                             t.line, t.col)
        if self.at_ctx("Option"):
            self.next(); self.expect_op("<")
            inner = self.parse_type_expr(); self.expect_op(">")
            return self.node("OptionType", {"elem": inner}, t)
        if self.at_ctx("Impl"):
            return self.parse_impl_type()
        if t.kind == "IDENT" and t.value in self._BASE_TYPES:
            self.next()
            return self.node("BaseType", {"name": t.value}, t)
        if t.kind == "IDENT":
            self.next()
            return self.node("NamedType", {"name": t.value}, t)
        if self.at("OP", "{"):
            self.next()
            fields = []
            if not self.at("OP", "}"):
                f = self.expect_field_name(); self.expect_op(":")
                ty = self.parse_type_expr()
                fields.append((f.value, ty))
                while self.accept_op(","):
                    f = self.expect_field_name(); self.expect_op(":")
                    ty = self.parse_type_expr()
                    fields.append((f.value, ty))
            self.expect_op("}")
            return self.node("RecordType", {"fields": fields}, t)
        if self.at("OP", "["):
            self.next()
            inner = self.parse_type_expr(); self.expect_op("]")
            return self.node("ListType", {"elem": inner}, t)
        if self.at("OP", "("):
            self.next()
            args = []
            if not self.at("OP", ")"):
                args.append(self.parse_type_expr())
                while self.accept_op(","):
                    args.append(self.parse_type_expr())
            self.expect_op(")")
            self.expect_op("->")
            ret = self.parse_type_expr()
            return self.node("FunType", {"args": args, "ret": ret}, t)
        raise ParseError(f"expected type expression, found {t.raw!r}", t.line, t.col)

    def parse_impl_type(self):
        t = self.expect_ctx("Impl")
        self.expect_op("(")
        a = self.parse_type_expr()
        self.expect_op("->")
        b = self.parse_type_expr()
        self.expect_op(")")
        return self.node("ImplType", {"arg": a, "ret": b}, t)

    # ---- Expr (precedence chain) ----
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        t = self.peek()
        left = self.parse_and()
        while self.at("OP", "\\/"):
            op = self.next()
            right = self.parse_and()
            left = self.node("BinOp", {"op": "\\/", "left": left, "right": right}, op)
        return left

    def parse_and(self):
        left = self.parse_impl()
        while self.at("OP", "/\\"):
            op = self.next()
            right = self.parse_impl()
            left = self.node("BinOp", {"op": "/\\", "left": left, "right": right}, op)
        return left

    def parse_impl(self):
        left = self.parse_cmp()
        if self.at("OP", "==>"):
            op = self.next()
            right = self.parse_cmp()
            return self.node("BinOp", {"op": "==>", "left": left, "right": right}, op)
        return left

    def parse_cmp(self):
        left = self.parse_add()
        t = self.peek()
        if t.kind == "OP" and t.value in ("==", "!=", "<", "<=", ">", ">="):
            op = self.next()
            right = self.parse_add()
            return self.node("BinOp", {"op": op.value, "left": left, "right": right}, op)
        return left

    def parse_add(self):
        left = self.parse_mul()
        while self.at("OP", "+") or self.at("OP", "-"):
            op = self.next()
            right = self.parse_mul()
            left = self.node("BinOp", {"op": op.value, "left": left, "right": right}, op)
        return left

    def parse_mul(self):
        left = self.parse_unary()
        while self.at("OP", "*") or self.at("OP", "/"):
            op = self.next()
            right = self.parse_unary()
            left = self.node("BinOp", {"op": op.value, "left": left, "right": right}, op)
        return left

    def parse_unary(self):
        t = self.peek()
        if t.kind == "OP" and t.value in ("!", "-"):
            op = self.next()
            operand = self.parse_postfix()
            return self.node("UnOp", {"op": op.value, "operand": operand}, op)
        return self.parse_postfix()

    def parse_postfix(self):
        base = self.parse_atom()
        while True:
            if self.at("OP", "."):
                op = self.next()
                f = self.expect_field_name()
                base = self.node("FieldAccess", {"base": base, "field": f.value}, op)
            elif self.at("OP", "["):
                op = self.next()
                idx = self.parse_expr()
                self.expect_op("]")
                base = self.node("Index", {"base": base, "index": idx}, op)
            else:
                return base

    def parse_atom(self):
        t = self.peek()
        if t.kind in ("STRING", "NAT", "REALLIT", "HEXFLOAT"):
            return self.parse_literal()
        if t.kind == "KEYWORD" and t.value in ("true", "false", "none"):
            self.next()
            return self.node("Literal", {"lit": t.value}, t)
        if t.kind == "IDENT":
            self.next()
            if self.at("OP", "("):
                self.next()
                args = []
                if not self.at("OP", ")"):
                    args.append(self.parse_expr())
                    while self.accept_op(","):
                        args.append(self.parse_expr())
                self.expect_op(")")
                return self.node("Call", {"fun": t.value, "args": args}, t)
            return self.node("Var", {"name": t.value}, t)
        if self.at("OP", "("):
            self.next()
            e = self.parse_expr()
            self.expect_op(")")
            return e
        if self.at("OP", "{"):
            return self.parse_record_literal()
        if self.at("KEYWORD", "if"):
            self.next()
            cond = self.parse_proposition()
            self.expect_kw("then")
            th = self.parse_expr()
            self.expect_kw("else")
            el = self.parse_expr()
            return self.node("If", {"cond": cond, "then": th, "else": el}, t)
        if self.at("KEYWORD", "let"):
            self.next()
            name = self.expect_ident()
            self.expect_op("=")
            val = self.parse_expr()
            self.expect_kw("in")
            body = self.parse_expr()
            return self.node("Let", {"name": name.value, "value": val, "body": body}, t)
        if self.at("KEYWORD", "case"):
            self.next()
            scrut = self.parse_expr()
            self.expect_kw("of"); self.expect_kw("some"); self.expect_op("(")
            binder = self.expect_ident(); self.expect_op(")")
            self.expect_op("->")
            some_b = self.parse_expr()
            self.expect_op("|"); self.expect_kw("none"); self.expect_op("->")
            none_b = self.parse_expr()
            return self.node("Case", {"scrut": scrut, "binder": binder.value,
                                      "some": some_b, "none": none_b}, t)
        if self.at("KEYWORD", "some"):
            self.next(); self.expect_op("(")
            e = self.parse_expr(); self.expect_op(")")
            return self.node("Some", {"expr": e}, t)
        if t.kind == "KEYWORD" and t.value in ("forall", "exists"):
            self.next()
            var = self.expect_ident()
            self.expect_kw("in")
            dom = self.parse_domain()
            self.expect_op("::")
            self.expect_op("(")
            body = self.parse_proposition()
            self.expect_op(")")
            kind = "Forall" if t.value == "forall" else "Exists"
            return self.node(kind, {"var": var.value, "domain": dom, "body": body}, t)
        raise ParseError(f"expected expression, found {t.raw!r}", t.line, t.col)

    def parse_record_literal(self):
        t = self.expect_op("{")
        fields = []
        if not self.at("OP", "}"):
            f = self.expect_field_name(); self.expect_op(":")
            e = self.parse_expr()
            fields.append((f.value, e))
            while self.accept_op(","):
                f = self.expect_field_name(); self.expect_op(":")
                e = self.parse_expr()
                fields.append((f.value, e))
        self.expect_op("}")
        return self.node("RecordLit", {"fields": fields}, t)

    def parse_domain(self):
        t = self.peek()
        if self.at("KEYWORD", "type"):
            self.next()
            ty = self.parse_type_expr()
            return self.node("TypeDomain", {"type": ty}, t)
        return self.node("ExprDomain", {"expr": self.parse_expr()}, t)

    def parse_literal(self):
        t = self.next()
        return self.node("Literal", {"lit": t.kind, "value": t.value, "raw": t.raw}, t)

    def parse_proposition(self):
        return self.parse_expr()

    def parse_predicate(self):
        return self.parse_expr()


def parse(source):
    return Parser(lex(source)).parse_specification()


# ---- grammar-conformance support: every production needs a parse method ----
_METHOD_FOR_PRODUCTION = {
    "Specification": "parse_specification",
    "Header": "parse_header",
    "Body": "parse_body",
    "Definition": "parse_definition",
    "TypeAlias": "parse_type_alias",
    "ValueDef": "parse_definition",
    "FunDef": "parse_definition",
    "Params": "parse_params",
    "AxiomDecl": "parse_definition",
    "AssumptionDecl": "parse_definition",
    "ExternalDecl": "parse_definition",
    "ConstraintGroup": "parse_constraint_group",
    "Constraint": "parse_constraint_group",
    "Projection": "parse_projection",
    "ProjPath": "parse_proj_path",
    "Goal": "parse_goal",
    "DeriveGoal": "parse_goal",
    "ConstructGoal": "parse_goal",
    "ProveGoal": "parse_goal",
    "CheckGoal": "parse_goal",
    "CompareGoal": "parse_goal",
    "Verification": "parse_verification",
    "VerifItem": "parse_verif_item",
    "ProofReq": "parse_verif_item",
    "RecomputeReq": "parse_verif_item",
    "TestReq": "parse_verif_item",
    "AssuranceReq": "parse_verif_item",
    "Qualifier": "parse_qualifier",
    "FuzzConfig": "parse_fuzz_config",
    "ResourceLimits": "parse_resource_limits",
    "ProvenanceReq": "parse_provenance_req",
    "ProvItem": "parse_prov_item",
    "TypeExpr": "parse_type_expr",
    "ImplType": "parse_impl_type",
    "Expr": "parse_expr",
    "OrExpr": "parse_or",
    "AndExpr": "parse_and",
    "ImplExpr": "parse_impl",
    "CmpExpr": "parse_cmp",
    "AddExpr": "parse_add",
    "MulExpr": "parse_mul",
    "Unary": "parse_unary",
    "Postfix": "parse_postfix",
    "Atom": "parse_atom",
    "Domain": "parse_domain",
    "Literal": "parse_literal",
    "Proposition": "parse_proposition",
    "Predicate": "parse_predicate",
}

def check_production_coverage():
    """Every production in grammar.py must have a parser method."""
    missing = [p for p in PRODUCTION_NAMES
               if _METHOD_FOR_PRODUCTION.get(p) not in dir(Parser)]
    extra = [m for m in _METHOD_FOR_PRODUCTION.values()
             if m not in dir(Parser)]
    return missing, extra

```
