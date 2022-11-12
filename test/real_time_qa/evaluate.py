import argparse
import json
import os
from typing import Optional

import tqdm

from main import PIQARD
from test.evaluator import Evaluator


class RealTimeQAEvaluator(Evaluator):
    def __init__(self, piqard: PIQARD):
        super().__init__(piqard)

    def preprocess(self, question: dict) -> tuple[str, str]:
        question_sentence = question["question_sentence"]
        answer = question["choices"][int(question["answer"][0])]
        return question_sentence, answer

    def evaluate(self, benchamark: list[dict]) -> dict:
        results = []
        report = []
        for question in tqdm.tqdm(benchamark, desc="Processing questions: "):
            question_sentence, answer = self.preprocess(question)
            predicted_answer, context = self.predict(question_sentence)
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
