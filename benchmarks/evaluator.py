import json
import string
import time
from collections import Counter
from pathlib import Path

import tqdm

from piqard.PIQARD import PIQARD
from piqard.language_models.language_model import LanguageModelAPIOverloadException
from utils import load_jsonl, directory


class Evaluator:
    def __init__(self, piqard: PIQARD):
        self.piqard = piqard

    def preprocess(self, benchmark: list[dict]) -> tuple[str, str, str]:
        pass

    def evaluate_question(self, question: dict) -> dict:
        pass

    def evaluate(self, benchmark: list[dict], checkpoint: str = None) -> dict:
        results = []
        if checkpoint:
            results = self.from_checkpoint(checkpoint)
            checkpoint = open(checkpoint, "a+")

        for question in tqdm.tqdm(benchmark[len(results):], desc="Processing questions: "):
            done = False
            while not done:
                try:
                    question_result = self.evaluate_question(question)
                    results.append(question_result)
                    done = True
                except LanguageModelAPIOverloadException:
                    print("\nAPI inference overload... waiting 60s")
                    time.sleep(60)

            if checkpoint:
                checkpoint.write(json.dumps(question_result) + '\n')

        if checkpoint:
            checkpoint.close()

        scores = self.gen_eval(results)
        return {"scores": scores, "report": results}

    @staticmethod
    def from_checkpoint(checkpoint: str) -> list[dict]:
        _ = directory("/".join(checkpoint.split('/')[:-1]))
        Path(checkpoint).touch(exist_ok=True)
        return load_jsonl(checkpoint)

    def predict(self, question: str, possible_answers: str = None) -> tuple[str, list[str]]:
        retrieved_documents = None
        if self.piqard.information_retriever is not None:
            retrieved_documents = self.piqard.information_retriever.get_documents(
                question
            )

        prompt = self.piqard.prompt_template.render(
            question=question, context=retrieved_documents, possible_answers=possible_answers
        )
        generated_answer = self.piqard.language_model.query(prompt)
        final_answer = generated_answer[0]["generated_text"][len(prompt):].split("\n")[
            0
        ]
        return final_answer, retrieved_documents

    @staticmethod
    def accuracy(results: list[tuple[str, str]]) -> dict:
        acc = sum(
            [prediction == ground_truth for prediction, ground_truth in results]
        ) / len(results)
        return {"accuracy": acc}

    def gen_eval(self, results: list[dict]) -> dict:
        em_total, cem_total, f1_total = 0, 0, 0
        count = len(results)
        for result in results:
            prediction, ground_truth = result['predicted_answer'], result['answer']
            em_total += self.exact_match_score(prediction, ground_truth)
            cem_total += self.cover_exact_match_score(prediction, ground_truth)
            f1_total += self.f1_score(prediction, ground_truth)
        return {
            "Exact match": em_total / count,
            "Cover Exact Match": cem_total / count,
            "F1": f1_total / count,
        }

    def exact_match_score(self, prediction: str, ground_truth: str) -> int:
        return self.__normalize_answer(prediction) == self.__normalize_answer(ground_truth)

    def f1_score(self, prediction: str, ground_truth: str) -> float:
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
        return (
            1
            if self.__normalize_answer(prediction).find(self.__normalize_answer(ground_truth)) != -1
            else 0
        )

    @staticmethod
    def __normalize_answer(answer: str) -> str:
        def remove_counter(text):
            return text.replace("年", "").replace("歳", "").replace("人", "").replace("년", "")

        def white_space_fix(text):
            return " ".join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return "".join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_counter(remove_punc(lower(answer))))
