"""

Harry Scells
May 2017
"""


class TrecEvalRun(object):
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
