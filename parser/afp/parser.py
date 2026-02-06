import time
from stream_sf import SfStreamer


def run():
    start_time = time.perf_counter()

    sf_streamer = SfStreamer("../../sample/POC_AFP_PARSE.afp")
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
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run()
