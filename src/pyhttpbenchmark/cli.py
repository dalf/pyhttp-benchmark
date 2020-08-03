import typing
import pathlib
import os
import sys
import click
import hashlib
import pkg_resources
import subprocess

from . import scenarios, model, output, cases, main


CASES_DIR = pathlib.Path(cases.__file__).parent
CASE_NAMES = [
    os.path.splitext(filename)[0]
    for filename in os.listdir(CASES_DIR)
    if filename != "__init__.py" and filename != "__pycache__"
]
CASE_NAMES.sort()
FORMATTED_CASES = ", ".join(map(repr, CASE_NAMES))
CADDY_PATH = pathlib.Path.home() / ".cache/pyhttpbenchmark/bin/caddy"


@click.group()
@click.option('-o', '--output', 'output_dir', metavar='<directory>', default='.', help='Output directory')
@click.pass_context
def cli(ctx, output_dir) -> None:
    if output_dir == '.':
        output.OUTPUTDIR = pathlib.Path.cwd()
    else:
        output.OUTPUTDIR = pathlib.Path.cwd() / output_dir
    print("Output directory: %s" % output.OUTPUTDIR)


def name_from_script(path: pathlib.Path) -> str:
    """
    return an identifier made of the filename and hash of its content
    """
    with open(path, 'rb') as f:
        hsh = hashlib.sha256(f.read()).hexdigest()[:8]
    return f"{path.stem}_{hsh}"


def get_loaded_case(case_name: str) -> model.LoadedCase:
    if not case_name:
        raise click.BadArgumentUsage(
            f"Expected a case. Choose from {FORMATTED_CASES}, or pass a Python script."
        )

    if case_name.endswith(".py"):
        # Absolute case script.
        path = pathlib.Path(case_name)

        if not path.exists():
            raise click.BadArgumentUsage(
                f"Path to Python script {case_name!r} does not exist."
            )

        name = name_from_script(path)
        return model.LoadedCase(name=name, path=path)

    # Built-in case.
    if case_name not in CASE_NAMES:
        raise click.BadArgumentUsage(
            f"Unknown built-in case: {case_name!r}. Valid options: {FORMATTED_CASES}"
        )

    name = case_name
    path = CASES_DIR / f"{name}.py"
    assert path.exists()

    return model.LoadedCase(name=name, path=path)


def handle_case(ctx: click.Context, param: click.Parameter, value: str) -> model.LoadedCase:
    return get_loaded_case(value)


def handle_cases(ctx: click.Context, param: click.Parameter, value: str) -> typing.List[model.LoadedCase]:
    case_name_list = [case.strip() for case in value.split(',')]
    if len(case_name_list) == 1 and case_name_list[0] == '.':
        case_name_list = CASE_NAMES
    return [get_loaded_case(case_name) for case_name in case_name_list]


def get_scenario(scenario_name: str) -> model.Scenario:
    if not scenario_name:
        raise click.BadArgumentUsage(
            f"Expected a case. Choose from {FORMATTED_CASES}, or pass a Python script."
        )

    # Built-in scenarios.
    if scenario_name not in scenarios.SCENARIOS:
        raise click.BadArgumentUsage(
            f"Unknown built-in case: {scenario_name!r}. Valid options: {FORMATTED_CASES}"
        )

    return scenarios.SCENARIOS[scenario_name]


def handle_scenario(ctx: click.Context, param: click.Parameter, value: str) -> model.Scenario:
    return get_scenario(value)


def handle_scenarios(ctx: click.Context, param: click.Parameter, value: str) -> typing.List[model.Scenario]:
    scenario_name_list = [scenario.strip() for scenario in value.split(',')]
    if len(scenario_name_list) == 1 and scenario_name_list[0] == '.':
        scenario_name_list = [scenario.id for scenario in scenarios.SCENARIOS.values()]
    return [get_scenario(scenario_name) for scenario_name in scenario_name_list]


def autocompletion_case(ctx, args, incomplete):
    return [k for k in CASE_NAMES if incomplete in k]


def autocompletion_scenario(ctx, args, incomplete):
    return [k for k in scenarios.SCENARIOS.keys() if incomplete in k]


def autocompletion_list(choices, incomplete):
    items = incomplete.split(',')
    head = ','.join(items[:-1])
    if len(items) > 1:
        head += ','
    last = items[-1].strip()
    return [head + k for k in choices if last in k and last not in items[:-1]]


def autocompletion_case_list(ctx, args, incomplete):
    return autocompletion_list(['.'] + CASE_NAMES, incomplete)


def autocompletion_scenario_list(ctx, args, incomplete):
    return autocompletion_list(['.'] + list(scenarios.SCENARIOS.keys()), incomplete)


@cli.command()
@click.option('--profile/--no-profile', default=False)
@click.option('--csv/--no-csv', default=False)
@click.option("--tries", type=int, default=None)
@click.argument("case_list", callback=handle_cases, required=False, default='.',
                autocompletion=autocompletion_case_list)
@click.argument("scenario_list", callback=handle_scenarios, required=False, default='.',
                autocompletion=autocompletion_scenario_list)
def run(profile, csv, tries, case_list, scenario_list) -> None:
    config = model.Config(record_profile=profile, record_csv=csv, tries=tries)
    server_config = model.ServerConfig(
        caddy_path=output.get_file(CADDY_PATH),
        caddy_log_path=output.get_output_file("logs/caddy.log"),
        caddy_config_path=output.get_output_directory("config"))
    # intro
    print("## Versions\n")
    print("* %-30s %s" % ("Python", sys.version.replace("\n", "")))
    for pkg in ["aiohttp", "httpx", "requests", "uvloop", "trio"]:
        print("* %-30s %s" % (pkg, pkg_resources.get_distribution(pkg).version))
    if len(case_list) > 1 or len(scenario_list) > 1:
        print("\n## Context\n")
        print("* Cases: %s" % (', '.join([case.name for case in case_list])))
        print("* Scenarios: %s" % (', '.join([scenario.id for scenario in scenario_list])))
        print("* Tries: %s" % ("default" if tries is None else tries))
        print()

    # run
    main.run_scenario_list(case_list, scenario_list, config, server_config)


@cli.command()
@click.argument("case", callback=handle_case, autocompletion=autocompletion_case)
@click.argument("scenario", callback=handle_scenario, autocompletion=autocompletion_scenario)
def view(case: model.LoadedCase, scenario: model.Scenario) -> None:
    args = ["snakeviz", str(output.get_prof_file(scenario, case))]
    subprocess.run(args)


@cli.group()
def show():
    pass


@show.command(name='scenarios')
def show_scenarios():
    for scenario in scenarios.SCENARIOS.values():
        print("%-30s %3i %-120s" % (scenario.id, scenario.tries, scenario.name))


@show.command(name='cases')
def show_cases():
    for case_name in CASE_NAMES:
        case = handle_case(None, None, case_name)
        print("%-30s %-120s" % (case.name, case.path))
