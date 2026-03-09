from collections.abc import Hashable
from enum import StrEnum

ColumnName = Hashable


class Lib(StrEnum):
    pd = "pandas"


class FrameClass(StrEnum):
    pd_DataFrame = f"{Lib.pd}.DataFrame"
