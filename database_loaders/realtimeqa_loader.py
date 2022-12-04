from utils import load_jsonl


def load_documents() -> list[dict]:
    raise NotImplemented


def load_questions(test: bool = False, number: int = None) -> list[dict]:
    raw_questions = load_jsonl(
        f"assets/database/realtimeqa/{'test' if test else 'train'}.jsonl"
    )
    if number is not None:
        raw_questions = raw_questions[: min(len(raw_questions), number)]
    prepared_questions = []
    for question in raw_questions:
        question_id = question["question_id"]
        question_sentence = question["question_sentence"]
        possible_answers = " ".join(
            [f"{idx}. {choice}" for idx, choice in enumerate(question["choices"])]
        )
        answer = f"{question['answer'][0]}. {question['choices'][int(question['answer'][0])]}"
        prepared_questions.append(
            {
                "id": question_id,
                "text": question_sentence,
                "possible_answers": possible_answers,
                "answer": answer,
            }
        )
    return prepared_questions
