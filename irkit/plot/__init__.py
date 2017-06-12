import argparse

from irkit.plot.trecplot import pr_curve

import irkit.trec.results


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--trec_results', help='trec_eval results files.',
                           required=True, type=argparse.FileType('r'), nargs='+')
    argparser.add_argument('--output', help='Name of the output file.', type=str,
                           default='output', required=False)

    args = argparser.parse_args()
    pr_curve([irkit.trec.results.load(f) for f in args.trec_results]).savefig('output',
                                                                              bbox_inches='tight')
