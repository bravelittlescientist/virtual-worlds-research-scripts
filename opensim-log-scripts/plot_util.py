#!/usr/bin/python

import sys

import matplotlib.pyplot as plt

def plot_multiline_graph(entries=3601, lines=[], labels=[], title="", xlabel="", ylabel="", plotLegend=True):
    """ Plots line chart of metrics over time """
    for i in range(len(lines)):
        plt.plot([e for e in range(entries)], lines[i], label=labels[i])

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)

    if plotLegend:
        legend = plt.legend(loc='lower right', shadow=True)

    plt.show()

def example_line_plot():
    """ An example multi-line graph with randomly generated values """
    # Labels and Legend
    xlabel = "X Label (units)"
    ylabel = "Y Label (units)"
    title = "Example Graph Title"
    doLegend = True

    lines = [range(low,low+10) for low in range(3)]
    labels = ["label " + str(n) for n in range(3)]
    entryN = len(lines[0])

    plot_multiline_graph(entries=entryN, lines=lines, labels=labels, title=title, xlabel=xlabel, ylabel=ylabel, plotLegend=doLegend)

if __name__ == "__main__":
    example_line_plot()
