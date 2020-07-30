import typing
import pathlib
import os
from . import model


OUTPUTDIR = pathlib.Path.cwd()


def get_output_directory(relative_path: typing.Union[str, pathlib.Path], remove_files: bool = False) -> pathlib.Path:
    result = OUTPUTDIR / relative_path
    result.mkdir(parents=True, exist_ok=True)
    if remove_files:
        for filename in os.listdir(result):
            os.remove(result / filename)
    return result


def get_file(path: typing.Union[str, pathlib.Path]) -> pathlib.Path:
    if type(path) == str:
        path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_output_file(relative_path: typing.Union[str, pathlib.Path]) -> pathlib.Path:
    return get_file(OUTPUTDIR / relative_path)


def get_prof_file(scenario: model.Scenario, case: model.LoadedCase) -> pathlib.Path:
    return get_output_file("results") / f"{scenario.id}_{case.name}.prof"


def get_csv_file(scenario: model.Scenario) -> pathlib.Path:
    return get_output_file("results") / f"{scenario.id}.csv"
