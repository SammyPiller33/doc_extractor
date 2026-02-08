"""
TaskTracker - CLI afp application
"""

from cli.cli import run
from dispatcher import init_dispatcher

from logger import get_logger
import json

def main():

    logger = get_logger(__name__)
    logger.info("Application started")

    cli_input = run()

    if cli_input is None:
        return 1

    dispatcher = init_dispatcher(cli_input.path, cli_input.config_path)
    logger.info(f"Dispatcher created for {cli_input.path}")
    logger.info(f"Filetype: {cli_input.filetype}")
    
    parser_processor = dispatcher.dispatch(cli_input.filetype)
    logger.info(f"Name of the parser processor: {parser_processor.__class__.__name__}")

    structure = parser_processor.run()

    # output_path = cli_input.path.replace('.afp', '_structure.json')
    # structure_dict = structure.to_dict()
    # # Write to file
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     json.dump(structure_dict, f, indent=2, ensure_ascii=False)
    #
    # logger.info(f"Structure saved to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# TODO 2 - Create a parser handler for manipulating the data (return it from the dispatcher ?)
# TODO 3 - Add parsing of easy SF data, like BDT, EDT, NOP, IMM and TLE
# TODO 4 - Gestion des erreurs
# TODO 5 - Regarder si lib pour mesure de performance