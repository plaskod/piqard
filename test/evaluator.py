from collections import Counter

from utils import normalize_answer


class Evaluator:
    def preprocess(self, benchmark: list[dict]) -> list[dict]:
        pass

    def predict(self, question: str, passage: str) -> str:
        pass

    def evaluate(self, benchmark: list[dict]) -> dict:
        pass

    def accuracy(self, results: list[tuple[str, str]]) -> dict:
        acc = sum(
            [prediction == ground_truth for prediction, ground_truth in results]
        ) / len(results)
        return {"accuracy": acc}

    def gen_eval(self, results: list[tuple[str, str]]) -> dict:
        em_total, cem_total, f1_total = 0, 0, 0
        count = len(results)
        for prediction, ground_truth in results:
            em_total += self.exact_match_score(prediction, ground_truth)
            cem_total += self.cover_exact_match_score(prediction, ground_truth)
            f1_total += self.f1_score(prediction, ground_truth)
        return {"Exact match": em_total / count, "Cover Exact Match": cem_total / count, "F1": f1_total / count}

    @staticmethod
    def exact_match_score(prediction: str, ground_truth: str) -> int:
        return normalize_answer(prediction) == normalize_answer(ground_truth)

    @staticmethod
    def f1_score(prediction: str, ground_truth: str) -> float:
        prediction_tokens = normalize_answer(prediction).split()
        ground_truth_tokens = normalize_answer(ground_truth).split()
        common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
        num_same = sum(common.values())

        if num_same == 0:
            return 0
        precision = 1.0 * num_same / len(prediction_tokens)
        recall = 1.0 * num_same / len(ground_truth_tokens)
        f1 = (2 * precision * recall) / (precision + recall)
        return f1

    @staticmethod
    def cover_exact_match_score(prediction: str, ground_truth: str) -> int:
        return 1 if normalize_answer(prediction).find(normalize_answer(ground_truth)) != -1 else 0
