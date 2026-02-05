from stream_sf import SfStreamer


def run():

    sf_streamer = SfStreamer("../../sample/start.afp")

    for sf in sf_streamer.stream():
        print(sf)

if __name__ == "__main__":
    run()

