"""M8 type checker for the MSVE formal language (v0.8).

Implements the §B.4 typing rules, plus:
- D-025 (R13): record-construction typing with expected-type propagation,
  duplicate/unknown/missing field detection.
- D-031 (R14): verification-item cardinality/conflict rules; Qualifier
  default = required.
- Goal/reference checks (§B.5): assuming/satisfying/under resolution,
  check-goal invocation rule, `cases: 0` admission rejection.

Error category: 'type' for typing failures, 'admission' for
specification-admission rule violations.
"""
from .resolve import BUILTINS

# ---- type representation ----
# 'String'|'Nat'|'Int'|'Real'|'Rat'|'Binary64'|'Bool'
# ('record', ((field, type), ...))  -- fields sorted by name
# ('list', t) | ('set', t) | ('option', t)
# ('fn', ((argtypes), ret)) | ('impl', (a, b)) | ('var', name)

def record(fields):
    return ("record", tuple(sorted(fields)))

CANDIDATE = record([("uci", "String"), ("rank", "Nat"), ("score", "Binary64")])
DECODE_OUTCOME = record([
    ("ok", "Bool"),
    ("candidates", ("list", CANDIDATE)),
    ("error", ("option", "String")),
])

BUILTIN_SCHEMES = {
    "len":                 ([("list", ("var", "T"))], "Nat"),
    "range":               (["Nat"], ("list", "Nat")),
    "is_finite":           (["Binary64"], "Bool"),
    "is_ascii_printable":  (["String"], "Bool"),
    "has_no_whitespace":   (["String"], "Bool"),
    "is_some":             ([("option", ("var", "T"))], "Bool"),
    "to_rat":              (["Real"], "Rat"),
    "decode_candidates":   (["String"], DECODE_OUTCOME),
}

class CheckError(Exception):
    def __init__(self, msg, node_or_line, col=None, category="type"):
        if col is None:
            # called as CheckError(msg, node)
            node = node_or_line
            line, col = node.line, node.col
        else:
            line = node_or_line
        super().__init__(f"{category} error at {line}:{col}: {msg}")
        self.line, self.col, self.category = line, col, category

def _resolve_alias(t, aliases, seen=()):
    if isinstance(t, str) and t in aliases:
        if t in seen:
            # NEW-A4: categorized diagnostic, not a crash (was ValueError).
            raise CheckError(f"cyclic type alias {t}", 0, 0, "admission")
        return _resolve_alias(aliases[t], aliases, seen + (t,))
    if isinstance(t, tuple):
        if t[0] == "record":
            return ("record", tuple(sorted((f, _resolve_alias(x, aliases, seen))
                                           for f, x in t[1])))
        if t[0] in ("list", "set", "option"):
            return (t[0], _resolve_alias(t[1], aliases, seen))
        if t[0] == "fn":
            return ("fn", (tuple(_resolve_alias(a, aliases, seen) for a in t[1][0]),
                           _resolve_alias(t[1][1], aliases, seen)))
        if t[0] == "impl":
            return ("impl", (_resolve_alias(t[1][0], aliases, seen),
                             _resolve_alias(t[1][1], aliases, seen)))
    return t

def _unify(t1, t2, subst):
    t1 = _apply(t1, subst); t2 = _apply(t2, subst)
    if t1 == t2:
        return subst
    if isinstance(t1, tuple) and t1[0] == "var":
        return _bind(t1[1], t2, subst)
    if isinstance(t2, tuple) and t2[0] == "var":
        return _bind(t2[1], t1, subst)
    if isinstance(t1, tuple) and isinstance(t2, tuple) and t1[0] == t2[0]:
        if t1[0] == "record":
            if [f for f, _ in t1[1]] != [f for f, _ in t2[1]]:
                return None
            for (_, a), (_, b) in zip(t1[1], t2[1]):
                subst = _unify(a, b, subst)
                if subst is None:
                    return None
            return subst
        if t1[0] in ("list", "set", "option"):
            return _unify(t1[1], t2[1], subst)
        if t1[0] == "fn":
            if len(t1[1][0]) != len(t2[1][0]):
                return None
            for a, b in zip(t1[1][0], t2[1][0]):
                subst = _unify(a, b, subst)
                if subst is None:
                    return None
            return _unify(t1[1][1], t2[1][1], subst)
        if t1[0] == "impl":
            subst = _unify(t1[1][0], t2[1][0], subst)
            return subst and _unify(t1[1][1], t2[1][1], subst)
    return None

