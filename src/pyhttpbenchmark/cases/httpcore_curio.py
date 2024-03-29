import ssl
from .. import model
from ..case import async_record_measure

import curio
import httpcore
import irl  # type: ignore

# make sure there is no import during the benchmark
import httpcore._async.http2
import stringprep


"""
httpcore
"""


async def get(url, transport):
    urlobj = irl.URL.parse(url)

    assert urlobj.scheme in ("http", "https")
    assert urlobj.host is not None
    scheme = urlobj.scheme.encode("utf-8")
    host = urlobj.host.encode("utf-8")
    port = urlobj.port
    full_path = urlobj.target()

    status_code, headers, stream, ext = await transport.handle_async_request(
        method=b"GET",
        url=(scheme, host, port, full_path),
        headers=[(b"host", urlobj.host_header())],
        stream=httpcore.AsyncByteStream(),
        extensions={}
    )

    try:
        content = b"".join([chunk async for chunk in stream])
    finally:
        await stream.aclose()

    return content


async def step_delay(g, step, transport):
    await curio.sleep(step.time)


async def step_requests(g, step, transport):
    for url in step.urls:
        await g.spawn(get, url, transport)


async def step_request(g, step, transport):
    await get(step.url, transport)


handlers: dict = {
    model.StepDelay: step_delay,
    model.StepRequests: step_requests,
    model.StepRequest: step_request,
}


def get_parameters():
    parameters = []
    for http2 in ['http2', 'http1']:
        parameters.append((http2,))
    return ('http2', parameters)


async def main(scenario: model.Scenario, sslconfig: model.SslConfig,
               http2: str = 'http1') -> None:
    ssl_context = (
        ssl.create_default_context(cafile=str(sslconfig.local_ca_file))
        if scenario.local_ca
        else None
    )
    http2 = http2 == 'http2'
    async with httpcore.AsyncConnectionPool(http2=http2, ssl_context=ssl_context) as transport:
        async with async_record_measure():
            async with curio.TaskGroup() as g:
                for step in scenario.steps:
                    await handlers[step.__class__](g, step, transport)
