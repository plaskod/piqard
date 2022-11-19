import argparse

from config_loader.config_loader import ConfigLoader
from test.openbookqa.evaluate import OpenBookQAEvaluator
from test.realtimeqa.evaluate import RealTimeQAEvaluator
from utils import load_jsonl, save_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        nargs="?",
        type=str,
        help="query",
        default="./test/openbookqa/openbookqa_config.yaml",
    )
    parser.add_argument(
        "--output", default="./result/result.json", help="output path for results"
    )
    args = parser.parse_args()

    benchmark_configs = {
        "realtimeqa": {
            "path": "./test/realtimeqa/20220617_qa.jsonl",
            "evaluator": RealTimeQAEvaluator,
        },
        "openbookqa": {
            "path": "./test/openbookqa/test.jsonl",
            "evaluator": OpenBookQAEvaluator,
        },
    }

    config_loader = ConfigLoader()
    config = config_loader.load(args.config)

    if config.benchmark not in benchmark_configs.keys():
        print(f"Benchmark {args.benchmark} is not implemented")
        exit(0)

    benchmark = load_jsonl(benchmark_configs[config.benchmark]["path"])

    piqard = config.piqard
    evaluator = benchmark_configs[config.benchmark]["evaluator"](piqard)
    results = evaluator.evaluate(benchmark)
    save_results(args.output, results)
