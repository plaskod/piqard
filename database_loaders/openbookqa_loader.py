from utils import load_jsonl


def load_documents() -> list[dict]:
    raw_documents = load_jsonl("assets/database/openbookqa/corpus.jsonl")
    prepared_documents = [document["text"] for document in raw_documents]
    return prepared_documents


def load_questions(test: bool = False, number: int = None) -> list[dict]:
    raw_questions = load_jsonl(
        f"assets/database/openbookqa/{'test' if test else 'train'}.jsonl"
    )
    if number is not None:
        raw_questions = raw_questions[: min(len(raw_questions), number)]
    prepared_questions = []
    for question in raw_questions:
        question_id = question["id"]
        question_sentence = question["question"]["stem"]
        possible_answers = " ".join(
            [
                ". ".join([choice["label"], choice["text"]])
                for choice in question["question"]["choices"]
            ]
        )
        answer = f"{question['answerKey']}. {list(filter(lambda choice: choice['label'] == question['answerKey'], question['question']['choices'], ))[0]['text']} "
        prepared_questions.append(
            {
                "id": question_id,
                "text": question_sentence,
                "possible_answers": possible_answers,
                "answer": answer,
            }
        )
    return prepared_questions
