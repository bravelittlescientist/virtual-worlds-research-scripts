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

positions = ["sitting", "standing"]
configurations = ["body", "filtered", "baseline"]
numbers = [10, 50, 100]
columns = ["_".join([c, p, str(n), str(r)]) for p in positions for c in configurations for n in numbers for r in range(1,4)]

# CPU Usage
with open(cpu_out, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(columns)

    cpus = {}
    for c in columns:
        #cpus[c] = get_single_cpu_run_by_prefix(c)
        pass

    n_rows = len(cpus[columns[0]])
    for row in range(n_rows):
        #writer.writerow([cpus[c][row] for c in columns])
        pass

# Network Usage
network_logs = log_preprocessing(log_directory, columns)
with open(network_out, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    print [k for k in network_logs]


