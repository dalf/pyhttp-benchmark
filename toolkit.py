import gc
import os
import inspect
import tempfile
import pickle
import logging
import contextlib
from contextlib import asynccontextmanager
import time
import multiprocessing
import statistics

spawn = multiprocessing.get_context("spawn")
stat_filename = None
stats = dict()


def print_stats():
    """Main process"""
    for test, stat in stats.items():
        median = statistics.median(stat)
        mean = statistics.mean(stat)
        stdev = statistics.stdev(stat)
        print("%-30s median: %.2fs  mean: %.2fs  stdev: %.2fs" % (test, median, mean, stdev))


def add_measure(measure):
    """Main process"""
    stat = stats.setdefault(measure[0], list())
    stat.append(measure[1])


def write_measure(test, runtime):
    """spawn process"""
    global stat_filename
    with open(stat_filename, 'wb') as f:
        measure = [ test,  runtime]
        f.write(pickle.dumps(measure))
        print("%-30s %.2f" % (measure[0], measure[1]))


@contextlib.contextmanager
def report_time(test):
    t0 = time.time()
    try:
        yield
    finally:
        write_measure(test, time.time() - t0)


@asynccontextmanager
async def async_report_time(test):
    t0 = time.time()
    try:
        yield
    finally:
        write_measure(test, time.time() - t0)


def wrapper_async(tempfile, co, *args):
    global stat_filename
    import asyncio
    import uvloop
    stat_filename = tempfile
    uvloop.install()
    loop = asyncio.get_event_loop()
    gc.disable()
    loop.run_until_complete(co(*args))
    gc.enable()


def wrapper_sync(tempfile, f, *args):
    global stat_filename
    stat_filename = tempfile
    gc.disable()
    f(*args)
    gc.enable()


def run(f, *args):
    global stats
    """
    Spawn a new Python process: no preexisting ssl connection.
    """
    if inspect.iscoroutinefunction(f):
        wrapper = wrapper_async
    else:
        wrapper = wrapper_sync

    fd, tempname = tempfile.mkstemp()
    p = spawn.Process(target=wrapper, args=[tempname, f, *args])
    p.start()
    p.join()

    import time
    time.sleep(1)

    with open(tempname, 'rb') as f:
        measure = pickle.load(f)
        add_measure(measure)

    os.remove(tempname)


__all__ = [ "report_time", "async_report_time", "run", "print_stats" ]