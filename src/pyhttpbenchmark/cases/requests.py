import typing
import random
import threading
import time
from uuid import uuid4

import requests

from .. import scenarios
from .. import model
from ..case import record_measure


"""
requests (1 session)
"""


def one_engine_request(session: requests.Session, url: str) -> None:
    session.get(url).content


def one_user_request(session: requests.Session, urls: typing.List[str]) -> None:
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


def step_requests(step: model.Step, session: requests.Session) -> typing.List[threading.Thread]:
    t = threading.Thread(target=one_user_request, args=(session, step.urls))
    t.start()
    return [t]


def step_request(step: model.Step, session: requests.Session) -> typing.List[threading.Thread]:
    one_engine_request(session, step.url)
    return []


def step_delay(step: model.Step, session: requests.Session) -> typing.List[threading.Thread]:
    time.sleep(step.time)
    return []


handlers = {scenarios.StepDelay: step_delay, scenarios.StepRequests: step_requests, scenarios.StepRequest: step_request}


def main_partial(session_list: typing.List[requests.Session], scenario: scenarios.Scenario, sslconfig: model.SslConfig) -> None:
    if scenario.local_ca:
        for session in session_list:
            session.verify = sslconfig.local_ca_file

    all_threads = []
    with record_measure():
        for step in scenario.steps:
            all_threads += handlers[step.__class__](step, random.choice(session_list))
        for t in all_threads:
            t.join()


def main(scenario: scenarios.Scenario, sslconfig: model.SslConfig) -> None:
    session_list = [requests.Session()]
    main_partial(session_list, scenario, sslconfig)
