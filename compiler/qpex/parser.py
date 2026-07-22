"""QPex recursive-descent Parser (Phase 2.1 subset)."""

from __future__ import annotations

from .ast_nodes import (
    AssignStmt,
    Attr,
    BinOp,
    Block,
    Call,
    ClassDecl,
    Coin,
    CompilationUnit,
    Dirac,
    EnumDecl,
    EvolveBody,
    EvolveExpr,
    FieldDecl,
    FunDecl,
    ImportDecl,
    Inspect,
    InterfaceDecl,
    KetLit,
    Lambda,
    LetBind,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    MainDecl,
    Measure,
    ModuleInfoDecl,
    NamespaceDecl,
    OpBin,
    OpLit,
    OpNumber,
    OpQuadrature,
    OpGridQuad,
    OpHop,
    OpPauli,
    OpPow,
    OpVar,
    PackageDecl,
    Param,
    Pipe,
    Snapshot,
    Span,
    StateBind,
    StructDecl,
    TensorExpr,
    TupleExpr,
    TypeRef,
    Vacuum,
    Var,
    WhenArm,
    WhenExpr,
)
from .tokens import Token, TokenKind


class ParseError(Exception):
    def __init__(self, message: str, line: int, col: int) -> None:
        super().__init__(message)
        self.line = line
        self.col = col
        self.message = message


