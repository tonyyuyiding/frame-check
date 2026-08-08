import argparse
import sys
from pathlib import Path

import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider

from ..lowering.cst2raw import lower_module as cst2raw_lower_module

IRS = ("cst", "raw")


def compile_file(input_file: Path, output_format: str) -> str:
    if not input_file.exists():
        print(f"Error: {input_file} does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as f:
        source_code = f.read()

    if output_format not in IRS:
        print(f"Error: Invalid output format '{output_format}'.", file=sys.stderr)
        sys.exit(1)

    ir_cst = cst.parse_module(source_code)
    if output_format == "cst":
        return str(ir_cst)
    wrapper = MetadataWrapper(ir_cst)
    code_ranges = wrapper.resolve(PositionProvider)
    ir_raw = cst2raw_lower_module(ir_cst, code_ranges)
    if output_format == "raw":
        return str(ir_raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a Python file to a frame-check IR"
    )
    parser.add_argument("input_file", type=Path, help="The input Python file")
    parser.add_argument("-o", "--output", type=str, choices=IRS, help="The output IR")
    args = parser.parse_args()

    result = compile_file(args.input_file, args.output)
    print(result)
