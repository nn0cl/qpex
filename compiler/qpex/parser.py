"""QPex recursive-descent Parser (Phase 2.1 subset)."""

from __future__ import annotations

from .ast_nodes import (
    Attr,
    BinOp,
    Block,
    Call,
    ClassDecl,
    Coin,
    CompilationUnit,
    Dirac,
    FunDecl,
    ImportDecl,
    Inspect,
    InterfaceDecl,
    Lambda,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    MainDecl,
    Measure,
    PackageDecl,
    Param,
    Pipe,
    Snapshot,
    Span,
    StateBind,
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


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0
        self.diagnostics: list[dict] = []

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
            if self._check(TokenKind.PUBLIC) or self._check(TokenKind.FUN):
                fun = self._fun_decl()
                if fun.name == "main":
                    main = MainDecl(params=fun.params, body=fun.body, span=fun.span)
                else:
                    decls.append(fun)
            elif self._check(TokenKind.CLASS):
                decls.append(self._class_decl())
            elif self._check(TokenKind.INTERFACE):
                decls.append(self._interface_decl())
            elif self._check(TokenKind.STATE):
                # script-style: collect into implicit main later
                break
            elif self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                # skip — diagnostics already from lexer; recover
                self._advance()
            elif self._check(TokenKind.ERROR):
                self._advance()
            else:
                # unexpected — try skip
                tok = self._peek()
                if tok.kind == TokenKind.EOF:
                    break
                self.diagnostics.append(
                    {
                        "code": "PARSE_ERROR",
                        "line": tok.line,
                        "col": tok.col,
                        "message": f"unexpected token `{tok.lexeme}`",
                    }
                )
                self._advance()

        # script sugar: remaining state/measure stmts → implicit main
        if main is None and (
            self._check(TokenKind.STATE)
            or self._check(TokenKind.MEASURE)
            or self._check(TokenKind.LET)
        ):
            body_stmts = []
            while not self._check(TokenKind.EOF):
                if self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                    self._advance()
                    continue
                body_stmts.append(self._stmt())
            main = MainDecl(
                params=[],
                body=Block(stmts=body_stmts, span=start),
                span=start,
            )

        return CompilationUnit(
            package=package,
            imports=imports,
            decls=decls,
            main=main,
            span=start,
        )

    def _package(self) -> PackageDecl:
        sp = self._span()
        self._expect(TokenKind.PACKAGE)
        path = self._dotted_path()
        return PackageDecl(path=path, span=sp)

    def _import(self) -> ImportDecl:
        sp = self._span()
        self._expect(TokenKind.IMPORT)
        path = self._dotted_path()
        name = path[-1] if path else ""
        return ImportDecl(path=path, name=name, span=sp)

    def _dotted_path(self) -> list[str]:
        parts = [self._expect_ident_like()]
        while self._match(TokenKind.DOT):
            parts.append(self._expect_ident_like())
        return parts

    def _fun_decl(self) -> FunDecl:
        sp = self._span()
        vis = "private"
        if self._match(TokenKind.PUBLIC):
            vis = "public"
        self._expect(TokenKind.FUN)
        name = self._expect_ident_like()
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
        name = self._expect_ident_like()
        args: list[TypeRef] = []
        if self._match(TokenKind.LT):  # State<Sys> — use LT/GT as angle brackets
            # careful: GE etc. — for PoC only simple State<Ident>
            args.append(self._type_ref())
            while self._match(TokenKind.COMMA):
                args.append(self._type_ref())
            if self._check(TokenKind.GT):
                self._advance()
            elif self._check(TokenKind.GE):
                # `>=` mislexed — shouldn't happen for types
                self._advance()
        return TypeRef(name=name, args=args)

    def _class_decl(self) -> ClassDecl:
        sp = self._span()
        self._expect(TokenKind.CLASS)
        name = self._expect_ident_like()
        ifaces: list[str] = []
        if self._match(TokenKind.COLON):
            ifaces.append(self._expect_ident_like())
            while self._match(TokenKind.COMMA):
                ifaces.append(self._expect_ident_like())
        # optional empty body
        if self._match(TokenKind.LBRACE):
            depth = 1
            while depth > 0 and not self._check(TokenKind.EOF):
                if self._check(TokenKind.LBRACE):
                    depth += 1
                elif self._check(TokenKind.RBRACE):
                    depth -= 1
                self._advance()
        return ClassDecl(name=name, ifaces=ifaces, span=sp)

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
        tok = self._peek()
        raise ParseError(f"expected statement, got `{tok.lexeme}`", tok.line, tok.col)

    def _state_bind(self) -> StateBind:
        sp = self._span()
        self._expect(TokenKind.STATE)
        name = self._expect_ident_like()
        self._expect(TokenKind.EQ)
        expr = self._expression()
        return StateBind(name=name, expr=expr, span=sp)

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
        expr = self._unary()
        while True:
            if self._match(TokenKind.STAR):
                op, sp = "*", self._span()
            elif self._match(TokenKind.SLASH):
                op, sp = "/", self._span()
            else:
                break
            rhs = self._unary()
            expr = BinOp(op=op, lhs=expr, rhs=rhs, span=sp)
        return expr

    def _unary(self):
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
            if self._match(TokenKind.LPAREN):
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
                    # inspect(e) already built in primary; ignore extra ()
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

        if self._match(TokenKind.COIN):
            if self._match(TokenKind.LPAREN):
                self._expect(TokenKind.RPAREN)
            return Coin(span=sp)

        if self._match(TokenKind.DIRAC):
            self._expect(TokenKind.LPAREN)
            arg = self._expression()
            self._expect(TokenKind.RPAREN)
            return Dirac(arg=arg, span=sp)

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

        if self._match(TokenKind.LPAREN):
            expr = self._expression()
            self._expect(TokenKind.RPAREN)
            return expr

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

    # --- helpers ---

    def _peek(self) -> Token:
        return self.tokens[self.i]

    def _check(self, kind: TokenKind) -> bool:
        return self._peek().kind == kind

    def _advance(self) -> Token:
        tok = self._peek()
        if tok.kind != TokenKind.EOF:
            self.i += 1
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
