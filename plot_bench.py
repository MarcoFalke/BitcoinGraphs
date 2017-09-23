#!/usr/bin/env python3

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as pl
import csv
import os
import argparse
import collections


def get_benches(folder):
    benches = collections.defaultdict(list)
    for file in [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]:
        with open(os.path.join(folder, file), newline='') as csvfile:
            rows = [row for row in csv.reader(csvfile, delimiter=',')]
            labels, rows = rows[0], rows[1:]
            for row in rows:
                bench_name = row[0]
                data_frame = pd.DataFrame(data=row[1:], index=labels[1:])
                times = data_frame.loc[['min', 'max', 'average']]
                cycles = data_frame.loc[['min_cycles', 'max_cycles', 'average_cycles']]
                files = [[file]] * len(cycles)
                data_frame = pd.DataFrame(data=np.concatenate([times, cycles, files], axis=1),
                                          columns=['times', 'cycles', 'files'])
                benches[bench_name] += [data_frame]
    for bench_name in benches:
        benches[bench_name] = pd.concat(benches[bench_name], axis=0)
    return benches


def plot_benches(benches, out_folder):
    for bench_name in benches:
        bench = benches[bench_name]
        sn.boxplot(x=bench['files'], y=bench['times'].apply(pd.to_numeric))
        pl.xlabel('Instance')
        pl.ylabel('Time')
        pl.ylim(ymin=0)
        pl.title(bench_name)
        pl.savefig(os.path.join(out_folder, bench_name + '.png'))
        pl.show()
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
