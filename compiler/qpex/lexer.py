"""QPex Lexer (ADR 0035 / qpex-token-specification.md)."""

from __future__ import annotations

from .tokens import (
    ACTIVE,
    CONTEXTUAL,
    FORBIDDEN,
    FORBIDDEN_MESSAGES,
    RETIRED,
    Token,
    TokenKind,
)


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.i = 0
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []
        self.diagnostics: list[dict] = []

    def tokenize(self) -> tuple[list[Token], list[dict]]:
        while not self._at_end():
            self._skip_trivia()
            if self._at_end():
                break
            start_line, start_col = self.line, self.col
            c = self._peek()

            if c.isalpha() or c == "_":
                self._ident_or_keyword(start_line, start_col)
                continue
            if c.isdigit():
                self._number(start_line, start_col)
                continue
            if c in "\"'":
                self._string(start_line, start_col)
                continue

            # multi-char ops
            if c == "|" and self._peek_at(1) == ">":
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenKind.PIPE_OP, "|>", start_line, start_col))
                continue
            if c == "-" and self._peek_at(1) == ">":
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenKind.ARROW, "->", start_line, start_col))
                continue
            if c == "=" and self._peek_at(1) == "=":
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenKind.EQEQ, "==", start_line, start_col))
                continue
            if c == "!" and self._peek_at(1) == "=":
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenKind.NEQ, "!=", start_line, start_col))
                continue
            if c == "<" and self._peek_at(1) == "=":
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenKind.LE, "<=", start_line, start_col))
                continue
            if c == ">" and self._peek_at(1) == "=":
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenKind.GE, ">=", start_line, start_col))
                continue

            single = {
                "+": TokenKind.PLUS,
                "-": TokenKind.MINUS,
                "*": TokenKind.STAR,
                "/": TokenKind.SLASH,
                "=": TokenKind.EQ,
                "<": TokenKind.LT,
                ">": TokenKind.GT,
                "(": TokenKind.LPAREN,
                ")": TokenKind.RPAREN,
                "{": TokenKind.LBRACE,
                "}": TokenKind.RBRACE,
                "[": TokenKind.LBRACKET,
                "]": TokenKind.RBRACKET,
                ",": TokenKind.COMMA,
                ".": TokenKind.DOT,
                ":": TokenKind.COLON,
                ";": TokenKind.SEMI,
            }
            if c in single:
                self._advance()
                self.tokens.append(Token(single[c], c, start_line, start_col))
                continue

            # unknown char — skip with error
            self._advance()
            self.diagnostics.append(
                {
                    "code": "LEX_ERROR",
                    "line": start_line,
                    "col": start_col,
                    "message": f"unexpected character {c!r}",
                }
            )
            self.tokens.append(Token(TokenKind.ERROR, c, start_line, start_col))

        self.tokens.append(Token(TokenKind.EOF, "", self.line, self.col))
        return self.tokens, self.diagnostics

    def _ident_or_keyword(self, line: int, col: int) -> None:
        start = self.i
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        lexeme = self.source[start : self.i]

        if lexeme in FORBIDDEN:
            self.diagnostics.append(
                {
                    "code": "FORBIDDEN_KEYWORD",
                    "token": lexeme,
                    "line": line,
                    "col": col,
                    "message": FORBIDDEN_MESSAGES.get(
                        lexeme, f"forbidden keyword `{lexeme}` (ADR 0035)"
                    ),
                }
            )
            self.tokens.append(Token(TokenKind.FORBIDDEN, lexeme, line, col))
            return

        if lexeme in RETIRED:
            repl = RETIRED[lexeme]
            self.diagnostics.append(
                {
                    "code": "RETIRED_KEYWORD",
                    "token": lexeme,
                    "replacement": repl,
                    "line": line,
                    "col": col,
                    "message": f"retired `{lexeme}` → use `{repl}`",
                }
            )
            self.tokens.append(
                Token(TokenKind.RETIRED, lexeme, line, col, meta={"replacement": repl})
            )
            return

        if lexeme in ACTIVE:
            self.tokens.append(Token(ACTIVE[lexeme], lexeme, line, col))
            return

        if lexeme in CONTEXTUAL:
            self.tokens.append(Token(CONTEXTUAL[lexeme], lexeme, line, col))
            return

        self.tokens.append(Token(TokenKind.IDENT, lexeme, line, col))

    def _number(self, line: int, col: int) -> None:
        start = self.i
        while not self._at_end() and self._peek().isdigit():
            self._advance()
        if not self._at_end() and self._peek() == "." and self._peek_at(1).isdigit():
            self._advance()
            while not self._at_end() and self._peek().isdigit():
                self._advance()
            lexeme = self.source[start : self.i]
            self.tokens.append(Token(TokenKind.FLOAT, lexeme, line, col, literal=float(lexeme)))
            return
        lexeme = self.source[start : self.i]
        self.tokens.append(Token(TokenKind.INT, lexeme, line, col, literal=int(lexeme)))

    def _string(self, line: int, col: int) -> None:
        quote = self._advance()
        chars: list[str] = []
        while not self._at_end() and self._peek() != quote:
            if self._peek() == "\\" and not self._at_end_at(1):
                self._advance()
                chars.append(self._advance())
            else:
                chars.append(self._advance())
        if self._at_end():
            self.diagnostics.append(
                {"code": "LEX_ERROR", "line": line, "col": col, "message": "unterminated string"}
            )
            self.tokens.append(Token(TokenKind.ERROR, "".join(chars), line, col))
            return
        self._advance()  # closing quote
        value = "".join(chars)
        self.tokens.append(Token(TokenKind.STRING, value, line, col, literal=value))

    def _skip_trivia(self) -> None:
        while not self._at_end():
            c = self._peek()
            if c in " \t\r":
                self._advance()
                continue
            if c == "\n":
                self._advance()
                continue
            if c == "/" and self._peek_at(1) == "/":
                while not self._at_end() and self._peek() != "\n":
                    self._advance()
                continue
            break

    def _at_end(self) -> bool:
        return self.i >= len(self.source)

    def _at_end_at(self, offset: int) -> bool:
        return self.i + offset >= len(self.source)

    def _peek(self) -> str:
        return self.source[self.i]

    def _peek_at(self, offset: int) -> str:
        j = self.i + offset
        if j >= len(self.source):
            return "\0"
        return self.source[j]

    def _advance(self) -> str:
        c = self.source[self.i]
        self.i += 1
        if c == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return c
