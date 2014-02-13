#!/usr/bin/python

import sys
import numpy
import os

from util import get_average_cpu_last_n_minutes
from plot_util import plot_multibar_chart

# Take as input a directory
log_directory = sys.argv[1]
if log_directory[-1] != "/":
    log_directory += "/"

# Check if valid directory
if not os.path.isdir(log_directory):
    exit()

# Prepare results tracker
cpu_numbers = {
        "optimal": [],
        "camera" : [],
        "body" : [],
        "head" : []
        }

# Pull CPU log info
for mode in cpu_numbers.keys():
    for n_bots in [10, 50, 100]:
        print mode, n_bots
        # prefix = log_directory + mode + "_sitting_" + str(n_bots) + "_"
        prefix = log_directory + "sample_"
        cpu = get_average_cpu_last_n_minutes(prefix, runs=1)
        cpu_numbers[mode].append(cpu)
        print cpu
