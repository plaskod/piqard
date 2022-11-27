import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import glob
from benchmarks.openbookqa.evaluate import OpenBookQAEvaluator
from piqard.PIQARD_loader import PIQARDLoader
from utils import load_jsonl, save_results


if __name__ == "__main__":
    benchmark = load_jsonl("./benchmarks/openbookqa/test.jsonl")

    piqard_loader = PIQARDLoader()
    for config in glob.glob("assets/configs/openbookqa/n_shots/*.yaml"):
        name = config.split("\\")[-1].replace(".yaml", "")
        piqard = piqard_loader.load(config)
        evaluator = OpenBookQAEvaluator(piqard)
        results = evaluator.evaluate(benchmark, f"result/openbookqa/experiments/n_shots/{name}_checkpoint.jsonl")
        save_results(f"result/openbookqa/experiments/n_shots/{name}.json", results)
