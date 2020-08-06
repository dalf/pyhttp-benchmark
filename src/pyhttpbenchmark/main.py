import typing
import httpx

from tqdm import tqdm  # type: ignore

from . import model, server, metrics, case_executor


def warm_up_server(scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    if scenario.local_ca:
        urls = set()
        for step in scenario.steps:
            if isinstance(step, model.StepRequest):
                urls.add(step.url)
            elif isinstance(step, model.StepRequests):
                urls = urls | set(step.urls)

        client = httpx.Client(verify=str(sslconfig.local_ca_file))
        for url in tqdm(urls, leave=False, disable=None, desc="Warming up the local server"):
            response = client.get(url)
            response.raise_for_status()


def run_scenario(cases: typing.List[model.LoadedCase], scenario: model.Scenario,
                 config: model.Config, sslconfig: model.SslConfig) -> None:
    effective_tries = scenario.tries if config.tries is None else config.tries
    metric = metrics.Metrics()
    stats = metrics.Stats()
    print("\n## Scenario %s: %s\n" % (scenario.id, scenario.name))
    warm_up_server(scenario, sslconfig)
    for case in tqdm(cases * effective_tries, leave=False, disable=None, desc=scenario.id):
        try:
            measure, stat = case_executor.run(case, scenario, config.record_profile, sslconfig)
            metric.add(case, measure)
            stats.add(case, stat)
        except Exception as e:
            print(e)
    metric.print()
    if config.record_csv:
        metric.save(scenario)
    if config.record_png:
        metric.save_png(scenario)
    if config.record_profile:
        stats.save(scenario)


def run_scenario_list(cases: typing.List[model.LoadedCase], scenario_list: typing.List[model.Scenario],
                      config: model.Config, server_config: model.ServerConfig) -> None:
    for scenario in scenario_list:
        with server.server(server_config, "localhost", list(range(4001, 4011))) as sslconfig:
            run_scenario(cases, scenario, config, sslconfig)
