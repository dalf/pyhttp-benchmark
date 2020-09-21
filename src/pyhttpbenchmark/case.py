import typing
import cProfile
import sys
import gc
import contextlib
import importlib
import inspect
import time
import pickle

if not sys.version_info.major == 3 and sys.version_info.minor >= 7:
    from contextlib import asynccontextmanager
else:
    from .contextlib import asynccontextmanager  # type: ignore

from .metrics import Measure
from . import model


MEASURE_FILENAME = None
STATS_FILENAME = None


def _save(runtime: float, cputime: float, pr) -> None:
    global STATS_FILENAME, MEASURE_FILENAME
    measure = Measure(runtime=runtime, cputime=cputime)
    if STATS_FILENAME:
        pr.dump_stats(STATS_FILENAME)
    if MEASURE_FILENAME:
        with open(MEASURE_FILENAME, "wb") as f:
            f.write(pickle.dumps(measure))


@contextlib.contextmanager
def record_measure() -> typing.Iterator[None]:
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
async def async_record_measure() -> typing.AsyncGenerator[None, None]:
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
def _no_gc() -> typing.Generator[None, None, None]:
    gc.collect()
    gc.disable()
    try:
        yield
    finally:
        gc.enable()


def _call_async_main(main, *args, **kwargs) -> None:
    import asyncio
    import uvloop  # type: ignore

    uvloop.install()
    loop = asyncio.get_event_loop()
    with _no_gc():
        loop.run_until_complete(main(*args, **kwargs))


def _call_trio_main(main, *args, **kwargs) -> None:
    import trio  # type: ignore

    async def main_args_kwargs():
        await main(*args, **kwargs)

    with _no_gc():
        trio.run(main_args_kwargs)


def _call_curio_main(main, *args, **kwargs) -> None:
    import curio

    async def main_args_kwargs():
        await main(*args, **kwargs)

    curio.run(main_args_kwargs, with_monitor=True)


def _call_sync_main(main, *args, **kwargs) -> None:
    with _no_gc():
        main(*args, **kwargs)


def _import_module(case: model.LoadedCase):
    # See: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    spec = importlib.util.spec_from_file_location(case.package_name, case.path)  # type: ignore
    module_instance = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module_instance)  # type: ignore
    return module_instance  # type: ignore


def run(measure_filename: str, stats_filename: str, case: model.LoadedCase, scenario: model.Scenario,
        sslconfig: model.SslConfig, **kwargs) -> None:
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
    elif 'curio' in sys.modules:
        call_main = _call_curio_main
    else:
        call_main = _call_async_main

    call_main(main, scenario, sslconfig, **kwargs)


def get_parameters(parameter_filename: str, case: model.LoadedCase):
    parameters_list = []

    module = _import_module(case)
    get_parameters = inspect.getattr_static(module, 'get_parameters', None)
    if get_parameters:
        parameters = get_parameters()
        names = [name.strip() for name in parameters[0].split(',')]
        for values in parameters[1]:
            case_parameter = dict()
            for i, name in enumerate(names):
                case_parameter[name] = values[i]
            parameters_list.append(frozenset(case_parameter.items()))

    with open(parameter_filename, 'wb') as f:
        f.write(pickle.dumps(parameters_list))
