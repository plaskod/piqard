import os
import pickle

import pytest
from unittest.mock import patch, MagicMock

from fastbm25 import fastbm25

from piqard.information_retrievers.retriever import Retriever


class TestRetriever:
    def test_init_Retriever(self, monkeypatch):
        mock_documents = ['mock document 1', 'mock document 2']
        mock_questions = [{'id': 1, 'text': 'mock question 1'}, {'id': 2, 'text': 'mock question 2'}]

        # Create a mock load_documents function
        def mock_load_documents(*args, **kwargs):
            return mock_documents

        # Create a mock load_questions function
        def mock_load_questions(*args, **kwargs):
            return mock_questions

        monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_documents', mock_load_documents)
        monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_questions', mock_load_questions)
        # factory = DatabaseLoaderFactory("openbookqa")
        # Call the Retriever class
        retriever = Retriever(database='openbookqa', database_path='path/to/database',
                              questions_path='path/to/questions', k=1, n=2)
        retriever("test")
        retriever.get_questions("test")
        # Assert that the documents are the same as the mock documents
        assert retriever.documents == mock_documents
        # Assert that the questions are the same as the mock questions
        assert retriever.questions == mock_questions
        # Assert that the k is 1
        assert retriever.k == 1
        # Assert that the n is 2
        assert retriever.n == 2
        assert str(retriever) == "Retriever"

    def test_init_Retriever_without_database(self, monkeypatch):
        # Call the Retriever class
        retriever = Retriever()

        assert retriever.k == 1
        assert retriever.n == 0

    # def test_pickle_load(self, monkeypatch):
    @pytest.fixture
    def index_file(self):
        index = fastbm25(["blabla", "testtest"])
        with open('index_file.pickle', 'wb') as handle:
            pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
        yield 'index_file.pickle'
        os.remove('index_file.pickle')

    def test_load_index(self, index_file):
        # call the function under test
        index = Retriever.load_index(index_file)

        # assert that the output is as expected
        assert isinstance(index,
                          fastbm25), f'Expected index to be of type fastbm25.fastbm25, but got {type(index)}'
