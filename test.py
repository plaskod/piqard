import argparse

from benchmarks.hotpotqa.evaluate import HotPotQAEvaluator
from benchmarks.openbookqa.evaluate import OpenBookQAEvaluator
from benchmarks.realtimeqa.evaluate import RealTimeQAEvaluator
from piqard.PIQARD_loader import PIQARDLoader
from utils import load_jsonl, save_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "benchmark", type=str, help="benchmark"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="query",
        default="./benchmarks/openbookqa/openbookqa_config.yaml",
    )
    parser.add_argument(
        "--output", default="./result/result.json", help="output path for results"
    )
    args = parser.parse_args()

    benchmark_configs = {
        "realtimeqa": {
            "path": "./benchmarks/realtimeqa/20220617_qa.jsonl",
            "evaluator": RealTimeQAEvaluator,
        },
        "openbookqa": {
            "path": "./benchmarks/openbookqa/test.jsonl",
            "evaluator": OpenBookQAEvaluator,
        },
        "hotpotqa": {
            "path": "./benchmarks/hotpotqa/queries_30.jsonl",
            "evaluator": HotPotQAEvaluator,
        },
    }

    if args.benchmark not in benchmark_configs.keys():
        print(f"Benchmark {args.benchmark} is not implemented")
        exit(0)

    benchmark = load_jsonl(benchmark_configs[args.benchmark]["path"])

    piqard_loader = PIQARDLoader()
    piqard = piqard_loader.load(args.config)
    evaluator = benchmark_configs[args.benchmark]["evaluator"](piqard)
    results = evaluator.evaluate(benchmark)
    save_results(args.output, results)
