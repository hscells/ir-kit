"""
Functions and classes for dealing with trec_eval results files.

Harry Scells
Mar 2017
"""
import io

import os
from typing import Dict


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


def load(trec_result_file: io.TextIOWrapper) -> TrecEvalResults:
    """
    Load trec_eval results from a file.
    
    :param trec_result_file: File pointer
    :return: Qrels object
    """
    return loads(os.linesep.join(trec_result_file.readlines()))
