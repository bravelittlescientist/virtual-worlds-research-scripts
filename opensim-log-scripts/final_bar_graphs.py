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
res = {
        "optimal": {
            "cpu" : { 10 : 0, 50 : 0, 100 : 0},
            "outgoing" : { 10 : 0, 50 : 0, 100 : 0},
            "inc" : { 10 : 0, 50 : 0, 100 : 0},
            "proc" : { 10 : 0, 50 : 0, 100 : 0}
            },
        "camera": {
            "cpu" : { 10 : 0, 50 : 0, 100 : 0},
            "outgoing" : { 10 : 0, 50 : 0, 100 : 0},
            "inc" : { 10 : 0, 50 : 0, 100 : 0},
            "proc" : { 10 : 0, 50 : 0, 100 : 0}
            },
        "body" : {
            "cpu" : { 10 : 0, 50 : 0, 100 : 0},
            "outgoing" : { 10 : 0, 50 : 0, 100 : 0},
            "inc" : { 10 : 0, 50 : 0, 100 : 0},
            "proc" : { 10 : 0, 50 : 0, 100 : 0}
            },
        "head" : {
            "cpu" : { 10 : 0, 50 : 0, 100 : 0},
            "outgoing" : { 10 : 0, 50 : 0, 100 : 0},
            "inc" : { 10 : 0, 50 : 0, 100 : 0},
            "proc" : { 10 : 0, 50 : 0, 100 : 0}
            }}

# Pull CPU log info
for mode in ["sample_"]:
    # for n_bots in [10, 50, 100]:
    # prefix = log_directory + mode + "_sitting_" + str(n_bots) + "_"
    prefix = log_directory + mode
    cpu = get_average_cpu_last_n_minutes(prefix, runs=1)
