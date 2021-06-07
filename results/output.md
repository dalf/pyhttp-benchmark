## Versions

* Python                         3.9.5 (default, Jun  7 2021, 19:22:50) [GCC 8.3.0]
* aiohttp                        3.7.4.post0
* httpx                          0.18.1
* httpcore                       0.13.3
* requests                       2.25.1
* uvloop                         0.15.2
* trio                           0.18.0
* curio                          1.5

## Context

* Cases: aiohttp, httpcore_curio_True, httpcore_curio_False, httpcore_trio_True, httpcore_trio_False, httpcore_uvloop_True, httpcore_uvloop_False, httpx_uvloop_True, httpx_uvloop_False, requests_1, requests_4
* Scenarios: external_p6_t5_p6, p6-8-5_t5_p6-8-5, p6-400-5_t5_p6-400-5, p100-2-5_t5_p100-2-5, s100_1_0, s100_2_0, s100_256_0, s100_1024_0, s30_8_4, p100_2048_5_t20_p100_2048_5, p60_1024_5
* Tries: default

Downloading https://github.com/caddyserver/caddy/releases/download/v2.1.1/caddy_2.1.1_linux_amd64.tar.gz 
 to /home/alexandre/.cache/pyhttpbenchmark/bin/caddy

## Scenario external_p6_t5_p6: External requests: Two sequences of searx requests, 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.16 |    1.21 |    0.21 |    0.04 |    0.04 |    0.00 |
| httpcore_curio_True              |    1.23 |    1.21 |    0.15 |    0.10 |    0.09 |    0.00 |
| httpcore_curio_False             |    1.36 |    1.32 |    0.15 |    0.06 |    0.06 |    0.00 |
| httpcore_trio_True               |    1.10 |    1.12 |    0.13 |    0.11 |    0.11 |    0.00 |
| httpcore_trio_False              |    1.35 |    1.27 |    0.15 |    0.08 |    0.08 |    0.00 |
| httpcore_uvloop_True             |    1.31 |    1.30 |    0.28 |    0.08 |    0.08 |    0.00 |
| httpcore_uvloop_False            |    1.36 |    1.26 |    0.17 |    0.04 |    0.04 |    0.00 |
| httpx_uvloop_True                |    1.10 |    1.12 |    0.17 |    0.09 |    0.09 |    0.00 |
| httpx_uvloop_False               |    1.35 |    1.29 |    0.14 |    0.06 |    0.06 |    0.00 |
| requests_1                       |    1.16 |    1.17 |    0.18 |    0.16 |    0.16 |    0.00 |
| requests_4                       |    1.18 |    1.23 |    0.19 |    0.19 |    0.19 |    0.04 |

![external_p6_t5_p6](external_p6_t5_p6.png)


## Scenario p6-8-5_t5_p6-8-5: Two sequences of 6 requests with a 8KB responses (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.42 |    1.42 |    0.00 |    0.03 |    0.03 |    0.00 |
| httpcore_curio_True              |    1.41 |    1.41 |    0.00 |    0.07 |    0.07 |    0.00 |
| httpcore_curio_False             |    1.46 |    1.46 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpcore_trio_True               |    1.41 |    1.41 |    0.00 |    0.08 |    0.08 |    0.00 |
| httpcore_trio_False              |    1.43 |    1.43 |    0.00 |    0.07 |    0.07 |    0.00 |
| httpcore_uvloop_True             |    1.41 |    1.41 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpcore_uvloop_False            |    1.42 |    1.42 |    0.00 |    0.03 |    0.03 |    0.00 |
| httpx_uvloop_True                |    1.41 |    1.41 |    0.00 |    0.07 |    0.07 |    0.00 |
| httpx_uvloop_False               |    1.42 |    1.42 |    0.00 |    0.05 |    0.05 |    0.00 |
| requests_1                       |    1.43 |    1.43 |    0.00 |    0.07 |    0.07 |    0.00 |
| requests_4                       |    1.43 |    1.43 |    0.00 |    0.07 |    0.07 |    0.00 |

![p6-8-5_t5_p6-8-5](p6-8-5_t5_p6-8-5.png)


