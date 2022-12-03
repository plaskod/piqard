import os
import sys
import inspect
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import glob
from benchmarks.openbookqa.evaluate import OpenBookQAEvaluator
from piqard.PIQARD_loader import PIQARDLoader
from utils import load_jsonl, save_results


if __name__ == "__main__":
    benchmark = load_jsonl("./benchmarks/openbookqa/test.jsonl")

    results_agg = {}
    piqard_loader = PIQARDLoader()
    for config in glob.glob("assets/configs/openbookqa/permutations/*.yaml"):
        name = config.split("\\")[-1].replace(".yaml", "")
        piqard = piqard_loader.load(config)
        evaluator = OpenBookQAEvaluator(piqard)
        results = evaluator.evaluate(benchmark, f"result/openbookqa/experiments/permutations/{name}_checkpoint.jsonl")
        results_agg[name] = results['report']
        save_results(f"result/openbookqa/experiments/permutations/{name}.json", results)

    consistency = defaultdict(int)
    for i in range(len(benchmark)):
        consistency[len(set([question[i]['predicted_answer'] for question in results_agg.values()]))] += 1
    save_results(f"result/openbookqa/experiments/permutations/consistency_report.json", {"percent_of_consistent_answers": consistency[1] / len(benchmark),
                                                                                         "numbers_of_unique_answers": consistency})
