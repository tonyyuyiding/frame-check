from collections import deque
from pathlib import Path

import pytest

from frame_check_core import check


@pytest.mark.benchmark
def test_long_benchmark():
    benchmark_file = Path(__file__).parent / "long_pandas.py"
    gen = check(benchmark_file)
    deque(gen, maxlen=0)  # Exhaust the generator to run the benchmark
