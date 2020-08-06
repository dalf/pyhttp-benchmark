#!/usr/bin/env python

"""
Usage:
pyhttpbench run --csv . .
cd results
csv2graph *.csv
"""

import typing
import matplotlib.pyplot as plt  # type: ignore
import statistics

from . import metrics, model, output


def save(metrics: metrics.Metrics, scenario: model.Scenario) -> None:
    stats: typing.Dict[str, typing.List[int]] = {
        'labels': list(),
        'runtime_mean': list(),
        'runtime_stdev': list(),
        'cputime_mean': list(),
        'cputime_stdev': list(),
    }

    for case, stat in metrics.values.items():
        runtime = list(map(lambda s: s[0], stat))
        cputime = list(map(lambda s: s[1], stat))

        runtime_mean = statistics.mean(runtime)
        runtime_stdev = statistics.stdev(runtime)

        cputime_mean = statistics.mean(cputime)
        cputime_stdev = statistics.stdev(cputime)

        stats['labels'].append(case.full_name)
        stats['runtime_mean'].append(runtime_mean)
        stats['runtime_stdev'].append(runtime_stdev)
        stats['cputime_mean'].append(cputime_mean)
        stats['cputime_stdev'].append(cputime_stdev)

    width = 0.5

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.subplots_adjust(bottom=0.2)
    plt.margins(0.2)

    ax.bar(stats['labels'], stats['runtime_mean'], width, yerr=stats['runtime_stdev'], label='Runtime')
    ax.bar(stats['labels'], stats['cputime_mean'], width, yerr=stats['cputime_stdev'], label='CPU time')

    ax.set_ylabel('Average response time with the standard deviation (second)')
    ax.set_title(scenario.id)
    ax.legend()
    plt.xticks(rotation='vertical')
    plt.savefig(output.get_png_file(scenario), format='png')