def _bind(var, t, subst):
    if ("var", var) in subst:
        return _unify(subst[("var", var)], t, subst)
    if t == ("var", var):
        return subst
    # occurs check
    if _occurs(var, t, subst):
        return None
    subst[("var", var)] = t
    return subst

def _occurs(var, t, subst):
    t = _apply(t, subst)
    if t == ("var", var):
        return True
    if isinstance(t, tuple):
        if t[0] == "record":
            return any(_occurs(var, x, subst) for _, x in t[1])
        if t[0] in ("list", "set", "option"):
            return _occurs(var, t[1], subst)
        if t[0] == "fn":
            return any(_occurs(var, a, subst) for a in t[1][0]) or _occurs(var, t[1][1], subst)
        if t[0] == "impl":
            return _occurs(var, t[1][0], subst) or _occurs(var, t[1][1], subst)
    return False

def _apply(t, subst):
    if isinstance(t, tuple) and t[0] == "var":
        if t in subst:
            return _apply(subst[t], subst)
        return t
    if isinstance(t, tuple):
        if t[0] == "record":
            return ("record", tuple(sorted((f, _apply(x, subst)) for f, x in t[1])))
        if t[0] in ("list", "set", "option"):
            return (t[0], _apply(t[1], subst))
        if t[0] == "fn":
            return ("fn", (tuple(_apply(a, subst) for a in t[1][0]), _apply(t[1][1], subst)))
        if t[0] == "impl":
            return ("impl", (_apply(t[1][0], subst), _apply(t[1][1], subst)))
    if isinstance(t, str):
        return subst.get(t, t)
    return t

def type_eq(t1, t2, aliases):
    t1 = _resolve_alias(t1, aliases); t2 = _resolve_alias(t2, aliases)
    return _unify(t1, t2, {}) is not None

def fmt(t):
    if isinstance(t, str):
        return t
    if t[0] == "record":
        return "{" + ", ".join(f"{f}: {fmt(x)}" for f, x in t[1]) + "}"
    if t[0] in ("list", "set", "option"):
        inner = fmt(t[1])
        return {"list": f"[{inner}]", "set": f"Set<{inner}>",
                "option": f"Option<{inner}>"}[t[0]]
    if t[0] == "fn":
        return "(" + ", ".join(fmt(a) for a in t[1][0]) + ") -> " + fmt(t[1][1])
    if t[0] == "impl":
        return f"Impl({fmt(t[1][0])} -> {fmt(t[1][1])})"
    if t[0] == "var":
        return f"?{t[1]}"
    return str(t)

