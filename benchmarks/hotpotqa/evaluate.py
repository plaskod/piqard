import tqdm

from piqard.PIQARD import PIQARD
from benchmarks.evaluator import Evaluator


class HotPotQAEvaluator(Evaluator):
    def __init__(self, piqard: PIQARD):
        super().__init__(piqard)

    def preprocess(self, question: dict) -> tuple[str, str]:
        question_sentence = question["text"]
        answer = question["metadata"]["answer"]
        return question_sentence, answer

    def evaluate_question(self, question: dict) -> dict:
        question_sentence, answer = self.preprocess(question)
        predicted_answer, context = self.predict(question_sentence)
        return {
                "id": question['_id'],
                "question": question_sentence,
                "answer": answer,
                "context": context,
                "predicted_answer": predicted_answer,
            }