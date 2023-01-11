from piqard.utils.io import load_jsonl


def load_documents(path: str) -> list[dict]:
    raw_documents = load_jsonl(path)
    prepared_documents = [document["text"] for document in raw_documents]
    return prepared_documents


def load_questions(path: str, number: int = None) -> list[dict]:
    raw_questions = load_jsonl(path)
    if number is not None:
        raw_questions = raw_questions[: min(len(raw_questions), number)]
    prepared_questions = []
    for question in raw_questions:
        question_id = question["_id"]
        question_sentence = question["question"]
        possible_answers = None
        answer = question["answer"]
        prepared_questions.append(
            {
                "id": question_id,
                "text": question_sentence,
                "possible_answers": possible_answers,
                "answer": answer,
            }
        )
    return prepared_questions
