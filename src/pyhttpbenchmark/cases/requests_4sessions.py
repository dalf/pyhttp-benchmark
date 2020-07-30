import requests
from .. import model
from . import requests as case_requests


"""
requests (4 session)

in the case of a WSGI application which sends HTTP requests,
it is not possible to have common pool.
this case uses 4 differents requests.Session to simulate this behavior.
"""


def main(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    session_list = [requests.Session(), requests.Session(), requests.Session(), requests.Session()]
    case_requests.main_partial(session_list, scenario, sslconfig)
