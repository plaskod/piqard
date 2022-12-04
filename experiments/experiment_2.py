import os
import sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import glob
from piqard.PIQARD_loader import PIQARDLoader
from utils import save_results
from experiments.benchmark_evaluator import BenchmarkEvaluator
from database_loaders.database_loader_factory import DataBaseLoaderFactory

if __name__ == "__main__":
    database_loader = DataBaseLoaderFactory("openbookqa")
    benchmark = database_loader.load_questions(test=True)

    piqard_loader = PIQARDLoader()
    for config in glob.glob("assets/configs/openbookqa/n_shots/*.yaml"):
        name = config.split("\\")[-1].replace(".yaml", "")
        piqard = piqard_loader.load(config)
        benchmark_evaluator = BenchmarkEvaluator(piqard)
        results = benchmark_evaluator.evaluate(benchmark, f"result/openbookqa/experiments/n_shots/{name}_checkpoint.jsonl")
        save_results(f"result/openbookqa/experiments/n_shots/{name}.json", results)
