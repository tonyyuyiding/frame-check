import ast
from collections.abc import Generator

from frame_check_core.models import Diagnostic, Unknown, VisitorContext, FCGenerator

from ._assign import visit_Assign
from ._call import visit_Call
from ._import import visit_Import
from ._name import visit_Name
from ._subscript import visit_Subscript

_VALUE_ATTR = "__frame_check_value__"


def visit(node: ast.AST, ctx: VisitorContext) -> FCGenerator:
    if hasattr(node, _VALUE_ATTR):
        return getattr(node, _VALUE_ATTR)
    if isinstance(node, ast.Assign):
        res = yield from visit_Assign(node, ctx)
    elif isinstance(node, ast.Call):
        res = yield from visit_Call(node, ctx)
    elif isinstance(node, ast.Import):
        res = visit_Import(node, ctx)
    elif isinstance(node, ast.Name):
        res = visit_Name(node, ctx)
    elif isinstance(node, ast.Subscript):
        res = yield from visit_Subscript(node, ctx)
    else:
        res = Unknown
    setattr(node, _VALUE_ATTR, res)
    return res


def check(
    node: ast.AST, ctx: VisitorContext | None = None
) -> Generator[Diagnostic, None, None]:
    if ctx is None:
        ctx = VisitorContext()
    yield from visit(node, ctx)
    for child in ast.iter_child_nodes(node):
        yield from check(child, ctx)
