import typing
import httpx

from tqdm import tqdm

from . import model, server, metrics, case_executor


def warm_up_server(scenario_list: typing.List[model.Scenario], sslconfig: model.SslConfig) -> None:
    urls = set()
    for scenario in scenario_list:
        if scenario.local_ca:
            for step in scenario.steps:
                if isinstance(step, model.StepRequest):
                    urls.add(step.url)
                elif isinstance(step, model.StepRequests):
                    urls = urls | set(step.urls)

    client = httpx.Client(verify=sslconfig.local_ca_file)
    for url in tqdm(urls, leave=False, disable=None, desc="Warming up the local server"):
        response = client.get(url)
        response.raise_for_status()


def run_scenario(cases: typing.List[model.LoadedCase], scenario: model.Scenario,
                 config: model.Config, sslconfig: model.SslConfig) -> None:
    effective_tries = scenario.tries if config.tries is None else config.tries
    metric = metrics.Metrics()
    stats = metrics.Stats()
    print("\n## Scenario %s: %s\n" % (scenario.id, scenario.name))
    for case in tqdm(cases * effective_tries, leave=False, disable=None):
        measure, stat = case_executor.run(case, scenario, config.record_profile, sslconfig)
        metric.add(case, measure)
        stats.add(case, stat)
    metric.print()
    if config.record_csv:
        metric.save(scenario)
    if config.record_profile:
        stats.save(scenario)


def run_scenario_list(cases: typing.List[model.LoadedCase], scenario_list: typing.List[model.Scenario],
                      config: model.Config, server_config: model.ServerConfig) -> None:
    with server.server(server_config) as sslconfig:
        warm_up_server(scenario_list, sslconfig)
        for scenario in scenario_list:
            run_scenario(cases, scenario, config, sslconfig)
