from typing import Dict, Callable

from parser.afp import SfStreamer
from processor.afp.afp_stream_processor import AFPStreamProcessor
from processor.file_processor import Processor

class ParserDispatcher:
    """Route le traitement vers le bon parser en fonction du type logique."""

    def __init__(self, registry: Dict[str, Callable[[], Processor]]) -> None:
        # valeur = factory (callable qui retourne un Processor)
        self._registry = dict(registry)

    def dispatch(self, filetype: str) -> Processor:
        factory = self._registry.get(filetype)

        if factory is None:
            raise ValueError(f"Aucun parser enregistré pour le type '{filetype}'")

        return factory()

def init_dispatcher(path: str, config: str) -> ParserDispatcher:
    return ParserDispatcher(
        registry={
            "afp": lambda: AFPStreamProcessor(SfStreamer(path), config),
        }
    )
