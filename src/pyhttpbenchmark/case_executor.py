import typing
import os
import tempfile
import pickle
import multiprocessing
import contextlib
import pstats

from . import metrics, model, case as case_module


spawn = multiprocessing.get_context("spawn")


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
def optional_tempfilename(enable=True) -> typing.Generator[typing.Optional[str], None, None]:
    filename = None
    if enable:
        _, filename = tempfile.mkstemp()
    try:
        yield filename
    finally:
        if filename:
            os.remove(filename)


def run(case: model.LoadedCase, scenario: model.Scenario, record_profile: bool,
        sslconfig: model.SslConfig) -> typing.Tuple[metrics.Measure, typing.Optional[pstats.Stats]]:
    """
    Spawn a new Python process
    """
    with optional_tempfilename() as measure_filename:
        with optional_tempfilename(record_profile) as stats_filename:
            process_name = f"run_{scenario.id}_{case.name}"
            process = spawn.Process(name=process_name, target=case_module.run,
                                    args=(measure_filename, stats_filename, case, scenario, sslconfig))
            try:
                process.start()
                process.join()
                if process.exitcode == 0:
                    measure = _read_measure(measure_filename)
                    stats = _read_stats(stats_filename)
                    return (measure, stats)
            finally:
                if process.is_alive():
                    process.kill()
    raise Exception("Error during run of " + str(case.path))
