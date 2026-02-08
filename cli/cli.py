from __future__ import annotations

import argparse
from dataclasses import dataclass

from pathlib import Path
from typing import Optional

VALID_TYPES = {"afp"}

def parse_args(argv: Optional[list[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Outil de parsing de fichiers ({", ".join(VALID_TYPES)})."
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Chemin complet du fichier à analyser",
    )
    parser.add_argument(
        "-t", "--type",
        required=True,
        choices=sorted(VALID_TYPES),
        help=f"Type mime du fichier ({", ".join(VALID_TYPES)}). "
    )
    parser.add_argument(
        "-c", "--config",
        required=False,
        help="Chemin vers un fichier JSON de configuration",
    )
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    path = Path(args.file)

    if not path.exists():
        raise ValueError(f"Fichier introuvable : {path}")
    if not path.is_file():
        raise ValueError(f"Le chemin correspondant n'est pas un fichier : {path}")

    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            raise ValueError(f"Fichier de configuration introuvable : {config_path}")
        if not config_path.is_file():
            raise ValueError(f"Le chemin de configuration n'est pas un fichier : {config_path}")

@dataclass(frozen=True)
class CliInput:
    path: str
    filetype: Optional[str]
    config_path: Optional[str] = None

    def __str__(self) -> str:
        config_str = f", Config : {self.config_path}" if self.config_path else ""
        return f"Path : {self.path}, Type : {self.filetype}{config_str}"

def build_cli_input(args: argparse.Namespace) -> CliInput:
    validate_args(args)
    return CliInput(
        path=args.file,
        filetype=args.type.lower(),
        config_path=args.config if hasattr(args, 'config') else None,
    )

def run(argv: Optional[list[str]] = None):
    """Main entry point for the CLI"""

    args = parse_args(argv)

    cli_input = build_cli_input(args)

    return cli_input
