import os
import sys
import inspect
from collections import defaultdict



currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from experiments.benchmark_evaluator import BenchmarkEvaluator
from utils import save_results
from database_loaders.database_loader_factory import DataBaseLoaderFactory
from piqard.PIQARD import PIQARD
from piqard.information_retrievers.annoy_retriver import AnnoyRetriever
from piqard.information_retrievers.ranking_retriever import RankingRetriever
from piqard.information_retrievers.vector_retirever import VectorRetriever
from piqard.language_models.bloom_176b_api import BLOOM176bAPI
from piqard.language_models.cohere_api import CohereAPI
from piqard.utils.prompt_template import PromptTemplate


if __name__ == "__main__":
    database_loader = DataBaseLoaderFactory("openbookqa")
    benchmark = database_loader.load_questions(test=True)

    language_models = [CohereAPI(stop_token="\n"), BLOOM176bAPI(stop_token="\n")]
    information_retrievers = [VectorRetriever]
    prompting_tempates_dir = "assets/prompting_templates/openbookqa/permutations/"

    for language_model in language_models:
        for information_retriever in information_retrievers:
            results_agg = {}
            for n in range(1, 7):
                retriver = information_retriever("openbookqa")
                piqard = PIQARD(PromptTemplate(f"{prompting_tempates_dir}permutation_{n}.txt"),
                                language_model,
                                retriver)
                benchmark_evaluator = BenchmarkEvaluator(piqard)
                results = benchmark_evaluator.evaluate(benchmark,
                                                       f"result/openbookqa/experiments/permutations/{language_model}/{retriver}/permutations_{n}_checkpoint.jsonl")
                save_results(f"result/openbookqa/experiments/permutations/{language_model}/{retriver}/permutations_{n}.json", results)

                results_agg[f"{n}_shot"] = results['report']

            consistency = defaultdict(int)
            for i in range(len(benchmark)):
                consistency[len(set([question[i]['predicted_answer'] for question in results_agg.values()]))] += 1
            save_results(f"result/openbookqa/experiments/permutations/{language_model}/{retriver}/consistency_report.json",
                         {"percent_of_consistent_answers": consistency[1] / len(benchmark),
                          "numbers_of_unique_answers": consistency})