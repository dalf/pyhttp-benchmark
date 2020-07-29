# pyhttp-benchmark
Micro-benchmarks on some very specify use-cases:
* simulate a [searx](https://github.com/asciimoo/searx) user request to different engines
* wait
* simulate a searx second user request

Each time the test runs inside a new spawn process with garbage collector stopped.
Use [time.perf_counter()](https://docs.python.org/3/library/time.html#time.perf_counter) and [time.process_time()](https://docs.python.org/3/library/time.html#time.process_time)

[requests](https://requests.readthedocs.io) test implementation is based on [searx/search.py](https://github.com/asciimoo/searx/blob/fc5d1c69cc01ec1c44e5d2d9644269b6b737fa5a/searx/search.py#L221-L239)

## Usage

```sh
pip install -r requirements.txt
./server/start.sh
```

In another terminal:
```sh
python main.py
```

## Results

### Scenario: Localhost, 8KB responses

| Test location: laptop           | Runtime |      |       | Cputime |      |       |
|---------------------------------|---------|------|-------|---------|------|-------|
|                                 |  median | mean | stdev |  median | mean | stdev |
| httpx                           |    1.45 | 1.46 |  0.02 |   0.18 |  0.18 |  0.05 |
| aiohttp                         |    1.52 | 1.52 |  0.03 |   0.08 |  0.08 |  0.02 |
| request (4 sessions)            |    1.55 | 1.55 |  0.04 |   0.19 |  0.19 |  0.04 |


### Scenario: Localhost, 400KB responses

| Test location: laptop           | Runtime |      |       | Cputime |      |       |
|---------------------------------|---------|------|-------|---------|------|-------|
|                                 |  median | mean | stdev |  median | mean | stdev |
| httpx                           |    1.46 | 1.47 |  0.06 |   0.33 |  0.33 |  0.16 |
| aiohttp                         |    1.52 | 1.53 |  0.06 |   0.12 |  0.13 |  0.06 |
| request (4 sessions)            |    1.55 | 1.55 |  0.04 |   0.24 |  0.26 |  0.09 |


### Scenario: Localhost, 100 requests at the same time

| Test location: laptop           | Runtime |      |       | Cputime |      |       |
|---------------------------------|---------|------|-------|---------|------|-------|
|                                 |  median | mean | stdev |  median | mean | stdev |
| httpx                           |    1.47 | 1.55 |  0.14 |   0.48 |  0.50 |  0.28 |
| aiohttp                         |    1.54 | 1.86 |  0.48 |   0.20 |  0.32 |  0.27 |
| request (4 sessions)            |    1.58 | 1.86 |  0.48 |   0.35 |  0.69 |  0.61 |

### Scenario: Real searx requests

| Test location: VPS              | Runtime |      |       | Cputime |      |       |
|---------------------------------|---------|------|-------|---------|------|-------|
|                                 |  median | mean | stdev |  median | mean | stdev |
| httpx                           |    1.02 | 1.03 |  0.13 |    0.11 | 0.11 |  0.01 |
| aiohttp                         |    0.99 | 1.06 |  0.29 |    0.06 | 0.06 |  0.01 |
| requests (4 sessions)           |    1.19 | 1.18 |  0.29 |    0.30 | 0.28 |  0.05 |

YMMV.
