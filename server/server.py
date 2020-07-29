import uvloop
import uvicorn
import asyncio
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from os import urandom


uvloop.install()

response_cache = dict()


async def answer(request):
    delay = request.path_params['delay']
    size = request.path_params['size']
    await asyncio.sleep(delay / 1000)
    if size in response_cache:
        response = response_cache[size]
    else:
        response = urandom(size)
        response_cache[size] = response
    return PlainTextResponse(response)


app = Starlette(debug=True, routes=[
    Route('/{delay:int}/{size:int}', answer),
])

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="error", workers=4)
