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


def get_parameters():
    """
    in the case of a WSGI application which sends HTTP requests,
    it is not possible to have common pool.
    this case uses 4 differents requests.Session to simulate this behavior.
    """
    return ('session_count', [(1), (4)])


def main_partial(scenario: model.Scenario, sslconfig: model.SslConfig, session_count: int = 1) -> None:
    session_list = [None] * session_count
    for i in range(session_count):
        session_list[i] = requests.Session()
    if scenario.local_ca:
        for session in session_list:
            session.verify = str(sslconfig.local_ca_file)

    all_threads = []
    with record_measure():
        for step in scenario.steps:
            all_threads += handlers[step.__class__](step, random.choice(session_list))
        for t in all_threads:
            t.join()
