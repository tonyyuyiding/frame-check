import ast
from collections.abc import Generator
from pathlib import Path

from frame_check_core.models import Diagnostic, VisitorContext

from .visit import visit


def _check(node: ast.AST, ctx: VisitorContext) -> Generator[Diagnostic, None, None]:
    yield from visit(node, ctx)
    for child in ast.iter_child_nodes(node):
        yield from _check(child, ctx)


def check(_target: ast.AST | Path, /) -> Generator[Diagnostic, None, None]:
    if isinstance(_target, ast.AST):
        target = _target
    elif isinstance(_target, Path):
        source = _target.read_text()
        target = ast.parse(source)
    else:
        raise TypeError(f"Unsupported target type: {type(_target)}")
    ctx = VisitorContext()
    yield from _check(target, ctx)
