import argparse
import urllib.parse
import webbrowser
import aiohttp
import sc2replaynotifier


class ReplayUploader(sc2replaynotifier.ReplayHandler):
    def __init__(self, upload_target):
        self._upload_target = upload_target

    async def handle_replay(self, replay_path: str):
        print("Uploading replay: " + replay_path)
        replay_file = open(replay_path, "rb")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self._upload_target, data=replay_file) as resp:
                if str(resp.status).startswith("3") and "Location" in resp.headers:
                    redirect = resp.headers["Location"]
                    webbrowser.open_new_tab(urllib.parse.urljoin(self._upload_target, redirect))


def main():
    parser = argparse.ArgumentParser(
        prog="sc2autouploader",
        description=
        "Automatically upload StarCraft II replays to a target destination.")
    parser.add_argument(
        "TARGET_URL", type=str, nargs=1, help="URL of replay upload target.")

    args = parser.parse_args()

    print("Waiting for replays...")
    sc2replaynotifier.create_replay_notifier(ReplayUploader(args.TARGET_URL)).handle_replays()


if __name__ == "__main__":
    main()
