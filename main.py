from toolkit import async_report_time, report_time, run, print_stats
import scenarios


def bench_request(test, session_list, url1, delay_in_between, url2, cafile):
    import random
    import threading
    import time
    from uuid import uuid4

    if cafile is not None:
        for session in session_list:
            session.verify = cafile

    def one_engine_request(session, url):
        session.get(url).content

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
        th_user1 = threading.Thread(target=one_user_request, args=(random.choice(session_list), url1))
        th_user2 = threading.Thread(target=one_user_request, args=(random.choice(session_list), url2))
        th_user1.start()
        time.sleep(delay_in_between)
        th_user2.start()
        th_user1.join()
        th_user2.join()


def bench_requests_one_session(url1, delay_in_between, url2, cafile):
    import requests
    bench_request("request (1 session)", [requests.Session()], url1, delay_in_between, url2, cafile)


def bench_requests_four_sessions(url1, delay_in_between, url2, cafile):
    import requests
    # four uwsgi processes --> four sessions and four connection pools
    bench_request("request (4 sessions)", [requests.Session(), requests.Session(), requests.Session(), requests.Session()], url1, delay_in_between, url2, cafile)


async def bench_aiohttp(url1, delay_in_between, url2, cafile):
    import asyncio
    import aiohttp
    import ssl

    loop = asyncio.get_event_loop()
    sslparam = ssl.create_default_context(cafile=cafile) if cafile else None

    async def get(session, url):
        async with session.get(url, ssl=sslparam) as response:
            return await response.read()

    async with async_report_time("aiohttp"):
        async with aiohttp.ClientSession() as session:
            task1 = list(map(lambda url: loop.create_task(get(session, url)), url1))
            await asyncio.sleep(delay_in_between)
            task2 = list(map(lambda url: loop.create_task(get(session, url)), url2))
            all_tasks = task1 + task2
            await asyncio.gather(*all_tasks)


async def bench_httpx(url1, delay_in_between, url2, cafile):
    import asyncio
    import httpx

    loop = asyncio.get_event_loop()

    async def get(client, url):
        response = await client.get(url)
        response.content

    async with async_report_time("httpx"):
        async with httpx.AsyncClient(http2=True, verify=cafile) as client:
            task1 = list(map(lambda url: loop.create_task(get(client, url)), url1))
            await asyncio.sleep(delay_in_between)
            task2 = list(map(lambda url: loop.create_task(get(client, url)), url2))
            all_tasks = task1 + task2
            await asyncio.gather(*all_tasks)


def run_scenario(scenario):
    print("\n%s\n" % scenario['name'])
    ten_of_tries = int(scenario["tries"] / 10)
    for i in range(scenario["tries"]):
        run_bench = lambda f: run(f, \
                                  scenario["url1"], \
                                  scenario["delay_in_between"], \
                                  scenario["url2"], \
                                  scenario["cafile"], \
                                  print_prefix="%2i / %2i" % (i+1, scenario["tries"]), \
                                  no_print=i%ten_of_tries>0)
        run_bench(bench_httpx)
        run_bench(bench_aiohttp)
        run_bench(bench_requests_four_sessions)
        #run_bench(bench_requests_one_session)
    print("\n## Scenario: %s\n" % scenario['name'])
    print_stats()
    print("\n")


def main():
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    run_scenario(scenarios.LOCALHOST)
    run_scenario(scenarios.LOCALHOST2)
    run_scenario(scenarios.LOCALHOST3)
    run_scenario(scenarios.EXTERNAL)


if __name__ == '__main__':
    main()
