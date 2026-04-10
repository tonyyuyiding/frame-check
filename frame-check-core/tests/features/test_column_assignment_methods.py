"""Feature tests for column assignment methods (CAM)."""

import pytest

from frame_check_core.models import FrameClass, FrameInstance

from tests.utils import assert_frame_equals, check_body_as_module


# --- CAM-1: Direct assignment ---


@pytest.mark.support(code="#CAM-1")
def test_cam_1_direct_assignment():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        df["c"] = [7, 8, 9]
        df["c"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0, f"Unexpected diagnostics: {res.diagnostics}"
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"a", "b", "c"}, False)
    assert_frame_equals(actual, expected)


# --- CAM-7: assign method ---


@pytest.mark.support(code="#CAM-7")
def test_cam_7_assign_method():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({})
        df = df.assign(A=[1, 2, 3])
        df["A"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"A"}, False)
    assert_frame_equals(actual, expected)


@pytest.mark.support(code="#CAM-7-1")
def test_cam_7_1_assign_subscript():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({})
        df = df.assign(A=[1, 2, 3])
        df["A"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"A"}, False)
    assert_frame_equals(actual, expected)


@pytest.mark.support(code="#CAM-7-2")
def test_cam_7_2_assign_chain():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({})
        df = df.assign(A=[1, 2, 3]).assign(B=[4, 5, 6])
        df["A"]
        df["B"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"A", "B"}, False)
    assert_frame_equals(actual, expected)


# --- CAM-9: insert method ---


@pytest.mark.support(code="#CAM-9")
def test_cam_9_insert_method():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({})
        df.insert(0, "A", [1, 2, 3])
        df["A"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"A"}, False)
    assert_frame_equals(actual, expected)


# --- CAM-10: setitem with list ---


@pytest.mark.support(code="#CAM-10")
def test_cam_10_setitem_with_list():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        df[["c", "d"]] = [[7, 8, 9], [10, 11, 12]]
        df["c"]
        df["d"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"a", "b", "c", "d"}, False)
    assert_frame_equals(actual, expected)