def _flatten_namespaces(decls: list) -> list:
    """Expand `namespace A.B { class C … }` → ClassDecl(namespace=[A,B], name=C)."""
    out: list = []
    for d in decls:
        if isinstance(d, NamespaceDecl):
            for inner in _flatten_namespaces(d.decls):
                if isinstance(inner, (ClassDecl, FunDecl, EnumDecl, StructDecl)):
                    inner.namespace = list(d.path) + list(inner.namespace)
                    out.append(inner)
                else:
                    out.append(inner)
        else:
            out.append(d)
    return out


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0
        self.diagnostics: list[dict] = []
        self._prev: Token | None = None

    def parse(self) -> CompilationUnit:
        start = self._span()
        package = None
        imports: list[ImportDecl] = []
        decls: list = []
        main: MainDecl | None = None

        if self._check(TokenKind.PACKAGE):
            package = self._package()

        while self._check(TokenKind.IMPORT):
            imports.append(self._import())

        while not self._check(TokenKind.EOF):
            if self._check(TokenKind.NAMESPACE):
                decls.append(self._namespace_decl())
            elif self._check(TokenKind.ENUM) or (
                self._is_visibility_start() and self._peek_after_visibility() == TokenKind.ENUM
            ):
                vis = self._parse_visibility()
                ed = self._enum_decl()
                ed.visibility = vis  # type: ignore[assignment]
                decls.append(ed)
            elif self._check(TokenKind.STRUCT) or (
                self._is_visibility_start()
                and self._peek_after_visibility() == TokenKind.STRUCT
            ):
                vis = self._parse_visibility()
                sd = self._struct_decl()
                sd.visibility = vis  # type: ignore[assignment]
                decls.append(sd)
            elif (
                self._check(TokenKind.PUBLIC)
               
                or self._check(TokenKind.PRIVATE)
                or self._check(TokenKind.FUN)
            ):
                nxt = self._peek_after_visibility()
                if nxt == TokenKind.CLASS:
                    vis = self._parse_visibility()
                    cd = self._class_decl()
                    cd.visibility = vis  # type: ignore[assignment]
                    decls.append(cd)
                elif nxt == TokenKind.ENUM:
                    vis = self._parse_visibility()
                    ed = self._enum_decl()
                    ed.visibility = vis  # type: ignore[assignment]
                    decls.append(ed)
                elif nxt == TokenKind.STRUCT:
                    vis = self._parse_visibility()
                    sd = self._struct_decl()
                    sd.visibility = vis  # type: ignore[assignment]
                    decls.append(sd)
                else:
                    fun = self._fun_decl()
                    if fun.name == "main":
                        if main is not None:
                            self.diagnostics.append(
                                {
                                    "code": "PARSE_ERROR",
                                    "line": fun.span.line,
                                    "col": fun.span.col,
                                    "message": "duplicate `main` entry point",
                                }
                            )
                        main = MainDecl(
                            params=fun.params, body=fun.body, span=fun.span
                        )
                    else:
                        decls.append(fun)
            elif self._check(TokenKind.CLASS) or (
                self._is_visibility_start()
                and self._peek_after_visibility() == TokenKind.CLASS
            ):
                vis = self._parse_visibility()
                cd = self._class_decl()
                cd.visibility = vis  # type: ignore[assignment]
                decls.append(cd)
            elif self._check(TokenKind.INTERFACE):
                decls.append(self._interface_decl())
            elif self._is_toplevel_executable_start():
                tok = self._peek()
                self.diagnostics.append(
                    {
                        "code": "TOPLEVEL_EXECUTION_ERROR",
                        "line": tok.line,
                        "col": tok.col,
                        "message": (
                            "executable statements are forbidden at top level; "
                            "place them inside `public fun main() { … }`"
                        ),
                    }
                )
                self._skip_until_toplevel_resync()
            elif self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                self._advance()
            elif self._check(TokenKind.ERROR):
                self._advance()
            else:
                tok = self._peek()
                if tok.kind == TokenKind.EOF:
                    break
                self.diagnostics.append(
                    {
                        "code": "PARSE_ERROR",
                        "line": tok.line,
                        "col": tok.col,
                        "message": f"unexpected token `{tok.lexeme}` at top level",
                    }
                )
                self._advance()

        decls = _flatten_namespaces(decls)
        return CompilationUnit(
            package=package,
            imports=imports,
            decls=decls,
            main=main,
            span=start,
        )

    def _is_toplevel_executable_start(self) -> bool:
        return (
            self._check(TokenKind.STATE)
            or self._check(TokenKind.MEASURE)
            or self._check(TokenKind.SNAPSHOT)
            or self._check(TokenKind.LET)
            or self._check(TokenKind.LPAREN)
            or self._is_type_first_start()
            or self._check(TokenKind.EVOLVE)
            or self._check(TokenKind.WHEN)
            or self._check(TokenKind.COIN)
            or self._check(TokenKind.DIRAC)
            or self._check(TokenKind.VACUUM)
            or self._check(TokenKind.INSPECT)
        )

    def _skip_until_toplevel_resync(self) -> None:
        """Recover after TOPLEVEL_EXECUTION_ERROR: skip one statement-ish chunk."""
        # Prefer consuming a well-formed stmt so diagnostics stay localized.
        try:
            self._stmt()
            return
        except ParseError:
            pass
        depth = 0
        while not self._check(TokenKind.EOF):
            tok = self._peek()
            if depth == 0 and tok.kind in {
                TokenKind.PUBLIC,
                TokenKind.FUN,
                TokenKind.CLASS,
                TokenKind.INTERFACE,
                TokenKind.PACKAGE,
                TokenKind.IMPORT,
            }:
                return
            if tok.kind == TokenKind.LBRACE:
                depth += 1
            elif tok.kind == TokenKind.RBRACE:
                depth = max(0, depth - 1)
            self._advance()

    def _package(self) -> PackageDecl:
        sp = self._span()
        self._expect(TokenKind.PACKAGE)
        path = self._dotted_path()
        return PackageDecl(path=path, span=sp)

    def _import(self) -> ImportDecl:
        sp = self._span()
        self._expect(TokenKind.IMPORT)
        path = self._dotted_path_import()
        name = path[-1] if path else ""
        return ImportDecl(path=path, name=name, span=sp)

    def _dotted_path(self) -> list[str]:
        parts = [self._expect_ident_like()]
        while self._match(TokenKind.DOT):
            parts.append(self._expect_ident_like())
        return parts

    def _dotted_path_import(self) -> list[str]:
        """`qpex.math` or `qpex.math.*`."""
        parts = [self._expect_ident_like()]
        while self._match(TokenKind.DOT):
            if self._match(TokenKind.STAR):
                parts.append("*")
                break
            parts.append(self._expect_ident_like())
        return parts

    def _is_visibility_start(self) -> bool:
        return self._check(TokenKind.PUBLIC) or self._check(TokenKind.PRIVATE)

    def _peek_after_visibility(self) -> TokenKind | None:
        """Look at token after an optional visibility keyword (`pub`/`public`/`private`)."""
        j = self.i
        if self.tokens[j].kind in {TokenKind.PUBLIC, TokenKind.PRIVATE}:
            j += 1
        if j < len(self.tokens):
            return self.tokens[j].kind
        return None

    def _parse_visibility(self) -> str:
        """ADR 0058: `pub`/`public` | `private` | (default → module-private)."""
        if self._match(TokenKind.PUBLIC):
            return "public"
        if self._match(TokenKind.PRIVATE):
            return "private"
        return "module"

    @staticmethod
    def _apply_underscore_privacy(name: str, vis: str) -> str:
        """Leading `_` ⇒ class/file private (noise-free encapsulation)."""
        if name.startswith("_") and not name.startswith("__"):
            return "private"
        return vis

    def parse_module_info(self) -> ModuleInfoDecl:
        """Parse a `module-info.qpex` compilation unit (ADR 0058)."""
        sp = self._span()
        self._expect(TokenKind.MODULE)
        name = self._dotted_path()
        exports: list[list[str]] = []
        requires: list[list[str]] = []
        self._expect(TokenKind.LBRACE)
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            if self._match(TokenKind.EXPORTS):
                exports.append(self._dotted_path())
                self._match(TokenKind.SEMI)
            elif self._match(TokenKind.REQUIRES):
                requires.append(self._dotted_path())
                self._match(TokenKind.SEMI)
            elif self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                self._advance()
            else:
                tok = self._peek()
                self.diagnostics.append(
                    {
                        "code": "PARSE_ERROR",
                        "line": tok.line,
                        "col": tok.col,
                        "message": (
                            f"expected `exports` or `requires` in module, "
                            f"got `{tok.lexeme}`"
                        ),
                    }
                )
                self._advance()
        self._expect(TokenKind.RBRACE)
        return ModuleInfoDecl(name=name, exports=exports, requires=requires, span=sp)

    def _fun_decl(self) -> FunDecl:
        sp = self._span()
        vis = self._parse_visibility()
        self._expect(TokenKind.FUN)
        name = self._expect_ident_like()
        vis = self._apply_underscore_privacy(name, vis)
        self._expect(TokenKind.LPAREN)
        params: list[Param] = []
        if not self._check(TokenKind.RPAREN):
            params.append(self._param())
            while self._match(TokenKind.COMMA):
                params.append(self._param())
        self._expect(TokenKind.RPAREN)
        body = self._block()
        return FunDecl(name=name, params=params, body=body, span=sp, visibility=vis)

    def _param(self) -> Param:
        name = self._expect_ident_like()
        ty = None
        if self._match(TokenKind.COLON):
            ty = self._type_ref()
        return Param(name=name, ty=ty)

    def _type_ref(self) -> TypeRef:
        """Type reference: `Mass`, `State<Length>`, `Topology.ChainLattice`, `(A, B)`."""
        # Product carrier: (T1, T2, …)
        if self._match(TokenKind.LPAREN):
            args = [self._type_ref()]
            while self._match(TokenKind.COMMA):
                args.append(self._type_ref())
            self._expect(TokenKind.RPAREN)
            return TypeRef(name="Tuple", args=args)

        tok = self._peek()
        if tok.kind == TokenKind.IDENT:
            name = self._advance().lexeme
            # ADR 0055: dotted type path Topology.ChainLattice
            while self._match(TokenKind.DOT):
                name = name + "." + self._expect_ident_like()
        elif tok.kind == TokenKind.STATE and tok.lexeme == "State":
            name = self._advance().lexeme
        else:
            raise ParseError(f"expected type name, got `{tok.lexeme}`", tok.line, tok.col)
        args: list[TypeRef] = []
        if self._match(TokenKind.LT):
            args.append(self._type_ref())
            while self._match(TokenKind.COMMA):
                args.append(self._type_ref())
            if self._check(TokenKind.GT):
                self._advance()
            elif self._check(TokenKind.GE):
                self._advance()
            else:
                t = self._peek()
                raise ParseError("expected `>` to close type arguments", t.line, t.col)
        return TypeRef(name=name, args=args)

    def _namespace_decl(self) -> NamespaceDecl:
        """`namespace Topology` / `namespace Physics.Parameters { … }` (ADR 0055)."""
        sp = self._span()
        self._expect(TokenKind.NAMESPACE)
        path = [self._expect_ident_like()]
        while self._match(TokenKind.DOT):
            path.append(self._expect_ident_like())
        decls: list = []
        self._expect(TokenKind.LBRACE)
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            if self._check(TokenKind.NAMESPACE):
                decls.append(self._namespace_decl())
            elif self._check(TokenKind.ENUM) or (
                self._is_visibility_start()
                and self._peek_after_visibility() == TokenKind.ENUM
            ):
                vis = self._parse_visibility()
                ed = self._enum_decl()
                ed.visibility = vis  # type: ignore[assignment]
                decls.append(ed)
            elif self._check(TokenKind.STRUCT) or (
                self._is_visibility_start()
                and self._peek_after_visibility() == TokenKind.STRUCT
            ):
                vis = self._parse_visibility()
                sd = self._struct_decl()
                sd.visibility = vis  # type: ignore[assignment]
                decls.append(sd)
            elif (
                self._check(TokenKind.PUBLIC)
               
                or self._check(TokenKind.PRIVATE)
                or self._check(TokenKind.FUN)
            ):
                nxt = self._peek_after_visibility()
                if nxt == TokenKind.CLASS or (
                    self._is_visibility_start()
                    and self._peek_after_visibility() == TokenKind.CLASS
                ):
                    vis = self._parse_visibility()
                    cd = self._class_decl()
                    cd.visibility = vis  # type: ignore[assignment]
                    decls.append(cd)
                else:
                    decls.append(self._fun_decl())
            elif self._check(TokenKind.CLASS) or (
                self._is_visibility_start()
                and self._peek_after_visibility() == TokenKind.CLASS
            ):
                vis = self._parse_visibility()
                cd = self._class_decl()
                cd.visibility = vis  # type: ignore[assignment]
                decls.append(cd)
            elif self._check(TokenKind.INTERFACE):
                decls.append(self._interface_decl())
            elif self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                self._advance()
            elif self._check(TokenKind.ERROR):
                self._advance()
            else:
                tok = self._peek()
                self.diagnostics.append(
                    {
                        "code": "PARSE_ERROR",
                        "line": tok.line,
                        "col": tok.col,
                        "message": (
                            f"unexpected `{tok.lexeme}` inside namespace "
                            f"`{'.'.join(path)}`"
                        ),
                    }
                )
                self._advance()
        self._expect(TokenKind.RBRACE)
        return NamespaceDecl(path=path, decls=decls, span=sp)

    def _enum_decl(self) -> EnumDecl:
        sp = self._span()
        self._expect(TokenKind.ENUM)
        name = self._expect_ident_like()
        variants: list[str] = []
        self._expect(TokenKind.LBRACE)
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            variants.append(self._expect_ident_like())
            self._match(TokenKind.COMMA)  # optional trailing commas
        self._expect(TokenKind.RBRACE)
        if not variants:
            self.diagnostics.append(
                {
                    "code": "PARSE_ERROR",
                    "line": sp.line,
                    "col": sp.col,
                    "message": f"enum `{name}` must declare at least one variant",
                }
            )
        return EnumDecl(name=name, variants=variants, span=sp)

    def _struct_decl(self) -> StructDecl:
        sp = self._span()
        self._expect(TokenKind.STRUCT)
        name = self._expect_ident_like()
        fields: list[FieldDecl] = []
        self._expect(TokenKind.LBRACE)
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            fields.append(self._field_decl(default_mutable=False))
            self._match(TokenKind.COMMA)
        self._expect(TokenKind.RBRACE)
        # struct fields are always immutable values
        for f in fields:
            f.mutable = False
        return StructDecl(name=name, fields=fields, span=sp)

    def _field_decl(self, *, default_mutable: bool) -> FieldDecl:
        """`[vis] val|var name: Type [= e]`."""
        sp = self._span()
        vis = self._parse_visibility()
        mutable = default_mutable
        if self._match(TokenKind.VAR):
            mutable = True
        elif self._match(TokenKind.VAL):
            mutable = False
        name = self._expect_ident_like()
        vis = self._apply_underscore_privacy(name, vis)
        self._expect(TokenKind.COLON)
        ty = self._type_ref()
        default = None
        if self._match(TokenKind.EQ):
            default = self._expression()
        return FieldDecl(
            name=name,
            ty=ty,
            mutable=mutable,
            default=default,
            span=sp,
            visibility=vis,  # type: ignore[arg-type]
        )

    def _class_decl(self) -> ClassDecl:
        sp = self._span()
        self._expect(TokenKind.CLASS)
        name = self._expect_ident_like()
        ifaces: list[str] = []
        if self._match(TokenKind.COLON):
            ifaces.append(self._expect_ident_like())
            while self._match(TokenKind.COMMA):
                ifaces.append(self._expect_ident_like())
        fields: list[StateBind] = []
        members: list[FieldDecl] = []
        methods: list[FunDecl] = []
        if self._match(TokenKind.LBRACE):
            while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
                if self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                    self._advance()
                    continue
                if (
                    self._check(TokenKind.PUBLIC)
                   
                    or self._check(TokenKind.PRIVATE)
                    or self._check(TokenKind.FUN)
                ):
                    # method or vis+val — distinguish by peek
                    nxt = self._peek_after_visibility()
                    if nxt == TokenKind.FUN or self._check(TokenKind.FUN):
                        methods.append(self._fun_decl())
                        continue
                    if nxt in {TokenKind.VAL, TokenKind.VAR}:
                        members.append(self._field_decl(default_mutable=False))
                        continue
                if self._check(TokenKind.VAL) or self._check(TokenKind.VAR):
                    members.append(self._field_decl(default_mutable=False))
                    continue
                if self._is_type_first_start():
                    fields.append(self._type_first_bind())
                else:
                    tok = self._peek()
                    self.diagnostics.append(
                        {
                            "code": "PARSE_ERROR",
                            "line": tok.line,
                            "col": tok.col,
                            "message": (
                                f"class `{name}` expects Type-First / val/var field "
                                f"or `fun` method; got `{tok.lexeme}`"
                            ),
                        }
                    )
                    self._advance()
            self._expect(TokenKind.RBRACE)
        return ClassDecl(
            name=name,
            ifaces=ifaces,
            span=sp,
            fields=fields,
            members=members,
            methods=methods,
        )

    def _interface_decl(self) -> InterfaceDecl:
        sp = self._span()
        self._expect(TokenKind.INTERFACE)
        name = self._expect_ident_like()
        if self._match(TokenKind.LBRACE):
            depth = 1
            while depth > 0 and not self._check(TokenKind.EOF):
                if self._check(TokenKind.LBRACE):
                    depth += 1
                elif self._check(TokenKind.RBRACE):
                    depth -= 1
                self._advance()
        return InterfaceDecl(name=name, span=sp)

    def _block(self) -> Block:
        sp = self._span()
        self._expect(TokenKind.LBRACE)
        stmts = []
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            if self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                self._advance()
                continue
            if self._check(TokenKind.ERROR):
                self._advance()
                continue
            stmts.append(self._stmt())
        self._expect(TokenKind.RBRACE)
        return Block(stmts=stmts, span=sp)

    def _stmt(self):
        if self._check(TokenKind.STATE):
            return self._state_bind()
        if self._check(TokenKind.MEASURE):
            return self._measure()
        if self._check(TokenKind.SNAPSHOT):
            return self._snapshot()
        if self._check(TokenKind.LPAREN):
            return self._tuple_bind()
        if self._is_type_first_start():
            return self._type_first_bind()
        # `this.field = expr` / `obj.field = expr`
        if self._check(TokenKind.THIS) or self._check(TokenKind.IDENT):
            saved = self.i
            try:
                target = self._call()
                if self._match(TokenKind.EQ) and isinstance(target, Attr):
                    sp = target.span
                    value = self._expression()
                    return AssignStmt(target=target, value=value, span=sp)
            except ParseError:
                pass
            self.i = saved
        tok = self._peek()
        raise ParseError(f"expected statement, got `{tok.lexeme}`", tok.line, tok.col)

    def _is_type_first_start(self) -> bool:
        """Type-First: physical quantity / State / Delta heads the declaration."""
        from .dimensions import TYPE_HEADS

        tok = self._peek()
        if tok.kind != TokenKind.IDENT:
            return False
        name = tok.lexeme
        if name in TYPE_HEADS:
            return True
        # Capitalized ident → quantity type (Mass, Length, …)
        return bool(name) and name[0].isupper()

    def _type_first_bind(self) -> StateBind:
        """`Mass m = e` / `State<(A,B)> (c, x) = e` / `Operator H = …`."""
        sp = self._span()
        ty = self._type_ref()
        if self._match(TokenKind.LPAREN):
            names = [self._expect_ident_like()]
            while self._match(TokenKind.COMMA):
                names.append(self._expect_ident_like())
            self._expect(TokenKind.RPAREN)
        else:
            names = [self._expect_ident_like()]
        self._expect(TokenKind.EQ)
        if ty.name == "Operator":
            if len(names) != 1:
                raise ParseError("Operator bind expects a single name", sp.line, sp.col)
            expr = self._op_expression()  # type: ignore[assignment]
        else:
            expr = self._expression()
        return StateBind(names=names, expr=expr, span=sp, ty=ty)  # type: ignore[arg-type]

    def _tuple_bind(self) -> StateBind:
        """`(x, p) = expr` — Type-First-friendly tuple bind without `state`."""
        sp = self._span()
        self._expect(TokenKind.LPAREN)
        names = [self._expect_ident_like()]
        while self._match(TokenKind.COMMA):
            names.append(self._expect_ident_like())
        self._expect(TokenKind.RPAREN)
        self._expect(TokenKind.EQ)
        expr = self._expression()
        return StateBind(names=names, expr=expr, span=sp, ty=None)

    def _state_bind(self) -> StateBind:
        sp = self._span()
        self._expect(TokenKind.STATE)
        if self._match(TokenKind.LPAREN):
            names = [self._expect_ident_like()]
            while self._match(TokenKind.COMMA):
                names.append(self._expect_ident_like())
            self._expect(TokenKind.RPAREN)
        else:
            names = [self._expect_ident_like()]
        self._expect(TokenKind.EQ)
        expr = self._expression()
        return StateBind(names=names, expr=expr, span=sp, ty=None)

    def _measure(self) -> Measure:
        sp = self._span()
        self._expect(TokenKind.MEASURE)
        expr = self._expression()
        sink = None
        if self._match(TokenKind.TO):
            sink = self._expect_ident_like()
        return Measure(expr=expr, span=sp, sink=sink)

    def _snapshot(self) -> Snapshot:
        sp = self._span()
        self._expect(TokenKind.SNAPSHOT)
        expr = self._expression()
        self._expect(TokenKind.TO)
        sink = self._expect_ident_like()
        return Snapshot(expr=expr, sink=sink, span=sp)

    # --- expressions (precedence climbing) ---

    def _expression(self):
        return self._pipe()

    def _pipe(self):
        expr = self._comparison()
        while self._match(TokenKind.PIPE_OP):
            sp = self._span()
            rhs = self._comparison()
            expr = Pipe(lhs=expr, rhs=rhs, span=sp)
        return expr

    def _comparison(self):
        expr = self._term()
        while True:
            op = None
            if self._match(TokenKind.GE):
                op = ">="
            elif self._match(TokenKind.LE):
                op = "<="
            elif self._match(TokenKind.GT):
                op = ">"
            elif self._match(TokenKind.LT):
                op = "<"
            elif self._match(TokenKind.EQEQ):
                op = "=="
            elif self._match(TokenKind.NEQ):
                op = "!="
            else:
                break
            sp = self._span()
            rhs = self._term()
            expr = BinOp(op=op, lhs=expr, rhs=rhs, span=sp)
        return expr

    def _term(self):
        expr = self._factor()
        while True:
            if self._match(TokenKind.PLUS):
                op, sp = "+", self._span()
            elif self._match(TokenKind.MINUS):
                op, sp = "-", self._span()
            else:
                break
            rhs = self._factor()
            expr = BinOp(op=op, lhs=expr, rhs=rhs, span=sp)
        return expr

    def _factor(self):
        expr = self._tensor()
        while True:
            if self._match(TokenKind.STAR):
                op, sp = "*", self._span()
            elif self._match(TokenKind.SLASH):
                op, sp = "/", self._span()
            else:
                break
            rhs = self._tensor()
            expr = BinOp(op=op, lhs=expr, rhs=rhs, span=sp)
        return expr

    def _tensor(self):
        expr = self._unary()
        while self._match(TokenKind.TENSOR_OP):
            sp = self._span()
            rhs = self._unary()
            expr = TensorExpr(left=expr, right=rhs, span=sp)
        return expr

    def _unary(self):
        if self._match(TokenKind.BANG):
            sp = self._span()
            inner = self._unary()
            from .ast_nodes import UnaryNot

            return UnaryNot(expr=inner, span=sp)
        if self._match(TokenKind.MINUS):
            sp = self._span()
            inner = self._unary()
            # desugar -e as 0 - e (LitInt 0 or LitFloat 0.0)
            zero = LitFloat(value=0.0, span=sp)
            return BinOp(op="-", lhs=zero, rhs=inner, span=sp)
        return self._call()

    def _call(self):
        expr = self._primary()
        while True:
            if self._check(TokenKind.LPAREN):
                # Newline before '(' → not a Call (avoids `x\n(y,z)` eating tuple results)
                if self._prev is not None and self._peek().line > self._prev.line:
                    break
                self._advance()  # (
                sp = self._span()
                args = []
                if not self._check(TokenKind.RPAREN):
                    args.append(self._expression())
                    while self._match(TokenKind.COMMA):
                        args.append(self._expression())
                self._expect(TokenKind.RPAREN)
                if isinstance(expr, (Coin, Dirac, Vacuum)):
                    continue
                if isinstance(expr, Inspect):
                    continue
                expr = Call(callee=expr, args=args, span=sp)
            elif self._match(TokenKind.DOT):
                sp = self._span()
                name = self._expect_ident_like()
                if self._match(TokenKind.LPAREN):
                    args = []
                    if not self._check(TokenKind.RPAREN):
                        args.append(self._expression())
                        while self._match(TokenKind.COMMA):
                            args.append(self._expression())
                    self._expect(TokenKind.RPAREN)
                    if name == "inspect":
                        label = None
                        if args and isinstance(args[0], LitString):
                            label = args[0].value
                        expr = Inspect(expr=expr, label=label, span=sp)
                    else:
                        # recv.name(args) → Call(Attr(recv, name), args)
                        expr = Call(
                            callee=Attr(obj=expr, name=name, span=sp),
                            args=args,
                            span=sp,
                        )
                else:
                    expr = Attr(obj=expr, name=name, span=sp)
            else:
                break
        return expr

    def _primary(self):
        sp = self._span()
        tok = self._peek()

        if self._match(TokenKind.INT):
            return LitInt(value=int(tok.literal), span=sp)
        if self._match(TokenKind.FLOAT):
            return LitFloat(value=float(tok.literal), span=sp)
        if self._match(TokenKind.TRUE):
            return LitBool(value=True, span=sp)
        if self._match(TokenKind.FALSE):
            return LitBool(value=False, span=sp)
        if self._match(TokenKind.STRING):
            return LitString(value=str(tok.literal), span=sp)

        if self._match(TokenKind.THIS):
            return Var(name="this", span=sp)

        if self._match(TokenKind.COIN):
            if self._match(TokenKind.LPAREN):
                self._expect(TokenKind.RPAREN)
            return Coin(span=sp)

        if self._match(TokenKind.DIRAC):
            self._expect(TokenKind.LPAREN)
            arg = self._expression()
            self._expect(TokenKind.RPAREN)
            return Dirac(arg=arg, span=sp)

        if self._match(TokenKind.KET):
            return KetLit(label=str(tok.literal), span=sp)

        if self._match(TokenKind.VACUUM):
            if self._match(TokenKind.LPAREN):
                self._expect(TokenKind.RPAREN)
            return Vacuum(span=sp)

        if self._match(TokenKind.INSPECT):
            self._expect(TokenKind.LPAREN)
            inner = self._expression()
            label = None
            if self._match(TokenKind.COMMA):
                lab = self._expression()
                if isinstance(lab, LitString):
                    label = lab.value
            self._expect(TokenKind.RPAREN)
            return Inspect(expr=inner, label=label, span=sp)

        if self._match(TokenKind.WHEN):
            return self._when_expr(sp)

        if self._match(TokenKind.EVOLVE):
            return self._evolve_expr(sp)

        if self._match(TokenKind.LPAREN):
            # grouping or tuple
            if self._check(TokenKind.RPAREN):
                self._advance()
                raise ParseError("empty tuple", sp.line, sp.col)
            first = self._expression()
            if self._match(TokenKind.COMMA):
                items = [first, self._expression()]
                while self._match(TokenKind.COMMA):
                    items.append(self._expression())
                self._expect(TokenKind.RPAREN)
                return TupleExpr(items=items, span=sp)
            self._expect(TokenKind.RPAREN)
            return first

        if self._match(TokenKind.IDENT):
            name = tok.lexeme
            if self._check(TokenKind.ARROW):
                self._advance()
                body = self._expression()
                return Lambda(param=name, body=body, span=sp)
            return Var(name=name, span=sp)

        # Forbidden/Retired in expr position — recover with dummy
        if self._match(TokenKind.FORBIDDEN) or self._match(TokenKind.RETIRED):
            return Var(name=tok.lexeme, span=sp)

        raise ParseError(f"unexpected token in expression: `{tok.lexeme}`", tok.line, tok.col)

    def _when_expr(self, sp: Span) -> WhenExpr:
        self._expect(TokenKind.LPAREN)
        ctrl = self._expression()
        self._expect(TokenKind.RPAREN)
        self._expect(TokenKind.LBRACE)
        arms: list[WhenArm] = []
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            if self._match(TokenKind.ELSE):
                self._expect(TokenKind.ARROW)
                body = self._expression()
                self._match(TokenKind.COMMA)
                arms.append(WhenArm(pat=None, body=body, is_else=True))
                continue
            # pattern: literal or ident
            pat_tok = self._peek()
            if self._match(TokenKind.INT):
                pat = int(pat_tok.literal)
            elif self._match(TokenKind.FLOAT):
                pat = float(pat_tok.literal)
            elif self._match(TokenKind.TRUE):
                pat = True
            elif self._match(TokenKind.FALSE):
                pat = False
            elif self._match(TokenKind.IDENT):
                pat = pat_tok.lexeme
            else:
                self.diagnostics.append(
                    {
                        "code": "PARSE_ERROR",
                        "line": pat_tok.line,
                        "col": pat_tok.col,
                        "message": f"bad when pattern `{pat_tok.lexeme}`",
                    }
                )
                self._advance()
                continue
            self._expect(TokenKind.ARROW)
            body = self._expression()
            self._match(TokenKind.COMMA)
            arms.append(WhenArm(pat=pat, body=body, is_else=False))
        self._expect(TokenKind.RBRACE)
        return WhenExpr(ctrl=ctrl, arms=arms, span=sp)

    def _evolve_expr(self, sp: Span) -> EvolveExpr:
        # Forms:
        #   evolve (seeds) times N { body }
        #   evolve (seeds) for dt { body }
        #   evolve psi under H for t          (ADR 0038)
        #   evolve (psi) under H for t
        if self._match(TokenKind.LPAREN):
            seeds = [self._expression()]
            while self._match(TokenKind.COMMA):
                seeds.append(self._expression())
            self._expect(TokenKind.RPAREN)
        else:
            seeds = [self._expression()]

        duration = None
        hamiltonian = None
        times = 1
        body: EvolveBody | None = None

        if self._match(TokenKind.UNDER):
            hamiltonian = self._expression()
            self._expect(TokenKind.FOR)
            duration = self._expression()
            times = 1
            if self._check(TokenKind.LBRACE):
                body = self._evolve_body()
            return EvolveExpr(
                seeds=seeds,
                times=times,
                body=body,
                span=sp,
                duration=duration,
                hamiltonian=hamiltonian,
            )

        if self._match(TokenKind.TIMES):
            # ADR 0060: integer literal or closed classical expression
            times = self._expression()
            body = self._evolve_body()
            return EvolveExpr(
                seeds=seeds, times=times, body=body, span=sp, duration=None
            )

        if self._match(TokenKind.FOR):
            duration = self._expression()
            times = 1
            body = self._evolve_body()
            return EvolveExpr(
                seeds=seeds, times=times, body=body, span=sp, duration=duration
            )

        tok = self._peek()
        raise ParseError(
            "evolve expects `times N`, `for duration`, or `under H for t`",
            tok.line,
            tok.col,
        )

    def _evolve_body(self) -> EvolveBody:
        sp = self._span()
        self._expect(TokenKind.LBRACE)
        lets: list[LetBind] = []
        result = None
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            if self._match(TokenKind.LET):
                lsp = self._span()
                name = self._expect_ident_like()
                self._expect(TokenKind.EQ)
                expr = self._expression()
                lets.append(LetBind(name=name, expr=expr, span=lsp))
                continue
            # result expression (may be tuple or plain)
            result = self._expression()
            break
        if result is None:
            tok = self._peek()
            raise ParseError("evolve body missing result expression", tok.line, tok.col)
        self._expect(TokenKind.RBRACE)
        return EvolveBody(lets=lets, result=result, span=sp)

    # --- helpers ---

    def _peek(self) -> Token:
        return self.tokens[self.i]

    def _check(self, kind: TokenKind) -> bool:
        return self._peek().kind == kind

    def _advance(self) -> Token:
        tok = self._peek()
        if tok.kind != TokenKind.EOF:
            self.i += 1
            self._prev = tok
        return tok

    def _match(self, kind: TokenKind) -> bool:
        if self._check(kind):
            self._advance()
            return True
        return False

    def _expect(self, kind: TokenKind) -> Token:
        if self._check(kind):
            return self._advance()
        tok = self._peek()
        raise ParseError(f"expected {kind.name}, got `{tok.lexeme}`", tok.line, tok.col)

    def _expect_ident_like(self) -> str:
        tok = self._peek()
        if tok.kind == TokenKind.IDENT:
            self._advance()
            return tok.lexeme
        raise ParseError(f"expected identifier, got `{tok.lexeme}`", tok.line, tok.col)

    def _span(self) -> Span:
        tok = self._peek()
        return Span(line=tok.line, col=tok.col)

    # --- Operator expressions (Type-First `Operator H = …`) ---

    def _op_expression(self):
        return self._op_sum()

    def _op_sum(self):
        expr = self._op_product()
        while True:
            if self._match(TokenKind.PLUS):
                op, sp = "+", self._span()
            elif self._match(TokenKind.MINUS):
                op, sp = "-", self._span()
            else:
                break
            rhs = self._op_product()
            expr = OpBin(op=op, lhs=expr, rhs=rhs, span=sp)
        return expr

    def _op_product(self):
        expr = self._op_power()
        while self._match(TokenKind.STAR):
            sp = self._span()
            rhs = self._op_power()
            expr = OpBin(op="*", lhs=expr, rhs=rhs, span=sp)
        return expr

    def _op_power(self):
        expr = self._op_unary()
        if self._match(TokenKind.CARET):
            sp = self._span()
            tok = self._expect(TokenKind.INT)
            return OpPow(base=expr, exp=int(tok.literal), span=sp)
        return expr

    def _op_unary(self):
        if self._match(TokenKind.MINUS):
            sp = self._span()
            inner = self._op_unary()
            return OpBin(op="*", lhs=OpLit(value=-1.0, span=sp), rhs=inner, span=sp)
        return self._op_primary()

    def _op_primary(self):
        sp = self._span()
        if self._match(TokenKind.LPAREN):
            expr = self._op_expression()
            self._expect(TokenKind.RPAREN)
            return expr
        if self._match(TokenKind.INT):
            tok = self._prev
            assert tok is not None
            return OpLit(value=float(tok.literal), span=sp)
        if self._match(TokenKind.FLOAT):
            tok = self._prev
            assert tok is not None
            return OpLit(value=float(tok.literal), span=sp)
        tok = self._peek()
        if tok.kind == TokenKind.IDENT:
            name = tok.lexeme
            self._advance()
            if name == "N":
                return OpNumber(span=sp)
            if name == "Q":
                return OpQuadrature(kind="Q", span=sp)
            if name == "P":
                # Momentum: Fock or Position-grid — resolved by op_space / evolve carrier
                return OpQuadrature(kind="P", span=sp)
            if name == "hop":
                # hop(i, j) → |i⟩⟨j| on discrete site / Fock-label basis
                self._expect(TokenKind.LPAREN)
                i_tok = self._expect(TokenKind.INT)
                self._expect(TokenKind.COMMA)
                j_tok = self._expect(TokenKind.INT)
                self._expect(TokenKind.RPAREN)
                return OpHop(i=int(i_tok.literal), j=int(j_tok.literal), span=sp)
            if name.upper() in {"I", "X", "Y", "Z"}:
                site = None
                if self._match(TokenKind.LPAREN):
                    site_tok = self._expect(TokenKind.INT)
                    site = int(site_tok.literal)
                    self._expect(TokenKind.RPAREN)
                return OpPauli(kind=name.upper(), site=site, span=sp)
            return OpVar(name=name, span=sp)
        raise ParseError(
            f"expected operator expression, got `{tok.lexeme}`", tok.line, tok.col
        )
