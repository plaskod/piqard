from piqard.information_retrievers.retriever import Retriever


def get_prompt_examples(question: str, information_retriever: Retriever) -> list[dict]:
    """
    Gets the prompt examples from the information retriever.

    :param question: The question to get the prompt examples for.
    :param information_retriever: The information retriever to get the prompt examples from.
    :return: The prompt examples.
    """
    example_questions = information_retriever.get_questions(question)
    for example_question in example_questions:
        example_question["context"] = information_retriever.get_documents(
            example_question["text"]
        )
    return example_questions
