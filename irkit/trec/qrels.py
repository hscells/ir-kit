"""
Functions and classes for dealing with English qrel files. The specification can be viewed at:
http://trec.nist.gov/data/qrels_eng/

>>> sample_qrels = '1 0 AP880212-0161 0\\n1 0 AP880216-0139 1\\n1 0 AP880216-0169 0'
>>> qrels = loads(sample_qrels)
>>> qrels.topic
['1', '1', '1']

>>> [x.topic for x in qrels['1']]
['1', '1', '1']

Harry Scells
Mar 2017
"""

import io

import os
from typing import List


class Qrel:
    """
    A line in a qrels file conforming to the specification at:
    http://trec.nist.gov/data/qrels_eng/
    """

    def __init__(self, topic: str, iteration: int, document_num: str, relevancy: int):
        self.topic = topic
        self.iteration = iteration
        self.document_num = document_num
        self.relevancy = relevancy

    def __str__(self):
        return '{} {} {} {}'.format(self.topic, self.iteration,
                                    self.document_num, self.relevancy)


class Qrels:
    """
    A python representation of a qrels file. It is a list of Qrel objects.
    """

    def __init__(self, qrels: List[Qrel]):
        self.qrels = qrels

    def __getattr__(self, field):
        """
        Access a column of the qrels by accessing the fields in a Qrel.
        :param field: One of the attributes (fields) of the qrel
        :return: The column for the field (i.e. only the topics, or only the document_num)
        """
        return [x.__getattribute__(field) for x in self.qrels]

    def __setitem__(self, key, value):
        raise Exception('Cannot set qrel values')

    def __delattr__(self, topic):
        self.qrels = [x for x in self.qrels if x.topic != topic]

    def __getitem__(self, topic):
        """
        Allow qrels to be indexed by topic id.
        :param topic: The topic
        :return: The rows of this topic
        """
        return [x for x in self.qrels if x.topic == topic]

    def __str__(self):
        return os.linesep.join([str(x) for x in self.qrels])

    def dumps(self):
        """
        Dump the qrels to a string.
        :return: Formatted qrels
        """
        return str(self)

    def dump(self, fp: io.IOBase):
        """
        Dump the qrels to a file
        :param fp: A File pointer
        """
        fp.writelines(self.dumps())


def loads(qrels: str) -> Qrels:
    """
    Load qrels from a string.
    :param qrels: Some string representation of qrels
    :return: Qrels object
    """
    data = []
    for line in qrels.split(os.linesep):
        if len(line.split()) > 0:
            topic, iteration, document_num, relevancy = line.split()
            data.append(Qrel(topic, int(iteration), document_num, int(relevancy)))
    return Qrels(data)


def load(qrels: io.IOBase) -> Qrels:
    """
    Load qrels from a file.
    :param qrels: File pointer
    :return: Qrels object
    """
    return loads(os.linesep.join(qrels.readlines()))
