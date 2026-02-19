"""
AfpParser - CLI afp application
"""
import time
from pathlib import Path

from cli.cli import run
from dispatcher import init_dispatcher

from logger import get_logger
from writer.writer_factory import create_writer


def main():
    """
    Main entry point for the AFP Parser application.

    This function orchestrates the entire parsing workflow:
    1. Initializes logging
    2. Runs the CLI to get user input and configuration
    3. Creates a dispatcher to handle the specific file type
    4. Executes the appropriate parser and generates output

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    start_time = time.perf_counter()

    # Initialize the application logger
    logger = get_logger(__name__)
    logger.info("Application started")

    # Run the CLI interface and parse command-line arguments
    # Returns None if CLI parsing fails (invalid or missing arguments)
    cli_input = run()

    if cli_input is None:
        return 1

    t1 = time.perf_counter()
    logger.info(f"[TIMING] After CLI: {t1 - start_time:.3f}s")

    # Initialize the dispatcher with the input file path and config
    # The dispatcher determines which parser to use based on file type
    dispatcher = init_dispatcher(cli_input.path, cli_input.config_path)
    
    t2 = time.perf_counter()
    logger.info(f"[TIMING] After init_dispatcher: {t2 - t1:.3f}s")
    
    logger.info(f"Dispatcher created for {cli_input.path}")
    logger.info(f"Filetype: {cli_input.filetype}")

    # Get the appropriate parser processor for the detected file type
    parser_processor = dispatcher.dispatch(cli_input.filetype)
    
    t3 = time.perf_counter()
    logger.info(f"[TIMING] After dispatch: {t3 - t2:.3f}s")

    # Create output path based on format
    output_path = cli_input.path.replace('.afp', f'_structure.{cli_input.output_format}')

    # Create and inject the writer based on the output format
    writer = create_writer(cli_input.output_format, Path(cli_input.path).name, output_path)
    
    t4 = time.perf_counter()
    logger.info(f"[TIMING] After create_writer: {t4 - t3:.3f}s")
    
    parser_processor.set_writer(writer)

    elapsed = time.perf_counter() - start_time
    logger.info(f"Time before parse: {elapsed:.3f}s")

    # Execute the parser and write output
    parser_processor.run(output_path)
    elapsed = time.perf_counter() - start_time
    logger.info(f"Total time: {elapsed:.3f}s")
    return 0

if __name__ == "__main__":
    # Execute main() and use its return value as the exit code
    raise SystemExit(main())
