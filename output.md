## Package versions

* aiohttp                        3.6.2
* httpx                          0.13.3
* requests                       2.24.0

## Context

* Cases: aiohttp, httpx, httpx_11, requests, requests_4sessions
* Scenarios: external_search, 6_2seq_8kb, 6_2seq_400kb, 100_2seq_2kb, 1_100seq_1, 1_100seq_2kb, 1_100seq_256kb, 1_100seq_1mb, 1_30seq_8kb_400ms, 30_1seq_8kb_400ms
* Tries: default


## Scenario external_search: External requests: Two sequences of searx requests, 0.5s in between

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    1.41 |    1.42 |    0.26 |    0.15 |    0.15 |    0.04 |
| httpx                           |    1.25 |    1.29 |    0.18 |    0.29 |    0.28 |    0.06 |
| httpx_11                        |    1.38 |    1.35 |    0.13 |    0.23 |    0.23 |    0.06 |
| requests                        |    1.52 |    1.72 |    0.65 |    0.74 |    0.82 |    0.26 |
| requests_4sessions              |    1.50 |    1.52 |    0.21 |    0.89 |    0.98 |    0.27 |



## Scenario 6_2seq_8kb: Two sequences of 6 requests with a 8KB responses (various delays), 0.5s in between

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    1.57 |    1.56 |    0.05 |    0.10 |    0.10 |    0.02 |
| httpx                           |    1.45 |    1.45 |    0.02 |    0.21 |    0.21 |    0.05 |
| httpx_11                        |    1.58 |    1.58 |    0.05 |    0.19 |    0.19 |    0.04 |
| requests                        |    1.60 |    1.60 |    0.08 |    0.21 |    0.21 |    0.06 |
| requests_4sessions              |    1.59 |    1.59 |    0.05 |    0.22 |    0.23 |    0.05 |



## Scenario 6_2seq_400kb: Two sequences of 6 requests with a 400KB responses (various delays), 0.5s in between

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    1.57 |    1.56 |    0.04 |    0.20 |    0.20 |    0.03 |
| httpx                           |    1.51 |    1.53 |    0.07 |    0.76 |    0.78 |    0.16 |
| httpx_11                        |    1.68 |    1.66 |    0.07 |    0.90 |    0.89 |    0.16 |
| requests                        |    1.60 |    1.62 |    0.12 |    0.37 |    0.38 |    0.05 |
| requests_4sessions              |    1.64 |    1.63 |    0.06 |    0.41 |    0.43 |    0.07 |



## Scenario 100_2seq_2kb: Two sequences of 100 parallel requests (various delays), 0.5s in between

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    3.52 |    3.54 |    0.16 |    0.85 |    0.88 |    0.09 |
| httpx                           |    1.99 |    2.03 |    0.21 |    1.43 |    1.43 |    0.24 |
| httpx_11                        |    4.64 |    4.56 |    0.36 |    1.91 |    1.91 |    0.09 |
| requests                        |    4.13 |    4.24 |    0.59 |    2.25 |    2.28 |    0.17 |
| requests_4sessions              |    4.32 |    4.35 |    0.52 |    2.27 |    2.27 |    0.21 |



## Scenario 1_100seq_1: 100 sequential requests, 1 byte response, 0 delay

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    0.53 |    0.58 |    0.22 |    0.23 |    0.22 |    0.05 |
| httpx                           |    0.95 |    1.07 |    0.32 |    0.63 |    0.66 |    0.12 |
| httpx_11                        |    0.82 |    1.07 |    0.56 |    0.55 |    0.56 |    0.10 |
| requests                        |    0.77 |    0.76 |    0.16 |    0.49 |    0.48 |    0.10 |
| requests_4sessions              |    1.19 |    1.29 |    0.39 |    0.56 |    0.57 |    0.10 |



## Scenario 1_100seq_2kb: 100 sequential requests, 2KB response, 0 delay

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    0.53 |    0.60 |    0.24 |    0.23 |    0.24 |    0.06 |
| httpx                           |    1.00 |    1.08 |    0.32 |    0.70 |    0.70 |    0.14 |
| httpx_11                        |    0.73 |    0.78 |    0.19 |    0.46 |    0.52 |    0.12 |
| requests                        |    0.79 |    0.92 |    0.36 |    0.51 |    0.54 |    0.12 |
| requests_4sessions              |    1.07 |    1.03 |    0.18 |    0.51 |    0.54 |    0.11 |



## Scenario 1_100seq_256kb: 100 sequential requests, 256KB response, 0 delay

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    0.95 |    1.01 |    0.36 |    0.55 |    0.54 |    0.13 |
| httpx                           |    3.53 |    3.70 |    0.81 |    2.89 |    3.06 |    0.61 |
| httpx_11                        |    3.51 |    3.58 |    0.55 |    3.22 |    3.28 |    0.50 |
| requests                        |    1.13 |    1.31 |    0.40 |    0.85 |    0.94 |    0.26 |
| requests_4sessions              |    1.31 |    1.43 |    0.34 |    0.86 |    0.93 |    0.23 |



## Scenario 1_100seq_1mb: 100 sequential requests, 1MB response, 0 delay

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    1.73 |    1.91 |    0.65 |    1.29 |    1.31 |    0.29 |
| httpx                           |   10.25 |   10.33 |    1.14 |    9.17 |    9.28 |    0.82 |
| httpx_11                        |   10.95 |   11.16 |    1.33 |   10.32 |   10.70 |    1.29 |
| requests                        |    2.77 |    2.90 |    0.52 |    2.37 |    2.42 |    0.45 |
| requests_4sessions              |    3.49 |    3.35 |    0.59 |    2.60 |    2.49 |    0.46 |



## Scenario 1_30seq_8kb_400ms: 30 sequential requests, 8KB response, 400ms delay

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |   12.35 |   12.34 |    0.08 |    0.12 |    0.11 |    0.03 |
| httpx                           |   12.60 |   12.61 |    0.16 |    0.30 |    0.32 |    0.08 |
| httpx_11                        |   12.47 |   12.60 |    0.29 |    0.24 |    0.27 |    0.08 |
| requests                        |   12.42 |   12.49 |    0.18 |    0.20 |    0.21 |    0.05 |
| requests_4sessions              |   12.68 |   12.69 |    0.19 |    0.24 |    0.25 |    0.08 |



## Scenario 30_1seq_8kb_400ms: One sequence of 30 requests, 8KB response, 400ms delay

|                                 | Runtime |         |         | Cputime |         |         |
|---------------------------------|---------|---------|---------|---------|---------|---------|
|                                 |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                         |    0.95 |    1.01 |    0.12 |    0.17 |    0.17 |    0.01 |
| httpx                           |    0.63 |    0.69 |    0.15 |    0.20 |    0.20 |    0.01 |
| httpx_11                        |    1.00 |    1.04 |    0.14 |    0.38 |    0.36 |    0.04 |
| requests                        |    0.97 |    1.02 |    0.16 |    0.36 |    0.37 |    0.04 |
| requests_4sessions              |    1.00 |    1.02 |    0.08 |    0.43 |    0.41 |    0.03 |
