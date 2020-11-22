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
import jinja2

from . import app, generate_certificates
from .. import model, scenarios


PLATFORM = "mac" if sys.platform == "darwin" else "linux"
CADDY_VERSION = "2.1.1"
CADDY_URL = (
    f"https://github.com/caddyserver/caddy/releases/download/v{CADDY_VERSION}/caddy_{CADDY_VERSION}_{PLATFORM}_amd64.tar.gz"  # noqa
)
CADDYFILE_TEMPLATE_PATH = pathlib.Path(__file__).parent.absolute() / "Caddyfile.template"

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)

APP_HOSTNAME = "127.0.0.1"
APP_PORT = 5000

process_app: typing.Optional[multiprocessing.context.SpawnProcess] = None
process_caddy: typing.Optional[subprocess.Popen] = None


def stop() -> None:
    global process_app
    global process_caddy

    # send SIGTERM
    if process_app is not None:
        process_app.terminate()
        process_app.join(3.0)
        process_app.close()
        process_app = None

    if process_caddy is not None:
        process_caddy.terminate()
        try:
            process_caddy.wait(3.0)
        except subprocess.TimeoutExpired:
            process_caddy.kill()
        process_caddy = None


def signal_handler(sig, frame) -> typing.NoReturn:
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


def create_caddyfile(src_template: str, dest: pathlib.Path, context: typing.Dict[typing.Any, typing.Any]) -> None:
    template = jinja2.Template(src_template)
    result = template.render(context)
    with open(dest, 'w', encoding='utf-8') as dest_file:
        dest_file.write(result)


def wait_for_url(url: str, certificates: model.Certificates, timeout: float) -> None:
    SLEEP_TIME = 0.2
    last_exception = None
    for _ in range(int(timeout / SLEEP_TIME)):
        time.sleep(SLEEP_TIME)
        try:
            response = httpx.get(url, verify=str(certificates.client_cert))
            response.raise_for_status()
        except Exception as e:
            last_exception = e
        else:
            return

    stop()
    raise SystemExit(f"{url} not available", last_exception)


def start(server_config: model.ServerConfig, caddy_log_file, certificates: model.Certificates,
          hostname: str, port_range: typing.List[int]) -> None:
    global process_app
    global process_caddy

    if process_app is not None or process_caddy is not None:
        raise Exception('A server is already running')

    # create Caddyfile
    caddypath_path = server_config.caddy_config_path / "Caddyfile"
    create_caddyfile(scenarios.CADDYFILE, caddypath_path, {
        "hostname": hostname,
        "ports": port_range,
        "certificates": certificates,
        "app": {
            "hostname": APP_HOSTNAME,
            "port": APP_PORT
        }
    })

    # signals
    for sig in HANDLED_SIGNALS:
        signal.signal(sig, signal_handler)

    # caddy
    if not server_config.caddy_path.exists():
        download_caddy(server_config.caddy_path)
    process_caddy = subprocess.Popen(
        (server_config.caddy_path, "run", "-config", caddypath_path),
        cwd=server_config.caddy_config_path, stdout=caddy_log_file, stderr=caddy_log_file,
    )

    # app
    spawn = multiprocessing.get_context("spawn")
    process_app = spawn.Process(target=app.main, args=(APP_HOSTNAME, APP_PORT))
    process_app.start()

    # wait for the servers to be ready
    wait_for_url(f"http://{APP_HOSTNAME}:{APP_PORT}/0/1", certificates, 5)
    for port in port_range:
        wait_for_url(f"https://{hostname}:{port}/0/1", certificates, 5)

    # check that the app is still running (another app on the same port is not running)
    if not process_app.is_alive():
      raise Exception('app has failed to start, the port is already bound')


@contextlib.contextmanager
def server(server_config: model.ServerConfig,
           hostname: str, port_range: typing.List[int]) -> typing.Generator[model.SslConfig, None, None]:
    with open(server_config.caddy_log_path, "w", encoding="utf-8") as caddy_log_file:
        with generate_certificates.generate_certificates(server_config.caddy_config_path, (hostname,)) as certificates:
            start(server_config, caddy_log_file, certificates, hostname, port_range)
            try:
                yield model.SslConfig(local_ca_file=certificates.client_cert)
            finally:
                stop()
