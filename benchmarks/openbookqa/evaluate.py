from piqard.PIQARD import PIQARD
from benchmarks.evaluator import Evaluator


class OpenBookQAEvaluator(Evaluator):
    def __init__(self, piqard: PIQARD):
        super().__init__(piqard)

    def preprocess(self, question: dict) -> tuple[str, str, str]:
        question_sentence = question["question"]["stem"]
        possible_answers = " ".join(
            [
                ". ".join([choice["label"], choice["text"]])
                for choice in question["question"]["choices"]
            ]
        )
        answer = f"{question['answerKey']}. {list(filter(lambda choice: choice['label'] == question['answerKey'], question['question']['choices'], ))[0]['text']}"
        return question_sentence, possible_answers, answer

    def evaluate_question(self, question: dict) -> dict:
        question_sentence, possible_answers, answer = self.preprocess(question)
        predicted_answer, context = self.predict(question_sentence, possible_answers)
        return {
                "id": question['id'],
                "question": question_sentence,
                "possible_answers": possible_answers,
                "answer": answer,
                "context": context,
                "predicted_answer": predicted_answer,
            }
