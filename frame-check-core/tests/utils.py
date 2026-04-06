import ast
import inspect
import textwrap
from dataclasses import dataclass
from typing import Callable

from frame_check_core.checker import _check
from frame_check_core.models import Diagnostic, FrameInstance, VisitorContext


@dataclass(frozen=True, slots=True)
class CheckRunResult:
    diagnostics: tuple[Diagnostic, ...]
    frame_definitions: dict[str, FrameInstance]


def check_body_as_module(func: Callable[[], None]) -> CheckRunResult:
    source = textwrap.dedent(inspect.getsource(func))
    func_def = ast.parse(source).body[0]
    assert isinstance(func_def, ast.FunctionDef)
    module = ast.Module(body=func_def.body, type_ignores=[])
    ctx = VisitorContext()
    diagnostics = tuple(_check(module, ctx))
    frame_definitions = {
        name: instance
        for name, instance in ctx.definitions.items()
        if isinstance(instance, FrameInstance)
    }
    return CheckRunResult(diagnostics, frame_definitions)


def assert_frame_equals(actual, expected: FrameInstance) -> None:
    assert isinstance(actual, FrameInstance), (
        f"Expected a FrameInstance, got {type(actual)}"
    )
    assert actual.class_ == expected.class_
    assert actual.columns == expected.columns
    assert actual.maybe_more == expected.maybe_more
