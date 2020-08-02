import typing
import tarfile
import tempfile
import multiprocessing
import signal
import subprocess
import pathlib
import sys
import time
import contextlib
import httpx

from . import app
from .. import model


CADDY_VERSION = "2.1.1"
CADDY_URL = (
    f"https://github.com/caddyserver/caddy/releases/download/v{CADDY_VERSION}/caddy_{CADDY_VERSION}_linux_amd64.tar.gz"
)
CADDY_CWD = pathlib.Path(__file__).parent.absolute()
CADDYFILE_PATH = CADDY_CWD / "Caddyfile"
CA_FILE = CADDY_CWD / "server.crt"

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)

process_app = None
process_caddy = None


def stop():
    global process_app
    global process_caddy

    # send SIGTERM
    if process_app is not None:
        process_app.terminate()
        process_app = None

    if process_caddy is not None:
        process_caddy.terminate()
        process_caddy = None


def signal_handler(sig, frame):
    stop()
    sys.exit(128 + sig)


def download_caddy(caddy_path: pathlib.Path) -> None:
    with tempfile.TemporaryFile() as f:
        print("Downloading", CADDY_URL, "\n to", caddy_path)
        response = httpx.get(CADDY_URL)
        response.raise_for_status()
        f.write(response.content)
        f.seek(0)
        t = tarfile.open(fileobj=f, mode="r")
        # assume that caddy_path ends with "caddy"
        t.extract("caddy", caddy_path.parent)


def wait_for_url(url, timeout):
    SLEEP_TIME = 0.2
    for _ in range(int(timeout / SLEEP_TIME)):
        time.sleep(SLEEP_TIME)
        try:
            response = httpx.get(url, verify=CA_FILE)
            response.raise_for_status()
        except Exception:
            pass
        else:
            return

    raise RuntimeError(f"{url} not available")


def start(server_config: model.ServerConfig, caddy_log_file):
    global process_app
    global process_caddy

    #
    for sig in HANDLED_SIGNALS:
        signal.signal(sig, signal_handler)

    # caddy
    if not server_config.caddy_path.exists():
        download_caddy(server_config.caddy_path)
    process_caddy = subprocess.Popen(
        (server_config.caddy_path, "run", "-config", CADDYFILE_PATH),
        cwd=CADDY_CWD, stdout=caddy_log_file, stderr=caddy_log_file,
    )

    # app
    spawn = multiprocessing.get_context("spawn")
    process_app = spawn.Process(target=app.main, args=("localhost", 5000))
    process_app.start()

    wait_for_url("http://localhost:5000/0/1", 5)
    wait_for_url("https://localhost:4001/0/1", 5)


@contextlib.contextmanager
def server(server_config: model.ServerConfig) -> typing.Generator[model.SslConfig, None, None]:
    with open(server_config.caddy_log_path, "w", encoding="utf-8") as caddy_log_file:
        start(server_config, caddy_log_file)
        try:
            yield model.SslConfig(local_ca_file=CA_FILE)
        finally:
            stop()
