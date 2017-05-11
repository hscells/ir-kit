"""
Functions and classes for dealing with trec_eval results files.

Harry Scells
Mar 2017
"""
import io
import os
from typing import Dict

eval_fields = {'num_q': int,
               'num_ret': int,
               'num_rel': int,
               'num_rel_ret': int,
               'map': float,
               'gm_map': float,
               'Rprec': float,
               'bpref': float,
               'recip_rank': float,
               'iprec_at_recall_0.00': float,
               'iprec_at_recall_0.10': float,
               'iprec_at_recall_0.20': float,
               'iprec_at_recall_0.30': float,
               'iprec_at_recall_0.40': float,
               'iprec_at_recall_0.50': float,
               'iprec_at_recall_0.60': float,
               'iprec_at_recall_0.70': float,
               'iprec_at_recall_0.80': float,
               'iprec_at_recall_0.90': float,
               'iprec_at_recall_1.00': float,
               'P_5': float,
               'P_10': float,
               'P_15': float,
               'P_20': float,
               'P_30': float,
               'P_100': float,
               'P_200': float,
               'P_500': float,
               'P_1000': float}


class TrecEvalResults:
    """
    An object that stores the results output by trec_eval.
    """

    def __init__(self, run_id: str, results: Dict, queries: Dict):
        self.run_id = run_id
        self.results = results
        self.queries = queries

    def __getitem__(self, query):
        """
        Allow trec results to be indexed by query num.
        :param query: The query to search
        :return: The rows of this topic
        """
        return self.queries[query]


def loads(trec_results: str) -> TrecEvalResults:
    """
    Load trec_eval results from a string.
    :param trec_results: Some string representation of trec results
    :return: TrecEvalResults object
    """
    run_id = ''
    results = {}
    queries = {}

    for line in trec_results.split(os.linesep):
        if not line.strip():
            continue
        field, query, value = line.split()
        if query == 'all':  # accumulated results over all queries
            if field == 'runid':
                run_id = value
            else:
                results[field] = value
        else:
            if query not in queries:
                queries[query] = {}
            queries[query][field] = float(value)

    return TrecEvalResults(run_id, results, queries)


def load(trec_result_file: io.IOBase) -> TrecEvalResults:
    """
    Load trec_eval results from a file.
    :param trec_result_file: File pointer
    :return: Qrels object
    """
    return loads(os.linesep.join(trec_result_file.readlines()))