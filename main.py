"""
TaskTracker - CLI afp application
"""

from cli.cli import run
from dispatcher import create_dispatcher
import time

def parser_handler(parser):
    start_time = time.perf_counter()

    sf_streamer = parser
    file_size_bytes = sf_streamer.afp_len
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    count = 0
    for _ in sf_streamer.stream():
        count += 1

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"\n{'=' * 60}")
    print(f"STATISTIQUES DE PERFORMANCE")
    print(f"{'=' * 60}")
    print(f"Temps d'exécution:        {elapsed_time:.4f} secondes")
    print(f"Taille du fichier:        {file_size_kb:.2f} Ko ({file_size_mb:.2f} MB)")
    print(f"Structured fields:        {count}")
    print(f"Vitesse:                  {count / elapsed_time:.2f} SF/sec")
    print(f"Débit:                    {file_size_mb / elapsed_time:.2f} MB/sec")
    print(f"Latence moyenne par SF:   {(elapsed_time / count) * 1_000_000:.2f} µs")
    print(f"Taille moyenne par SF:    {file_size_bytes / count:.0f} octets")

def main():

    print("main")

    cli_input = run()
    if cli_input is None:
        return 1

    dispatcher = create_dispatcher(cli_input.path)
    parser = dispatcher.dispatch(cli_input.filetype)

    parser_handler(parser)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




# TODO 1 - Observabilité : Add the logger and call it from the main + Create logo for application
# TODO 2 - Create a parser handler for manipulating the data (return it from the dispatcher ?)
# TODO 3 - Add parsing of easy SF data, like BDT, EDT, NOP, IMM and TLE
# TODO 4 - Gestion des erreurs
# TODO 5 - Regarder si lib pour mesure de performance
