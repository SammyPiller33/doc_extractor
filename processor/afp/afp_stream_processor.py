from parser.afp import SfStreamer
from parser.afp.sf_filter import SfFilter
from processor.file_processor import Processor
from logger import get_logger

class AFPStreamProcessor(Processor):

    def __init__(self, sf_streamer: SfStreamer, config_path: str) -> None:

        super().__init__(sf_streamer)

        logger = get_logger(__name__)

        if config_path:
            try:
                sf_filter = SfFilter(config_path)
                self.parser.set_config(sf_filter)
                logger.info(f"Filtre SF chargé : {sf_filter.get_filter_info()}")
            except (ValueError, FileNotFoundError) as e:
                logger.error(f"Erreur de chargement du filtre : {e}")

        # self.builder = None

    def run(self):
        """Process the AFP stream and build the document structure."""
        # Initialize builder with file info
        # self.builder = AFPStructureBuilder(
        #     file_path=str(self.parser._path),
        #     file_size=self.parser.afp_len
        # )
        sfs = []
        # Stream and process each SF
        for sf in self.parser.stream():
            sfs.append(sf)
            # self.builder.add_structured_field(sf)
        
        # Finalize and get structure
        # structure = self.builder.finalize()
        
        # Convert to JSON
        # json_output = structure.to_dict()
        #
        # # Pretty print for demonstration
        # print(json.dumps(json_output, indent=2, ensure_ascii=False))
        
        return sfs