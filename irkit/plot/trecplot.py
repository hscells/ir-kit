"""
Various plotting functions.

Harry Scells
Mar 2017
"""

import re

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from typing import List

from irkit.trec.results import TrecEvalResults

# This causes matplotlib to use Type 42 (a.k.a. TrueType) fonts for PostScript and PDF files.
# This allows you to avoid Type 3 fonts without limiting yourself to the stone-age technology
# of Type 1 fonts.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

plt.style.use('grayscale')
plt.style.use('seaborn-poster')
plt.style.use('seaborn-white')


def pr_curve(results: List[TrecEvalResults]) -> plt:
    """
    Create a precision-recall graph from trec_eval results.
    :param results: A list of TrecEvalResults files
    :return: a matplotlib plt object
    """

    names = [r.run_id for r in results]
    iprec = [[r.results['iprec_at_recall_0.00'],
              r.results['iprec_at_recall_0.10'],
              r.results['iprec_at_recall_0.20'],
              r.results['iprec_at_recall_0.30'],
              r.results['iprec_at_recall_0.40'],
              r.results['iprec_at_recall_0.50'],
              r.results['iprec_at_recall_0.60'],
              r.results['iprec_at_recall_0.70'],
              r.results['iprec_at_recall_0.80'],
              r.results['iprec_at_recall_0.90'],
              r.results['iprec_at_recall_1.00']] for r in results]

    recall = np.arange(0, 1.1, 0.1)

    mpl.rc('xtick', labelsize=35)
    mpl.rc('ytick', labelsize=35)

    plt.xlabel('Recall', fontsize=35)
    plt.ylabel('Interpolated Precision', fontsize=35)

    for p in iprec:
        plt.plot(recall, p, linewidth=10)

    plt.legend(names, fontsize=35)
    return plt


def topic_ap(results: List[TrecEvalResults], sort_on_ap=False):
    """

    :param results:
    :param sort_on_ap:
    :return:
    """

    def natural_sort(l):
        """

        :param l: List to sort
        :return: naturally sorted list
        """

        def convert(text):
            return int(text) if text.isdigit() else text.lower()

        def alphanum_key(key):
            return [convert(c) for c in re.split('([0-9]+)', key)]

        return sorted(l, key=alphanum_key)

    # noinspection PyShadowingNames
    # we really don't care about shadowing names in this case
    def plot(ap, ylabel, topic_names, sort_on_ap=False):
        """

        :param ap:
        :param ylabel:
        :param topic_names:
        :param sort_on_ap:
        :return:
        """
        if sort_on_ap:
            topic_names = [n for (d, n) in sorted(zip(ap, topic_names), reverse=True)]
            ap = sorted(ap, reverse=True)

        ind = np.arange(len(topic_names))
        width = 1.0
        plt.bar(ind, ap, width)
        plt.xticks(ind + 0.5 * width, topic_names, fontsize=10, rotation='vertical')
        plt.ylabel(ylabel)
        plt.xlabel('Topic')

        return plt

    if len(results) == 2:
        r1 = results[0]
        r2 = results[1]
        assert all([k in r2.queries for k in r1.queries.keys()]), 'Topic set is not the same!'
        assert all([k in r1.queries for k in r2.queries.keys()]), 'Topic set is not the same!'

        topic_names = natural_sort(r1.queries.keys())

        ap1 = np.array([r1.queries[q]['map'] for q in topic_names])
        ap2 = np.array([r2.queries[q]['map'] for q in topic_names])

        ap = ap1 - ap2
        ylabel = 'Average Precision difference'

        return plot(ap, ylabel, topic_names, sort_on_ap)
    elif len(results) == 1:
        r = results[0]
        topic_names = natural_sort(r.queries.keys())
        ap = np.array([r.queries[q]['map'] for q in topic_names])
        ylabel = 'Average Precision'

        return plot(ap, ylabel, topic_names, sort_on_ap)
    else:
        raise Exception('Can only plot either one or two TrecEvalResults objects.')
