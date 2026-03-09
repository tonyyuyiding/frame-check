import ast
from collections.abc import Callable

from ..models import (
    FCValue,
    FCCallableInit,
    FCGenerator,
    FrameClass,
    FrameInstance,
    Lib,
    VisitorContext,
)

_FCMethodInit = Callable[
    [FrameInstance, VisitorContext, list[ast.expr], list[ast.keyword]],
    FCGenerator | FCValue,
]

_method_registry: dict[FrameClass, dict[str, _FCMethodInit]] = {}
_func_registry: dict[Lib, dict[str, FCCallableInit]] = {}


def method(fc: FrameClass, name: str) -> Callable[[_FCMethodInit], _FCMethodInit]:
    def decorator(func: _FCMethodInit) -> _FCMethodInit:
        if fc not in _method_registry:
            _method_registry[fc] = {}
        _method_registry[fc][name] = func
        return func

    return decorator


def func(lib: Lib, name: str) -> Callable[[FCCallableInit], FCCallableInit]:
    def decorator(func: FCCallableInit) -> FCCallableInit:
        if lib not in _func_registry:
            _func_registry[lib] = {}
        _func_registry[lib][name] = func
        return func

    return decorator
