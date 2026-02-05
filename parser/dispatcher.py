from pathlib import Path
from typing import Dict

from parser.common.file_parser import FileParser
from afp_parser import AfpParser

class ParserDispatcher:
    """Route le traitement vers le bon parser en fonction du type logique."""

    def __init__(self, registry: Dict[str, FileParser]) -> None:
        # clé = type logique ("afp", "pdf", ...)
        self._registry = dict(registry)

    def dispatch(self, filetype: str) -> FileParser:
        parser = self._registry.get(filetype)

        if parser is None:
            raise ValueError(f"Aucun parser enregistré pour le type '{filetype}'")

        return parser

def create_dispatcher(path: Path) -> ParserDispatcher:
    return ParserDispatcher(
        registry={
            "afp": AfpParser(path)
        }
    )