## Scenario p6-400-5_t5_p6-400-5: Two sequences of 6 requests with a 400KB responses (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.42 |    1.42 |    0.00 |    0.07 |    0.07 |    0.00 |
| httpcore_curio_True              |    1.42 |    1.42 |    0.00 |    0.22 |    0.22 |    0.00 |
| httpcore_curio_False             |    1.47 |    1.47 |    0.01 |    0.13 |    0.13 |    0.00 |
| httpcore_trio_True               |    1.43 |    1.43 |    0.00 |    0.24 |    0.24 |    0.01 |
| httpcore_trio_False              |    1.44 |    1.44 |    0.00 |    0.18 |    0.18 |    0.00 |
| httpcore_uvloop_True             |    1.42 |    1.42 |    0.00 |    0.12 |    0.12 |    0.00 |
| httpcore_uvloop_False            |    1.42 |    1.42 |    0.00 |    0.07 |    0.07 |    0.00 |
| httpx_uvloop_True                |    1.42 |    1.42 |    0.00 |    0.15 |    0.15 |    0.00 |
| httpx_uvloop_False               |    1.43 |    1.43 |    0.00 |    0.12 |    0.12 |    0.00 |
| requests_1                       |    1.43 |    1.43 |    0.00 |    0.13 |    0.13 |    0.00 |
| requests_4                       |    1.43 |    1.43 |    0.00 |    0.13 |    0.13 |    0.00 |

![p6-400-5_t5_p6-400-5](p6-400-5_t5_p6-400-5.png)


## Scenario p100-2-5_t5_p100-2-5: Two sequences of 100 parallel requests (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.96 |    1.96 |    0.03 |    0.30 |    0.29 |    0.00 |
| httpcore_curio_True              |    1.47 |    1.47 |    0.01 |    0.34 |    0.34 |    0.01 |
| httpcore_curio_False             |    1.64 |    1.64 |    0.01 |    0.58 |    0.58 |    0.01 |
| httpcore_trio_True               |    1.48 |    1.48 |    0.01 |    0.46 |    0.45 |    0.01 |
| httpcore_trio_False              |    1.63 |    1.63 |    0.00 |    0.64 |    0.64 |    0.01 |
| httpcore_uvloop_True             |    1.47 |    1.48 |    0.01 |    0.22 |    0.23 |    0.01 |
| httpcore_uvloop_False            |    1.60 |    1.60 |    0.01 |    0.38 |    0.38 |    0.00 |
| httpx_uvloop_True                |    1.50 |    1.50 |    0.01 |    0.38 |    0.37 |    0.01 |
| httpx_uvloop_False               |    1.95 |    1.96 |    0.02 |    0.66 |    0.66 |    0.01 |
| requests_1                       |    1.68 |    1.68 |    0.01 |    0.83 |    0.83 |    0.01 |
| requests_4                       |    1.73 |    1.72 |    0.03 |    0.89 |    0.88 |    0.02 |

![p100-2-5_t5_p100-2-5](p100-2-5_t5_p100-2-5.png)


## Scenario s100_1_0: 100 sequential requests, 1 byte response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.17 |    0.17 |    0.01 |    0.07 |    0.07 |    0.00 |
| httpcore_curio_True              |    0.29 |    0.28 |    0.01 |    0.18 |    0.18 |    0.01 |
| httpcore_curio_False             |    0.24 |    0.24 |    0.00 |    0.12 |    0.12 |    0.00 |
| httpcore_trio_True               |    0.33 |    0.33 |    0.01 |    0.24 |    0.24 |    0.01 |
| httpcore_trio_False              |    0.21 |    0.21 |    0.01 |    0.14 |    0.14 |    0.00 |
| httpcore_uvloop_True             |    0.27 |    0.28 |    0.01 |    0.15 |    0.15 |    0.01 |
| httpcore_uvloop_False            |    0.19 |    0.19 |    0.01 |    0.09 |    0.09 |    0.01 |
| httpx_uvloop_True                |    0.35 |    0.36 |    0.01 |    0.24 |    0.24 |    0.01 |
| httpx_uvloop_False               |    0.22 |    0.22 |    0.01 |    0.14 |    0.14 |    0.01 |
| requests_1                       |    0.28 |    0.28 |    0.01 |    0.17 |    0.18 |    0.01 |
| requests_4                       |    0.33 |    0.33 |    0.03 |    0.20 |    0.20 |    0.02 |

![s100_1_0](s100_1_0.png)


