#!/usr/bin/python

import sys
import numpy
import os

from util import get_average_cpu_last_n_minutes

# Take as input a directory
log_directory = sys.argv[1]
if log_directory[-1] != "/":
    log_directory += "/"

# Check if valid directory
if not os.path.isdir(log_directory):
    exit()

# Prepare results tracker
cpu_numbers = {
        "body_sitting_" : [],
        "body_standing_" : [],
        "filtered_sitting_" : [],
        "filtered_standing_" : [],
        "baseline_sitting_" : [],
        "baseline_standing_" : []
        }

# Pull CPU log info
for mode in cpu_numbers.keys():
    for n in [10,50,100]:
        print mode, n, "bots"
        prefix = log_directory + mode + str(n) + "_"
        cpu = get_average_cpu_last_n_minutes(prefix)
        print cpu
