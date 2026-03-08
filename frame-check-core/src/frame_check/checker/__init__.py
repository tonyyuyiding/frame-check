import ast

from ..models import Unknown, VisitorContext, FCGenerator

from ._assign import visit_Assign
from ._call import visit_Call
from ._import import visit_Import
from ._name import visit_Name
from ._subscript import visit_Subscript

_VALUE_ATTR = "__frame_check_value__"


def visit(ctx: VisitorContext, node: ast.AST) -> FCGenerator:
    if hasattr(node, _VALUE_ATTR):
        return getattr(node, _VALUE_ATTR)
    if isinstance(node, ast.Assign):
        res = yield from visit_Assign(ctx, node)
    elif isinstance(node, ast.Call):
        res = yield from visit_Call(ctx, node)
    elif isinstance(node, ast.Import):
        res = visit_Import(ctx, node)
    elif isinstance(node, ast.Name):
        res = visit_Name(ctx, node)
    elif isinstance(node, ast.Subscript):
        res = yield from visit_Subscript(ctx, node)
    else:
        res = Unknown
    setattr(node, _VALUE_ATTR, res)
    return res
