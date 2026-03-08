import ast

from ..models import VisitorContext, FCGenerator


def visit_Call(ctx: VisitorContext, node: ast.Call) -> FCGenerator: ...
