from utils import load_jsonl


def load_documents() -> list[dict]:
    raw_documents = load_jsonl("assets/database/hotpotqa/corpus.jsonl")
    prepared_documents = [document["text"] for document in raw_documents]
    return prepared_documents


def load_questions(test: bool = False) -> list[dict]:
    raw_questions = load_jsonl(f"assets/database/hotpotqa/{'test' if test else 'train'}.jsonl")
    prepared_questions = []
    for question in raw_questions:
        question_id = question["_id"]
        question_sentence = question["text"]
        possible_answers = None
        answer = question["metadata"]["answer"]
        prepared_questions.append(
            {
                "id": question_id,
                "text": question_sentence,
                "possible_answers": possible_answers,
                "answer": answer,
            }
        )
    return prepared_questions
