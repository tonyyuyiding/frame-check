import ast
from collections.abc import Generator
from pathlib import Path

from frame_check_core.models import Diagnostic, VisitorContext

from .visit import visit

type CheckResult = Generator[Diagnostic, None, None]


def _check(node: ast.AST, ctx: VisitorContext) -> CheckResult:
    # TODO: These node types are not supported yet, and we early return to avoid errors.
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Lambda)):
        return

    yield from visit(node, ctx)
    for child in ast.iter_child_nodes(node):
        yield from _check(child, ctx)


def check(_target: ast.AST | Path, /, ctx: VisitorContext | None = None) -> CheckResult:
    if isinstance(_target, ast.AST):
        target = _target
    elif isinstance(_target, Path):
        source = _target.read_text()
        target = ast.parse(source)
    else:
        raise TypeError(f"Unsupported target type: {type(_target)}")
    if ctx is None:
        ctx = VisitorContext()
    yield from _check(target, ctx)
