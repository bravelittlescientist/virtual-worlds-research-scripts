#!/usr/bin/python

import sys
import numpy

def get_start_time(base):
    """ Read start file, return start time string """
    with open(base + ".start") as f:
        return f.readline().split()[3]

def get_dat_file_contents(base):
    with open(base + ".dat") as f:
        data = f.read()
    return data

def extract_time_chunk(start_time, f_content, minutes):
    data = f_content.strip().split("\n")
    include = False
    entries = (minutes*60)+1

    chunk = []

    for line in data:
        if include or line.split()[0].strip() == start_time.strip():
            chunk.append(float(line.split()[1]))
            include = True
    return chunk[:entries]

def mean(li):
    """ Computes average of numbers in a list """
    return sum(li)/len(li)

def average_over_runs(cpu_chunks):

    entries = len(cpu_chunks[0])
    runs = len(cpu_chunks)
    average = []

    for c in range(entries):
        average.append(mean([cpu_chunks[r][c] for r in range(runs)]))

    return average

def get_average_cpu_usage_by_prefix(base, minutes=60, runs=3):
    """ Returns the CPU usage from the start point to end """

    base_content = []

    for i in range(runs):
        start_time = get_start_time(base + str(i + 1))
        file_contents = get_dat_file_contents(base + str(i + 1))
        base_content.append(extract_time_chunk(start_time, file_contents, minutes))

    return average_over_runs(base_content)

def get_average_cpu_last_n_minutes(base, minutes=30, n=1, runs=3):
    """ Computes average cpu usage over last n minutes of a run """
    # Validate number of minutes, average over whole thing if needed
    n = min(n, minutes)

    # Figure out number of entries to average
    entries = 60

    # Return mean of last entries provides of result
    cpu_average = get_average_cpu_usage_by_prefix(base, minutes, runs)

    return mean(cpu_average[-60:])

if __name__ == "__main__":
    print "Utility scripts for OpenSimulator log parsing"
