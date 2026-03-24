from functools import partial

from ._registry import _method_registry, _func_registry
from ..models import Lib, FrameInstance, FCCallable

from . import _pandas as _pandas


def get_callable(obj: FrameInstance | Lib, attr: str) -> FCCallable:
    if isinstance(obj, FrameInstance):
        fc = obj.class_
        if fc in _method_registry and attr in _method_registry[fc]:
            method = _method_registry[fc][attr]
            return FCCallable(partial(method, obj))
    elif isinstance(obj, Lib):
        if obj in _func_registry and attr in _func_registry[obj]:
            func = _func_registry[obj][attr]
            return FCCallable(func)
    return FCCallable.empty()
