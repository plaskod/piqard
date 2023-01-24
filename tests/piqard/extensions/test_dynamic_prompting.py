from piqard.information_retrievers import AnnoyRetriever
from piqard.extensions.dynamic_prompting import get_prompt_examples

def test_get_prompt_examples():
    retriever = AnnoyRetriever(
        database="openbookqa",
        database_index="tests/testAnnoyIndex.ann",
        database_path="tests/database.jsonl",
        questions_index="tests/testQuestion.ann",
        questions_path="tests/questions.jsonl",
        k=1,
        n=1,
        dimensions=384,
        sentence_transformer="multi-qa-MiniLM-L6-cos-v1"
    )
    questions = get_prompt_examples("bee", retriever)
    assert isinstance(questions, list)
