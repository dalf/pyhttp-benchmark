from toolkit import async_report_time, report_time, run, print_stats

TRIES = 20
URL = [
    "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",
    "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=linux%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",
    "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",
    "https://www.wikidata.org/w/index.php?search=linux&ns0=1",
    "https://www.etymonline.com/search?page=1&q=linux",
    "https://api.duckduckgo.com/?q=time&format=json&pretty=0&no_redirect=1&d=1"
]


def bench_requests():
    import requests
    import threading
    from uuid import uuid4

    def do_request(session, url):
        session.get(url)

    session = requests.Session()
    with report_time("FuturesSession w/ max workers"):
        search_id = uuid4().__str__()
        for url in URL:
            th = threading.Thread(
                target = do_request,
                args = (session, url),
                name=search_id,
            )
            th.start()

        for th in threading.enumerate():
            if th.name == search_id:
                th.join()


async def bench_aiohttp():
    import asyncio
    import aiohttp

    async def get(session, url):
        async with session.get(url) as response:
            return await response.read()

    async with async_report_time("aiohttp"):
        async with aiohttp.ClientSession() as session:
            r = await asyncio.gather(*[get(session, url) for url in URL])


async def bench_httpx():
    import asyncio
    import httpx

    async with async_report_time("httpx"):
        async with httpx.AsyncClient() as client:
            r = await asyncio.gather(*[client.get(url) for url in URL])


def main():
    # logging.basicConfig(level=logging.DEBUG)

    for _ in range(TRIES):
        # aiohttp
        run(bench_httpx)

        # async code
        run(bench_aiohttp)

        # requests
        run(bench_requests)

        import time
        time.sleep(1)

    print_stats()


if __name__ == '__main__':
    main()