## Scenario s100_2_0: 100 sequential requests, 2KB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.18 |    0.18 |    0.01 |    0.07 |    0.08 |    0.01 |
| httpcore_curio_True              |    0.29 |    0.29 |    0.02 |    0.18 |    0.18 |    0.01 |
| httpcore_curio_False             |    0.24 |    0.24 |    0.00 |    0.12 |    0.12 |    0.00 |
| httpcore_trio_True               |    0.33 |    0.33 |    0.01 |    0.24 |    0.24 |    0.01 |
| httpcore_trio_False              |    0.20 |    0.20 |    0.00 |    0.14 |    0.14 |    0.00 |
| httpcore_uvloop_True             |    0.28 |    0.28 |    0.02 |    0.15 |    0.15 |    0.01 |
| httpcore_uvloop_False            |    0.19 |    0.19 |    0.01 |    0.09 |    0.09 |    0.01 |
| httpx_uvloop_True                |    0.38 |    0.37 |    0.01 |    0.25 |    0.25 |    0.01 |
| httpx_uvloop_False               |    0.24 |    0.24 |    0.01 |    0.15 |    0.15 |    0.01 |
| requests_1                       |    0.30 |    0.30 |    0.01 |    0.19 |    0.19 |    0.01 |
| requests_4                       |    0.34 |    0.33 |    0.02 |    0.20 |    0.20 |    0.01 |

![s100_2_0](s100_2_0.png)


## Scenario s100_256_0: 100 sequential requests, 256KB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.52 |    0.55 |    0.14 |    0.23 |    0.23 |    0.01 |
| httpcore_curio_True              |    0.99 |    0.98 |    0.07 |    0.79 |    0.79 |    0.02 |
| httpcore_curio_False             |    0.81 |    0.95 |    0.57 |    0.36 |    0.37 |    0.05 |
| httpcore_trio_True               |    1.01 |    1.03 |    0.07 |    0.90 |    0.89 |    0.02 |
| httpcore_trio_False              |    1.20 |    1.36 |    0.67 |    0.57 |    0.59 |    0.08 |
| httpcore_uvloop_True             |    0.51 |    0.52 |    0.06 |    0.36 |    0.36 |    0.01 |
| httpcore_uvloop_False            |    1.66 |    1.63 |    0.54 |    0.29 |    0.29 |    0.02 |
| httpx_uvloop_True                |    1.21 |    1.14 |    0.23 |    0.58 |    0.58 |    0.02 |
| httpx_uvloop_False               |    0.87 |    1.02 |    0.39 |    0.45 |    0.45 |    0.04 |
| requests_1                       |    0.75 |    0.78 |    0.23 |    0.36 |    0.37 |    0.03 |
| requests_4                       |    0.70 |    0.67 |    0.21 |    0.38 |    0.37 |    0.04 |

![s100_256_0](s100_256_0.png)


## Scenario s100_1024_0: 100 sequential requests, 1MB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.00 |    1.00 |    0.20 |    0.60 |    0.60 |    0.01 |
| httpcore_curio_True              |    2.94 |    3.00 |    0.26 |    2.33 |    2.34 |    0.06 |
| httpcore_curio_False             |    1.21 |    1.37 |    0.39 |    1.01 |    1.02 |    0.04 |
| httpcore_trio_True               |    2.91 |    3.05 |    0.30 |    2.70 |    2.71 |    0.05 |
| httpcore_trio_False              |    1.74 |    1.92 |    0.37 |    1.55 |    1.55 |    0.04 |
| httpcore_uvloop_True             |    1.31 |    1.40 |    0.30 |    0.96 |    0.96 |    0.02 |
| httpcore_uvloop_False            |    1.20 |    1.24 |    0.40 |    0.61 |    0.62 |    0.02 |
| httpx_uvloop_True                |    1.87 |    1.94 |    0.36 |    1.36 |    1.35 |    0.04 |
| httpx_uvloop_False               |    1.41 |    1.45 |    0.18 |    1.10 |    1.09 |    0.02 |
| requests_1                       |    1.23 |    1.25 |    0.15 |    0.94 |    0.93 |    0.02 |
| requests_4                       |    1.25 |    1.40 |    0.45 |    0.93 |    0.94 |    0.03 |

![s100_1024_0](s100_1024_0.png)


