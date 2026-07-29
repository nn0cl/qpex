"""Lossless token/trivia capture for LISS-0072 Slice A."""

from __future__ import annotations

from dataclasses import dataclass, field

from .lexer import Lexer
from .tokens import Token, TokenKind


@dataclass(frozen=True, slots=True)
class Trivia:
    kind: str
    text: str


@dataclass(frozen=True, slots=True)
class TriviaToken:
    token: Token
    leading_trivia: tuple[Trivia, ...] = ()
    trailing_trivia: tuple[Trivia, ...] = ()


@dataclass(frozen=True, slots=True)
class CstNode:
    kind: str
    source: str
    children: tuple[TriviaToken, ...] = field(default_factory=tuple)


def lossless_lex(source: str) -> list[TriviaToken]:
    """Return token records with attached whitespace/comment trivia.

    This keeps the existing lexer as the token authority and reconstructs
    trivia ownership from token spans in the original source.
    """

    tokens, _diagnostics = Lexer(source).tokenize()
    line_starts = _line_starts(source)
    records = [TriviaToken(token=token) for token in tokens]

    non_eof_indexes = [
        index for index, record in enumerate(records) if record.token.kind is not TokenKind.EOF
    ]
    if not non_eof_indexes:
        return records

    spans = {
        index: _token_span(source, records[index].token, line_starts) for index in non_eof_indexes
    }

    first = non_eof_indexes[0]
    first_start, _ = spans[first]
    records[first] = _with_leading(records[first], _classify_trivia(source[:first_start]))

    for current, nxt in zip(non_eof_indexes, non_eof_indexes[1:]):
        _, current_end = spans[current]
        next_start, _ = spans[nxt]
        records[current] = _with_trailing(
            records[current], _classify_trivia(source[current_end:next_start])
        )

    last = non_eof_indexes[-1]
    _, last_end = spans[last]
    records[last] = _with_trailing(records[last], _classify_trivia(source[last_end:]))

    return records


def build_lossless_cst(source: str) -> CstNode:
    """Build the initial CST root from a trivia-aware token stream."""

    return CstNode(
        kind="CompilationUnit",
        source=source,
        children=tuple(lossless_lex(source)),
    )


def _line_starts(source: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(source):
        if char == "\n":
            starts.append(index + 1)
    return starts


def _token_span(source: str, token: Token, line_starts: list[int]) -> tuple[int, int]:
    start = line_starts[token.line - 1] + token.col - 1
    end = start + len(token.lexeme)
    return start, min(end, len(source))


def _classify_trivia(text: str) -> tuple[Trivia, ...]:
    items: list[Trivia] = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("//", i):
            start = i
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            items.append(Trivia(kind="comment", text=text[start:i]))
            continue

        if text[i] in " \t\r\n":
            start = i
            while i < n and text[i] in " \t\r\n":
                i += 1
            items.append(Trivia(kind="whitespace", text=text[start:i]))
            continue

        items.append(Trivia(kind="unknown", text=text[i]))
        i += 1
    return tuple(items)


def _with_leading(record: TriviaToken, trivia: tuple[Trivia, ...]) -> TriviaToken:
    if not trivia:
        return record
    return TriviaToken(
        token=record.token,
        leading_trivia=trivia,
        trailing_trivia=record.trailing_trivia,
    )


def _with_trailing(record: TriviaToken, trivia: tuple[Trivia, ...]) -> TriviaToken:
    if not trivia:
        return record
    return TriviaToken(
        token=record.token,
        leading_trivia=record.leading_trivia,
        trailing_trivia=trivia,
    )
