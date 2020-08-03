Output directory: /home/alexandre/code/pyhttp
## Versions

* Python                         3.8.2 (default, Apr 27 2020, 15:53:34) [GCC 9.3.0]
* aiohttp                        3.6.2
* httpx                          0.13.3
* requests                       2.22.0
* uvloop                         0.14.0
* trio                           0.16.0

## Context

* Cases: aiohttp, httpx, httpx_11, requests, requests_4sessions
* Scenarios: external_search, 6_2seq_8kb, 6_2seq_400kb, 100_2seq_2kb, 1_100seq_1, 1_100seq_2kb, 1_100seq_256kb, 1_100seq_1mb, 1_30seq_8kb_400ms, 30_1seq_8kb_400ms
* Tries: default


## Scenario external_search: External requests: Two sequences of searx requests, 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.40 |    1.59 |    0.77 |    0.09 |    0.09 |    0.02 |
| httpx                            |    1.21 |    1.22 |    0.17 |    0.15 |    0.13 |    0.05 |
| httpx_11                         |    1.31 |    1.29 |    0.12 |    0.12 |    0.11 |    0.04 |
| requests                         |    1.35 |    1.44 |    0.41 |    0.21 |    0.19 |    0.05 |
| requests_4sessions               |    1.28 |    1.29 |    0.13 |    0.25 |    0.26 |    0.07 |



## Scenario 6_2seq_8kb: Two sequences of 6 requests with a 8KB responses (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.42 |    1.42 |    0.01 |    0.04 |    0.04 |    0.00 |
| httpx                            |    1.42 |    1.42 |    0.00 |    0.08 |    0.07 |    0.01 |
| httpx_11                         |    1.42 |    1.42 |    0.01 |    0.07 |    0.07 |    0.01 |
| requests                         |    1.44 |    1.44 |    0.01 |    0.09 |    0.09 |    0.01 |
| requests_4sessions               |    1.45 |    1.45 |    0.01 |    0.10 |    0.10 |    0.01 |



## Scenario 6_2seq_400kb: Two sequences of 6 requests with a 400KB responses (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.43 |    1.43 |    0.01 |    0.11 |    0.11 |    0.01 |
| httpx                            |    1.45 |    1.45 |    0.00 |    0.34 |    0.34 |    0.01 |
| httpx_11                         |    1.46 |    1.46 |    0.01 |    0.34 |    0.34 |    0.03 |
| requests                         |    1.45 |    1.45 |    0.01 |    0.17 |    0.17 |    0.01 |
| requests_4sessions               |    1.46 |    1.46 |    0.00 |    0.18 |    0.18 |    0.01 |



## Scenario 100_2seq_2kb: Two sequences of 100 parallel requests (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.91 |    1.90 |    0.04 |    0.39 |    0.39 |    0.02 |
| httpx                            |    1.50 |    1.50 |    0.01 |    0.43 |    0.42 |    0.02 |
| httpx_11                         |    1.90 |    1.90 |    0.00 |    0.75 |    0.75 |    0.01 |
| requests                         |    1.67 |    1.66 |    0.03 |    1.01 |    1.01 |    0.03 |
| requests_4sessions               |    1.68 |    1.67 |    0.02 |    1.04 |    1.04 |    0.02 |



## Scenario 1_100seq_1: 100 sequential requests, 1 byte response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.09 |    0.09 |    0.01 |    0.05 |    0.05 |    0.00 |
| httpx                            |    0.14 |    0.14 |    0.01 |    0.09 |    0.10 |    0.00 |
| httpx_11                         |    0.11 |    0.11 |    0.00 |    0.08 |    0.08 |    0.00 |
| requests                         |    0.14 |    0.14 |    0.00 |    0.10 |    0.10 |    0.00 |
| requests_4sessions               |    0.15 |    0.15 |    0.00 |    0.10 |    0.10 |    0.00 |



## Scenario 1_100seq_2kb: 100 sequential requests, 2KB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.09 |    0.09 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpx                            |    0.14 |    0.14 |    0.00 |    0.10 |    0.10 |    0.00 |
| httpx_11                         |    0.12 |    0.12 |    0.00 |    0.09 |    0.09 |    0.00 |
| requests                         |    0.15 |    0.15 |    0.00 |    0.10 |    0.10 |    0.00 |
| requests_4sessions               |    0.16 |    0.16 |    0.00 |    0.11 |    0.11 |    0.00 |



