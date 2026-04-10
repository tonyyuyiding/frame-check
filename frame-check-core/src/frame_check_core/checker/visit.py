import ast

from frame_check_core.models import Unknown, VisitorContext, FCGenerator

from ._assign import visit_Assign
from ._call import visit_Call
from ._import import visit_Import
from ._name import visit_Name
from ._subscript import visit_Subscript
from .marks import VALUE_ATTR


def visit(node: ast.AST, ctx: VisitorContext) -> FCGenerator:
    if hasattr(node, VALUE_ATTR):
        return getattr(node, VALUE_ATTR)
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
    setattr(node, VALUE_ATTR, res)
    return res
