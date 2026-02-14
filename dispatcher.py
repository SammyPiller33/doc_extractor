
from typing import Dict, Callable

from parser.afp import SfStreamer
from processor.afp_stream_processor import AFPStreamProcessor
from processor.file_processor import Processor

class ParserDispatcher:
    """Routes processing to the appropriate parser based on logical file type."""

    def __init__(self, registry: Dict[str, Callable[[], Processor]]) -> None:
        # Registry maps file types to processor factories
        self._registry = dict(registry)

    def dispatch(self, filetype: str) -> Processor:
        """Returns the appropriate processor for the given file type."""
        factory = self._registry.get(filetype)

        if factory is None:
            raise ValueError(f"No parser registered for type '{filetype}'")

        return factory()

def init_dispatcher(path: str, config: str) -> ParserDispatcher:
    """Initializes the dispatcher with available parsers."""
    return ParserDispatcher(
        registry={
            "afp": lambda: AFPStreamProcessor(SfStreamer(path), config),
        }
    )