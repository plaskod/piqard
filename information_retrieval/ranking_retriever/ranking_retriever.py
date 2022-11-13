import pickle
import fastbm25
from nltk.stem import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords


class RankingRetriever:
    def __init__(self, documents_path: str, index_path: str):
        self.stemmer = PorterStemmer()
        self.documents = self.__load_documents(documents_path)
        self.index = self.__load_index(index_path)

    @staticmethod
    def __load_documents(path: str) -> list:
        with open(path) as f:
            return [line.replace("\"", "") for line in f.readlines()]

    @staticmethod
    def __load_index(index_path: str) -> fastbm25.fastbm25:
        with open(index_path, 'rb') as f:
            return pickle.load(f)

    def preprocess_query(self, query: str) -> list[str]:
        new_sentance = []
        sentence = remove_stopwords(query)
        for word in sentence.lower().split():
            new_sentance.append(self.stemmer.stem(word))
        return new_sentance

    def get_documents(self, question: str, n: int = 1):
        document_list = self.index.top_k_sentence(self.preprocess_query(question), k=n)
        retireved_documents = [self.documents[document_info[1]] for document_info in document_list]
        return retireved_documents
