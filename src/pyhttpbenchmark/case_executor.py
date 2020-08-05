import typing
import os
import tempfile
import pickle
import multiprocessing
import contextlib
import pstats

from . import metrics, model, case as case_module


spawn = multiprocessing.get_context("spawn")
forkserver = multiprocessing.get_context("forkserver")


def _read_measure(tempname: typing.Optional[str]) -> typing.Any:
    """Run in the main process"""
    if tempname:
        with open(tempname, "rb") as f:
            return pickle.load(f)
    return None


def _read_stats(tempname: typing.Optional[str]) -> typing.Optional[pstats.Stats]:
    """Run in the main process"""
    if tempname and os.path.getsize(tempname) > 0:
        stats = pstats.Stats()
        stats.load_stats(tempname)
        return stats
    return None


@contextlib.contextmanager
def tempfilename() -> typing.Generator[str, None, None]:
    fd, filename = tempfile.mkstemp()
    os.close(fd)
    try:
        yield filename
    finally:
        os.remove(filename)


@contextlib.contextmanager
def optional_tempfilename(enable=True) -> typing.Generator[typing.Optional[str], None, None]:
    if enable:
        with tempfilename() as filename:
            yield filename
    else:
        yield None


def start_and_join_process(process: typing.Union[multiprocessing.process.BaseProcess]) -> None:
    try:
        process.start()
        process.join(120.0)
        if process.exitcode == 0:
            return
        if process.exitcode is None:
            raise Exception(f"{process.name}: Timeout")
        if process.exitcode > 0:
            raise Exception(f"{process.name}: exitcode={process.exitcode}")
    finally:
        if process.is_alive():
            process.kill()
    raise Exception(f"{process.name}: error")


def run(case: model.LoadedCase, scenario: model.Scenario, record_profile: bool,
        sslconfig: model.SslConfig) -> typing.Tuple[metrics.Measure, typing.Optional[pstats.Stats]]:
    with tempfilename() as measure_filename:
        with optional_tempfilename(record_profile) as stats_filename:
            process_name = f"run_{scenario.id}_{case.full_name}"
            start_and_join_process(
                spawn.Process(name=process_name, target=case_module.run,
                              args=(measure_filename, stats_filename, case, scenario, sslconfig),
                              kwargs=dict(case.parameters)))
            measure = _read_measure(measure_filename)
            stats = _read_stats(stats_filename)
            return (measure, stats)


def parametrize(case: model.LoadedCase) -> typing.List[model.LoadedCase]:
    with tempfilename() as parameters_filename:
        process_name = f"getparam_{case.full_name}"
        start_and_join_process(
            forkserver.Process(name=process_name, target=case_module.get_parameters, args=(parameters_filename, case)))
        with open(parameters_filename, 'rb') as f:
            case_parameters_list = pickle.load(f)
    if type(case_parameters_list) != list:
        raise Exception('PARAMETERS is not a list')
    if len(case_parameters_list) == 0:
        return [case]
    return [model.LoadedCase(name=case.name, path=case.path, parameters=case_parameters)
            for case_parameters in case_parameters_list]
