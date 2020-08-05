import sys
import pathlib
from io import StringIO
import csv
import numpy as np
import matplotlib.pyplot as plt
import statistics

def create_png(finput_name: str, foutput_name: str):
    with open(finput_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        runtime_stats = dict()
        cputime_stats = dict()
        for row in reader:
            if len(row) > 0 and row[0] != 'case':
                runtime_stat = runtime_stats.setdefault(row[0], list())
                runtime_stat.append(float(row[1]))
                cputime_stat = cputime_stats.setdefault(row[0], list())
                cputime_stat.append(float(row[2]))
            
    stats = {
        'labels': list(),
        'runtime_mean': list(),
        'runtime_stdev': list(),
        'cputime_mean': list(),
        'cputime_stdev': list(),
    }
    for k in runtime_stats.keys():
        stats['labels'].append(k)
        stats['runtime_mean'].append(statistics.mean(runtime_stats[k]))
        stats['runtime_stdev'].append(statistics.stdev(runtime_stats[k]))
        stats['cputime_mean'].append(statistics.mean(cputime_stats[k]))
        stats['cputime_stdev'].append(statistics.stdev(cputime_stats[k]))

    width = 0.5       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.subplots_adjust(bottom=0.2)
    plt.margins(0.2)

    ax.bar(stats['labels'], stats['runtime_mean'], width, yerr=stats['runtime_stdev'], label='Runtime')
    ax.bar(stats['labels'], stats['cputime_mean'], width, yerr=stats['cputime_stdev'], label='CPU time')

    ax.set_ylabel('Response time (second)')
    ax.set_title(finput_name)
    ax.legend()
    plt.xticks(rotation='vertical')
    plt.savefig(foutput_name, format='png')


if len(sys.argv)>=2:
    for input_name in sys.argv[1:]:
        input_path = pathlib.Path(input_name)
        output_path = input_path.with_suffix('.png')
        create_png(input_path, output_path)
