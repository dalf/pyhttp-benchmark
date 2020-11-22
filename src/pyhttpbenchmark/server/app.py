import typing
import uvloop  # type: ignore
import uvicorn  # type: ignore
import asyncio
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from os import urandom


uvloop.install()

response_cache: typing.Dict[int, bytes] = dict()


async def answer(request):
    delay = request.path_params["delay"]
    size = request.path_params["size"]
    await asyncio.sleep(delay / 1000)
    if size in response_cache:
        response = response_cache[size]
    else:
        response = urandom(size)
        response_cache[size] = response
    return PlainTextResponse(response)


app = Starlette(debug=True, routes=[Route("/{delay:int}/{size:int}", answer), ])


def main(host, port):
    uvicorn.run("pyhttpbenchmark.server.app:app", host=host, port=port, log_level="error")


if __name__ == "__main__":
    main("127.0.0.1", 5000)
