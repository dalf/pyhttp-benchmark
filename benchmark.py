from toolkit import async_report_time, report_time, run, print_stats

TRIES = 20
URL1 = [
    "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",
    "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=linux%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",
    "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",
    "https://www.wikidata.org/w/index.php?search=linux&ns0=1",
    "https://www.etymonline.com/search?page=1&q=linux",
    "https://api.duckduckgo.com/?q=time&format=json&pretty=0&no_redirect=1&d=1"
]
DELAY_IN_BETWEEN = 0.5
URL2 = [
    "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=searx&format=json&sroffset=0&srlimit=5&srwhat=text",
    "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=searx%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",
    "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=searx&format=json&sroffset=0&srlimit=5&srwhat=text",
    "https://www.wikidata.org/w/index.php?search=searx&ns0=1",
    "https://www.etymonline.com/search?page=1&q=searx",
    "https://api.duckduckgo.com/?q=searx&format=json&pretty=0&no_redirect=1&d=1"
]


def bench_request(test, session_list):
    import random
    import threading
    import time
    from uuid import uuid4

    def one_engine_request(session, url):
        session.get(url)

    def one_user_request(session, url_list):
        search_id = uuid4().__str__()
        for url in url_list:
            th_engine = threading.Thread(
                target=one_engine_request,
                args=(session, url),
                name=search_id,
            )
            th_engine.start()

        for th_engine in threading.enumerate():
            if th_engine.name == search_id:
                th_engine.join()

    with report_time(test):
        th_user1 = threading.Thread(target=one_user_request, args=(random.choice(session_list), URL1))
        th_user2 = threading.Thread(target=one_user_request, args=(random.choice(session_list), URL2))
        th_user1.start()
        time.sleep(DELAY_IN_BETWEEN)
        th_user2.start()
        th_user1.join()
        th_user2.join()


def bench_requests_one_session():
    import requests
    bench_request("request (1 session)", [requests.Session()])


def bench_requests_four_sessions():
    import requests
    # four uwsgi processes --> four sessions and four connection pools
    bench_request("request (4 sessions)", [requests.Session(), requests.Session(), requests.Session(), requests.Session()])


async def bench_aiohttp():
    import asyncio
    import aiohttp

    loop = asyncio.get_event_loop()

    async def get(session, url):
        async with session.get(url) as response:
            return await response.read()

    async with async_report_time("aiohttp"):
        async with aiohttp.ClientSession() as session:
            task1 = list(map(lambda url: loop.create_task(get(session, url)), URL1))
            await asyncio.sleep(DELAY_IN_BETWEEN)
            task2 = list(map(lambda url: loop.create_task(get(session, url)), URL2))
            all_tasks = task1 + task2
            await asyncio.gather(*all_tasks)


async def bench_httpx():
    import asyncio
    import httpx

    loop = asyncio.get_event_loop()

    async with async_report_time("httpx"):
        async with httpx.AsyncClient(http2=True) as client:
            task1 = list(map(lambda url: loop.create_task(client.get(url)), URL1))
            await asyncio.sleep(DELAY_IN_BETWEEN)
            task2 = list(map(lambda url: loop.create_task(client.get(url)), URL2))
            all_tasks = task1 + task2
            await asyncio.gather(*all_tasks)


def main():
    # import logging
    # logging.basicConfig(level=logging.DEBUG)

    for i in range(1, TRIES+1):
        prefix = "%2i / %2i" % (i, TRIES)
        run(bench_httpx, print_prefix=prefix)
        run(bench_aiohttp, print_prefix=prefix)
        run(bench_requests_four_sessions, print_prefix=prefix)
        #run(bench_requests_one_session, print_prefix=prefix)

    print_stats()


if __name__ == '__main__':
    main()
