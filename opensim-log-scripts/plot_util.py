#!/usr/bin/python

import sys

import numpy as np
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

def plot_multibar_chart(bars, labels, title, xlabel, ylabel):
    """ Plots bar chart with multiple bars """

    index = np.arange(len(bars[0]))
    fig, ax = plt.subplots()
    bar_width = .2

    colors = ['r', 'g', 'b', 'y']

    # Go through sublists to generate rectangles:
    for b in range(len(bars)):
        plt.bar(index + b*bar_width,
                tuple(bars[b]),
                bar_width,
                color = colors[b],
                label = labels[b])

    #plt.xlabel('Group')
    #plt.ylabel('Scores')
    #plt.title('Scores by group and gender')

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(index+bar_width)
    ax.set_xticklabels(('10', '50', '100'))
    plt.legend(loc='upper left')

    plt.tight_layout()
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

def example_bar_chart():
    """ An example bar chart with randomly generated values """
    xlabel = "X Label (units)"
    ylabel = "Y Label (units)"
    titlex = "Example Graph Title"
    doLegend = True

    bar_data = [(1,2,3),(2,3,4),(3,4,5),(4,5,6)]
    labels = ["label 1", "label 2", "label 3", "label 4"]
    plot_multibar_chart(bar_data, labels, titlex, xlabel, ylabel)

if __name__ == "__main__":
    example_bar_chart()
