#!/usr/bin/python

import csv
import sys
import os

from util import get_single_cpu_run_by_prefix
from os_logparser import log_preprocessing

# Take as input a directory
log_directory = sys.argv[1]
if log_directory[-1] != "/":
    log_directory += "/"

# Check if valid directory
if not os.path.isdir(log_directory):
    exit()

# Output files
network_out = "network_out.csv"
cpu_out = "cpu_usage.csv"

configurations = ["baseline_sitting", "body_sitting", "filtered_sitting", "baseline_standing", "body_standing", "filtered_standing"]

numbers = [10, 50, 100, 200]
columns = ["_".join([c, str(n), str(r)]) for c in configurations for n in numbers for r in range(1,4)]
labels = [c.replace("body","unfiltered") for c in columns]

# CPU Usage
cpus = {}
for c in columns:
    cpus[c] = get_single_cpu_run_by_prefix(log_directory + c)[-60:]

with open(cpu_out, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(labels)

    n_rows = 60
    for row in range(n_rows):
        writer.writerow([cpus[c][row] for c in columns])

# Network
measures = [
    "clientstack.Potato.OutgoingUDPSendsCount",
    "clientstack.Potato.IncomingPacketsProcessedCount",
    "clientstack.Potato.IncomingUDPReceivesCount"
]

network_logs = log_preprocessing(log_directory, columns)


for m in measures:
    out = m.split(".")[-1] + ".csv"
    with open(out, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(labels)

        n_rows = 121
        for row in range(n_rows):
            write_row = row - n_rows
            writer.writerow([network_logs[c][write_row][1][m] for c in columns])
