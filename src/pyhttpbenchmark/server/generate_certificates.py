import typing
import contextlib
import pathlib
import trustme  # type: ignore

from .. import model, types


@contextlib.contextmanager
def generate_certificates(
    directory: types.Pathlike, identities: typing.Sequence[str], key_size: int = 2048,
) -> typing.Iterator[model.Certificates]:
    cert_dir = pathlib.Path(directory)
    cert_dir.mkdir(exist_ok=True)

    # Generate the CA certificate.
    trustme._KEY_SIZE = key_size
    ca = trustme.CA()
    cert = ca.issue_cert(*identities)

    # Write the server private key.
    server_key = cert_dir / "server.key"
    cert.private_key_pem.write_to_path(path=str(server_key))

    # Write the server certificate.
    server_cert = cert_dir / "server.pem"
    with server_cert.open(mode="w") as f:
        f.truncate()
    for blob in cert.cert_chain_pems:
        blob.write_to_path(path=str(server_cert), append=True)

    # Write the client certificate.
    client_cert = cert_dir / "client.pem"
    ca.cert_pem.write_to_path(path=str(client_cert))

    yield model.Certificates(
        server_key=server_key, server_cert=server_cert,
        client_cert=client_cert
    )
