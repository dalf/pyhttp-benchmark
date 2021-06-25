import typing
from .. import model
from ..case import async_record_measure

import asyncio
import httpx
import anyio  # enable anyio

# make sure there is no import during the benchmark
import httpcore._async.http2
import stringprep

"""
httpx
"""

main_caller = 'anyio'


async def get(client, url):
    response = await client.get(url)
    response.content


async def step_delay(task_group, step, client):
    await asyncio.sleep(step.time)


async def step_requests(task_group, step, client):
    return list(map(lambda url: task_group.start_soon(get, client, url), step.urls))


async def step_request(task_group, step, client):
    await get(client, step.url)


handlers: typing.Dict[typing.Any,
                      typing.Callable[[asyncio.events.AbstractEventLoop,
                                       typing.Any,
                                       httpx.AsyncClient],
                                      None]] =\
    {model.StepDelay: step_delay, model.StepRequests: step_requests, model.StepRequest: step_request}


async def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    verify: typing.Union[bool, str] = True if not scenario.local_ca else str(sslconfig.local_ca_file)
    async with httpx.AsyncClient(verify=verify, timeout=20.0) as client:
        async with async_record_measure():
            async with anyio.create_task_group() as task_group:
                for step in scenario.steps:
                    task_group.start_soon(handlers[step.__class__], task_group, step, client)
