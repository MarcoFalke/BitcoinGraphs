#!/usr/bin/env python3

import matplotlib
from collections import namedtuple
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as pl
import csv
import os
import argparse
import collections

Bench = namedtuple('Bench', 'file, times')


def get_benches(folder):
    print('Collecting benchmarks ...')
    benches = collections.defaultdict(list)
    csv_dialect = csv.excel  # The default dialect
    csv_dialect.skipinitialspace = True
    for file in sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]):
        with open(os.path.join(folder, file), newline='') as csvfile:
            print(' ... found bench file "{}"'.format(file))
            rows = [row for row in csv.reader(csvfile, dialect=csv_dialect, delimiter=',')]
            labels, rows = rows[0], rows[1:]
            for row in rows:
                bench_name = row[0]
                # Make sure to break when the format changes
                assert labels == ['# Benchmark', 'evals', 'iterations', 'total', 'min', 'max', 'median']
                times = row[4:]
                benches[bench_name] += [Bench(file, times)]
    return benches


def plot_benches(benches, out_folder):
    print('Creating plots for benches ...')
    for bench_name in benches:
        files = [b.file for b in benches[bench_name]]
        time_data = [pd.Series(b.times).apply(pd.to_numeric) for b in benches[bench_name]]
        sn.boxplot(x=files, y=time_data)
        #pl.xlabel('File')
        pl.ylabel('time')
        pl.ylim(ymin=0)
        pl.title(bench_name)
        print(' ... {}'.format(bench_name))
        pl.savefig(os.path.join(out_folder, bench_name + '.png'))
        #pl.show()
        pl.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_folder',
                        help='The folder which contains outputs of bench_bitcoin',
                        default='./assets/bench_outputs/')
    parser.add_argument('-o', '--out_folder',
                        help='The folder to put the plots in',
                        default='./assets/bench_plots/')
    args = parser.parse_args()
    benches = get_benches(args.in_folder)
    plot_benches(benches, args.out_folder)


if __name__ == '__main__':
    main()