class Checker:
    def __init__(self, resolver):
        self.r = resolver
        self.aliases = {}   # type alias name -> type
        self.tenv = {}      # top-level value/function name -> type
        self.errors = []
        self._var_counter = 0

    def err(self, msg, node, category="type"):
        self.errors.append(CheckError(msg, node.line, node.col, category))

    def fresh(self, base):
        self._var_counter += 1
        return ("var", f"{base}${self._var_counter}")

    # ---- entry ----
    def check(self, spec):
        body = spec.fields["body"]
        self.build_tenv(body)
        for d in body.fields["definitions"]:
            self.check_definition(d)
        self.check_goal(body.fields["goal"], body)
        self.check_verification(body.fields["verification"], body.fields["goal"])
        self.check_limits(body.fields["limits"])
        return self.errors

    def build_tenv(self, body):
        for d in body.fields["definitions"]:
            k = d.kind
            if k == "TypeAlias":
                try:
                    self.aliases[d.fields["name"]] = self.type_of_texpr(
                        d.fields["type"], d)
                except CheckError as e:
                    self.errors.append(e)
        # NEW-A4: detect cyclic aliases after all are collected.
        for name in list(self.aliases):
            try:
                _resolve_alias(name, self.aliases)
            except CheckError as e:
                self.errors.append(e)
                # break the cycle so later uses don't cascade
                self.aliases[name] = "Nat"
        for d in body.fields["definitions"]:
            k = d.kind
            if k == "TypeAlias":
                continue
            elif k == "ValueDef":
                try:
                    self.tenv[d.fields["name"]] = self.type_of_texpr(
                        d.fields["type"], d)
                except CheckError as e:
                    self.errors.append(e)
            elif k == "FunDef":
                try:
                    at = tuple(self.type_of_texpr(p.fields["type"], p)
                               for p in d.fields["params"])
                    rt = self.type_of_texpr(d.fields["rtype"], d)
                    self.tenv[d.fields["name"]] = ("fn", (at, rt))
                except CheckError as e:
                    self.errors.append(e)
            elif k == "ExternalDecl":
                try:
                    self.tenv[d.fields["name"]] = self.type_of_texpr(
                        d.fields["type"], d)
                except CheckError as e:
                    self.errors.append(e)

    def type_of_texpr(self, node, ctx):
        k = node.kind
        if k == "BaseType":
            return node.fields["name"]
        if k == "NamedType":
            name = node.fields["name"]
            if name not in self.aliases and name not in self.r.type_aliases:
                # NEW-A5: unbound type names are an error (was silently allowed).
                raise CheckError(f"unbound type name '{name}'", node,
                                 category="name-resolution")
            return name
        if k == "RecordType":
            seen = set()
            fields = []
            for fname, ftype in node.fields["fields"]:
                if fname in seen:
                    raise CheckError(f"duplicate field '{fname}' in record type",
                                     node)
                seen.add(fname)
                fields.append((fname, self.type_of_texpr(ftype, ctx)))
            return record(fields)
        if k == "ListType":
            return ("list", self.type_of_texpr(node.fields["elem"], ctx))
        if k == "SetType":
            return ("set", self.type_of_texpr(node.fields["elem"], ctx))
        if k == "OptionType":
            return ("option", self.type_of_texpr(node.fields["elem"], ctx))
        if k == "FunType":
            at = tuple(self.type_of_texpr(a, ctx) for a in node.fields["args"])
            rt = self.type_of_texpr(node.fields["ret"], ctx)
            return ("fn", (at, rt))
        if k == "ImplType":
            a = self.type_of_texpr(node.fields["arg"], ctx)
            b = self.type_of_texpr(node.fields["ret"], ctx)
            return ("impl", (a, b))
        raise CheckError(f"bad type expression {k}", node)

    # ---- definitions ----
    def check_definition(self, d):
        k = d.kind
        if k in ("TypeAlias", "AxiomDecl", "AssumptionDecl", "ExternalDecl"):
            if k in ("AxiomDecl", "AssumptionDecl"):
                try:
                    # Axioms/assumptions take no locals, but quantifier
                    # binders inside their propositions must still resolve.
                    from .resolve import Resolver as _Resolver
                    r2 = _Resolver()
                    r2.defs, r2.type_aliases = self.r.defs, self.r.type_aliases
                    r2.resolve_expr(d.fields["prop"], {}, allow_output=False)
                    for re_ in r2.errors:
                        self.errors.append(CheckError(str(re_), re_.line, re_.col,
                                                      "name-resolution"))
                    t = self.check_expr(d.fields["prop"], dict(self.tenv), None)
                    self.expect_bool(t, d.fields["prop"], "axiom/assume proposition")
                except CheckError as e:
                    self.errors.append(e)
            return
        name = d.fields["name"]
        declared = self.tenv.get(name)
        env = dict(self.tenv)
        body_expected = declared
        if k == "FunDef":
            for p in d.fields["params"]:
                try:
                    env[p.fields["name"]] = self.type_of_texpr(p.fields["type"], p)
                except CheckError as e:
                    self.errors.append(e)
            # the body is checked against the RETURN type, not the fn type
        try:
            fn = _resolve_alias(declared, self.aliases)
            if isinstance(fn, tuple) and fn[0] == "fn":
                body_expected = fn[1][1]
            got = self.check_expr(d.fields["body"], env, body_expected)
            if body_expected is not None and not type_eq(got, body_expected, self.aliases):
                self.err(f"body has type {fmt(_resolve_alias(got, self.aliases))}, "
                         f"declared {fmt(_resolve_alias(body_expected, self.aliases))}", d)
        except CheckError as e:
            self.errors.append(e)

    # ---- expressions ----
    def check_expr(self, e, env, expected):
        k = e.kind
        if k == "Literal":
            return self.check_literal(e, expected)
        if k == "Var":
            return self.check_var(e, env)
        if k == "Call":
            return self.check_call(e, env)
        if k == "BinOp":
            return self.check_binop(e, env)
        if k == "UnOp":
            return self.check_unop(e, env)
        if k == "If":
            return self.check_if(e, env, expected)
        if k == "Let":
            vt = self.check_expr(e.fields["value"], env, None)
            env2 = dict(env); env2[e.fields["name"]] = vt
            return self.check_expr(e.fields["body"], env2, expected)
        if k == "Case":
            return self.check_case(e, env, expected)
        if k == "Some":
            it = self.check_expr(e.fields["expr"], env, None)
            t = ("option", it)
            if expected is not None and not type_eq(t, expected, self.aliases):
                raise CheckError(f"some(_) has type {fmt(t)}, expected {fmt(expected)}", e)
            return t
        if k in ("Forall", "Exists"):
            return self.check_quant(e, env)
        if k == "FieldAccess":
            bt = self.check_expr(e.fields["base"], env, None)
            bt = _resolve_alias(bt, self.aliases)
            if not (isinstance(bt, tuple) and bt[0] == "record"):
                raise CheckError(f"field access on non-record type {fmt(bt)}", e)
            for f, ft in bt[1]:
                if f == e.fields["field"]:
                    return ft
            raise CheckError(f"record has no field '{e.fields['field']}'", e)
        if k == "Index":
            bt = self.check_expr(e.fields["base"], env, None)
            bt = _resolve_alias(bt, self.aliases)
            if not (isinstance(bt, tuple) and bt[0] == "list"):
                raise CheckError(f"indexing non-list type {fmt(bt)}", e)
            it = self.check_expr(e.fields["index"], env, None)
            if not type_eq(it, "Nat", self.aliases):
                raise CheckError(f"list index must be Nat, got {fmt(it)}", e)
            return bt[1]
        if k == "RecordLit":
            return self.check_record_lit(e, env, expected)
        raise CheckError(f"unhandled expression kind {k}", e)

    def check_literal(self, e, expected):
        lit = e.fields["lit"]
        if lit == "STRING":
            t = "String"
        elif lit == "NAT":
            t = "Nat"
        elif lit == "REALLIT":
            t = "Real"
        elif lit == "HEXFLOAT":
            t = "Binary64"
        elif lit in ("true", "false"):
            t = "Bool"
        elif lit == "none":
            t = ("option", self.fresh("T"))
        else:
            raise CheckError(f"unknown literal {lit}", e)
        if expected is not None and not type_eq(t, expected, self.aliases):
            raise CheckError(f"literal has type {fmt(t)}, expected {fmt(expected)}", e)
        return _apply(t, {}) if not isinstance(t, tuple) or t[0] != "var" else t

    def check_var(self, e, env):
        res = e.fields.get("resolved")
        name = e.fields["name"]
        if res is None:
            raise CheckError(f"unresolved variable '{name}'", e)
        tag = res[0]
        if tag == "local" or tag == "output":
            if name not in env:
                raise CheckError(f"'{name}' not in scope", e)
            return env[name]
        if tag == "define":
            if name not in self.tenv:
                raise CheckError(f"definition '{name}' has no type", e)
            return _resolve_alias(self.tenv[name], self.aliases)
        if tag == "builtin":
            raise CheckError(f"builtin '{name}' used as a value; builtins are call-only", e)
        raise CheckError(f"cannot resolve '{name}'", e)

    def check_call(self, e, env):
        res = e.fields.get("resolved")
        name = e.fields["fun"]
        args = [self.check_expr(a, env, None) for a in e.fields["args"]]
        if res is None:
            raise CheckError(f"unresolved callee '{name}'", e)
        tag = res[0]
        if tag == "builtin":
            atypes, ret = BUILTIN_SCHEMES[name]
            # freshen type vars
            mapping = {}
            def fresh_t(t):
                if isinstance(t, tuple) and t[0] == "var":
                    if t[1] not in mapping:
                        mapping[t[1]] = self.fresh(t[1])
                    return mapping[t[1]]
                if isinstance(t, tuple):
                    if t[0] == "record":
                        return ("record", tuple(sorted((f, fresh_t(x)) for f, x in t[1])))
                    if t[0] in ("list", "set", "option"):
                        return (t[0], fresh_t(t[1]))
                    if t[0] == "fn":
                        return ("fn", (tuple(fresh_t(a) for a in t[1][0]), fresh_t(t[1][1])))
                    if t[0] == "impl":
                        return ("impl", (fresh_t(t[1][0]), fresh_t(t[1][1])))
                return t
            atypes = [fresh_t(a) for a in atypes]
            ret = fresh_t(ret)
            if len(args) != len(atypes):
                raise CheckError(
                    f"builtin '{name}' expects {len(atypes)} arguments, got {len(args)}", e)
            subst = {}
            for a, formal in zip(args, atypes):
                ar = _resolve_alias(a, self.aliases)
                subst = _unify(ar, formal, subst)
                if subst is None:
                    raise CheckError(
                        f"builtin '{name}': argument type {fmt(ar)} does not match "
                        f"{fmt(formal)}", e)
            return _apply(ret, subst)
        if tag == "define":
            ft = self.tenv.get(name)
            ft = _resolve_alias(ft, self.aliases)
            if not (isinstance(ft, tuple) and ft[0] == "fn"):
                raise CheckError(f"'{name}' is not a function", e)
            formals, ret = ft[1]
            if len(args) != len(formals):
                raise CheckError(
                    f"'{name}' expects {len(formals)} arguments, got {len(args)}", e)
            for a, formal in zip(args, formals):
                if not type_eq(a, formal, self.aliases):
                    raise CheckError(
                        f"'{name}': argument type {fmt(a)} does not match {fmt(formal)}", e)
            return ret
        if tag == "local":
            # NEW-A8: a local with a function type is callable.
            lt = env.get(name)
            lt = _resolve_alias(lt, self.aliases) if lt else None
            if isinstance(lt, tuple) and lt[0] == "fn":
                formals, ret = lt[1]
                if len(args) != len(formals):
                    raise CheckError(
                        f"'{name}' expects {len(formals)} arguments, got {len(args)}", e)
                for a, formal in zip(args, formals):
                    if not type_eq(a, formal, self.aliases):
                        raise CheckError(
                            f"'{name}': argument type {fmt(a)} does not match {fmt(formal)}", e)
                return ret
            raise CheckError(f"calling a local variable '{name}' (not a function)", e)
        raise CheckError(f"cannot call '{name}'", e)

    NUMERIC = ("Nat", "Int", "Real", "Rat", "Binary64")

    def check_binop(self, e, env):
        op = e.fields["op"]
        lt = self.check_expr(e.fields["left"], env, None)
        rt = self.check_expr(e.fields["right"], env, None)
        l = _resolve_alias(lt, self.aliases); r = _resolve_alias(rt, self.aliases)
        if op in ("+", "-", "*"):
            return self.arith_result(op, l, r, e)
        if op == "/":
            if l == r and l in self.NUMERIC:
                return l
            if {l, r} <= {"Nat", "Int"}:
                return "Int" if "Int" in (l, r) else "Nat"
            raise CheckError(f"/ requires same numeric type, got {fmt(l)} and {fmt(r)}", e)
        if op in ("==", "!="):
            if not type_eq(l, r, self.aliases):
                raise CheckError(f"{op} requires same type, got {fmt(l)} and {fmt(r)}", e)
            return "Bool"
        if op in ("<", "<=", ">", ">="):
            if l == r and l in self.NUMERIC + ("String",):
                return "Bool"
            raise CheckError(f"{op} requires matching ordered type, got {fmt(l)} and {fmt(r)}", e)
        if op in ("\\/", "/\\", "==>"):
            self.expect_bool(l, e.fields["left"], op)
            self.expect_bool(r, e.fields["right"], op)
            return "Bool"
        raise CheckError(f"unknown operator {op}", e)

    def arith_result(self, op, l, r, e):
        if l == r and l in self.NUMERIC:
            return l
        if {l, r} <= {"Nat", "Int"}:
            return "Int"  # the one exact embedding
        raise CheckError(
            f"{op} requires same numeric type (or Nat/Int), got {fmt(l)} and {fmt(r)}", e)

    def check_unop(self, e, env):
        op = e.fields["op"]
        t = _resolve_alias(self.check_expr(e.fields["operand"], env, None), self.aliases)
        if op == "!":
            self.expect_bool(t, e, "!")
            return "Bool"
        if op == "-":
            table = {"Nat": "Int", "Int": "Int", "Real": "Real",
                     "Rat": "Rat", "Binary64": "Binary64"}
            if t in table:
                return table[t]
            raise CheckError(f"unary - requires numeric type, got {fmt(t)}", e)
        raise CheckError(f"unknown unary operator {op}", e)

    def expect_bool(self, t, node, ctx):
        if not type_eq(t, "Bool", self.aliases):
            raise CheckError(f"{ctx} requires Bool, got {fmt(t)}", node)

    def check_if(self, e, env, expected):
        ct = self.check_expr(e.fields["cond"], env, None)
        self.expect_bool(ct, e.fields["cond"], "if condition")
        tt = self.check_expr(e.fields["then"], env, expected)
        et = self.check_expr(e.fields["else"], env, expected)
        if not type_eq(tt, et, self.aliases):
            raise CheckError(f"if branches have different types {fmt(tt)} vs {fmt(et)}", e)
        if expected is not None and not type_eq(tt, expected, self.aliases):
            raise CheckError(f"if has type {fmt(tt)}, expected {fmt(expected)}", e)
        return tt

    def check_case(self, e, env, expected):
        st = _resolve_alias(self.check_expr(e.fields["scrut"], env, None), self.aliases)
        if not (isinstance(st, tuple) and st[0] == "option"):
            raise CheckError(f"case scrutinee must be Option<T>, got {fmt(st)}", e)
        env2 = dict(env); env2[e.fields["binder"]] = st[1]
        t1 = self.check_expr(e.fields["some"], env2, expected)
        t2 = self.check_expr(e.fields["none"], env, expected)
        if not type_eq(t1, t2, self.aliases):
            raise CheckError(f"case branches have different types {fmt(t1)} vs {fmt(t2)}", e)
        if expected is not None and not type_eq(t1, expected, self.aliases):
            raise CheckError(f"case has type {fmt(t1)}, expected {fmt(expected)}", e)
        return t1

    def check_quant(self, e, env):
        dom = e.fields["domain"]
        if dom.kind == "TypeDomain":
            vt = self.type_of_texpr(dom.fields["type"], dom)
        else:
            dt = _resolve_alias(self.check_expr(dom.fields["expr"], env, None), self.aliases)
            # NEW-A10: Option is not an iterable domain (no defined semantics).
            if isinstance(dt, tuple) and dt[0] in ("list", "set"):
                vt = dt[1]
            else:
                raise CheckError(
                    f"quantifier domain must be 'type T' or a list/set, got {fmt(dt)}", e)
        env2 = dict(env); env2[e.fields["var"]] = vt
        bt = self.check_expr(e.fields["body"], env2, None)
        self.expect_bool(bt, e.fields["body"], "quantifier body")
        return "Bool"

    def check_record_lit(self, e, env, expected):
        # D-025: no duplicate fields; field types checked; against an
        # expected record type the field set must match exactly.
        seen = {}
        for fname, fexpr in e.fields["fields"]:
            if fname in seen:
                raise CheckError(f"duplicate field '{fname}' in record literal", e)
            seen[fname] = fexpr
        exp = _resolve_alias(expected, self.aliases) if expected is not None else None
        if exp is not None and not (isinstance(exp, tuple) and exp[0] == "record"):
            raise CheckError(f"record literal used where {fmt(exp)} expected", e)
        exp_fields = dict(exp[1]) if exp is not None else {}
        if exp is not None:
            lit_fields = set(seen)
            exp_names = set(exp_fields)
            if lit_fields != exp_names:
                missing = sorted(exp_names - lit_fields)
                unknown = sorted(lit_fields - exp_names)
                parts = []
                if missing:
                    parts.append(f"missing fields {missing}")
                if unknown:
                    parts.append(f"unknown fields {unknown}")
                raise CheckError("record literal field mismatch: " + "; ".join(parts), e)
        ftypes = []
        for fname, fexpr in e.fields["fields"]:
            fexp = exp_fields.get(fname)
            ft = self.check_expr(fexpr, env, fexp)
            if fexp is not None and not type_eq(ft, fexp, self.aliases):
                raise CheckError(
                    f"field '{fname}' has type {fmt(ft)}, expected {fmt(fexp)}", e)
            ftypes.append((fname, ft))
        return record(ftypes)

    # ---- goal ----
    def check_goal(self, goal, body):
        groups = {g.fields["name"]: g for g in body.fields["constraint_groups"]}
        projs = {p.fields["name"] for p in body.fields["projections"]}
        k = goal.kind
        if k == "DeriveGoal":
            try:
                self.check_expr(goal.fields["expr"], dict(self.tenv), None)
            except CheckError as e:
                self.errors.append(e)
        elif k == "ConstructGoal":
            for ref in goal.fields["refs"]:
                if ref not in groups:
                    self.err(f"unknown constraint group '{ref}'", goal, "admission")
            try:
                target = self.type_of_texpr(goal.fields["type"], goal)
            except CheckError as e:
                self.errors.append(e); return
            for ref in goal.fields["refs"]:
                self.check_output_scope(groups[ref], target)
        elif k == "ProveGoal":
            for ref in goal.fields["refs"]:
                if ref not in {d.fields["name"] for d in body.fields["definitions"]
                               if d.kind in ("AxiomDecl", "AssumptionDecl")}:
                    self.err(f"assuming '{ref}' is not an axiom/assumption", goal, "admission")
            try:
                t = self.check_expr(goal.fields["prop"], dict(self.tenv), None)
                self.expect_bool(t, goal.fields["prop"], "prove proposition")
            except CheckError as e:
                self.errors.append(e)
        elif k == "CheckGoal":
            f, h = goal.fields["fun"], goal.fields["impl"]
            ft = self.tenv.get(f); ht = self.tenv.get(h)
            if ft is None:
                self.err(f"check target function '{f}' undefined", goal, "admission")
            if ht is None:
                self.err(f"check target impl '{h}' undefined", goal, "admission")
            if ft is not None and ht is not None:
                ft = _resolve_alias(ft, self.aliases); ht = _resolve_alias(ht, self.aliases)
                if not (isinstance(ft, tuple) and ft[0] == "fn" and len(ft[1][0]) == 2):
                    self.err(f"check function '{f}' must have type (In, Out) -> Bool", goal, "admission")
                elif not (isinstance(ht, tuple) and ht[0] == "impl"):
                    self.err(f"check impl '{h}' must have an Impl type", goal, "admission")
                else:
                    (fi, fo), fret = ft[1]
                    hi, ho = ht[1]
                    if not (type_eq(fi, hi, self.aliases) and type_eq(fo, ho, self.aliases)
                            and type_eq(fret, "Bool", self.aliases)):
                        self.err(f"check-goal type mismatch: {f}: {fmt(ft)} vs {h}: {fmt(ht)}",
                                 goal, "admission")
        elif k == "CompareGoal":
            for ref in goal.fields["refs"]:
                if ref not in groups:
                    self.err(f"unknown constraint group '{ref}'", goal, "admission")
            try:
                mtype = self.type_of_texpr(goal.fields["type"], goal)
            except CheckError as e:
                self.errors.append(e); return
            for ref in goal.fields["refs"]:
                self.check_output_scope(groups[ref], mtype)
            if goal.fields["under"] and goal.fields["under"] not in projs:
                self.err(f"unknown projection '{goal.fields['under']}'", goal, "admission")
            # NEW-A3: projection paths resolve against the model type (§B.5a).
            if goal.fields["under"]:
                pname = goal.fields["under"]
                for p in body.fields["projections"]:
                    if p.fields["name"] == pname:
                        self.check_proj_paths(p, mtype)
                        break

    def check_proj_paths(self, proj, mtype):
        # NEW-A3: each path must start at `output` and walk record fields.
        mt = _resolve_alias(mtype, self.aliases)
        for path in proj.fields["paths"]:
            parts = path.fields["parts"]
            if not parts or parts[0] != "output":
                self.err(f"projection path must start with 'output', got "
                         f"{'.'.join(parts)}", path, "admission")
                continue
            cur = mt
            for seg in parts[1:]:
                cur = _resolve_alias(cur, self.aliases)
                if not (isinstance(cur, tuple) and cur[0] == "record"):
                    self.err(f"projection path '{'.'.join(parts)}': '{seg}' "
                             f"not a record field", path, "admission")
                    break
                fields = dict(cur[1])
                if seg not in fields:
                    self.err(f"projection path '{'.'.join(parts)}': unknown "
                             f"field '{seg}'", path, "admission")
                    break
                cur = fields[seg]

    def check_output_scope(self, group, target):
        env = dict(self.tenv); env["output"] = _resolve_alias(target, self.aliases)
        for c in group.fields["items"]:
            try:
                t = self.check_expr(c.fields["pred"], env, None)
                self.expect_bool(t, c.fields["pred"], f"{c.fields['kind']} predicate")
            except CheckError as e:
                self.errors.append(e)

    # ---- verification (D-031) ----
    def check_verification(self, verif, goal):
        items = verif.fields["items"]
        by_kind = {}
        for it in items:
            by_kind.setdefault(it.kind, []).append(it)
        # cardinality / conflict rules
        for kind, group in by_kind.items():
            if kind in ("ProofReq", "RecomputeReq", "AssuranceReq"):
                if len(group) > 1:
                    modes = [g.fields["mode"] for g in group]
                    if all(m == "none" for m in modes):
                        self.err(f"{kind}: duplicate 'none' declarations",
                                 group[1], "admission")
                    elif "none" in modes:
                        self.err(f"{kind}: 'none' conflicts with an active declaration "
                                 f"(conflicting-verification-requirements)", group[1], "admission")
                    else:
                        # two active declarations
                        if kind == "AssuranceReq":
                            self.err(f"{kind}: two assurance levels conflict", group[1], "admission")
                        else:
                            c0 = group[0].fields.get("checker"); c1 = group[1].fields.get("checker")
                            same = (c0 is not None and c1 is not None
                                    and c0.fields["slug"].fields["parts"] == c1.fields["slug"].fields["parts"]
                                    and c0.fields["version"] == c1.fields["version"])
                            self.err(f"{kind}: {'duplicate declaration' if same else 'conflicting declarations'}",
                                     group[1], "admission")
            elif kind == "TestReq":
                seen_methods = {}
                for g in group:
                    m = g.fields["mode"]
                    if m in seen_methods:
                        self.err(f"TestReq: duplicate '{m}' test", g, "admission")
                    seen_methods[m] = g
                if "none" in seen_methods and len(seen_methods) > 1:
                    self.err("TestReq: 'none' conflicts with an active test", group[0], "admission")
        # assurance/goal coherence (Level A admission)
        assurance = by_kind.get("AssuranceReq", [])
        if assurance:
            mode = assurance[0].fields["mode"]
            if mode == "level-a":
                if goal.kind == "ProveGoal":
                    proofs = by_kind.get("ProofReq", [])
                    if not any(p.fields["mode"] == "kernel-checked" for p in proofs):
                        self.err("assurance level-a with prove goal requires a kernel-checked proof",
                                 assurance[0], "admission")
                elif goal.kind == "DeriveGoal":
                    proofs = by_kind.get("ProofReq", [])
                    recomps = by_kind.get("RecomputeReq", [])
                    if not (any(p.fields["mode"] == "kernel-checked" for p in proofs)
                            or any(r.fields["mode"] == "by" for r in recomps)):
                        self.err("assurance level-a with derive goal requires kernel proof or recomputation",
                                 assurance[0], "admission")
                else:
                    # NEW-A2: construct / check / compare-models + level-a
                    self.err("assurance level-a unavailable for this goal kind "
                             "(assurance-level-unavailable)",
                             assurance[0], "admission")
        # fuzz cases: 0 -> INVALID_INPUT
        for it in by_kind.get("TestReq", []):
            if it.fields["mode"] == "property-fuzz":
                if it.fields["config"]["cases"] == 0:
                    self.err("property-fuzz with cases: 0 (empty corpus)", it, "admission")

    def check_limits(self, limits):
        # NEW-A1: §B.8 ranges enforced (was a stub).
        import re as _re
        to = limits.fields.get("timeout")
        if to is not None:
            m = _re.fullmatch(r"([0-9]+)(ms|s|min|h)", str(to))
            if not m:
                self.err(f"bad duration {to!r}", limits, "admission")
            else:
                n, unit = int(m.group(1)), m.group(2)
                secs = n * {"ms": 0.001, "s": 1, "min": 60, "h": 3600}[unit]
                if not (1 <= secs <= 24 * 3600):
                    self.err(f"timeout {to} outside 1s..24h", limits,
                             "admission")
        steps = limits.fields.get("steps")
        if steps is not None and int(steps) == 0:
            self.err("steps: 0 is degenerate", limits, "admission")


def typecheck(spec, resolver):
    c = Checker(resolver)
    return c.check(spec), c
