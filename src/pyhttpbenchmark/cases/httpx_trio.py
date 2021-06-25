import typing
from .. import model
from ..case import async_record_measure

import trio
import httpx

# make sure there is no import during the benchmark
import httpcore._async.http2
import stringprep

"""
httpx
"""

main_caller = 'trio'


async def get(client, url):
    response = await client.get(url)
    response.content


async def step_delay(nursery, step, client):
    await trio.sleep(step.time)


async def step_requests(nursery, step, client):
    for url in step.urls:
        nursery.start_soon(get, client, url)


async def step_request(nursery, step, client):
    await get(client, step.url)


handlers: typing.Dict[typing.Any,
                      typing.Callable[[trio.Nursery,
                                       typing.Any,
                                       httpx.AsyncClient],
                                      None]] =\
    {model.StepDelay: step_delay, model.StepRequests: step_requests, model.StepRequest: step_request}


async def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    verify: typing.Union[bool, str] = True if not scenario.local_ca else str(sslconfig.local_ca_file)
    async with httpx.AsyncClient(verify=verify, timeout=20.0) as client:
        async with async_record_measure():
            async with trio.open_nursery() as nursery:
                for step in scenario.steps:
                    await handlers[step.__class__](nursery, step, client)