## Scenario s30_8_4: One sequence of 30 requests, 8KB response, 400ms delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.46 |    0.46 |    0.02 |    0.05 |    0.05 |    0.00 |
| httpcore_curio_True              |    0.50 |    0.50 |    0.00 |    0.06 |    0.06 |    0.00 |
| httpcore_curio_False             |    0.52 |    0.52 |    0.00 |    0.10 |    0.10 |    0.00 |
| httpcore_trio_True               |    0.46 |    0.46 |    0.00 |    0.07 |    0.07 |    0.00 |
| httpcore_trio_False              |    0.48 |    0.48 |    0.00 |    0.12 |    0.12 |    0.00 |
| httpcore_uvloop_True             |    0.44 |    0.44 |    0.00 |    0.04 |    0.04 |    0.00 |
| httpcore_uvloop_False            |    0.46 |    0.46 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpx_uvloop_True                |    0.46 |    0.46 |    0.01 |    0.07 |    0.07 |    0.00 |
| httpx_uvloop_False               |    0.46 |    0.46 |    0.01 |    0.09 |    0.09 |    0.00 |
| requests_1                       |    0.50 |    0.50 |    0.00 |    0.16 |    0.16 |    0.00 |
| requests_4                       |    0.50 |    0.50 |    0.00 |    0.16 |    0.16 |    0.00 |

![s30_8_4](s30_8_4.png)


## Scenario p100_2048_5_t20_p100_2048_5: 2 sequences of 100 requests, between 2KB and 2MB responses (various delays), 2s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    3.04 |    3.04 |    0.00 |    0.75 |    0.75 |    0.01 |
| httpcore_curio_True              |    3.58 |    3.58 |    0.01 |    2.48 |    2.48 |    0.03 |
| httpcore_curio_False             |    3.08 |    3.08 |    0.00 |    1.28 |    1.28 |    0.01 |
| httpcore_trio_True               |    3.69 |    3.69 |    0.01 |    2.73 |    2.74 |    0.02 |
| httpcore_trio_False              |    3.16 |    3.16 |    0.00 |    1.74 |    1.73 |    0.01 |
| httpcore_uvloop_True             |    3.11 |    3.11 |    0.00 |    1.05 |    1.05 |    0.01 |
| httpcore_uvloop_False            |    3.04 |    3.04 |    0.01 |    0.74 |    0.74 |    0.01 |
| httpx_uvloop_True                |    3.25 |    3.25 |    0.01 |    1.60 |    1.60 |    0.01 |
| httpx_uvloop_False               |    3.14 |    3.14 |    0.01 |    1.42 |    1.42 |    0.01 |
| requests_1                       |    3.09 |    3.09 |    0.01 |    1.61 |    1.60 |    0.02 |
| requests_4                       |    3.20 |    3.17 |    0.05 |    1.71 |    1.69 |    0.05 |

![p100_2048_5_t20_p100_2048_5](p100_2048_5_t20_p100_2048_5.png)


## Scenario p60_1024_5: 60 requests, 1MB response (various delays)

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.06 |    1.06 |    0.01 |    0.41 |    0.41 |    0.01 |
| httpcore_curio_True              |    1.77 |    1.77 |    0.01 |    1.39 |    1.39 |    0.01 |
| httpcore_curio_False             |    1.16 |    1.16 |    0.01 |    0.69 |    0.69 |    0.01 |
| httpcore_trio_True               |    1.87 |    1.87 |    0.01 |    1.51 |    1.51 |    0.01 |
| httpcore_trio_False              |    1.23 |    1.23 |    0.01 |    0.95 |    0.95 |    0.01 |
| httpcore_uvloop_True             |    1.04 |    1.04 |    0.00 |    0.56 |    0.57 |    0.01 |
| httpcore_uvloop_False            |    1.06 |    1.06 |    0.01 |    0.38 |    0.39 |    0.00 |
| httpx_uvloop_True                |    1.26 |    1.26 |    0.01 |    0.88 |    0.88 |    0.01 |
| httpx_uvloop_False               |    1.06 |    1.06 |    0.01 |    0.67 |    0.67 |    0.00 |
| requests_1                       |    1.11 |    1.11 |    0.01 |    0.76 |    0.77 |    0.02 |
| requests_4                       |    1.10 |    1.10 |    0.02 |    0.76 |    0.77 |    0.01 |

![p60_1024_5](p60_1024_5.png)
