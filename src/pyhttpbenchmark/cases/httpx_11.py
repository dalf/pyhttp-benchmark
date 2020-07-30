from .. import model
from . import httpx


"""
httpx HTTP/1.1
"""


async def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    await httpx.main_partial(False, scenario, sslconfig)
