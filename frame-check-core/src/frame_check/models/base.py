from enum import StrEnum
from typing import TypeGuard

# Not using Hashable directly because `Unknown` is also hashable.
ColumnName = str | int | bool


def is_column_name(value) -> TypeGuard[ColumnName]:
    return isinstance(value, ColumnName)


class Lib(StrEnum):
    pd = "pandas"


class FrameClass(StrEnum):
    pd_DataFrame = f"{Lib.pd}.DataFrame"
