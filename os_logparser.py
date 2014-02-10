#!/usr/bin/python2

import sys

from datetime import datetime
from os import walk

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt

from os_log_units import get_units

def entry_parsing_example(parsed_log):
    first_entry = parsed_log[parsed_log.keys()[0]]
    for k in first_entry.keys():
        print k, first_entry[k]

def metric_entry_parser(measure,result):
    return float(result.split()[0].strip("%").strip(","))

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
    for m in measure_keys:

        m_values = []

        for k in prefix_keys:
            m_values.append([comparisons[k][s][1][m] for s in range(steps)])

        m_steps = []
        for step in range(steps):
            average = sum([m_values[grp][step] for grp in range(len(m_values))])/len(m_values)
            m_steps.append(average)
        measures[m] = m_steps

    return measures

def plot_property(propname, label_data):
    fig = plt.figure()
    units = get_units()

    # 60 minutes and x axis
    entries = 721
    t = [x*5 for x in range(entries)]

    for label in label_data.keys():
        plt.plot(t, label_data[label][:entries], label=label)

    plt.title('OpenSim Monitoring, 10 bots, 1 hour: ' + propname)
    plt.ylabel(propname.split(".")[-1])
    if propname in units.keys():
        plt.ylabel(propname.split(".")[-1] + " (" + units[propname] + ")")
    plt.xlabel('Time (s)')
    plt.xlim((0,720*5))
    plt.legend(loc='lower right', shadow=True)
    return fig

def plot_figure_to_pdf(pdf, figure):
    pdf.savefig(figure)
    return pdf

def create_pdf(output_filename):
    pdf = PdfPages(output_filename)
    return pdf

def close_pdf(pdf):
    pdf.close()

if __name__ == "__main__":

    # No command line arguments
    if len(sys.argv) == 1:
        print_usage()

    # Just 2 keys
    elif len(sys.argv) == 2:
        print "1 argument: requested log plotting for directory:",sys.argv[1]
        print_usage()

    # At least 1
    else:
        log_directory = sys.argv[1]
        prefixes = sys.argv[2:]

        comparisons = log_preprocessing(log_directory, prefixes)

        stats = {}
        for p in prefixes:
            stats[p] = average_statistics_for_prefix(p, comparisons)
        keys = stats[prefixes[0]].keys()

        plt.close("all")
        pdf = create_pdf("output.pdf")

        for k in keys:
            label_plots = {}
            for key in stats.keys():
                label_plots[key] = stats[key][k]

            fig = plot_property(k, label_plots)
            pdf = plot_figure_to_pdf(pdf, fig)
            plt.close(fig)

        close_pdf(pdf)