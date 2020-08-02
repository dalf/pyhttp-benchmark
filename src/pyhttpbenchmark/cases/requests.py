import typing
import random
import threading
import time
from uuid import uuid4

import requests

from .. import model
from ..case import record_measure


"""
requests (1 session)
"""


def one_engine_request(session, url) -> None:
    session.get(url).content


def one_user_request(session, urls) -> None:
    """
    based on https://github.com/asciimoo/searx/blob/b06fc319423c84f3513a771b58441fb304d0606f/searx/search.py#L221-L239
    """
    search_id = uuid4().__str__()
    for url in urls:
        th_engine = threading.Thread(target=one_engine_request, args=(session, url), name=search_id,)
        th_engine.start()

    for th_engine in threading.enumerate():
        if th_engine.name == search_id:
            th_engine.join()


def step_requests(step, session) -> typing.List[threading.Thread]:
    t = threading.Thread(target=one_user_request, args=(session, step.urls))
    t.start()
    return [t]


def step_request(step, session) -> typing.List[threading.Thread]:
    one_engine_request(session, step.url)
    return []


def step_delay(step, session) -> typing.List[threading.Thread]:
    time.sleep(step.time)
    return []


handlers: typing.Dict[typing.Any, typing.Callable[[typing.Any, requests.Session], typing.List[threading.Thread]]] =\
    {model.StepRequests: step_requests, model.StepRequest: step_request, model.StepDelay: step_delay}


def main_partial(session_list: typing.List[requests.Session], scenario: model.Scenario,
                 sslconfig: model.SslConfig) -> None:
    if scenario.local_ca:
        for session in session_list:
            session.verify = str(sslconfig.local_ca_file)

    all_threads = []
    with record_measure():
        for step in scenario.steps:
            all_threads += handlers[step.__class__](step, random.choice(session_list))
        for t in all_threads:
            t.join()


def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    session_list = [requests.Session()]
    main_partial(session_list, scenario, sslconfig)
