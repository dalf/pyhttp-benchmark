import typing
from .. import model
from ..case import async_record_measure

import asyncio
import httpx


"""
httpx HTTP/2
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


async def main_partial(http2, scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    loop = asyncio.get_event_loop()
    all_tasks = []
    verify: typing.Union[bool, str] = True if not scenario.local_ca else str(sslconfig.local_ca_file)
    async with httpx.AsyncClient(http2=http2, verify=verify) as client:
        async with async_record_measure():
            for step in scenario.steps:
                all_tasks += await handlers[step.__class__](loop, step, client)
            await asyncio.gather(*all_tasks)


async def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    await main_partial(True, scenario, sslconfig)
