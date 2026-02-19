from __future__ import annotations

import argparse
from dataclasses import dataclass

from pathlib import Path
from typing import Optional

VALID_TYPES = {"afp"}
OUTPUT_FORMATS = {"json"}

def parse_args(argv: Optional[list[str]]) -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description=f"File parsing tool ({", ".join(VALID_TYPES)})."
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Full path to the file to analyze",
    )
    parser.add_argument(
        "-t", "--type",
        required=True,
        choices=sorted(VALID_TYPES),
        help=f"File mime type ({", ".join(VALID_TYPES)}). "
    )
    parser.add_argument(
        "-c", "--config",
        required=False,
        help="Path to a JSON configuration file",
    )
    parser.add_argument(
        "-o", "--output-format",
        default="json",
        choices=sorted(OUTPUT_FORMATS),
        help="Output format (json by default)"
    )
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    path = Path(args.file)

    if not path.exists():
        raise ValueError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"The specified path is not a file: {path}")

    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            raise ValueError(f"Configuration file not found: {config_path}")
        if not config_path.is_file():
            raise ValueError(f"The configuration path is not a file: {config_path}")

@dataclass(frozen=True)
class CliInput:
    path: str
    filetype: Optional[str]
    config_path: Optional[str] = None
    output_format: str = "json"

    def __str__(self) -> str:
        config_str = f", Config : {self.config_path}" if self.config_path else ""
        return f"Path : {self.path}, Type : {self.filetype}, Output : {self.output_format}{config_str}"

def build_cli_input(args: argparse.Namespace) -> CliInput:
    validate_args(args)
    return CliInput(
        path=args.file,
        filetype=args.type.lower(),
        config_path=args.config if hasattr(args, 'config') else None,
        output_format=args.output_format if hasattr(args, 'output_format') else "json",
    )

def run(argv: Optional[list[str]] = None):
    """Main entry point for the CLI"""

    args = parse_args(argv)

    # A dataclass is created from the parsed arguments after validation
    cli_input = build_cli_input(args)

    return cli_input
