import ast

import libcst as cst

from ..ir import raw
from ..ir.common import BinOperator
from .common import CodeRanges


def lower_module(module: cst.Module, code_ranges: CodeRanges) -> raw.Module:
    stmts: tuple[raw.stmt, ...] = ()
    for node in module.body:
        stmts += _lower_statements(node, code_ranges)
    return raw.Module(body=tuple(stmts), code_range=code_ranges.get(module, None))


# ---------------------------------------------------------------------------
# Statement lowering
# ---------------------------------------------------------------------------


def _lower_statements(node: cst.BaseStatement, cr: CodeRanges) -> tuple[raw.stmt, ...]:
    match node:
        case cst.SimpleStatementLine():
            return _lower_simple_statement_line(node, cr)
        case _:
            return ()


def _lower_simple_statement_line(
    node: cst.SimpleStatementLine, cr: CodeRanges
) -> tuple[raw.stmt]:
    return tuple(
        stmt
        for small_stmt in node.body
        if (stmt := _lower_small_statement(small_stmt, cr)) is not None
    )


def _lower_small_statement(
    node: cst.BaseSmallStatement, cr: CodeRanges
) -> raw.stmt | None:
    match node:
        case cst.Assign():
            return _lower_assign(node, cr)
        case cst.Expr():
            return raw.Expr(
                value=_lower_expression(node.value, cr), code_range=cr.get(node, None)
            )
        case cst.Import():
            return _lower_import(node, cr)
        case cst.ImportFrom():
            return _lower_import_from(node, cr)
        case _:
            return None


def _lower_assign(node: cst.Assign, cr: CodeRanges) -> raw.Assign:
    return raw.Assign(
        targets=tuple(_lower_expression(t.target, cr) for t in node.targets),
        value=_lower_expression(node.value, cr),
        type_comment=None,
        code_range=cr.get(node, None),
    )


def _lower_import(node: cst.Import, cr: CodeRanges) -> raw.Import:
    return raw.Import(
        names=tuple(_lower_import_alias(n, cr) for n in node.names),
        code_range=cr.get(node, None),
    )


def _lower_import_from(node: cst.ImportFrom, cr: CodeRanges) -> raw.ImportFrom:
    match node.names:
        case cst.ImportStar():
            names = (
                raw.ImportAlias(name="*", asname=None, code_range=cr.get(node, None)),
            )
        case _:
            names = tuple(_lower_import_alias(n, cr) for n in node.names)
    return raw.ImportFrom(
        module=_parse_module_name(node.module) if node.module is not None else None,
        names=names,
        level=len(node.relative) if node.relative else 0,
        code_range=cr.get(node, None),
    )


def _lower_import_alias(node: cst.ImportAlias, cr: CodeRanges) -> raw.ImportAlias:
    asname = _lower_asname(node.asname) if node.asname is not None else None
    return raw.ImportAlias(
        name=_parse_module_name(node.name), asname=asname, code_range=cr.get(node, None)
    )


def _parse_module_name(node: cst.Attribute | cst.Name) -> str:
    match node:
        case cst.Name():
            return node.value
        case cst.Attribute():
            if not isinstance(node.value, (cst.Name, cst.Attribute)):
                raise TypeError(f"Unexpected module reference node: {type(node.value)}")
            return f"{_parse_module_name(node.value)}.{node.attr.value}"


def _lower_asname(node: cst.AsName) -> str:
    match node.name:
        case cst.Name() as n:
            return n.value
        case _:
            raise ValueError(f"Unexpected asname target: {type(node.name)}")


# ---------------------------------------------------------------------------
# Expression lowering
# ---------------------------------------------------------------------------


def _lower_expression(node: cst.BaseExpression, cr: CodeRanges) -> raw.expr:
    match node:
        case cst.Name():
            return _lower_name(node, cr)
        case cst.Attribute():
            return _lower_attribute(node, cr)
        case cst.Call():
            return _lower_call(node, cr)
        case cst.BinaryOperation():
            return _lower_binary_op(node, cr)
        case cst.Integer() | cst.Float() | cst.Imaginary():
            return _lower_number(node, cr)
        case cst.SimpleString():
            return _lower_string(node, cr)
        case cst.Dict():
            return _lower_dict(node, cr)
        case cst.List():
            return _lower_list(node, cr)
        case _:
            return raw.Unknown(code_range=cr.get(node, None))


