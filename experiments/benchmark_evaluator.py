import json
import string
import time
from collections import Counter
from pathlib import Path

import tqdm
from nltk.translate.bleu_score import sentence_bleu

from piqard.PIQARD import PIQARD
from piqard.utils.exceptions import Response500Exception, LanguageModelAPIOverloadException
from piqard.utils.io import directory, load_jsonl


class BenchmarkEvaluator:
    """
    BenchmarkEvaluator is a class that evaluates the performance of a PIQARD model on a given benchmark.
    """
    def __init__(self, piqard: PIQARD):
        """
        Constructor of the BenchmarkEvaluator class.

        :param piqard: PIQARD model to evaluate.
        """
        self.piqard = piqard

    def query(self, question: dict) -> dict:
        """
        Query the PIQARD model with a question.

        :param: question: Question to query the PIQARD model with.
        :return: Query result.
        """
        result = self.piqard(question["text"], question["possible_answers"])
        return {
            "id": question["id"],
            "question": question["text"],
            "possible_answers": question["possible_answers"],
            "answer": question["answer"],
            "context": result["context"],
            "predicted_answer": result["answer"],
            "raw_predicted_answer": result["raw_answer"],
            "chain_trace": result["chain_trace"].to_json(),
        }

    def evaluate(self, benchmark: list[dict], checkpoint: str = None) -> dict:
        """
        Evaluate the PIQARD model on a given benchmark.

        :param benchmark: Questions to evaluate the PIQARD model on.
        :param checkpoint: Checkpoint to load the actual results of evaluation.
        :return: Evaluation results.
        """
        results = []
        if checkpoint:
            results = self.from_checkpoint(checkpoint)
            checkpoint = open(checkpoint, "a+")

        for question in tqdm.tqdm(
            benchmark[len(results):], desc="Processing questions: "
        ):
            done = False
            while not done:
                try:
                    question_result = self.query(question)
                    results.append(question_result)
                    done = True
                except (LanguageModelAPIOverloadException, Response500Exception) as e:
                    print(
                        e.message + f"... waiting 10s"
                    )
                    time.sleep(10)

            if checkpoint:
                checkpoint.write(json.dumps(question_result) + "\n")

        if checkpoint:
            checkpoint.close()

        scores = self.gen_eval(results)
        return {"scores": scores, "report": results}

    @staticmethod
    def from_checkpoint(checkpoint: str) -> list[dict]:
        """
        Load the results of evaluation from a checkpoint.

        :param checkpoint: Checkpoint to load the results of evaluation from.
        :return: Results of evaluation from checkpoint.
        """
        _ = directory("/".join(checkpoint.split("/")[:-1]))
        Path(checkpoint).touch(exist_ok=True)
        return load_jsonl(checkpoint)

    @staticmethod
    def accuracy(results: list[tuple[str, str]]) -> dict:
        """
        Compute the accuracy of the PIQARD model on a given benchmark.

        :param results: Results of evaluation.
        :return: Accuracy of the PIQARD model on a given benchmark.
        """
        acc = sum(
            [prediction == ground_truth for prediction, ground_truth in results]
        ) / len(results)
        return {"accuracy": acc}

    def gen_eval(self, results: list[dict]) -> dict:
        """
        Compute the evaluation metrics of the PIQARD model on a given benchmark.

        :param results: Results of evaluation.
        :return: Evaluation metrics of the PIQARD model on a given benchmark.
        """
        em_total, cem_total, f1_total = 0, 0, 0
        bleu1_total, bleu2_total, bleu3_total = 0, 0, 0
        count = len(results)
        for result in results:
            prediction, ground_truth = result["predicted_answer"], result["answer"]
            em_total += self.exact_match_score(prediction, ground_truth)
            cem_total += self.cover_exact_match_score(prediction, ground_truth)
            f1_total += self.f1_score(prediction, ground_truth)
            bleu1_total += self.bleu_score(prediction, ground_truth, n=1)
            bleu2_total += self.bleu_score(prediction, ground_truth, n=2)
            bleu3_total += self.bleu_score(prediction, ground_truth, n=3)
        return {
            "Exact match": em_total / count,
            "Cover Exact Match": cem_total / count,
            "F1": f1_total / count,
            "Bleu-1": bleu1_total / count,
            "Bleu-2": bleu2_total / count,
            "Bleu-3": bleu3_total / count
        }

    def exact_match_score(self, prediction: str, ground_truth: str) -> int:
        """
        Compute the exact match score of the PIQARD model on a given question.

        :param prediction: Prediction of the PIQARD model.
        :param ground_truth: Ground truth.
        :return: Exact match score of the PIQARD model on a given question.
        """
        return self.__normalize_answer(prediction) == self.__normalize_answer(
            ground_truth
        )

    def f1_score(self, prediction: str, ground_truth: str) -> float:
        """
        Compute the F1 score of the PIQARD model on a given question.

        :param prediction: Prediction of the PIQARD model.
        :param ground_truth: Ground truth.
        :return: F1 score of the PIQARD model on a given question.
        """
        prediction_tokens = self.__normalize_answer(prediction).split()
        ground_truth_tokens = self.__normalize_answer(ground_truth).split()
        common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
        num_same = sum(common.values())

        if num_same == 0:
            return 0
        precision = 1.0 * num_same / len(prediction_tokens)
        recall = 1.0 * num_same / len(ground_truth_tokens)
        f1 = (2 * precision * recall) / (precision + recall)
        return f1

    def cover_exact_match_score(self, prediction: str, ground_truth: str) -> int:
        """
        Compute the cover exact match score of the PIQARD model on a given question.

        :param prediction: Prediction of the PIQARD model.
        :param ground_truth: Ground truth.
        :return: Cover exact match score of the PIQARD model on a given question.
        """
        return (
            1
            if self.__normalize_answer(prediction).find(
                self.__normalize_answer(ground_truth)
            )
            != -1
            else 0
        )

    def bleu_score(self, prediction: str, ground_truth: str, n: int = 1) -> float:
        """
        Compute the BLEU score of the PIQARD model on a given question.

        :param prediction: Prediction of the PIQARD model.
        :param ground_truth: Ground truth.
        :param n: N-gram order.
        :return: BLEU score of the PIQARD model on a given question.
        """
        prediction_tokens = self.__normalize_answer(prediction).split()
        ground_truth_tokens = self.__normalize_answer(ground_truth).split()
        weights = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)]
        return sentence_bleu([ground_truth_tokens], prediction_tokens, weights=weights[n - 1])

    @staticmethod
    def __normalize_answer(answer: str) -> str:
        """
        Normalize the answer.

        :param answer: Answer to normalize.
        :return: Normalized answer.
        """
        def remove_counter(text):
            return (
                text.replace("年", "").replace("歳", "").replace("人", "").replace("년", "")
            )

        def white_space_fix(text):
            return " ".join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return "".join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_counter(remove_punc(lower(answer))))
