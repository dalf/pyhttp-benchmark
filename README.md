# pyhttp-benchmark
Micro-benchmarks of the Python HTTP clients. Heavily inspired by [httpxprof](https://github.com/florimondmanca/httpxprof).

Each test runs inside a new spawn process with garbage collector stopped. Use [time.perf_counter()](https://docs.python.org/3/library/time.html#time.perf_counter) and [time.process_time()](https://docs.python.org/3/library/time.html#time.process_time).

See:
* [List of scenarios](https://github.com/dalf/pyhttp-benchmark/blob/master/src/pyhttpbenchmark/scenarios.py)
* [List of cases](https://github.com/dalf/pyhttp-benchmark/tree/master/src/pyhttpbenchmark/cases)

The HTTPS server uses:
* [caddy](https://caddyserver.com/) (downloaded automatically in ```~/.cache/pyhttpbenchmark/bin/caddy```)
* a [starlette application](https://github.com/dalf/pyhttp-benchmark/blob/master/src/pyhttpbenchmark/server/app.py)

## Usage

In a virtualenv:
```sh
# install
pip install -e git+https://github.com/dalf/pyhttp-benchmark#egg=pyhttpbenchmark

# install shell completion
eval "$(_PYHTTPBENCHMARK_COMPLETE=source_bash pyhttpbenchmark )"

# run all cases, all scenarios
# output in the current directory
# it can be changed with the --output parameter
pyhttpbenchmark run . .
```

See the [output](output.md).

```sh
# display available cases and scenarios
pyhttpbenchmark show cases
pyhttpbenchmark show scenarios

# run some cases and some scenarios
pyhttpbenchmark run httpx,httpx_11 100_2seq_2kb,1_30seq_8kb_400ms

# run one case with one scenario
# record .prof, .csv files and create graph store as .png file (require matplotlib)
pyhttpbenchmark run --png --csv --profile httpx 1_100seq_1mb

# view .prof file using snakeviz
pyhttpbenchmark view httpx 1_100seq_1mb

# custom cases
wget https://gist.githubusercontent.com/dalf/cebb2032578151357b8c9ab2a320b51f/raw/dab40e925ced12738cc6f69c61b43a2d20f0c509/httpx_trio.py
wget https://gist.githubusercontent.com/dalf/cebb2032578151357b8c9ab2a320b51f/raw/7dbc414f53034d256f8063fc9da21dc94eefb65f/httpx_hack.py
cat httpx_trio.py
cat httpx_hack.py
pyhttpbenchmark run --tries 4 --profile ./httpx_trio.py,./httpx_hack.py,httpx,aiohttp 1_100seq_1mb
pyhttpbenchmark view ./httpx_hack.py 1_100seq_1mb
```
