"""
TaskTracker - CLI afp application
"""
import time

import orjson


from cli.cli import run
from dispatcher import init_dispatcher

from logger.logger import get_logger

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

    # Performance measurement - Parsing
    start_parse = time.perf_counter()
    structure = parser_processor.run()
    end_parse = time.perf_counter()
    parse_duration = end_parse - start_parse

    logger.info(f"Parsing completed in {parse_duration:.3f}s ({len(structure)} SFs parsed)")

    output_path = cli_input.path.replace('.afp', '_structure.json')

    # Performance measurement - JSON serialization
    start_json = time.perf_counter()

    # orjson écrit directement en bytes et est beaucoup plus rapide
    with open(output_path, 'wb') as f:
        f.write(orjson.dumps(
            structure,
            option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS
        ))

    end_json = time.perf_counter()
    json_duration = end_json - start_json

    logger.info(f"JSON serialization completed in {json_duration:.3f}s")
    logger.info(f"Structure saved to {output_path}")
    logger.info(f"Total execution time: {parse_duration + json_duration:.3f}s")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# TODO 3 - Add parsing of easy SF data, like BDT, EDT, NOP, IMM and TLE
# TODO 4 - Gestion des erreurs
# TODO 5 - tester/améliorer perf, refactor...
# TODO 6 - Gérer l'output
# TODO 7 - ajouter des tests unitaires