# pyhttp-benchmark
Micro-benchmark on one very specify use-case:
* simulate a [searx](https://github.com/asciimoo/searx) user request to different engines
* wait 500ms
* simulate a searx second user request

Each time the test runs inside a new spawn process with garbage collector stopped.
Use [time.perf_counter()](https://docs.python.org/3/library/time.html#time.perf_counter) and [time.process_time()](https://docs.python.org/3/library/time.html#time.process_time)

[requests](https://requests.readthedocs.io) test implementation is based on [searx/search.py](https://github.com/asciimoo/searx/blob/fc5d1c69cc01ec1c44e5d2d9644269b6b737fa5a/searx/search.py#L221-L239)

## Results

|                       | Runtime |      |       | Cputime |      |       |
|-----------------------|---------|------|-------|---------|------|-------|
|                       |  median | mean | stdev |  median | mean | stdev |
| httpx                 |    1.02 | 1.03 |  0.13 |    0.11 | 0.11 |  0.01 |
| aiohttp               |    0.99 | 1.06 |  0.29 |    0.06 | 0.06 |  0.01 |
| requests (4 sessions) |    1.19 | 1.18 |  0.29 |    0.30 | 0.28 |  0.05 |

YMMV.
