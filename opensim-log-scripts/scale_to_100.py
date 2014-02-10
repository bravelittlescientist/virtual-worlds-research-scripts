#!/usr/bin/python

import sys

from util import get_average_cpu_usage_by_prefix

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
        modes[mode].append(get_average_cpu_usage_by_prefix(prefix))


# Get last value in each as our steady state
for mode in modes:
    print mode
    for k in range(len(modes[mode])):
        print len(modes[mode][k])
        #print (k+1)*10,"bots, CPU %:", modes[mode][k][-1]
