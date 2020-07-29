import gc
import os
import inspect
import tempfile
import pickle
import time
import multiprocessing
import statistics
import contextlib
from contextlib import asynccontextmanager

__all__ = ["report_time", "async_report_time", "run", "print_stats"]
spawn = multiprocessing.get_context("spawn")
STAT_FILENAME = None
STATS = dict()


def print_stats():
    """
    Print the statistics recorded by report_time and async_report_time

    Run in the main process
    """
    for test, stat in STATS.items():
        runtime = list(map(lambda s: s[0], stat))
        cputime = list(map(lambda s: s[1], stat))

        runtime_median = statistics.median(runtime)
        runtime_mean = statistics.mean(runtime)
        runtime_stdev = statistics.stdev(runtime)

        cputime_median = statistics.median(cputime)
        cputime_mean = statistics.mean(cputime)
        cputime_stdev = statistics.stdev(cputime)
        print("%-30s runtime[ median: %.2fs  mean: %.2fs  stdev: %.2fs ] cputime[ median: %.2fs  mean: %.2fs  stdev: %.2fs ]" % (test, runtime_median, runtime_mean, runtime_stdev, cputime_median, cputime_mean, cputime_stdev))


def _read_and_add_measure(tempname, print_prefix=""):
    """Run in the main process"""
    with open(tempname, 'rb') as f:
        measure = pickle.load(f)
        stat = STATS.setdefault(measure[0], list())
        stat.append((measure[1], measure[2]))
        print("%-10s %-30s runtime: %.2f cputime: %.2f" % (print_prefix, measure[0], measure[1], measure[2]))


def _write_measure(test, runtime, cputime):
    """Run a spawn process"""
    global STAT_FILENAME
    with open(STAT_FILENAME, 'wb') as f:
        measure = [test, runtime, cputime]
        f.write(pickle.dumps(measure))


@contextlib.contextmanager
def report_time(test):
    """
    Record time (sync version)

    Run a spawn process
    """

    t0r = time.perf_counter()
    t0c = time.process_time()
    try:
        yield
    finally:
        _write_measure(test, time.perf_counter() - t0r, time.process_time() - t0c)


@asynccontextmanager
async def async_report_time(test):
    """
    Record time (async version)

    Run a spawn process
    """

    t0r = time.perf_counter()
    t0c = time.process_time()
    try:
        yield
    finally:
        _write_measure(test, time.perf_counter() - t0r, time.process_time() - t0c)


def _wrapper_async(stat_filename, co, *args):
    """
    Bootstrap an async function in a spawn process
    """
    global STAT_FILENAME
    import asyncio
    import uvloop
    STAT_FILENAME = stat_filename
    uvloop.install()
    loop = asyncio.get_event_loop()
    gc.collect()
    gc.disable()
    loop.run_until_complete(co(*args))
    gc.enable()


def _wrapper_sync(stat_filename, f, *args):
    """
    Bootstrap a sync function in a spawn process
    """
    global STAT_FILENAME
    STAT_FILENAME = stat_filename
    gc.collect()
    gc.disable()
    f(*args)
    gc.enable()


def run(func, *args, print_prefix=""):
    """
    Spawn a new Python process: no preexisting ssl connection.
    """
    global STATS
    _, stat_filename = tempfile.mkstemp()
    try:
        wrapper = _wrapper_async if inspect.iscoroutinefunction(func) else _wrapper_sync
        process = spawn.Process(target=wrapper, args=[stat_filename, func, *args])
        try:
            process.start()
            process.join()
            if process.exitcode == 0:
                _read_and_add_measure(stat_filename, print_prefix=print_prefix)
        finally:
            if process.is_alive():
                process.kill()
    finally:
        os.remove(stat_filename)
