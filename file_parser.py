from pathlib import Path


class FileParser:
    """Interface simple pour les parsers de fichiers."""
    def __init__(self, path: Path) -> None:
        self._path = path

    def parse(self) -> dict:
        raise NotImplementedError
