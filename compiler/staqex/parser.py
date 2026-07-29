"""QPex recursive-descent Parser (Phase 2.1 subset)."""

from __future__ import annotations

from .ast_nodes import (
    AssignStmt,
    Attr,
    BinOp,
    BinderOrigin,
    Block,
    Call,
    ClassDecl,
    Coin,
    CompilationUnit,
    Dirac,
    DiscretizationBridgeDecl,
    DiscretizationDecl,
    DynamicQpuStmt,
    EnumDecl,
    EvolveBody,
    EvolveExpr,
    Expr,
    ExprStmt,
    FieldDecl,
    ForEachStmt,
    FunDecl,
    ImportDecl,
    ImplDecl,
    Inspect,
    InterfaceDecl,
    BraLit,
    KetLit,
    Lambda,
    ListExpr,
    LetBind,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    MeasureExpr,
    MainDecl,
    Measure,
    ModuleInfoDecl,
    NamespaceDecl,
    OpBin,
    OpBinder,
    OpCall,
    OpIndexed,
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
    ReturnStmt,
    Snapshot,
    ScientificScopeDecl,
    Span,
    StateBind,
    StructDecl,
    SuzukiPolicy,
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


# Names the Operator-DSL parser (_op_expression / _op_primary) reserves for
# itself: `sum`/`product` binders and the Pauli/hop atoms. An `Operator`
# bind's factory-call heuristic must never treat these as an ordinary
# function call, even when immediately followed by `(` (LISS-0051).
_OPERATOR_DSL_RESERVED_ATOMS = {"sum", "product", "adjoint", "I", "X", "Y", "Z", "hop"}
_SUPPORTED_SOURCE_VERSIONS = frozenset({"1.0"})


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0
        self.diagnostics: list[dict] = []
        self._prev: Token | None = None
        # Resolve reserved operator-looking calls against the complete source
        # declaration set.  A user callable named `Z` must remain a callable;
        # only an unresolved `Z(0)` is retired operator-index syntax.
        self._function_names = {
            tokens[index + 1].lexeme
            for index, token in enumerate(tokens[:-1])
            if token.kind == TokenKind.FUN
            and tokens[index + 1].kind == TokenKind.IDENT
        }
        # LISS-0073 Slice F: Operator-context `[A, B]` → commutator (not ListExpr).
        self._commutator_bracket_context = False

    def parse(self) -> CompilationUnit:
        start = self._span()
        package = None
        source_version = None
        imports: list[ImportDecl] = []
        decls: list = []
        main: MainDecl | None = None

        if self._check(TokenKind.PACKAGE):
            package = self._package()

        if self._at_package_source_version():
            source_version = self._package_source_version()

        while self._check(TokenKind.IMPORT):
            imports.append(self._import())

        while not self._check(TokenKind.EOF):
            if self._check(TokenKind.IDENT) and self._peek().lexeme in {
                "theory",
                "experiment",
                "workflow",
                "execution",
                "report",
                "system",
            }:
                decls.append(self._scientific_scope_decl())
            elif self._check(TokenKind.IDENT) and self._peek().lexeme == "discretization":
                decls.append(self._discretization_decl())
            elif self._check(TokenKind.IDENT) and self._peek().lexeme == "use":
                decls.append(self._discretization_bridge_decl())
            elif self._check(TokenKind.NAMESPACE):
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
                        if fun.return_type is None:
                            self.diagnostics.append(
                                {
                                    "code": "MISSING_RETURN_TYPE",
                                    "line": fun.span.line,
                                    "col": fun.span.col,
                                    "message": "`main` must declare `-> Unit`",
                                }
                            )
                        elif fun.return_type.name != "Unit":
                            self.diagnostics.append(
                                {
                                    "code": "MAIN_RETURN_TYPE_ERROR",
                                    "line": fun.span.line,
                                    "col": fun.span.col,
                                    "message": "`main` must return `Unit`",
                                }
                            )
                        if any(isinstance(stmt, ReturnStmt) for stmt in fun.body.stmts):
                            self.diagnostics.append(
                                {
                                    "code": "MAIN_RETURN_ERROR",
                                    "line": fun.span.line,
                                    "col": fun.span.col,
                                    "message": (
                                        "`main` must terminate with terminal `measure`; "
                                        "it cannot return a value"
                                    ),
                                }
                            )
                        elif fun.body.result is not None:
                            self.diagnostics.append(
                                {
                                    "code": "MAIN_RESULT_ERROR",
                                    "line": fun.span.line,
                                    "col": fun.span.col,
                                    "message": (
                                        "`main` must terminate with terminal `measure`; "
                                        "it cannot return a final expression"
                                    ),
                                }
                            )
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
                            params=fun.params,
                            body=fun.body,
                            span=fun.span,
                            return_type=fun.return_type,
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
            elif self._check(TokenKind.IMPL):
                decls.append(self._impl_decl())
            elif self._is_toplevel_executable_start():
                tok = self._peek()
                self.diagnostics.append(
                    {
                        "code": "TOPLEVEL_EXECUTION_ERROR",
                        "line": tok.line,
                        "col": tok.col,
                        "message": (
                            "executable statements are forbidden at top level; "
                            "place them inside `pub fn main() -> Unit { … }`"
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

        self._check_scientific_scope_graph(decls)
        decls = _flatten_namespaces(decls)
        return CompilationUnit(
            package=package,
            imports=imports,
            decls=decls,
            main=main,
            span=start,
            source_version=source_version,
        )

    def _package_source_version(self) -> str | None:
        tok = self._peek()
        self._expect_ident_like()  # qpex_version
        self._expect(TokenKind.EQ)
        value = self._expect(TokenKind.STRING)
        version = str(value.literal)
        if version in _SUPPORTED_SOURCE_VERSIONS:
            return version
        self.diagnostics.append(self._unsupported_source_version_diag(tok.line, tok.col, version))
        return version

    def _at_package_source_version(self) -> bool:
        return self._check(TokenKind.IDENT) and self._peek().lexeme == "qpex_version"

    @staticmethod
    def _unsupported_source_version_diag(
        line: int, col: int, version: str
    ) -> dict[str, object]:
        return {
            "code": "UNSUPPORTED_QPEX_VERSION",
            "line": line,
            "col": col,
            "message": f"unsupported qpex_version `{version}`",
        }

    def _scientific_scope_decl(self) -> ScientificScopeDecl:
        start = self._span()
        kind = self._advance().lexeme
        name = self._expect_ident_like()
        self._expect(TokenKind.LBRACE)
        depth = 1
        body: list[Token] = []
        while depth > 0 and not self._check(TokenKind.EOF):
            tok = self._advance()
            if tok.kind == TokenKind.LBRACE:
                depth += 1
            elif tok.kind == TokenKind.RBRACE:
                depth -= 1
                if depth == 0:
                    break
            body.append(tok)
        references: list[str] = []
        symbols: list[str] = []
        for index, tok in enumerate(body):
            if tok.kind != TokenKind.IDENT:
                continue
            direct_reference = index and body[index - 1].lexeme in {
                "theory",
                "experiment",
                "workflow",
                "uses",
            }
            assigned_reference = (
                index >= 2
                and body[index - 1].kind == TokenKind.EQ
                and body[index - 2].lexeme in {
                    "theory",
                    "experiment",
                    "workflow",
                    "uses",
                }
            )
            if direct_reference or assigned_reference:
                references.append(tok.lexeme)
            if index + 1 < len(body) and body[index + 1].kind == TokenKind.EQ:
                symbols.append(tok.lexeme)
        if kind == "theory" and any(
            tok.lexeme in {"shots", "backend", "retry", "Host"} for tok in body
        ):
            self.diagnostics.append(
                {
                    "code": "PHASE_SCOPE_DEPENDENCY_ERROR",
                    "line": start.line,
                    "col": start.col,
                    "message": "Theory scope cannot reference execution/Host symbols",
                }
            )
        if kind == "theory" and any(tok.lexeme == "continuous_operator" for tok in body):
            self.diagnostics.append(
                {
                    "code": "DISCRETIZATION_REQUIRED_ERROR",
                    "line": start.line,
                    "col": start.col,
                    "message": "continuous operators require an explicit discretization contract",
                }
            )
        body_declarations = self._parse_scientific_body_declarations(body)
        registers = self._parse_system_registers(body) if kind == "system" else []
        if kind == "system":
            seen_registers: set[str] = set()
            for register_name, width in registers:
                if register_name in seen_registers:
                    self.diagnostics.append(
                        {
                            "code": "MULTI_REGISTER_SHAPE_ERROR",
                            "line": start.line,
                            "col": start.col,
                            "message": f"duplicate register `{register_name}` in system `{name}`",
                        }
                    )
                if width <= 0:
                    self.diagnostics.append(
                        {
                            "code": "MULTI_REGISTER_SHAPE_ERROR",
                            "line": start.line,
                            "col": start.col,
                            "message": f"register `{register_name}` requires a positive static width",
                        }
                    )
                seen_registers.add(register_name)
        workflow_fields, workflow_parameter_types = (
            self._parse_workflow_fields(body) if kind == "workflow" else ([], [])
        )
        return ScientificScopeDecl(
            kind=kind,
            name=name,
            references=references,
            symbols=symbols,
            span=start,
            body_declarations=tuple(body_declarations),
            workflow_fields=tuple(workflow_fields),
            workflow_parameter_types=tuple(workflow_parameter_types),
            registers=tuple(registers),
        )

    @staticmethod
    def _parse_system_registers(body: list[Token]) -> list[tuple[str, int]]:
        """Read the small, declarative `system` register-shape surface."""
        registers: list[tuple[str, int]] = []
        index = 0
        while index + 6 < len(body):
            if (
                body[index].lexeme == "register"
                and body[index + 1].kind == TokenKind.IDENT
                and body[index + 2].kind == TokenKind.COLON
                and body[index + 3].lexeme == "QubitRegister"
                and body[index + 4].kind == TokenKind.LT
                and body[index + 5].kind == TokenKind.INT
                and body[index + 6].kind in {TokenKind.GT, TokenKind.GE}
            ):
                width = int(body[index + 5].literal)
                registers.append((body[index + 1].lexeme, width))
                index += 7
                continue
            index += 1
        return registers

    def _discretization_decl(self) -> DiscretizationDecl:
        start = self._span()
        self._expect_ident_like()  # discretization
        name = self._expect_ident_like()
        self._expect(TokenKind.LBRACE)
        body: list[Token] = []
        depth = 1
        while depth > 0 and not self._check(TokenKind.EOF):
            token = self._advance()
            if token.kind == TokenKind.LBRACE:
                depth += 1
            elif token.kind == TokenKind.RBRACE:
                depth -= 1
                if depth == 0:
                    break
            body.append(token)
        field_heads = {"domain", "basis", "resolution", "boundary", "approximation", "error_bound"}
        fields: list[tuple[str, str]] = []
        index = 0
        while index < len(body):
            if body[index].lexeme not in field_heads:
                index += 1
                continue
            key = body[index].lexeme
            index += 1
            if index < len(body) and body[index].kind == TokenKind.EQ:
                index += 1
            values: list[str] = []
            while index < len(body) and body[index].lexeme not in field_heads:
                values.append(body[index].lexeme)
                index += 1
            if values:
                fields.append((key, self._normalize_contract_value(values)))
        return DiscretizationDecl(name=name, fields=tuple(fields), span=start)

    def _discretization_bridge_decl(self) -> DiscretizationBridgeDecl:
        start = self._span()
        self._expect_ident_like()
        contract = self._expect_ident_like()
        self._expect(TokenKind.FOR)
        source_parts = [self._expect_ident_like()]
        while self._match(TokenKind.DOT):
            source_parts.append(self._expect_ident_like())
        as_name = self._expect_ident_like()
        if as_name != "as":
            raise ParseError("expected `as` in discretization bridge", start.line, start.col)
        alias = self._expect_ident_like()
        self._match(TokenKind.SEMI)
        return DiscretizationBridgeDecl(
            contract=contract,
            source=".".join(source_parts),
            alias=alias,
            span=start,
        )

    @staticmethod
    def _normalize_contract_value(values: list[str]) -> str:
        value = " ".join(values)
        value = value.replace(" (", "(")
        value = value.replace("( ", "(").replace(" )", ")")
        value = value.replace("[ ", "[").replace(" ]", "]")
        return value

    def _parse_workflow_fields(self, body: list[Token]) -> tuple[list[tuple[str, str]], list[str]]:
        fields: list[tuple[str, str]] = []
        parameter_types: list[str] = []
        field_heads = {"experiment", "parameter", "observable", "until", "update", "backend"}
        index = 0
        while index < len(body):
            token = body[index]
            if token.lexeme not in field_heads:
                index += 1
                continue
            key = token.lexeme
            if key == "backend":
                self.diagnostics.append(
                    {
                        "code": "WORKFLOW_SURFACE_ERROR",
                        "line": token.line,
                        "col": token.col,
                        "message": "workflow surface cannot contain provider/backend values",
                    }
                )
            index += 1
            if key == "experiment" and index < len(body) and body[index].kind == TokenKind.EQ:
                index += 1
            if key == "update" and index < len(body) and body[index].kind == TokenKind.EQ:
                index += 1
            if key == "parameter":
                if index < len(body) and body[index].kind == TokenKind.IDENT:
                    fields.append((key, body[index].lexeme))
                    index += 1
                    if index < len(body) and body[index].kind == TokenKind.COLON:
                        index += 1
                        type_tokens: list[str] = []
                        while index < len(body) and body[index].lexeme not in field_heads:
                            type_tokens.append(body[index].lexeme)
                            index += 1
                        parameter_types.append("".join(type_tokens))
                continue
            if key == "observable":
                if index < len(body) and body[index].kind == TokenKind.IDENT:
                    value = body[index].lexeme
                    if value in {"Job", "Task", "ProviderSdk"}:
                        self.diagnostics.append(
                            {
                                "code": "WORKFLOW_SURFACE_ERROR",
                                "line": body[index].line,
                                "col": body[index].col,
                                "message": f"workflow cannot observe Host value `{value}`",
                            }
                        )
                    fields.append((key, value))
                    index += 1
                continue
            if key == "experiment":
                if index < len(body) and body[index].kind == TokenKind.IDENT:
                    fields.append((key, body[index].lexeme))
                    index += 1
                continue
            if key == "update":
                expression: list[Token] = []
                while index < len(body) and body[index].lexeme not in field_heads:
                    expression.append(body[index])
                    index += 1
                if len(expression) == 1 and expression[0].kind == TokenKind.IDENT:
                    fields.append((key, expression[0].lexeme))
                else:
                    self.diagnostics.append(
                        {
                            "code": "WORKFLOW_SURFACE_ERROR",
                            "line": token.line,
                            "col": token.col,
                            "message": "update must name a Host callback",
                        }
                    )
                continue
            expression: list[str] = []
            while index < len(body) and body[index].lexeme not in field_heads:
                expression.append(body[index].lexeme)
                index += 1
            if key == "until" and expression:
                fields.append((key, " ".join(expression)))
        return fields, parameter_types

    def _parse_scientific_body_declarations(self, body: list[Token]) -> list[Any]:
        """Preserve supported declaration forms inside a scientific scope."""

        if not body:
            return []
        eof = body[-1]
        nested = Parser(body + [Token(TokenKind.EOF, "", eof.line, eof.col)])
        declarations: list[Any] = []
        while not nested._check(TokenKind.EOF):
            if nested._is_type_first_start():
                saved = nested.i
                try:
                    declarations.append(nested._type_first_bind())
                    nested._match(TokenKind.SEMI)
                    continue
                except ParseError:
                    nested.i = saved
            nested._advance()
        self.diagnostics.extend(nested.diagnostics)
        return declarations

    def _check_scientific_scope_graph(self, decls: list) -> None:
        scopes = {d.name: d for d in decls if isinstance(d, ScientificScopeDecl)}
        graph = {
            name: [ref for ref in decl.references if ref in scopes]
            for name, decl in scopes.items()
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(name: str) -> None:
            if name in visiting:
                decl = scopes[name]
                self.diagnostics.append(
                    {
                        "code": "PHASE_SCOPE_CYCLE_ERROR",
                        "line": decl.span.line,
                        "col": decl.span.col,
                        "message": f"scientific scope dependency cycle includes `{name}`",
                    }
                )
                return
            if name in visited:
                return
            visiting.add(name)
            for child in graph.get(name, []):
                visit(child)
            visiting.remove(name)
            visited.add(name)

        for name in graph:
            visit(name)

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
        """Look at token after an optional visibility keyword (`pub`/`private`)."""
        j = self.i
        if self.tokens[j].kind in {TokenKind.PUBLIC, TokenKind.PRIVATE}:
            j += 1
        if j < len(self.tokens):
            return self.tokens[j].kind
        return None

    def _parse_visibility(self) -> str:
        """ADR 0058: `pub` | `private` | (default → module-private)."""
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
        """Parse a `module-info.sqx` compilation unit (ADR 0058)."""
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
        generic_bounds = self._generic_bounds()
        self._expect(TokenKind.LPAREN)
        params: list[Param] = []
        if not self._check(TokenKind.RPAREN):
            params.append(self._param())
            while self._match(TokenKind.COMMA):
                params.append(self._param())
        self._expect(TokenKind.RPAREN)
        return_type = None
        if self._match(TokenKind.ARROW):
            return_type = self._type_ref()
        effects = self._effects_clause()
        operator_return = return_type is not None and return_type.name == "Operator"
        body = self._block(operator_return=operator_return)
        if name not in {"init", "main"} and return_type is None:
            self.diagnostics.append(
                {
                    "code": "MISSING_RETURN_TYPE",
                    "line": sp.line,
                    "col": sp.col,
                    "message": f"`{name}` must declare an explicit return type",
                }
            )
        return FunDecl(
            name=name,
            params=params,
            body=body,
            span=sp,
            return_type=return_type,
            visibility=vis,
            effects=tuple(effects),
            generic_bounds=tuple(generic_bounds),
        )

    def _effects_clause(self) -> list[str]:
        """Parse the optional fixed effect annotation after a return type."""
        if self._peek().lexeme != "effects":
            return []
        self._advance()
        self._expect(TokenKind.LBRACE)
        effects: list[str] = []
        if not self._check(TokenKind.RBRACE):
            effects.append(self._expect_ident_like())
            while self._match(TokenKind.COMMA):
                effects.append(self._expect_ident_like())
        self._expect(TokenKind.RBRACE)
        return effects

    def _generic_bounds(self) -> list[tuple[str, str]]:
        """Parse the accepted inline `<T: Interface>` bound form."""
        if not self._match(TokenKind.LT):
            return []
        bounds: list[tuple[str, str]] = []
        while True:
            type_param = self._expect_ident_like()
            self._expect(TokenKind.COLON)
            bounds.append((type_param, self._expect_ident_like()))
            if not self._match(TokenKind.COMMA):
                break
        self._expect(TokenKind.GT)
        return bounds

    def _param(self) -> Param:
        name = self._expect_ident_like()
        ty = None
        if self._match(TokenKind.COLON):
            ty = self._type_ref()
        return Param(name=name, ty=ty)

    def _type_ref(self) -> TypeRef:
        """Type reference with symbolic/numeric args, e.g. `QubitRegister<3>`."""
        # Product carrier: (T1, T2, …)
        if self._match(TokenKind.LPAREN):
            args = [self._type_ref()]
            while self._match(TokenKind.COMMA):
                args.append(self._type_ref())
            self._expect(TokenKind.RPAREN)
            return TypeRef(name="Tuple", args=args)

        tok = self._peek()
        if tok.kind == TokenKind.INT:
            name = str(self._advance().literal)
        elif tok.kind == TokenKind.IDENT:
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
            if self._match(TokenKind.RANGE):
                if name != "Index":
                    tok = self._peek()
                    raise ParseError("inclusive ranges are only valid for `Index`", tok.line, tok.col)
                args.append(self._type_ref())
            else:
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
                                f"or `fn` method; got `{tok.lexeme}`"
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
        type_params: list[str] = []
        if self._match(TokenKind.LT):
            type_params.append(self._expect_ident_like())
            while self._match(TokenKind.COMMA):
                type_params.append(self._expect_ident_like())
            self._expect(TokenKind.GT)
        if self._match(TokenKind.LBRACE):
            depth = 1
            while depth > 0 and not self._check(TokenKind.EOF):
                if self._check(TokenKind.LBRACE):
                    depth += 1
                elif self._check(TokenKind.RBRACE):
                    depth -= 1
                self._advance()
        return InterfaceDecl(name=name, span=sp, type_params=tuple(type_params))

    def _impl_decl(self) -> ImplDecl:
        sp = self._span()
        self._expect(TokenKind.IMPL)
        interface = self._type_ref()
        self._expect(TokenKind.FOR)
        target = self._type_ref()
        self._expect(TokenKind.LBRACE)
        methods: list[FunDecl] = []
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            methods.append(self._fun_decl())
        self._expect(TokenKind.RBRACE)
        return ImplDecl(interface=interface, target=target, methods=methods, span=sp)

    def _block(self, *, operator_return: bool = False) -> Block:
        sp = self._span()
        self._expect(TokenKind.LBRACE)
        stmts = []
        result = None
        while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
            if self._check(TokenKind.FORBIDDEN) or self._check(TokenKind.RETIRED):
                self._advance()
                continue
            if self._check(TokenKind.ERROR):
                self._advance()
                continue
            if self._check(TokenKind.RETURN):
                returned = self._return_stmt(operator_return=operator_return)
                stmts.append(returned)
                result = returned.expr
                if not self._check(TokenKind.RBRACE):
                    tok = self._peek()
                    self.diagnostics.append(
                        {
                            "code": "RETURN_NOT_TERMINAL",
                            "line": tok.line,
                            "col": tok.col,
                            "message": "`return` must be the final statement in a function",
                        }
                    )
                    while not self._check(TokenKind.RBRACE) and not self._check(TokenKind.EOF):
                        self._advance()
                break
            saved = self.i
            try:
                stmts.append(self._stmt())
            except ParseError:
                # Implicit final expressions are retained only for parser
                # recovery; the typechecker rejects them for ordinary fns.
                self.i = saved
                result = self._expression()
                if not self._check(TokenKind.RBRACE):
                    tok = self._peek()
                    raise ParseError(
                        "function result expression must be the final item in a block",
                        tok.line,
                        tok.col,
                    )
                break
        self._expect(TokenKind.RBRACE)
        return Block(stmts=stmts, span=sp, result=result)

    def _return_stmt(self, *, operator_return: bool = False) -> ReturnStmt:
        sp = self._span()
        self._expect(TokenKind.RETURN)
        expression = self._op_expression() if operator_return else self._expression()
        return ReturnStmt(expr=expression, span=sp)

    def _stmt(self):
        if self._check(TokenKind.FOREACH):
            return self._foreach_stmt()
        if self._check(TokenKind.DYNAMIC):
            return self._dynamic_qpu_stmt()
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
                if isinstance(target, Call):
                    return ExprStmt(expr=target, span=target.span)
            except ParseError:
                pass
            self.i = saved
        tok = self._peek()
        raise ParseError(f"expected statement, got `{tok.lexeme}`", tok.line, tok.col)

    def _foreach_stmt(self) -> ForEachStmt:
        """Parse static circuit elaboration: `forEach q in register(3) { … }`."""
        sp = self._span()
        self._expect(TokenKind.FOREACH)
        element = self._expect_ident_like()
        self._expect(TokenKind.IN)
        collection = self._expression()
        body = self._block()
        return ForEachStmt(element=element, collection=collection, body=body, span=sp)

    def _dynamic_qpu_stmt(self) -> DynamicQpuStmt:
        """Parse an explicit dynamic lane for capability diagnostics."""
        sp = self._span()
        self._expect(TokenKind.DYNAMIC)
        name = self._expect_ident_like()
        if name != "qpu":
            raise ParseError(
                "dynamic lane must be written as `dynamic qpu { … }`",
                sp.line,
                sp.col,
            )
        return DynamicQpuStmt(body=self._block(), span=sp)

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
            # LISS-0073: Dirac ket/bra and algebra brackets desugar to `Call`
            # nodes (`outer` / `projector` / `inner` / `commutator` /
            # `anticommutator`), not OpDSL atoms.
            if self._peek().kind in (TokenKind.KET, TokenKind.BRA):
                expr = self._expression()
            elif self._peek().kind in (TokenKind.LBRACKET, TokenKind.LBRACE):
                self._commutator_bracket_context = (
                    self._peek().kind == TokenKind.LBRACKET
                )
                try:
                    expr = self._expression()
                finally:
                    self._commutator_bracket_context = False
            elif (
                self._peek().kind == TokenKind.IDENT
                and (
                    self._peek().lexeme not in _OPERATOR_DSL_RESERVED_ATOMS
                    or self._peek().lexeme in self._function_names
                )
                and self._peek_at_kind(1) == TokenKind.LPAREN
            ):
                expr = self._expression()
            else:
                expr = self._op_expression()  # type: ignore[assignment]
        elif ty.name in {
            "FermionOperator",
            "BosonOperator",
            "SpinOperator",
            "QubitOperator",
        }:
            if (
                self._peek().kind == TokenKind.IDENT
                and self._peek_at_kind(1) == TokenKind.LBRACKET
            ):
                # Second-quantized indexed atoms share the Operator DSL AST;
                # only mapping calls such as `map(Hf, JordanWigner)` remain
                # ordinary expression calls.
                expr = self._op_expression()
            else:
                expr = self._expression()
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
        povm = None
        if self._peek().kind == TokenKind.IDENT and self._peek().lexeme == "with":
            self._advance()
            povm = self._expression()
        sink = None
        if self._match(TokenKind.TO):
            sink = self._expect_ident_like()
        return Measure(expr=expr, span=sp, sink=sink, povm=povm)

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
            elif self._match(TokenKind.DAGGER):
                # LISS-0073 Slice E: expression postfix † → adjoint(…)
                # (OpDSL keeps OpCall("adjoint") via _op_postfix).
                expr = self._algebra_call("adjoint", [expr], expr.span)
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
            return self._ket_or_outer(tok, sp)
        if self._match(TokenKind.BRA):
            return self._bra_or_inner(tok, sp)

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

        if self._match(TokenKind.MEASURE):
            # Expression-position measurement is retained only so a boundary
            # checker can reject it precisely (especially in a forEach bound).
            inner = self._expression()
            return MeasureExpr(expr=inner, span=sp)

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

        if self._match(TokenKind.LBRACKET):
            items = self._comma_expr_items(TokenKind.RBRACKET)
            # Slice F: Operator-context exactly-two `[A, B]` → commutator.
            if self._commutator_bracket_context:
                if len(items) != 2:
                    raise ParseError(
                        "commutator brackets `[A, B]` require exactly two operands",
                        sp.line,
                        sp.col,
                    )
                return self._algebra_call("commutator", items, sp)
            return ListExpr(items=items, span=sp)

        if self._match(TokenKind.LBRACE):
            # Slice F: `{A, B}` → anticommutator (no set/dict literal in MVP).
            items = self._comma_expr_items(TokenKind.RBRACE)
            if len(items) != 2:
                raise ParseError(
                    "anticommutator braces `{A, B}` require exactly two operands",
                    sp.line,
                    sp.col,
                )
            return self._algebra_call("anticommutator", items, sp)

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
            suzuki = self._suzuki_policy()
            until_predicate = None
            max_steps = None
            if self._match(TokenKind.UNTIL):
                until_predicate = self._expression()
                if self._match(TokenKind.MAX):
                    max_steps = self._expression()
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
                until_predicate=until_predicate,
                max_steps=max_steps,
                suzuki=suzuki,
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

    def _suzuki_policy(self) -> SuzukiPolicy | None:
        if self._peek().lexeme != "using":
            return None
        sp = self._span()
        self._advance()
        name = self._expect_ident_like()
        if name != "Suzuki":
            raise ParseError(
                "evolve `using` currently supports only `Suzuki(...)`",
                sp.line,
                sp.col,
            )
        self._expect(TokenKind.LPAREN)
        values: dict[str, Expr] = {}
        while not self._check(TokenKind.RPAREN):
            key = self._expect_ident_like()
            self._expect(TokenKind.EQ)
            values[key] = self._expression()
            if not self._match(TokenKind.COMMA):
                break
        self._expect(TokenKind.RPAREN)
        order = values.get("order", LitInt(value=0, span=sp))
        error_mode = None
        error = values.get("error")
        if isinstance(error, Var):
            error_mode = error.name
        return SuzukiPolicy(
            order=order,
            steps=values.get("steps"),
            tolerance=values.get("tolerance"),
            error_mode=error_mode,
            span=sp,
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

    def _ket_or_outer(self, ket_tok: Token, span: Span):
        """Alone ket or Slice D `|ψ⟩⟨φ|` → `outer` / matching-label `projector`."""
        ket = KetLit(label=str(ket_tok.literal), span=span)
        if not self._check(TokenKind.BRA):
            return ket
        bra_tok = self._advance()
        bra = BraLit(label=str(bra_tok.literal), span=span)
        if bra.label == ket.label:
            return self._algebra_call("projector", [ket], span)
        return self._algebra_call("outer", [ket, bra], span)

    def _bra_or_inner(self, bra_tok: Token, span: Span):
        """Alone bra, `⟨φ|ψ⟩` inner, or `⟨φ|A|ψ⟩` → `inner(φ, A(ψ))` (Slices A–C)."""
        bra = BraLit(label=str(bra_tok.literal), span=span)
        if self._check(TokenKind.KET):
            return self._inner_call(bra, self._take_ket_lit(), span)
        # Slice C: speculative mid-expr then trailing ket (restore on miss).
        saved_i, saved_prev = self.i, self._prev
        try:
            mid = self._call()
        except ParseError:
            self.i, self._prev = saved_i, saved_prev
            return bra
        if not self._check(TokenKind.KET):
            self.i, self._prev = saved_i, saved_prev
            return bra
        ket = self._take_ket_lit()
        applied = Call(callee=mid, args=[ket], span=span)
        return self._inner_call(bra, applied, span)

    def _take_ket_lit(self) -> KetLit:
        ket_tok = self._advance()
        return KetLit(
            label=str(ket_tok.literal),
            span=Span(line=ket_tok.line, col=ket_tok.col),
        )

    def _inner_call(self, left: Expr, right: Expr, span: Span) -> Call:
        return self._algebra_call("inner", [left, right], span)

    def _algebra_call(self, name: str, args: list[Expr], span: Span) -> Call:
        return Call(callee=Var(name=name, span=span), args=args, span=span)

    def _comma_expr_items(self, closer: TokenKind) -> list[Expr]:
        items: list[Expr] = []
        if not self._check(closer):
            items.append(self._expression())
            while self._match(TokenKind.COMMA):
                items.append(self._expression())
        self._expect(closer)
        return items

    def _comma_op_expr_items(self, closer: TokenKind) -> list:
        items: list = []
        if not self._check(closer):
            items.append(self._op_expression())
            while self._match(TokenKind.COMMA):
                items.append(self._op_expression())
        self._expect(closer)
        return items

    def _peek(self) -> Token:
        return self.tokens[self.i]

    def _peek_at_kind(self, offset: int) -> TokenKind | None:
        index = self.i + offset
        if index >= len(self.tokens):
            return None
        return self.tokens[index].kind

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
        return self._op_comparison()

    def _op_comparison(self):
        expr = self._op_sum()
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
            rhs = self._op_sum()
            expr = OpBin(op=op, lhs=expr, rhs=rhs, span=sp)
        return expr

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
        return self._op_postfix()

    def _op_postfix(self):
        """Apply zero or more postfix operator-DSL suffixes.

        LISS-0069: postfix `†` is dual-accept sugar for `adjoint(…)`.
        """
        expr = self._op_primary()
        while self._match(TokenKind.DAGGER):
            expr = OpCall(name="adjoint", args=[expr], span=expr.span)
        return expr

    def _op_primary(self):
        sp = self._span()
        if self._match(TokenKind.LPAREN):
            expr = self._op_expression()
            self._expect(TokenKind.RPAREN)
            return expr
        if self._match(TokenKind.LBRACKET):
            # LISS-0073 Slice F: OpDSL `[A, B]` → commutator (expression Call).
            items = self._comma_op_expr_items(TokenKind.RBRACKET)
            if len(items) != 2:
                raise ParseError(
                    "commutator brackets `[A, B]` require exactly two operands",
                    sp.line,
                    sp.col,
                )
            return self._algebra_call("commutator", items, sp)
        if self._match(TokenKind.LBRACE):
            items = self._comma_op_expr_items(TokenKind.RBRACE)
            if len(items) != 2:
                raise ParseError(
                    "anticommutator braces `{A, B}` require exactly two operands",
                    sp.line,
                    sp.col,
                )
            return self._algebra_call("anticommutator", items, sp)
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
            if name in {"sum", "product"}:
                return self._op_binder(name, sp)
            if name == "N":
                return OpNumber(span=sp)
            if name == "Q":
                return OpQuadrature(kind="Q", span=sp)
            if name == "P":
                # Momentum: Fock or Position-grid — resolved by op_space / evolve carrier
                return OpQuadrature(kind="P", span=sp)
            if name == "hop":
                # hop(i, j) → |i⟩⟨j| on discrete site / Fock-label basis.
                # Any reserved name parsed here that can be immediately
                # followed by `(` must stay listed in
                # _OPERATOR_DSL_RESERVED_ATOMS (LISS-0051), or an
                # `Operator` bind's factory-call heuristic will shadow it.
                self._expect(TokenKind.LPAREN)
                i_tok = self._expect(TokenKind.INT)
                self._expect(TokenKind.COMMA)
                j_tok = self._expect(TokenKind.INT)
                self._expect(TokenKind.RPAREN)
                return OpHop(i=int(i_tok.literal), j=int(j_tok.literal), span=sp)
            if name in {"I", "X", "Y", "Z"}:
                # Pauli atom with an optional site, e.g. `Z(0)`. Listed in
                # _OPERATOR_DSL_RESERVED_ATOMS (LISS-0051) so an `Operator`
                # bind's factory-call heuristic never shadows it.
                site = None
                if self._match(TokenKind.LPAREN):
                    args: list = []
                    if not self._check(TokenKind.RPAREN):
                        args.append(self._op_expression())
                        while self._match(TokenKind.COMMA):
                            args.append(self._op_expression())
                    self._expect(TokenKind.RPAREN)
                    # A declaration named like an atom is handled by the
                    # generic expression path in `_type_first_bind`; this
                    # marker is only used for unresolved operator syntax.
                    return OpCall(name=name, args=args, span=sp)
                base = OpPauli(kind=name.upper(), site=site, span=sp)
            else:
                if self._match(TokenKind.LPAREN):
                    args: list = []
                    if not self._check(TokenKind.RPAREN):
                        args.append(self._op_expression())
                        while self._match(TokenKind.COMMA):
                            args.append(self._op_expression())
                    self._expect(TokenKind.RPAREN)
                    return OpCall(name=name, args=args, span=sp)
                base = OpVar(name=name, span=sp)
            if self._match(TokenKind.LBRACKET):
                index = self._op_expression()
                self._expect(TokenKind.RBRACKET)
                return OpIndexed(base=base, index=index, span=sp)
            return base
        raise ParseError(
            f"expected operator expression, got `{tok.lexeme}`", tok.line, tok.col
        )

    def _op_binder(self, kind: str, sp: Span):
        self._expect(TokenKind.LPAREN)
        bindings = []
        while True:
            variable = self._expect_ident_like()
            self._expect(TokenKind.IN)
            if self._check(TokenKind.IDENT) and self._peek_at_kind(1) == TokenKind.LT:
                domain = self._type_ref()
            else:
                domain = OpVar(name=self._expect_ident_like(), span=self._span())
            bindings.append((variable, domain))
            if not self._match(TokenKind.COMMA):
                break
        self._expect(TokenKind.RPAREN)
        guard = None
        if self._check(TokenKind.IDENT) and self._peek().lexeme == "where":
            self._advance()
            guard = self._op_comparison()
        self._expect(TokenKind.LBRACE)
        body = self._op_expression()
        self._expect(TokenKind.RBRACE)
        origin = BinderOrigin(
            source_span=sp,
            variables=tuple(variable for variable, _domain in bindings),
            desugared=len(bindings) > 1,
        )
        for variable, domain in reversed(bindings):
            body = OpBinder(
                kind=kind,
                variable=variable,
                domain=domain,
                body=body,
                span=sp,
                guard=guard,
                origin=origin,
            )
            guard = None
        return body
