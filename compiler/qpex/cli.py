"""QPex CLI — run / check / inspect / repl (Phase 3)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TextIO

from .ir.dag import lower_source_ast
from .pipeline import compile_source
from .run import HARD_CODES, run_source
from .runtime.evaluator import Evaluator
from .stdlib.io_ops import format_marginal_table
from .stdlib.prelude import PRELUDE_NAMES


def cmd_run(args: argparse.Namespace) -> int:
    source = _load_source(args)
    result = run_source(source, seed=args.seed, stdout=sys.stdout)
    if not result.compile_ok:
        _print_diags(result.diagnostics)
        return 1
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    source = _load_source(args)
    compiled = compile_source(source)
    diags = compiled.diagnostics
    # check focuses on Forbidden / Retired / Early Collapse / Parse
    interesting = [
        d
        for d in diags
        if d.get("code")
        in {
            "FORBIDDEN_KEYWORD",
            "RETIRED_KEYWORD",
            "EARLY_COLLAPSE_ERROR",
            "PARSE_ERROR",
            "LEX_ERROR",
            "TYPE_NOT_STATE",
        }
    ]
    if not interesting:
        print("ok — no vocabulary / collapse / parse issues")
        if args.dag and compiled.unit is not None:
            dag = lower_source_ast(compiled.unit)
            print(f"dag nodes: {dag.summary()['node_count']}")
        return 0
    for d in interesting:
        code = d.get("code")
        msg = d.get("message", "")
        line = d.get("line", "?")
        fix = ""
        if code == "RETIRED_KEYWORD" and d.get("replacement"):
            fix = f"  (fix-it: use `{d['replacement']}`)"
        print(f"{code}:{line}: {msg}{fix}", file=sys.stderr)
    hard = any(d.get("code") in HARD_CODES for d in interesting)
    return 1 if hard else 0  # retired-only → exit 0? use 0 for warn-only


def cmd_inspect(args: argparse.Namespace) -> int:
    """Non-destructive: compile, eval pure stmts, print marginal tables (no measure sample)."""
    source = _load_source(args)
    # Strip terminal measure for inspect mode — show joint before collapse
    compiled = compile_source(source)
    if compiled.unit is None or any(d.get("code") in HARD_CODES for d in compiled.diagnostics):
        _print_diags(compiled.diagnostics)
        return 1
    unit = compiled.unit
    # drop Measure stmts for inspect
    from .ast_nodes import Measure

    if unit.main is not None:
        unit.main.body.stmts = [s for s in unit.main.body.stmts if not isinstance(s, Measure)]
    buf: TextIO = sys.stdout
    ev = Evaluator(seed=args.seed, inspect_sink=buf)
    result = ev.run_unit(unit, stdout=buf)
    print("--- joint marginals ---")
    for var in result.joint.variables():
        print(format_marginal_table(result.joint.marginal(var), label=var), end="")
    if result.joint.is_vacuum():
        print("(vacuum)")
    if args.dag:
        # recompile original for dag
        full = compile_source(source)
        if full.unit:
            print(lower_source_ast(full.unit).to_dot())
    return 0


def cmd_repl(args: argparse.Namespace) -> int:
    print("QPex REPL — enter statements; blank line runs; :quit to exit")
    print(f"Prelude: {', '.join(sorted(PRELUDE_NAMES))}")
    buf: list[str] = []
    seed = args.seed
    while True:
        try:
            line = input("qpex> " if not buf else "...   ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if line.strip() in {":quit", ":exit", ":q"}:
            return 0
        if line.strip() == ":clear":
            buf.clear()
            continue
        if line.strip() == "" and buf:
            source = "\n".join(buf) + "\n"
            buf.clear()
            # auto-measure last state if no measure
            if "measure" not in source:
                # find last state name
                last = None
                for ln in source.splitlines():
                    s = ln.strip()
                    if s.startswith("state "):
                        last = s.split("=")[0].replace("state", "").strip()
                if last:
                    source = source + f"measure {last}\n"
            result = run_source(source, seed=seed, stdout=sys.stdout)
            if not result.compile_ok:
                _print_diags(result.diagnostics)
            continue
        buf.append(line)


def cmd_dag(args: argparse.Namespace) -> int:
    source = _load_source(args)
    compiled = compile_source(source)
    if compiled.unit is None:
        _print_diags(compiled.diagnostics)
        return 1
    dag = lower_source_ast(compiled.unit)
    if args.dot:
        print(dag.to_dot(), end="")
    else:
        print(dag.summary())
    return 0


def _load_source(args: argparse.Namespace) -> str:
    if getattr(args, "expr", None):
        return args.expr
    if getattr(args, "file", None):
        return Path(args.file).read_text(encoding="utf-8")
    raise SystemExit("provide a file or -e source")


def _print_diags(diags: list) -> None:
    for d in diags:
        print(f"{d.get('code')}: {d.get('message')}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qpex", description="QPex toolchain (Phase 3)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_src(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("file", nargs="?", help=".qpex source file")
        sp.add_argument("-e", "--eval", dest="expr", help="source string")
        sp.add_argument("--seed", type=int, default=None)

    pr = sub.add_parser("run", help="compile and execute (terminal measure)")
    add_src(pr)
    pr.set_defaults(func=cmd_run)

    pc = sub.add_parser("check", help="lint Forbidden/Retired + Early Collapse")
    add_src(pc)
    pc.add_argument("--dag", action="store_true", help="print DAG node count if ok")
    pc.set_defaults(func=cmd_check)

    pi = sub.add_parser("inspect", help="non-destructive joint dump (no sample)")
    add_src(pi)
    pi.add_argument("--dag", action="store_true", help="also print DOT DAG")
    pi.set_defaults(func=cmd_inspect)

    pd = sub.add_parser("dag", help="lower AST to computation DAG IR")
    add_src(pd)
    pd.add_argument("--dot", action="store_true", help="emit Graphviz DOT")
    pd.set_defaults(func=cmd_dag)

    prepl = sub.add_parser("repl", help="interactive shell")
    prepl.add_argument("--seed", type=int, default=None)
    prepl.set_defaults(func=cmd_repl)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # backward compat: `qpex file.qpex` / `qpex -e ...` → run
    if argv and argv[0] not in {
        "run",
        "check",
        "inspect",
        "dag",
        "repl",
        "-h",
        "--help",
    }:
        argv = ["run", *argv]
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
