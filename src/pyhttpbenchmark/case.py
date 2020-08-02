import cProfile
import sys
import gc
import contextlib
import importlib
import inspect
import time
import pickle
from contextlib import asynccontextmanager

from .metrics import Measure
from . import model


MEASURE_FILENAME = None
STATS_FILENAME = None


def _save(runtime: int, cputime: int, pr) -> None:
    global STATS_FILENAME, MEASURE_FILENAME
    measure = Measure(runtime=runtime, cputime=cputime)
    if STATS_FILENAME:
        pr.dump_stats(STATS_FILENAME)
    with open(MEASURE_FILENAME, "wb") as f:
        f.write(pickle.dumps(measure))


@contextlib.contextmanager
def record_measure() -> None:
    """
    Record time (sync version)
    """
    global STATS_FILENAME
    pr = None
    if STATS_FILENAME:
        pr = cProfile.Profile()
        pr.enable()
    t0r = time.perf_counter()
    t0c = time.process_time()
    try:
        yield
    finally:
        runtime = time.perf_counter() - t0r
        cputime = time.process_time() - t0c
        if pr:
            pr.disable()
        _save(runtime, cputime, pr)


@asynccontextmanager
async def async_record_measure() -> None:
    """
    Record time (async version)
    """
    global STATS_FILENAME
    pr = None
    if STATS_FILENAME:
        pr = cProfile.Profile()
        pr.enable()
    t0r = time.perf_counter()
    t0c = time.process_time()
    try:
        yield
    finally:
        runtime = time.perf_counter() - t0r
        cputime = time.process_time() - t0c
        if pr:
            pr.disable()
        _save(runtime, cputime, pr)


@contextlib.contextmanager
def _no_gc() -> None:
    gc.collect()
    gc.disable()
    try:
        yield
    finally:
        gc.enable()


def _call_async_main(main, *args) -> None:
    import asyncio
    import uvloop

    uvloop.install()
    loop = asyncio.get_event_loop()
    with _no_gc():
        loop.run_until_complete(main(*args))


def _call_trio_main(main, *args) -> None:
    import trio

    with _no_gc():
        trio.run(main, *args)


def _call_sync_main(main, *args) -> None:
    with _no_gc():
        main(*args)


def _import_module(case: model.LoadedCase):
    # See: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    spec = importlib.util.spec_from_file_location(case.package_name, case.path)
    module_instance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_instance)  # type: ignore
    return module_instance  # type: ignore


def run(measure_filename: str, stats_filename: str, case: model.LoadedCase, scenario: model.Scenario, sslconfig: model.SslConfig) -> None:
    global MEASURE_FILENAME
    global STATS_FILENAME
    MEASURE_FILENAME = measure_filename
    STATS_FILENAME = stats_filename

    module = _import_module(case)
    main = module.main
    if not inspect.iscoroutinefunction(main):
        call_main = _call_sync_main
    elif 'trio' in sys.modules:
        call_main = _call_trio_main
    else:
        call_main = _call_async_main

    call_main(main, scenario, sslconfig)