def _lower_name(node: cst.Name, cr: CodeRanges) -> raw.Name:
    return raw.Name(id=node.value, code_range=cr.get(node, None))


def _lower_number(
    node: cst.Integer | cst.Float | cst.Imaginary, cr: CodeRanges
) -> raw.Constant | raw.Unknown:
    match node:
        case cst.Integer():
            return raw.Constant(value=int(node.value, 0), code_range=cr.get(node, None))
        case _:
            return raw.Unknown(code_range=cr.get(node, None))


def _lower_string(node: cst.SimpleString, cr: CodeRanges) -> raw.Constant | raw.Unknown:
    try:
        value = ast.literal_eval(node.value)
    except (ValueError, SyntaxError):
        return raw.Unknown(code_range=cr.get(node, None))
    if isinstance(value, str):
        return raw.Constant(value=value, code_range=cr.get(node, None))
    return raw.Unknown(code_range=cr.get(node, None))


def _lower_attribute(node: cst.Attribute, cr: CodeRanges) -> raw.Attribute:
    return raw.Attribute(
        value=_lower_expression(node.value, cr),
        attr=node.attr.value,
        code_range=cr.get(node, None),
    )


def _lower_call(node: cst.Call, cr: CodeRanges) -> raw.Call:
    func = _lower_expression(node.func, cr)
    args: tuple[raw.expr, ...] = tuple(
        _lower_expression(arg.value, cr) for arg in node.args if arg.keyword is None
    )
    keywords: tuple[raw.CallKeyword, ...] = tuple(
        _lower_call_keyword(arg, cr) for arg in node.args if arg.keyword is not None
    )
    return raw.Call(
        func=func,
        args=tuple(args),
        keywords=tuple(keywords),
        code_range=cr.get(node, None),
    )


def _lower_call_keyword(node: cst.Arg, cr: CodeRanges) -> raw.CallKeyword:
    kw = node.keyword
    return raw.CallKeyword(
        arg=kw.value if kw is not None else None,
        value=_lower_expression(node.value, cr),
        code_range=cr.get(node, None),
    )


def _lower_binary_op(node: cst.BinaryOperation, cr: CodeRanges) -> raw.BinOp:
    return raw.BinOp(
        left=_lower_expression(node.left, cr),
        op=_lower_binary_operator(node.operator),
        right=_lower_expression(node.right, cr),
        code_range=cr.get(node, None),
    )


def _lower_binary_operator(op: cst.BaseBinaryOp) -> BinOperator:
    match op:
        case cst.Add():
            return BinOperator.ADD
        case cst.Subtract():
            return BinOperator.SUBTRACT
        case cst.Multiply():
            return BinOperator.MULTIPLY
        case cst.Divide():
            return BinOperator.DIVIDE
        case cst.FloorDivide():
            return BinOperator.FLOOR_DIVIDE
        case cst.Modulo():
            return BinOperator.MODULO
        case cst.Power():
            return BinOperator.POWER
        case cst.LeftShift():
            return BinOperator.LEFT_SHIFT
        case cst.RightShift():
            return BinOperator.RIGHT_SHIFT
        case cst.BitOr():
            return BinOperator.BIT_OR
        case cst.BitAnd():
            return BinOperator.BIT_AND
        case cst.BitXor():
            return BinOperator.BIT_XOR
        case cst.MatrixMultiply():
            return BinOperator.MATRIX_MULTIPLY
        case _:
            raise ValueError(f"Unknown binary operator: {type(op).__name__}")


def _lower_dict(node: cst.Dict, cr: CodeRanges) -> raw.Dict:
    keys: list[raw.expr | None] = []
    values: list[raw.expr] = []
    for element in node.elements:
        match element:
            case cst.DictElement():
                keys.append(_lower_expression(element.key, cr))
                values.append(_lower_expression(element.value, cr))
            case _:
                pass
    return raw.Dict(
        keys=tuple(keys), values=tuple(values), code_range=cr.get(node, None)
    )


def _lower_list(node: cst.List, cr: CodeRanges) -> raw.List:
    elts: list[raw.expr] = []
    for elem in node.elements:
        match elem:
            case cst.Element():
                elts.append(_lower_expression(elem.value, cr))
            case _:
                pass
    return raw.List(elts=tuple(elts), code_range=cr.get(node, None))
