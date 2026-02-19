from pathlib import Path


class FileParser:
    """Simple interface for file parsers."""
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def set_config(self, config) -> None:
        raise NotImplementedError

    def parse(self) -> dict:
        raise NotImplementedError

    def stream(self):
        raise NotImplementedError
