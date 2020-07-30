# pyhttp-benchmark
Micro-benchmarks on some very specify use-cases heavily inspired by [httpxprof](https://github.com/florimondmanca/httpxprof).

Each time the test runs inside a new spawn process with garbage collector stopped.
Use [time.perf_counter()](https://docs.python.org/3/library/time.html#time.perf_counter) and [time.process_time()](https://docs.python.org/3/library/time.html#time.process_time).

[requests](https://github.com/dalf/pyhttp-benchmark/blob/master/src/pyhttpbenchmark/cases/requests.py) test implementation is based on [searx/search.py](https://github.com/asciimoo/searx/blob/fc5d1c69cc01ec1c44e5d2d9644269b6b737fa5a/searx/search.py#L221-L239)

Test against a local server:
* [caddy](https://caddyserver.com/) to provide a HTTPS server (downloaded automatically in ```~/.cache/pyhttpbenchmark/bin/caddy```)
* [starlette application](https://github.com/dalf/pyhttp-benchmark/blob/master/src/pyhttpbenchmark/server/app.py)

## Usage

In a virtualenv:
```sh
# install
pip install -e git+https://github.com/dalf/pyhttp-benchmark#egg=pyhttpbenchmark

# install shell completion
eval "$(_PYHTTPBENCHMARK_COMPLETE=source_bash pyhttpbenchmark )"

# run all cases, all scenarios
pyhttpbenchmark run . .
```

See the [output](output.md).

```sh
# display available cases and scenarios
pyhttpbenchmark run cases
pyhttpbenchmark run scenarios

# run some cases and some scenarios
pyhttpbenchmark run httpx,httpx_11 100_2seq_2kb,1_30seq_8kb_400ms

# run one case with one scenario, record .prof file
pyhttpbenchmark run --profile httpx 1_100seq_1mb

# view
pyhttpbenchmark view httpx 1_100seq_1mb
```
