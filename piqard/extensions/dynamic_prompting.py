from piqard.information_retrievers.retriever import Retriever


def get_prompt_examples(question: str, information_retriever: Retriever):
    example_questions = information_retriever.get_questions(question)
    for example_question in example_questions:
        example_question['context'] = information_retriever.get_documents(example_question['text'])
    return example_questions
