import typing
from .. import model
from ..case import async_record_measure

import asyncio
import httpx
import httpcore


"""
httpx
"""


async def get(client, url):
    response = await client.get(url)
    response.content


async def step_delay(loop, step, client):
    await asyncio.sleep(step.time)
    return []


async def step_requests(loop, step, client):
    return list(map(lambda url: loop.create_task(get(client, url)), step.urls))


async def step_request(loop, step, client):
    await get(client, step.url)
    return []


handlers: typing.Dict[typing.Any,
                      typing.Callable[[asyncio.events.AbstractEventLoop,
                                       typing.Any,
                                       httpx.AsyncClient],
                                      typing.Awaitable[typing.List[asyncio.Task]]]] =\
    {model.StepDelay: step_delay, model.StepRequests: step_requests, model.StepRequest: step_request}


def get_parameters():
    parameters = []
    for http2 in [True, False]:
        for read_num_bytes in range(9):
            parameters.append((http2, 4096*2**read_num_bytes))
    return ('http2,read_num_bytes', parameters)


async def main(scenario: model.Scenario, sslconfig: model.SslConfig, http2: bool = True, read_num_bytes: int = None) -> None:
    if read_num_bytes:
        httpcore._async.http2.AsyncHTTP2Connection.READ_NUM_BYTES = read_num_bytes
        httpcore._async.http11.AsyncHTTP11Connection.READ_NUM_BYTES = read_num_bytes
    loop = asyncio.get_event_loop()
    all_tasks = []
    verify: typing.Union[bool, str] = True if not scenario.local_ca else str(sslconfig.local_ca_file)
    async with httpx.AsyncClient(http2=http2, verify=verify, timeout=20.0) as client:
        async with async_record_measure():
            for step in scenario.steps:
                all_tasks += await handlers[step.__class__](loop, step, client)
            await asyncio.gather(*all_tasks)
