from nltk.stem import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords

from piqard.information_retrievers.exceptions import DynamicPromptingNotImplementedException
from piqard.information_retrievers.retriever import Retriever


class RankingRetriever(Retriever):
    def __init__(self, database: str, k: int = 1, n: int = 0):
        super().__init__(database, k, n)
        self.index = self.load_index(f"assets/database/{database}/bm25_index.pickle")
        if n > 0:
            try:
                self.question_index = self.load_index(f"assets/database/{database}/question_bm25_index.pickle")
            except FileNotFoundError:
                raise DynamicPromptingNotImplementedException
        self.stemmer = PorterStemmer()

    def preprocess_query(self, query: str) -> list[str]:
        new_sentance = []
        sentence = remove_stopwords(query)
        for word in sentence.lower().split():
            new_sentance.append(self.stemmer.stem(word))
        return new_sentance

    def get_documents(self, question: str):
        document_list = self.index.top_k_sentence(self.preprocess_query(question), k=self.k)
        retrieved_documents = [
            self.documents[document_info[1]] for document_info in document_list
        ]
        return retrieved_documents

    def get_questions(self, question: str) -> list[dict]:
        question_list = self.question_index.top_k_sentence(self.preprocess_query(question), k=self.n)
        retrieved_questions = [
            self.questions[question_info[1]] for question_info in question_list
        ]
        return retrieved_questions
