"""Feature tests for DataFrame creation methods (DCMS)."""

from pathlib import Path

import pytest

from frame_check_core.models import FrameClass, FrameInstance

from tests.utils import assert_frame_equals, check_body_as_module

CSV_TEST_FILE = (Path(__file__).parent.parent / "data" / "csv_file.csv").as_posix()


# --- DCMS-1: Dictionary of Lists ---


@pytest.mark.support(code="#DCMS-1")
def test_dcms_1_dictionary_of_lists():
    def scenario():
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        df["a"]
        df["b"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"a", "b"}, False)
    assert_frame_equals(actual, expected)


# --- DCMS-2: List of Dictionaries ---


@pytest.mark.support(code="#DCMS-2")
def test_dcms_2_list_of_dictionaries():
    def scenario():
        import pandas as pd

        df = pd.DataFrame([{"a": 1, "b": 3}, {"a": 2, "b": 4}])
        df["a"]
        df["b"]

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"a", "b"}, False)
    assert_frame_equals(actual, expected)


# --- DCMS-6: From CSV ---


def test_dcms_6_read_csv():
    def scenario():
        import pandas as pd

        df = pd.read_csv(CSV_TEST_FILE)  # noqa: F841

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {}, True)
    assert_frame_equals(actual, expected)


@pytest.mark.support(code="#DCMS-6")
def test_dcms_6_read_csv_usecols():
    def scenario():
        import pandas as pd

        df = pd.read_csv(CSV_TEST_FILE, usecols=["a", "b", "c"])  # noqa: F841

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"a", "b", "c"}, False)
    assert_frame_equals(actual, expected)


@pytest.mark.support(code="#DCMS-6-1")
@pytest.mark.xfail(
    reason="Variable-resolved usecols is not implemented in frame_check_core",
    strict=True,
)
def test_dcms_6_1_read_csv_usecols_indirect():
    """pd.read_csv with usecols from variable"""

    def scenario():
        import pandas as pd

        cols = ["a", "b", "c"]
        df = pd.read_csv(CSV_TEST_FILE, usecols=cols)  # noqa: F841

    res = check_body_as_module(scenario)
    assert len(res.diagnostics) == 0
    actual = res.frame_definitions.get("df")
    expected = FrameInstance(FrameClass.pd_DataFrame, {"a", "b", "c"}, False)
    assert_frame_equals(actual, expected)
