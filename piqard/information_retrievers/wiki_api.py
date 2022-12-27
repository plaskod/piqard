import wikipedia
from piqard.information_retrievers.exceptions import (
    DynamicPromptingNotImplementedException,
)
from piqard.information_retrievers.retriever import Retriever


class WikiAPI(Retriever):
    def __init__(self, database: str = None, k: int = 1, n: int = 0):
        super().__init__(database, k)
        if n > 0:
            raise DynamicPromptingNotImplementedException(self.__str__())

    def get_documents(self, question: str):
        try:
            return [wikipedia.summary(question, sentences=self.k)]
        except wikipedia.exceptions.PageError as e:
            possible_results = wikipedia.search(f"[{question}]")
            return f"Could not find {question}. Similar: {possible_results[:5]}."
        except wikipedia.exceptions.DisambiguationError as e:
            possible_results = wikipedia.search(f"[{question}]")
            return f"Could not find {question}. Similar: {possible_results[:5]}."

    def __str__(self):
        return "WikiAPI"
