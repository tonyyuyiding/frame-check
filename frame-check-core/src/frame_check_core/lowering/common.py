from collections.abc import Mapping

import libcst as cst
from libcst.metadata import CodeRange

type CodeRanges = Mapping[cst.CSTNode, CodeRange]