## Scenario 1_100seq_256kb: 100 sequential requests, 256KB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.18 |    0.18 |    0.00 |    0.13 |    0.13 |    0.00 |
| httpx                            |    0.53 |    0.53 |    0.02 |    0.47 |    0.47 |    0.01 |
| httpx_11                         |    0.54 |    0.54 |    0.00 |    0.49 |    0.49 |    0.00 |
| requests                         |    0.21 |    0.22 |    0.00 |    0.17 |    0.17 |    0.00 |
| requests_4sessions               |    0.23 |    0.23 |    0.01 |    0.17 |    0.17 |    0.00 |



## Scenario 1_100seq_1mb: 100 sequential requests, 1MB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.45 |    0.44 |    0.03 |    0.39 |    0.38 |    0.02 |
| httpx                            |    1.67 |    1.68 |    0.04 |    1.59 |    1.59 |    0.04 |
| httpx_11                         |    1.78 |    1.79 |    0.03 |    1.72 |    1.73 |    0.03 |
| requests                         |    0.49 |    0.49 |    0.00 |    0.44 |    0.44 |    0.00 |
| requests_4sessions               |    0.51 |    0.51 |    0.01 |    0.44 |    0.44 |    0.00 |



## Scenario 1_30seq_8kb_400ms: 30 sequential requests, 8KB response, 400ms delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |   12.18 |   12.18 |    0.01 |    0.10 |    0.10 |    0.00 |
| httpx                            |   12.25 |   12.25 |    0.01 |    0.18 |    0.18 |    0.01 |
| httpx_11                         |   12.24 |   12.23 |    0.01 |    0.17 |    0.17 |    0.01 |
| requests                         |   12.23 |   12.23 |    0.01 |    0.17 |    0.17 |    0.01 |
| requests_4sessions               |   12.25 |   12.25 |    0.01 |    0.18 |    0.17 |    0.01 |



## Scenario 30_1seq_8kb_400ms: One sequence of 30 requests, 8KB response, 400ms delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.45 |    0.45 |    0.01 |    0.05 |    0.05 |    0.01 |
| httpx                            |    0.44 |    0.44 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpx_11                         |    0.47 |    0.47 |    0.00 |    0.10 |    0.10 |    0.00 |
| requests                         |    0.50 |    0.49 |    0.01 |    0.21 |    0.20 |    0.02 |
| requests_4sessions               |    0.50 |    0.49 |    0.01 |    0.20 |    0.19 |    0.03 |

## Versions

* Python                         3.8.2 (default, Apr 27 2020, 15:53:34) [GCC 9.3.0]
* aiohttp                        3.6.2
* httpx                          0.13.3
* requests                       2.22.0
* uvloop                         0.14.0
* trio                           0.16.0

## Context

* Cases: aiohttp, httpx, httpx_11, requests, requests_4sessions
* Scenarios: external_search, 6_2seq_8kb, 6_2seq_400kb, 100_2seq_2kb, 1_100seq_1, 1_100seq_2kb, 1_100seq_256kb, 1_100seq_1mb, 1_30seq_8kb_400ms, 30_1seq_8kb_400ms
* Tries: default


## Scenario external_search: External requests: Two sequences of searx requests, 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.40 |    1.59 |    0.77 |    0.09 |    0.09 |    0.02 |
| httpx                            |    1.21 |    1.22 |    0.17 |    0.15 |    0.13 |    0.05 |
| httpx_11                         |    1.31 |    1.29 |    0.12 |    0.12 |    0.11 |    0.04 |
| requests                         |    1.35 |    1.44 |    0.41 |    0.21 |    0.19 |    0.05 |
| requests_4sessions               |    1.28 |    1.29 |    0.13 |    0.25 |    0.26 |    0.07 |



## Scenario 6_2seq_8kb: Two sequences of 6 requests with a 8KB responses (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.42 |    1.42 |    0.01 |    0.04 |    0.04 |    0.00 |
| httpx                            |    1.42 |    1.42 |    0.00 |    0.08 |    0.07 |    0.01 |
| httpx_11                         |    1.42 |    1.42 |    0.01 |    0.07 |    0.07 |    0.01 |
| requests                         |    1.44 |    1.44 |    0.01 |    0.09 |    0.09 |    0.01 |
| requests_4sessions               |    1.45 |    1.45 |    0.01 |    0.10 |    0.10 |    0.01 |



## Scenario 6_2seq_400kb: Two sequences of 6 requests with a 400KB responses (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.43 |    1.43 |    0.01 |    0.11 |    0.11 |    0.01 |
| httpx                            |    1.45 |    1.45 |    0.00 |    0.34 |    0.34 |    0.01 |
| httpx_11                         |    1.46 |    1.46 |    0.01 |    0.34 |    0.34 |    0.03 |
| requests                         |    1.45 |    1.45 |    0.01 |    0.17 |    0.17 |    0.01 |
| requests_4sessions               |    1.46 |    1.46 |    0.00 |    0.18 |    0.18 |    0.01 |



