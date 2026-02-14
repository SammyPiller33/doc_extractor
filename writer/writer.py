from abc import ABC, abstractmethod

class Writer(ABC):
    """Abstract base class for all output writers."""

    def __init__(self, output_path: str, **options):
        """
        Initialize writer with output path and options.

        Args:
            output_path: Path where output will be written
            **options: Format-specific options
        """
        self.output_path = output_path
        self.options = options

    @abstractmethod
    def __enter__(self) -> 'Writer':
        """
        Setup resources (open files, etc.)

        Returns:
            Self for context manager usage
        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleanup resources"""
        pass

    @abstractmethod
    def write(self, data: dict) -> None:
        """
        Write a single data item.

        Args:
            data: Dictionary containing data to write
        """
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush buffered data to output."""
        pass


