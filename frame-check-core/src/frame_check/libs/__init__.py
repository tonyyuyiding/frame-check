from ..models import FCCallable, Lib, FrameInstance


def get_callable(_obj: FrameInstance | Lib, /, attr_name: str) -> FCCallable: ...
