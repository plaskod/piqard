import os
import sys
import inspect
from collections import defaultdict


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from experiments.benchmark_evaluator import BenchmarkEvaluator
from database_loaders.database_loader_factory import DataBaseLoaderFactory
import glob
from piqard.PIQARD_loader import PIQARDLoader
from utils import save_results


if __name__ == "__main__":
    database_loader = DataBaseLoaderFactory("openbookqa")
    benchmark = database_loader.load_questions(test=True)

    results_agg = {}
    piqard_loader = PIQARDLoader()
    for config in glob.glob("assets/configs/openbookqa/permutations/*.yaml"):
        name = config.split("\\")[-1].replace(".yaml", "")
        piqard = piqard_loader.load(config)
        benchmark_evaluator = BenchmarkEvaluator(piqard)
        results = benchmark_evaluator.evaluate(benchmark, f"result/openbookqa/experiments/permutations/{name}_checkpoint.jsonl")
        results_agg[name] = results['report']
        save_results(f"result/openbookqa/experiments/permutations/{name}.json", results)

    consistency = defaultdict(int)
    for i in range(len(benchmark)):
        consistency[len(set([question[i]['predicted_answer'] for question in results_agg.values()]))] += 1
    save_results(f"result/openbookqa/experiments/permutations/consistency_report.json", {"percent_of_consistent_answers": consistency[1] / len(benchmark),
                                                                                         "numbers_of_unique_answers": consistency})
