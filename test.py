import argparse

from main import PIQARD
from test.open_book_qa.evaluate import OpenBookQAEvaluator
from test.real_time_qa.evaluate import RealTimeQAEvaluator
from utils import load_jsonl, save_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "benchmark", nargs="?", default="realtimeqa", help="benchamark name"
    )
    parser.add_argument(
        "--output", default="./result/result.json", help="output path for results"
    )
    args = parser.parse_args()

    benchmark_configs = {
        "realtimeqa": {
            "path": "./test/real_time_qa/20220617_qa.jsonl",
            "evaluator": RealTimeQAEvaluator,
        },
        "openbookqa": {
            "path": "./test/open_book_qa/test_30.jsonl",
            "evaluator": OpenBookQAEvaluator,
        },
    }

    if args.benchmark not in benchmark_configs.keys():
        print(f"Benchmark {args.benchmark} is not implemented")
        exit(0)

    benchmark = load_jsonl(benchmark_configs[args.benchmark]["path"])

    piqard = PIQARD()
    evaluator = benchmark_configs[args.benchmark]["evaluator"](piqard)
    results = evaluator.evaluate(benchmark)
    save_results(args.output, results)
