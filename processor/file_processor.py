from logger import get_logger
from parser.file_parser import FileParser
from typing import Optional

# Import the Writer type
from writer.writer import Writer


class Processor:
    """
    Base processor class that delegates parsing to an injected FileParser strategy.

    Subclasses must implement the run() method with format-specific processing logic.
    """

    def __init__(self, file_parser: FileParser, writer: Optional[Writer] = None):
        """
        Initialize processor with a specific parser implementation.

        Args:
            file_parser: Parser instance for the target file format
            writer: Optional writer instance for output (can be set later)
        """
        self.parser: FileParser = file_parser
        self.writer: Optional[Writer] = writer
        self.logger = get_logger(__name__)
        self.logger.info(f"Name of the parser processor: {self.__class__.__name__}")

        if writer:
            self.logger.info(f"Writer injected: {writer.__class__.__name__}")

    def set_writer(self, writer: Writer) -> None:
        """
        Inject the writer to be used for output.

        Args:
            writer: Writer instance for the desired output format
        """
        self.writer = writer
        self.logger.info(f"Writer set: {writer.__class__.__name__}")

    def run(self, output_path: str) -> None:
        """
        Execute the processing logic. Must be implemented by subclasses.

        Args:
            output_path: Path where processing results should be written

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError