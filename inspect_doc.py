#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dispatcher import create_dispatcher

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
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    path = Path(args.file)

    if not path.exists():
        raise ValueError(f"Fichier introuvable : {path}")
    if not path.is_file():
        raise ValueError(f"Le chemin correspondant n'est pas un fichier : {path}")

@dataclass(frozen=True)
class CliInput:
    path: Path
    filetype: Optional[str]


def build_cli_input(args: argparse.Namespace) -> CliInput:
    validate_args(args)
    return CliInput(
        path=Path(args.file),
        filetype=args.type.lower(),
    )


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    try:
        cli_input = build_cli_input(args)
        print(f"Analyse du fichier '{cli_input.path}' en cours...")
        print(f"{cli_input}")
    except ValueError as e:
        print(f"Erreur de paramètre : {e}")
        return 2

    dispatcher = create_dispatcher(cli_input.path).dispatch(cli_input.filetype)
    dispatcher.parse()


    return 0


if __name__ == "__main__":
    raise SystemExit(main())
