import argparse

from benchmarks.benchmark_evaluator import BenchmarkEvaluator
from database_loaders.database_loader_factory import DataBaseLoaderFactory
from piqard.PIQARD_loader import PIQARDLoader
from utils import save_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark", type=str, help="benchmark")
    parser.add_argument(
        "--config",
        type=str,
        help="query",
        default="./assets/configs/config.yaml",
    )
    parser.add_argument(
        "--output", default="./result/result.json", help="output path for results"
    )
    args = parser.parse_args()

    database_loader = DataBaseLoaderFactory(args.benchmark)
    benchmark = database_loader.load_questions(test=True, number=30)

    piqard_loader = PIQARDLoader()
    piqard = piqard_loader.load(args.config)

    benchmark_evaluator = BenchmarkEvaluator(piqard)
    results = benchmark_evaluator.evaluate(
        benchmark, args.output.replace(".json", "_checkpoint.jsonl")
    )
    save_results(args.output, results)
