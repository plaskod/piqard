import tqdm

from piqard.PIQARD import PIQARD
from benchmarks.evaluator import Evaluator


class RealTimeQAEvaluator(Evaluator):
    def __init__(self, piqard: PIQARD):
        super().__init__(piqard)

    def preprocess(self, question: dict) -> tuple[str, str, str]:
        question_sentence = question["question_sentence"]
        possible_answers = " ".join(
            [f"{idx}. {choice}" for idx, choice in enumerate(question["choices"])]
        )
        answer = f"{question['answer'][0]}. {question['choices'][int(question['answer'][0])]}"
        return question_sentence, possible_answers, answer

    def evaluate(self, benchamark: list[dict]) -> dict:
        results = []
        report = []
        for question in tqdm.tqdm(benchamark, desc="Processing questions: "):
            question_sentence, possible_answers, answer = self.preprocess(question)
            predicted_answer, context = self.predict(
                question_sentence, possible_answers
            )
            results.append((predicted_answer, answer))
            report.append(
                {
                    "question": question_sentence,
                    "answer": answer,
                    "context": context,
                    "predicted_answer": predicted_answer,
                }
            )

        scores = self.gen_eval(results)
        return {"scores": scores, "report": report}
