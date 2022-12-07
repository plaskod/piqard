import os
import sys
import inspect


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

    language_models = [CohereAPI(stop_token="|||"), BLOOM176bAPI(stop_token="|||")]
    prompting_templates_dir = "assets/prompting_templates/openbookqa/chain_of_thought"

    for language_model in language_models:
        for n in [1, 3, 5]:
            piqard = PIQARD(PromptTemplate(f"{prompting_templates_dir}/cot_{n}_shot.txt",
                                           fix_text="So the final answer is:"),
                            language_model)
            benchmark_evaluator = BenchmarkEvaluator(piqard)
            results = benchmark_evaluator.evaluate(benchmark,
                                                   f"result/openbookqa/experiments/chain_of_thought/{language_model}/{n}_shot_checkpoint.jsonl")
            save_results(f"result/openbookqa/experiments/chain_of_thought/{language_model}/{n}_shot.json", results)
