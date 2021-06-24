import typing
import pathlib
import os
import sys
import click
import hashlib
import pkg_resources
import subprocess

from . import scenarios, model, output, cases, main, case_executor


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
    sys.stderr.write("Output directory: %s\n" % output.OUTPUTDIR)
    sys.stderr.flush()


def name_from_script(path: pathlib.Path) -> str:
    """
    return an identifier made of the filename and hash of its content
    """
    with open(path, 'rb') as f:
        hsh = hashlib.sha256(f.read()).hexdigest()[:8]
    return f"{path.stem}_{hsh}"


def get_loaded_case(case_name: str) -> typing.List[model.LoadedCase]:
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
        case = model.LoadedCase(name=name, path=path, parameters=frozenset())
        return case_executor.parametrize(case)

    # Built-in case
    base_case_name = None
    for c in CASE_NAMES:
        if case_name.startswith(c):
            base_case_name = c
            break
    else:
        raise click.BadArgumentUsage(
            f"Unknown built-in case: {case_name!r}. Valid options: {FORMATTED_CASES}"
        )

    path = CASES_DIR / f"{base_case_name}.py"
    assert path.exists()

    case = model.LoadedCase(name=base_case_name, path=path, parameters=frozenset())
    case_list = case_executor.parametrize(case)

    if case_name == base_case_name:
        return case_list
    else:
        for case in case_list:
            if case.full_name == case_name:
                return [case]
        else:
            raise click.BadArgumentUsage(
                f"Unknown built-in case: {case_name!r}. Valid options: {FORMATTED_CASES}"
            )


def handle_cases(ctx: click.Context, param: click.Parameter, value: str) -> typing.List[model.LoadedCase]:
    case_name_list = [case.strip() for case in value.split(',')]
    if len(case_name_list) == 1 and case_name_list[0] == '.':
        case_name_list = CASE_NAMES

    case_list = []
    for case_name in case_name_list:
        case_list += get_loaded_case(case_name)
    return case_list


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
@click.option('--png/--no-png', default=False)
@click.option("--tries", type=int, default=None)
@click.argument("case_list", callback=handle_cases, required=False, default='.',
                autocompletion=autocompletion_case_list)
@click.argument("scenario_list", callback=handle_scenarios, required=False, default='.',
                autocompletion=autocompletion_scenario_list)
def run(profile, csv, png, tries, case_list, scenario_list) -> None:
    config = model.Config(record_profile=profile, record_csv=csv, record_png=png, tries=tries)
    server_config = model.ServerConfig(
        caddy_path=output.get_file(CADDY_PATH),
        caddy_log_path=output.get_output_file("logs/caddy.log"),
        caddy_config_path=output.get_output_directory("config"))
    # intro
    print("## Versions\n")
    print("* %-30s %s" % ("Python", sys.version.replace("\n", "")))
    for pkg in ["aiohttp", "httpx", "httpcore", "requests", "uvloop", "trio", "curio", "anyio"]:
        print("* %-30s %s" % (pkg, pkg_resources.get_distribution(pkg).version))
    if len(case_list) > 1 or len(scenario_list) > 1:
        print("\n## Context\n")
        print("* Cases: %s" % (', '.join([case.full_name for case in case_list])))
        print("* Scenarios: %s" % (', '.join([scenario.id for scenario in scenario_list])))
        print("* Tries: %s" % ("default" if tries is None else tries))
        print()

    # run
    main.run_scenario_list(case_list, scenario_list, config, server_config)


@cli.command()
@click.argument("case_list", callback=handle_cases, autocompletion=autocompletion_case, metavar='CASE')
@click.argument("scenario", callback=handle_scenario, autocompletion=autocompletion_scenario)
def view(case_list: typing.List[model.LoadedCase], scenario: model.Scenario) -> None:
    if len(case_list) != 1:
        case_names = ', '.join([case.full_name for case in case_list])
        raise click.BadArgumentUsage(
                f"Require one case. Current list: {case_names}."
            )

    args = ["snakeviz", str(output.get_prof_file(scenario, case_list[0]))]
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
    case_list = []
    for case_name in CASE_NAMES:
        case_list += get_loaded_case(case_name)
    for case in case_list:
        print("%-30s %-120s" % (case.full_name, case.path))
