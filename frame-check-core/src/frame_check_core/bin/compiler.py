import argparse
import sys
from pathlib import Path

import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider

from ..lowering.cst2raw import lower_module as cst2raw_lower_module

IRS = ("cst", "raw")
FORMATS = ("str", "repr")


def compile_file(input_file: Path, output_ir: str, output_format: str) -> str:
    if not input_file.exists():
        print(f"Error: {input_file} does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as f:
        source_code = f.read()

    if output_ir not in IRS:
        print(f"Error: Invalid output format '{output_ir}'.", file=sys.stderr)
        sys.exit(1)

    match output_format:
        case "str":
            format_func = str
        case "repr":
            format_func = repr

    ir_cst = cst.parse_module(source_code)
    if output_ir == "cst":
        return format_func(ir_cst)
    wrapper = MetadataWrapper(ir_cst)
    code_ranges = wrapper.resolve(PositionProvider)
    ir_raw = cst2raw_lower_module(ir_cst, code_ranges)
    if output_ir == "raw":
        return format_func(ir_raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a Python file to a frame-check IR"
    )
    parser.add_argument("input_file", type=Path, help="The input Python file")
    parser.add_argument(
        "-o", "--output-ir", type=str, choices=IRS, help="The output IR"
    )
    parser.add_argument(
        "-f",
        "--output-format",
        type=str,
        choices=FORMATS,
        default="str",
        help="The output format",
    )
    args = parser.parse_args()

    result = compile_file(args.input_file, args.output_ir, args.output_format)
    print(result)
