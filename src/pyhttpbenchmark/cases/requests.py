import typing
import threading
import time

import requests

from .. import model
from ..case import record_measure


"""
requests
"""


def one_engine_request(session, url) -> None:
    session.get(url).content


def step_requests(step, session) -> typing.List[threading.Thread]:
    threads = []
    for url in step.urls:
        th_engine = threading.Thread(target=one_engine_request, args=(session, url))
        th_engine.start()
        threads.append(th_engine)
    return threads


def step_request(step, session) -> typing.List[threading.Thread]:
    one_engine_request(session, step.url)
    return []


def step_delay(step, session) -> typing.List[threading.Thread]:
    time.sleep(step.time)
    return []


handlers: typing.Dict[typing.Any, typing.Callable[[typing.Any, requests.Session], typing.List[threading.Thread]]] =\
    {model.StepRequests: step_requests, model.StepRequest: step_request, model.StepDelay: step_delay}


def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    session = requests.Session()
    if scenario.local_ca:
        session.verify = str(sslconfig.local_ca_file)

    with record_measure():
        threads = []
        for step in scenario.steps:
            threads += handlers[step.__class__](step, session)
        for th in threads:
            th.join()