## Scenario 100_2seq_2kb: Two sequences of 100 parallel requests (various delays), 0.5s in between

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    1.91 |    1.90 |    0.04 |    0.39 |    0.39 |    0.02 |
| httpx                            |    1.50 |    1.50 |    0.01 |    0.43 |    0.42 |    0.02 |
| httpx_11                         |    1.90 |    1.90 |    0.00 |    0.75 |    0.75 |    0.01 |
| requests                         |    1.67 |    1.66 |    0.03 |    1.01 |    1.01 |    0.03 |
| requests_4sessions               |    1.68 |    1.67 |    0.02 |    1.04 |    1.04 |    0.02 |



## Scenario 1_100seq_1: 100 sequential requests, 1 byte response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.09 |    0.09 |    0.01 |    0.05 |    0.05 |    0.00 |
| httpx                            |    0.14 |    0.14 |    0.01 |    0.09 |    0.10 |    0.00 |
| httpx_11                         |    0.11 |    0.11 |    0.00 |    0.08 |    0.08 |    0.00 |
| requests                         |    0.14 |    0.14 |    0.00 |    0.10 |    0.10 |    0.00 |
| requests_4sessions               |    0.15 |    0.15 |    0.00 |    0.10 |    0.10 |    0.00 |



## Scenario 1_100seq_2kb: 100 sequential requests, 2KB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.09 |    0.09 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpx                            |    0.14 |    0.14 |    0.00 |    0.10 |    0.10 |    0.00 |
| httpx_11                         |    0.12 |    0.12 |    0.00 |    0.09 |    0.09 |    0.00 |
| requests                         |    0.15 |    0.15 |    0.00 |    0.10 |    0.10 |    0.00 |
| requests_4sessions               |    0.16 |    0.16 |    0.00 |    0.11 |    0.11 |    0.00 |



## Scenario 1_100seq_256kb: 100 sequential requests, 256KB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.18 |    0.18 |    0.00 |    0.13 |    0.13 |    0.00 |
| httpx                            |    0.53 |    0.53 |    0.02 |    0.47 |    0.47 |    0.01 |
| httpx_11                         |    0.54 |    0.54 |    0.00 |    0.49 |    0.49 |    0.00 |
| requests                         |    0.21 |    0.22 |    0.00 |    0.17 |    0.17 |    0.00 |
| requests_4sessions               |    0.23 |    0.23 |    0.01 |    0.17 |    0.17 |    0.00 |



## Scenario 1_100seq_1mb: 100 sequential requests, 1MB response, 0 delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.45 |    0.44 |    0.03 |    0.39 |    0.38 |    0.02 |
| httpx                            |    1.67 |    1.68 |    0.04 |    1.59 |    1.59 |    0.04 |
| httpx_11                         |    1.78 |    1.79 |    0.03 |    1.72 |    1.73 |    0.03 |
| requests                         |    0.49 |    0.49 |    0.00 |    0.44 |    0.44 |    0.00 |
| requests_4sessions               |    0.51 |    0.51 |    0.01 |    0.44 |    0.44 |    0.00 |



## Scenario 1_30seq_8kb_400ms: 30 sequential requests, 8KB response, 400ms delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |   12.18 |   12.18 |    0.01 |    0.10 |    0.10 |    0.00 |
| httpx                            |   12.25 |   12.25 |    0.01 |    0.18 |    0.18 |    0.01 |
| httpx_11                         |   12.24 |   12.23 |    0.01 |    0.17 |    0.17 |    0.01 |
| requests                         |   12.23 |   12.23 |    0.01 |    0.17 |    0.17 |    0.01 |
| requests_4sessions               |   12.25 |   12.25 |    0.01 |    0.18 |    0.17 |    0.01 |



## Scenario 30_1seq_8kb_400ms: One sequence of 30 requests, 8KB response, 400ms delay

|                                  | Runtime |         |         | Cputime |         |         |
|----------------------------------|---------|---------|---------|---------|---------|---------|
|                                  |  median |    mean |   stdev |  median |    mean |   stdev |
| aiohttp                          |    0.45 |    0.45 |    0.01 |    0.05 |    0.05 |    0.01 |
| httpx                            |    0.44 |    0.44 |    0.00 |    0.05 |    0.05 |    0.00 |
| httpx_11                         |    0.47 |    0.47 |    0.00 |    0.10 |    0.10 |    0.00 |
| requests                         |    0.50 |    0.49 |    0.01 |    0.21 |    0.20 |    0.02 |
| requests_4sessions               |    0.50 |    0.49 |    0.01 |    0.20 |    0.19 |    0.03 |

