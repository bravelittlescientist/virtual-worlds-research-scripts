#!/usr/bin/python

from matplotlib.backends.backend_pdf import PdfPages

def pdf_create(output_filename):
    """ Creates and returns a PdfPages object with the provided name """
    pdf = PdfPages(output_filename)
    return pdf

def pdf_post(pdf):
    """ Given a pdf object, performs preprocessing and closes.

    Just closes, for now. """
    pdf.close()

def pdf_save_figure(pdf, figure):
    """ Given a pdf and a figure, writes figure to pdf and returns updated """
    pdf.savefig(figure)
    return pdf

if __name__ == "__main__":
    print "PDF generation utilities for OpenSimulator log visualization recording"
