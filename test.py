import argparse
import json

from main import PIQARD
from test.real_time_qa.evaluate import RealTimeQAEvaluator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", nargs='?', default="./test/real_time_qa/20220617_qa.jsonl", help="benchamark path")
    args = parser.parse_args()

    with open(args.benchmark, 'r') as f:
        benchmark = [json.loads(jline) for jline in f.read().splitlines()]

    piqard = PIQARD()
    evaluator = RealTimeQAEvaluator(piqard, with_passage=True)
    results = evaluator.evaluate(benchmark)
    print(results)

