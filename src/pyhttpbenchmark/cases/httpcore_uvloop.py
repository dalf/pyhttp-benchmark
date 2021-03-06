import ssl
from .. import model
from ..case import async_record_measure

import asyncio
import httpcore
import irl  # type: ignore


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

    status_code, headers, stream, ext = await transport.arequest(
        method=b"GET",
        url=(scheme, host, port, full_path),
        headers=[(b"host", urlobj.host_header())],
    )

    try:
        content = b"".join([chunk async for chunk in stream])
    finally:
        await stream.aclose()

    return content


async def step_delay(step, transport):
    await asyncio.sleep(step.time)
    return []


async def step_requests(step, transport):
    return [asyncio.create_task(get(url, transport)) for url in step.urls]


async def step_request(step, transport):
    await get(step.url, transport)
    return []


handlers: dict = {
    model.StepDelay: step_delay,
    model.StepRequests: step_requests,
    model.StepRequest: step_request,
}


def get_parameters():
    parameters = []
    for http2 in [True, False]:
        parameters.append((http2,))
    return ('http2', parameters)


async def main(scenario: model.Scenario, sslconfig: model.SslConfig,
               http2: bool = True) -> None:
    ssl_context = (
        ssl.create_default_context(cafile=str(sslconfig.local_ca_file))
        if scenario.local_ca
        else None
    )
    async with httpcore.AsyncConnectionPool(http2=http2, ssl_context=ssl_context) as transport:
        async with async_record_measure():
            tasks = []
            for step in scenario.steps:
                tasks += await handlers[step.__class__](step, transport)
            await asyncio.gather(*tasks)
