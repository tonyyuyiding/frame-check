import ast

_SETITEM_ATTR = "__frame_check_is_setitem__"
VALUE_ATTR = "__frame_check_value__"


def mark_setitem(node: ast.Subscript) -> None:
    setattr(node, _SETITEM_ATTR, True)


def is_setitem(node: ast.Subscript) -> bool:
    return getattr(node, _SETITEM_ATTR, False)
