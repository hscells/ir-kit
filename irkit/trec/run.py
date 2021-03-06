"""
Functions and classes for dealing with trec_eval run files. For a description on how run files 
look, see: http://faculty.washington.edu/levow/courses/ling573_SPR2011/hw/trec_eval_desc.htm

Usage:

>>> sample_run = '''351   0  DOC1  1   100   run-name\\n351   0  DOC2  2   50   run-name'''
>>> runs = loads(sample_run)
>>> runs.dumps()
'351\tQ0\tDOC1\t1\t100\trun-name\n351\tQ0\tDOC2\t2\t50\trun-name'
>>> [str(run) for run in runs.runs]
['351\tQ0\tDOC1\t1\t100\trun-name', '351\tQ0\tDOC2\t2\t50\trun-name']
>>> [str(run) for run in runs['351']]
['351\tQ0\tDOC1\t1\t100\trun-name', '351\tQ0\tDOC2\t2\t50\trun-name']
>>> runs.rank
['1', '2']
>>> TrecEvalRuns(runs['351']).rank
['1', '2']

Harry Scells
May 2017
"""
import io

import os
from typing import List


class TrecEvalRun(object):
    """
    TrecEvalRun is a container class for a line in a trec_eval run file.
    """

    def __init__(self, topic: str, q: int, doc_id: str, rank: int, score: float, run_id: str):
        self.topic = topic
        self.q = q
        self.doc_id = doc_id
        self.rank = rank
        self.score = score
        self.run_id = run_id

    def __str__(self):
        return '{}\tQ{}\t{}\t{}\t{}\t{}'.format(self.topic, self.q, self.doc_id, self.rank,
                                                self.score, self.run_id)


class TrecEvalRuns(object):
    """
    TrecEvalRuns is a wrapper around a TrecEvalRun which is just a container class for a line in
    a trec_eval run file. This class contains some convenience functions for dealing with runs, 
    such as getting a list of the runs but topic id or slicing by column.
    """

    def __init__(self, runs: List[TrecEvalRun]):
        self.runs = runs

    def __getattr__(self, field):
        """
        Access a column of the runs by accessing the fields in a run.
        
        :param field: One of the attributes (fields) of the qrel
        :return: The column for the field (i.e. only the topics, or only the document_num)
        """
        return [x.__getattribute__(field) for x in self.runs]

    def __setitem__(self, key, value):
        raise Exception('Cannot set run values')

    def __delattr__(self, topic):
        self.runs = [x for x in self.runs if x.topic != topic]

    def __getitem__(self, topic):
        """
        Allow runs to be indexed by topic id.
        
        :param topic: The topic
        :return: The rows of this topic
        """
        return [x for x in self.runs if x.topic == topic]

    def __str__(self):
        return os.linesep.join([str(run) for run in self.runs])

    def dumps(self) -> str:
        """
        Dump the qrels to a string.
        
        :return: Formatted qrels
        """
        return str(self)

    def dump(self, fp: io.TextIOWrapper) -> None:
        """
        Dump the qrels to a file
        
        :param fp: A File pointer
        """
        fp.writelines(self.dumps())


def loads(runs: str) -> TrecEvalRuns:
    """
    Load a trec_eval run file from a string.
    
    :param runs: A string containing runs.
    :return: TrecEvalRuns
    """
    data = []
    for line in runs.split(os.linesep):
        if len(line.split()) > 0:
            topic, q, doc_id, rank, score, run_id = line.split()
            data.append(TrecEvalRun(topic, q, doc_id, rank, score, run_id))
    return TrecEvalRuns(data)


def load(runs: io.TextIOWrapper) -> TrecEvalRuns:
    """
    Load a trec_eval run file.
    
    :param runs: A file pointer containing runs.
    :return: TrecEvalRuns
    """
    return loads(runs.read())
