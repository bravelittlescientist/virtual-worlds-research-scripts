#!/usr/bin/python

import sys
import numpy

from util import get_average_cpu_usage_by_prefix

if len(sys.argv) == 0:
    print "Usage: ./sacle_to_100.py [log-directory]"

else:

    # Parse log directory
    log_dir = sys.argv[1]
    if log_dir[-1] != '/':
        log_dir = log_dir + "/"

    # Store 60-minute logs in mode map
    modes = {"optimal": [], "camera": [], "body" : [], "head" : []}

    for mode in modes:
        for nbots in range(10,110,10):
            # Prefix of file
            prefix = log_dir + mode + "_sitting_" + str(nbots) + "_"
            modes[mode].append(get_average_cpu_usage_by_prefix(prefix, minutes=30))


    # Get last value in each as our steady state
    for mode in modes:
        print mode
        for k in range(len(modes[mode])):
            print numpy.mean(modes[mode][k][-20:])
