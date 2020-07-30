import typing
import pathlib
import os
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
    hsh = hashlib.md5(str(path).encode()).hexdigest()
    return f"{path.stem}_{hsh}"


def handle_case(ctx: click.Context, param: click.Parameter, value: str) -> model.LoadedCase:
    if not value:
        raise click.BadArgumentUsage(
            f"Expected a case. Choose from {FORMATTED_CASES}, or pass a Python script."
        )

    if value.endswith(".py"):
        # Absolute case script.
        path = pathlib.Path(value)

        if not path.exists():
            raise click.BadArgumentUsage(
                f"Path to Python script {value!r} does not exist."
            )

        name = name_from_script(path)
        return model.LoadedCase(name=name, path=path)

    # Built-in case.
    if value not in CASE_NAMES:
        raise click.BadArgumentUsage(
            f"Unknown built-in case: {value!r}. Valid options: {FORMATTED_CASES}"
        )

    name = value
    path = CASES_DIR / f"{name}.py"
    assert path.exists()

    return model.LoadedCase(name=name, path=path)


def handle_cases(ctx: click.Context, param: click.Parameter, value: str) -> typing.List[model.LoadedCase]:
    case_name_list = [case.strip() for case in value.split(',')]
    if len(case_name_list) == 1 and case_name_list[0] == '.':
        case_name_list = CASE_NAMES
    return [handle_case(None, None, case_name) for case_name in case_name_list]


def handle_scenario(ctx: click.Context, param: click.Parameter, value: str):
    if not value:
        raise click.BadArgumentUsage(
            f"Expected a case. Choose from {FORMATTED_CASES}, or pass a Python script."
        )

    # Built-in scenarios.
    if value not in scenarios.SCENARIOS:
        raise click.BadArgumentUsage(
            f"Unknown built-in case: {value!r}. Valid options: {FORMATTED_CASES}"
        )

    return scenarios.SCENARIOS[value]


def handle_scenarios(ctx: click.Context, param: click.Parameter, value: str) -> typing.List[model.Scenario]:
    scenario_name_list = [scenario.strip() for scenario in value.split(',')]
    if len(scenario_name_list) == 1 and scenario_name_list[0] == '.':
        scenario_name_list = [scenario.id for scenario in scenarios.SCENARIOS.values()]
    return [handle_scenario(None, None, scenario_name) for scenario_name in scenario_name_list]


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
@click.argument("case_list", callback=handle_cases, required=False, default='.', autocompletion=autocompletion_case_list)
@click.argument("scenario_list", callback=handle_scenarios, required=False, default='.', autocompletion=autocompletion_scenario_list)
def run(profile, csv, tries, case_list, scenario_list) -> None:
    config = model.Config(record_profile=profile, record_csv=csv, tries=tries)
    server_config = model.ServerConfig(
        caddy_path=output.get_file(pathlib.Path.home() / ".cache/pyhttpbenchmark/bin/caddy"),
        caddy_log_path=output.get_output_file("logs/caddy.log"))
    # intro
    print("## Package versions\n")
    for pkg in ["aiohttp", "httpx", "requests"]:
        print("* %-30s %s" % (pkg, pkg_resources.get_distribution(pkg).version))
    if len(case_list) > 1 and len(scenario_list) > 1:
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
