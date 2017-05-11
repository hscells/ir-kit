"""
Various plotting functions.

Harry Scells
Mar 2017
"""

import argparse
import re

import numpy as np
import matplotlib.pyplot as plt
from typing import List

try:
    from trec import trec_eval_results
    from trec.trec_eval_results import TrecEvalResults
except ImportError:
    from irkit.trec import trec_eval_results
    from irkit.trec.trec_eval_results import TrecEvalResults


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

    plt.xlabel('Recall')
    plt.ylabel('Interpolated Precision')

    for p in iprec:
        plt.plot(recall, p)

    plt.legend(names)
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

        # plt.savefig(outfile, bbox_inches='tight')
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


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--trec_results', help='trec_eval results files',
                           required=True, type=argparse.FileType('r'), nargs='+')

    args = argparser.parse_args()

    pr_curve([trec_eval_results.load(f) for f in args.trec_results]).savefig('output',
                                                                             bbox_inches='tight')
