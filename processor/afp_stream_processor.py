import time

from parser.afp import SfStreamer
from parser.afp.sf_filter import SfFilter
from processor.file_processor import Processor

class AFPStreamProcessor(Processor):

    def __init__(self, sf_streamer: SfStreamer, config_path: str = None) -> None:
        super().__init__(sf_streamer)

        if config_path:
            try:
                sf_filter = SfFilter(config_path)
                self.parser.set_config(sf_filter)
                self.logger.info(f"SF filter loaded : {sf_filter.get_filter_info()}")
            except (ValueError, FileNotFoundError) as e:
                self.logger.error(f"Error in charging the filter : {e}")

    def run(self, cli_output_path):
        """Process the AFP stream and build the document structure."""

        if self.writer is None:
            raise ValueError("Writer not set. Call set_writer() before run().")

        start_time = time.perf_counter()
        sf_count = 0
        error_count = 0

        self.logger.info(f"Processing AFP stream : {cli_output_path}")

        try:
            with self.writer as writer:
                for sf in self.parser.stream():
                    try:
                        sf_count += 1
                        writer.write(sf)
                    except Exception as e:
                        error_count += 1
                        self.logger.warning(f"Error processing SF #{sf_count}: {e}")
                        # Continue processing or raise based on config

        except Exception as e:
            self.logger.error(f"Fatal error during processing: {e}")
            raise
        finally:
            elapsed_time = time.perf_counter() - start_time
            self.logger.info(
                f"Traitement terminé : {sf_count} SF en {elapsed_time:.3f}s "
                f"({sf_count / elapsed_time:.0f} SF/s) - {error_count} erreurs"
            )