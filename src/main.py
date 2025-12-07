import argparse
from pathlib import Path
import re
from typing import Literal


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a sequence number to a file")

    parser.add_argument(
        "--start", type=int, default=1, help="The start number of the sequence"
    )
    parser.add_argument(
        "--end", type=int, default=1000, help="The end number of the sequence"
    )
    parser.add_argument("--step", type=int, default=1, help="The step of the sequence")
    parser.add_argument(
        "--padding",
        choices=["0", " "],
        default="0",
        help="The padding of the sequence number",
    )

    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        default="sequence.txt",
        help="The filename to generate the sequence number to",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        choices=[".", "~", "exec_file"],
        required=True,
        help="The directory to output the sequence number to",
    )
    parser.add_argument(
        "-p",
        "--parent_dir_flug",
        type=bool,
        default=True,
        help="If True, sequence/ will be created in the output directory if it does not exist",
    )

    return parser.parse_args()


def validate_range_arguments(start: int, end: int, step: int):
    if start < 0:
        raise ValueError("start must be greater than 0")

    if end <= 0:
        raise ValueError("end must be greater than 0")

    if step <= 0:
        raise ValueError("step must be greater than 0")

    if start > end:
        raise ValueError("start must be less than end")

    return start, end, step


def sanitize_filename(
    filename: str, replacement: Literal["_", "-"] = "_", max_length: int = 50
) -> str:
    invalid_chars = r"[^A-Za-z0-9_\-]"

    filename = re.sub(invalid_chars, replacement, filename)
    filename = filename.lower()
    filename = re.sub(f"{replacement}+", replacement, filename)

    if max_length <= 0:
        raise ValueError("max_length must be greater than 0")

    if max_length > 255:
        raise ValueError("max_length must be less than 255")

    if len(filename) > max_length:
        filename = filename[:max_length]

    return filename[:max_length]


def generate_output_filepath(
    output_dir: str, filename: str, parent_dir_flug: bool
) -> Path:
    if output_dir == ".":
        dir_path = Path().cwd()
    if output_dir == "~":
        dir_path = Path().home()
    if output_dir == "exec_file":
        dir_path = Path(__file__).resolve().parent

    if parent_dir_flug:
        dir_path = dir_path / "sequence"

    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)

    return dir_path / filename


def write_sequence_to_file(
    start: int, end: int, step: int, padding: Literal["0", " "], output_filepath: Path
):
    digit = len(str(end))

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            for i in range(start, end + 1, step):
                f.write(f"{i:{padding}{digit}}. \n")
    except IOError as e:
        raise IOError(f"Failed to write sequence to file: {e}")


def main():
    args = parse_args()
    start, end, step = validate_range_arguments(args.start, args.end, args.step)
    padding = args.padding
    filename = sanitize_filename(args.filename)
    output_filepath = generate_output_filepath(
        args.output_dir, filename, args.parent_dir_flug
    )
    write_sequence_to_file(start, end, step, padding, output_filepath)


if __name__ == "__main__":
    main()
