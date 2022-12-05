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

    language_models = [CohereAPI(stop_token="\n"), BLOOM176bAPI(stop_token="\n")]
    information_retrievers = [AnnoyRetriever, RankingRetriever, VectorRetriever]
    prompting_tempates_dir = "assets/prompting_templates/openbookqa/"

    for language_model in language_models:
        for information_retriever in information_retrievers:
            for k in range(1, 4):
                retriver = information_retriever("openbookqa", k=k)
                piqard = PIQARD(PromptTemplate(f"{prompting_tempates_dir}5_shot_{k}_documents.txt"),
                                language_model,
                                retriver)
                benchmark_evaluator = BenchmarkEvaluator(piqard)
                results = benchmark_evaluator.evaluate(benchmark,
                                                       f"result/openbookqa/experiments/k_documents/{language_model}/{retriver}/{k}_documents_checkpoint.jsonl")
                save_results(f"result/openbookqa/experiments/k_documents/{language_model}/{retriver}/{k}_documents.json", results)

        piqard = PIQARD(PromptTemplate(f"{prompting_tempates_dir}5_shot_{0}_documents.txt"),
                        language_model)
        benchmark_evaluator = BenchmarkEvaluator(piqard)
        results = benchmark_evaluator.evaluate(benchmark,
                                               f"result/openbookqa/experiments/k_documents/{language_model}/0_documents_checkpoint.jsonl")
        save_results(f"result/openbookqa/experiments/k_documents/{language_model}/0_documents.json", results)