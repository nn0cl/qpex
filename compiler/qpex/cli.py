"""QPex CLI — run / check / inspect / emit-qasm / repl (Phase 3–4)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TextIO

from .codegen.openqasm import emit_openqasm3
from .ir.dag import lower_source_ast
from .pipeline import compile_path, compile_source
from .run import HARD_CODES
from .host import run_path as host_run_path, run_source as host_run_source
from .runtime.evaluator import Evaluator
from .stdlib.io_ops import format_marginal_table
from .stdlib.prelude import PRELUDE_NAMES


def _compile_args(args: argparse.Namespace):
    """Prefer path-linked compile when a file is given (ADR 0054)."""
    if getattr(args, "expr", None):
        return compile_source(args.expr)
    if getattr(args, "file", None):
        return compile_path(args.file)
    raise SystemExit("provide a file or -e source")


def _run_args(args: argparse.Namespace, *, stdout: TextIO | None = None):
    seed = getattr(args, "seed", None)
    out = stdout if stdout is not None else sys.stdout
    settings = {"target": getattr(args, "target", "cpu"), "seed": seed}
    if getattr(args, "expr", None):
        return host_run_source(args.expr, settings=settings, stdout=out)
    if getattr(args, "file", None):
        return host_run_path(args.file, settings=settings, stdout=out)
    raise SystemExit("provide a file or -e source")


def _parse_target(raw: str | None) -> tuple[str, str | None]:
    """Return (family, profile) e.g. ('cpu', None), ('qpu', 'openqasm3')."""
    if raw is None or raw == "":
        return "cpu", None
    t = raw.strip().lower()
    if t in {"cpu", "local", "sim", "simulator"}:
        return "cpu", None
    if t in {"gpu", "cuda"}:
        return "gpu", None
    if t.startswith("qpu:"):
        return "qpu", t.split(":", 1)[1] or "openqasm3"
    if t == "qpu":
        return "qpu", "openqasm3"
    raise SystemExit(f"unknown --target {raw!r} (use cpu|gpu|qpu:openqasm3|qpu:<profile>)")


def cmd_run(args: argparse.Namespace) -> int:
    family, profile = _parse_target(getattr(args, "target", None))

    if getattr(args, "emit_qasm", False) or family == "qpu":
        compiled = _compile_args(args)
        if compiled.unit is None or any(d.get("code") in HARD_CODES for d in compiled.diagnostics):
            _print_diags(compiled.diagnostics)
            return 1
        topo = "linear"
        if profile and profile.startswith("grid"):
            topo = profile
        elif profile in {"linear", "grid", "grid-2x2", "grid-3x3"}:
            topo = profile
        emitted = emit_openqasm3(compiled.unit, topology=topo, route=True)
        for n in emitted.notes:
            print(f"// note: {n}", file=sys.stderr)
        if not emitted.ok:
            return 1
        text = emitted.qasm if emitted.qasm.endswith("\n") else emitted.qasm + "\n"
        out_path = getattr(args, "output", None)
        if out_path:
            Path(out_path).write_text(text, encoding="utf-8")
            print(f"// wrote {out_path}", file=sys.stderr)
        else:
            print(text, end="")
        if family == "qpu" and profile not in {None, "openqasm3", "linear", "grid", "grid-2x2", "grid-3x3"}:
            print(
                f"// qpu cloud submit reserved (profile={profile}); OpenQASM emitted locally",
                file=sys.stderr,
            )
        if family == "qpu" and not getattr(args, "also_run", False):
            return 0

    if family == "gpu":
        print(
            "gpu target reserved (Phase 4.2); falling back to cpu Joint",
            file=sys.stderr,
        )

    result = _run_args(args, stdout=sys.stdout)
    if result.status != "succeeded":
        _print_diags(list(result.diagnostics))
        return 1
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    family, profile = _parse_target(getattr(args, "target", None))
    compiled = _compile_args(args)
    diags = compiled.diagnostics
    interesting = [
        d
        for d in diags
        if d.get("code")
        in {
            "FORBIDDEN_KEYWORD",
            "RETIRED_KEYWORD",
            "EARLY_COLLAPSE_ERROR",
            "NESTED_WHEN_ERROR",
            "PARSE_ERROR",
            "LEX_ERROR",
            "TYPE_NOT_STATE",
        }
    ]
    if family == "qpu" and compiled.unit is not None:
        dag = lower_source_ast(compiled.unit)
        coins = sum(1 for k in dag.summary()["kinds"] if k == "coin")
        if coins > 127 and profile and "eagle" in profile:
            print(
                f"TARGET_WARN: estimated logical coins={coins} may exceed profile {profile}",
                file=sys.stderr,
            )
            interesting.append(
                {
                    "code": "TARGET_WARN",
                    "message": f"coin-count {coins} vs profile {profile}",
                    "line": "?",
                }
            )

    if not interesting:
        print("ok — no vocabulary / collapse / parse issues")
        if family != "cpu":
            print(f"target: {family}" + (f":{profile}" if profile else ""))
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
    return 1 if hard else 0


def cmd_inspect(args: argparse.Namespace) -> int:
    compiled = _compile_args(args)
    if compiled.unit is None or any(d.get("code") in HARD_CODES for d in compiled.diagnostics):
        _print_diags(compiled.diagnostics)
        return 1
    unit = compiled.unit
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
        full = _compile_args(args)
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
            if "measure" not in source:
                last = None
                for ln in source.splitlines():
                    s = ln.strip()
                    if s.startswith("state "):
                        last = s.split("=")[0].replace("state", "").strip()
                if last:
                    source = source + f"measure {last}\n"
            result = host_run_source(
                source,
                settings={"target": "local", "seed": seed},
                stdout=sys.stdout,
            )
            if result.status != "succeeded":
                _print_diags(list(result.diagnostics))
            continue
        buf.append(line)


def cmd_dag(args: argparse.Namespace) -> int:
    compiled = _compile_args(args)
    if compiled.unit is None:
        _print_diags(compiled.diagnostics)
        return 1
    dag = lower_source_ast(compiled.unit)
    if args.dot:
        print(dag.to_dot(), end="")
    else:
        print(dag.summary())
    return 0


def cmd_emit_qasm(args: argparse.Namespace) -> int:
    compiled = _compile_args(args)
    if compiled.unit is None or any(d.get("code") in HARD_CODES for d in compiled.diagnostics):
        _print_diags(compiled.diagnostics)
        return 1
    emitted = emit_openqasm3(compiled.unit)
    for n in emitted.notes:
        print(f"// note: {n}", file=sys.stderr)
    if not emitted.ok:
        return 1
    out = emitted.qasm
    if getattr(args, "output", None):
        Path(args.output).write_text(out if out.endswith("\n") else out + "\n", encoding="utf-8")
    else:
        print(out, end="" if out.endswith("\n") else "\n")
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


def _add_target(sp: argparse.ArgumentParser) -> None:
    sp.add_argument(
        "-t",
        "--target",
        default="cpu",
        help="cpu | gpu | qpu:<profile> (ADR 0036; source stays portable)",
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qpex", description="QPex toolchain (Phase 3–4)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_src(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("file", nargs="?", help=".qpex source file")
        sp.add_argument("-e", "--eval", dest="expr", help="source string")
        sp.add_argument("--seed", type=int, default=None)

    pr = sub.add_parser("run", help="compile and execute (terminal measure)")
    add_src(pr)
    _add_target(pr)
    pr.add_argument("--emit-qasm", action="store_true", help="print OpenQASM 3 sketch")
    pr.add_argument("-o", "--output", help="write OpenQASM to file (with qpu / --emit-qasm)")
    pr.add_argument(
        "--also-run",
        action="store_true",
        help="with --target qpu, also run cpu Joint after emit",
    )
    pr.set_defaults(func=cmd_run)

    pc = sub.add_parser("check", help="lint Forbidden/Retired + Early Collapse")
    add_src(pc)
    _add_target(pc)
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

    pe = sub.add_parser("emit-qasm", help="lower to OpenQASM 3 sketch (ADR 0036)")
    add_src(pe)
    pe.add_argument("-o", "--output", help="write QASM to file")
    pe.set_defaults(func=cmd_emit_qasm)

    prepl = sub.add_parser("repl", help="interactive shell")
    prepl.add_argument("--seed", type=int, default=None)
    prepl.set_defaults(func=cmd_repl)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in {
        "run",
        "check",
        "inspect",
        "dag",
        "emit-qasm",
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
