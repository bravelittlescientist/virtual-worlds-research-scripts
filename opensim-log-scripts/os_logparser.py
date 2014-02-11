#!/usr/bin/python

import sys

from datetime import datetime
from os import walk

from matplotlib import pyplot as plt

from os_log_units import get_units
from pdf_utils import pdf_create, pdf_post, pdf_save_figure

delta_measures = [
    "clientstack.Potato.OutgoingUDPSendsCount",
    "clientstack.Potato.IncomingPacketsProcessedCount"
]

def entry_parsing_example(parsed_log):
    first_entry = parsed_log[parsed_log.keys()[0]]
    for k in first_entry.keys():
        print k, first_entry[k]

def metric_entry_parser(measure,result):
    res = float(result.split()[-1].strip("/s,"))
    #res = float(result.split()[0].strip("%").strip(","))
    return res

def organize_log_metrics(filename, start_time):
    timed_log_entries = []
    time_entry = ""
    metrics = {}

    readf = open(filename)

    for line in readf:
        if "STATS REPORT" in line:
            if len(time_entry) > 0:
                datetime_format = datetime.strptime(time_entry.decode("utf-8-sig"), '%Y-%m-%d %H:%M:%S')

                if (datetime_format >= start_time):
                    timed_log_entries.append([datetime_format, metrics])

            time_entry = line.split(" - ")[0].split(",")[0]
            metrics = {}
        else:
            metric = line.split(" - ")[1].strip()
            category = metric.split(" : ")[0]
            res = metric.split(" : ")[1]

            if category in delta_measures:
                metrics[category] = metric_entry_parser(category,res)

    readf.close()

    return timed_log_entries

def print_usage():
    print "Usage: os_logparser.py [log_directory] [prefixes,...]"

def get_opensim_logs_in_directory(directory):
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend(filenames)
        break
    return [f for f in files if ".log" in f]

def filter_logfiles_by_prefixes(logfiles, prefixes):
    return [log for log in logfiles if any(p in log for p in prefixes)]

def get_start_files_in_directory(directory, prefixes):
    startfiles = []
    for (dirpath, dirnames, filenames) in walk(directory):
        startfiles.extend(filenames)
        break
    return [sf for sf in startfiles if any(p in sf for p in prefixes) and ".start" in sf]

def read_start_times(log_directory, start_files):
    keyword_starts = {}
    for s in sorted(start_files):
        f = open(log_directory + s)
        start_datetime = f.readline().strip()
        keyword = s.split(".")[0]
        keyword_starts[keyword] = datetime.strptime(start_datetime, '%a %b %d %H:%M:%S %Z %Y')

        f.close()

    return keyword_starts

def log_preprocessing(log_directory, prefixes):

    comparisons = {}
    start_times = {}

    # Filter out any logs not needed for this experiment
    opensim_log_in_dir = get_opensim_logs_in_directory(log_directory)
    requested_logs = filter_logfiles_by_prefixes(opensim_log_in_dir, prefixes)

    # Retriever start time files so we can start runs at the right spot
    print
    print "calibrating logs to experiment durations..."

    start_files = get_start_files_in_directory(log_directory, prefixes)
    start_times = read_start_times(log_directory, start_files)

    # Process actual opensim log monitoring outputs
    print
    print "processing",log_directory,"for",", ".join(prefixes)

    for log in sorted(requested_logs):
        fkey = log.split(".")[0]
        comparisons[fkey] = organize_log_metrics(log_directory + log, start_times[fkey])

    return comparisons

def average_statistics_for_prefix(prefix, comparisons):
    print "Creating keyword timelines for", prefix.strip("_")

    prefix_keys = [key for key in comparisons.keys() if prefix in key]
    steps = min(len(comparisons[key]) for key in prefix_keys)

    measures = {}
    measure_keys = comparisons[prefix_keys[0]][0][1].keys()
    for m in delta_measures:
        m_values = []

        for k in prefix_keys:
            m_values.append([comparisons[k][s][1][m] for s in range(steps)])

        m_steps = []

        for step in range(steps):
            average = sum([m_values[grp][step] for grp in range(len(m_values))])/len(m_values)
            m_steps.append(average)

        measures[m] = m_steps

    return measures

def plot_property(propname, label_data, title=""):
    fig = plt.figure()
    units = get_units()

    # 60 minutes and x axis
    entries = 721
    t = [x*5 for x in range(entries)]

    markers = {
            "camera" : '1',
            "body" : '2',
            "head" : '3',
            "optimal" : '4'
            }

    for label in label_data.keys():
        shorthand = label.split("_")[0]
        print shorthand, label_data[label][-1], propname
        plt.plot(t, label_data[label][:entries], label=shorthand, marker=markers[shorthand])

    plt.title(title + "\n" + propname.split(".")[-1])
    plt.ylabel("delta " + propname.split(".")[-1] + " /5s")
    if propname in units.keys():
        plt.ylabel(propname.split(".")[-1] + " (" + units[propname] + ")")
    plt.xlabel('Time (s)')
    plt.xlim((0,720*5))
    plt.legend(loc='lower right', shadow=True)

    return fig

if __name__ == "__main__":

    # Insufficient command line arguments
    if len(sys.argv) <= 2:
        print_usage()

    # OK Command line arguments
    else:
        prefixes = [
                "camera_sitting_",
                "body_sitting_",
                "head_sitting_",
                "optimal_sitting_"]

        n_bots = sys.argv[1]
        log_directory = sys.argv[2]
        prefixes = [p + str(n_bots) + "_" for p in prefixes]

        comparisons = log_preprocessing(log_directory, prefixes)

        stats = {}
        for p in prefixes:
            stats[p] = average_statistics_for_prefix(p, comparisons)
        keys = stats[prefixes[0]].keys()

        plt.close("all")
        pdf = pdf_create("output.pdf")

        for k in keys:
            label_plots = {}
            for key in stats.keys():
                label_plots[key] = stats[key][k]

            ptitle = "OpenSimulator Monitoring, 1 hour, " + n_bots + " sitting bots"
            fig = plot_property(k, label_plots, title=ptitle)
            pdf = pdf_save_figure(pdf, fig)
            plt.close(fig)

        pdf_post(pdf)
