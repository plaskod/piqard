import argparse
import json
import os
from typing import Optional

import tqdm

from main import PIQARD
from test.evaluator import Evaluator


class RealTimeQAEvaluator(Evaluator):
    def __init__(self, piqard: PIQARD, with_passage: bool = False):
        self.piqard = piqard
        self.with_passage = with_passage

    def preprocess(self, question: dict) -> tuple[str, str, Optional[str]]:
        question_sentence = question["question_sentence"]
        answer = question["choices"][int(question["answer"][0])]
        passage = question["evidence"]
        return question_sentence, answer, passage

    def predict(self, question: str, passage: str) -> tuple[str, str]:
        if not self.with_passage:
            if self.piqard.information_retriever is not None:
                retireved_documents = self.piqard.information_retriever.request(
                    question
                )
                if retireved_documents:
                    passage = " ".join(retireved_documents[0]["text"].split()[:100])
                else:
                    passage = None
            else:
                passage = None
        prompt = self.piqard.prompt_generator.generate(question, passage)
        generated_answer = self.piqard.large_language_model.query(prompt)
        final_answer = generated_answer[0]["generated_text"][len(prompt) :].split("\n")[
            0
        ]
        return final_answer, passage

    def evaluate(self, benchamark: list[dict]) -> dict:
        results = []
        report = []
        for question in tqdm.tqdm(benchamark, desc="Processing questions: "):
            question_sentence, answer, passage = self.preprocess(question)
            predicted_answer, context = self.predict(question_sentence, passage)
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
