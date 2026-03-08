from collections.abc import Hashable
from enum import StrEnum

ColumnName = Hashable


class Lib(StrEnum):
    pandas = "pandas"


class FrameClass(StrEnum):
    pandas_DataFrame = f"{Lib.pandas}.DataFrame"
