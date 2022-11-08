import argparse
import json

from main import PIQARD
from test.real_time_qa.evaluate import RealTimeQAEvaluator
from utils import load_jsonl, save_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", nargs='?', default="./test/real_time_qa/20220617_qa.jsonl", help="benchamark path")
    parser.add_argument("--output", default="./result/20220617_qa.json", help="output path for results")
    args = parser.parse_args()

    benchmark = load_jsonl(args.benchmark)

    piqard = PIQARD()
    evaluator = RealTimeQAEvaluator(piqard, with_passage=True)
    results = evaluator.evaluate(benchmark)
    save_results(args.output, results)

