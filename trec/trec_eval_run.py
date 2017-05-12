"""

Harry Scells
May 2017
"""


class TrecEvalRun(object):
    def __init__(self, topic: str, doc_id: str, rank: int, score: float, run_id: str):
        self.run_id = run_id
        self.score = score
        self.rank = rank
        self.doc_id = doc_id
        self.topic = topic

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}'.format(self.topic, self.doc_id, self.rank, self.score,
                                           self.run_id)
