import asyncio
import aiohttp
import ssl
from .. import scenarios, model
from ..case import async_record_measure


"""
aiohttp
"""


async def get(session, sslparam, url):
    async with session.get(url, ssl=sslparam) as response:
        return await response.read()


async def step_delay(loop, step, session, sslparam):
    await asyncio.sleep(step.time)
    return []


async def step_requests(loop, step, session, sslparam):
    return list(map(lambda url: loop.create_task(get(session, sslparam, url)), step.urls))


async def step_request(loop, step, session, sslparam):
    await get(session, sslparam, step.url)
    return []


handlers = {scenarios.StepDelay: step_delay, scenarios.StepRequests: step_requests, scenarios.StepRequest: step_request}


async def main(scenario: scenarios.Scenario, sslconfig: model.SslConfig) -> None:
    loop = asyncio.get_event_loop()
    sslparam = ssl.create_default_context(cafile=sslconfig.local_ca_file) if scenario.local_ca else None
    all_tasks = []
    async with aiohttp.ClientSession() as session:
        async with async_record_measure():
            for step in scenario.steps:
                all_tasks += await handlers[step.__class__](loop, step, session, sslparam)
            await asyncio.gather(*all_tasks)
