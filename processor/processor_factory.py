from abc import ABC, abstractmethod

from processor.file_processor import Processor

class ProcessorFactory(ABC):
    """Abstract factory for creating processor instances."""

    @abstractmethod
    def create(self) -> Processor:
        """Create and return a processor instance."""
        pass

