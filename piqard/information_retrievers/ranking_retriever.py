from nltk.stem import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords

from piqard.information_retrievers.retriever import Retriever


class RankingRetriever(Retriever):
    def __init__(self, database: str):
        super().__init__(database)
        self.index = self.load_index(f"assets/database/{database}/bm25_index.pickle")
        self.stemmer = PorterStemmer()

    def preprocess_query(self, query: str) -> list[str]:
        new_sentance = []
        sentence = remove_stopwords(query)
        for word in sentence.lower().split():
            new_sentance.append(self.stemmer.stem(word))
        return new_sentance

    def get_documents(self, question: str, n: int = 1):
        document_list = self.index.top_k_sentence(self.preprocess_query(question), k=n)
        retireved_documents = [
            self.documents[document_info[1]] for document_info in document_list
        ]
        return retireved_documents
