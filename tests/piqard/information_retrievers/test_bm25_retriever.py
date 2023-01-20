import pytest
from unittest.mock import MagicMock, patch, Mock

from piqard.information_retrievers import BM25Retriever
from piqard.utils.exceptions import DynamicPromptingNotImplementedException


class TestBM25Retriever:

    def test_init(self, monkeypatch):
        mock_documents = ['mock document 1', 'mock document 2']
        mock_index = {'mock document 1': 'index 1', 'mock document 2': 'index 2'}
        mock_questions = [{'id': 1, 'text': 'mock question 1'}, {'id': 2, 'text': 'mock question 2'}]
        mock_question_index = {'mock question 1': 'index 1', 'mock question 2': 'index 2'}

        # Create a mock load_documents function
        def mock_load_documents(*args, **kwargs):
            return mock_documents

        # Create a mock load_index function
        def mock_load_index(*args, **kwargs):
            return mock_index

        # Create a mock load_questions function
        def mock_load_questions(*args, **kwargs):
            return mock_questions

        monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_documents', mock_load_documents)
        monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_questions', mock_load_questions)
        monkeypatch.setattr('piqard.information_retrievers.BM25_retriever.BM25Retriever.load_index',
                            mock_load_index)
        # Create a test instance of BM25Retriever
        retriever = BM25Retriever('openbookqa', 'index_path', 'db_path', 'question_index_path', 'question_path', k=10, n=5)

        assert retriever.documents == mock_documents
        assert retriever.index == mock_index
        assert retriever.questions == mock_questions
        assert retriever.question_index == mock_index
        assert retriever.k == 10
        assert retriever.n == 5
        assert str(retriever) == "BM25Retriever"

    def test_preprocess_query(self, monkeypatch):
        mock_documents = ['mock document 1', 'mock document 2']
        mock_index = {'mock document 1': 'index 1', 'mock document 2': 'index 2'}
        mock_questions = [{'id': 1, 'text': 'mock question 1'}, {'id': 2, 'text': 'mock question 2'}]
        mock_question_index = {'mock question 1': 'index 1', 'mock question 2': 'index 2'}

        # Create a mock load_documents function
        def mock_load_documents(*args, **kwargs):
            return mock_documents

        # Create a mock load_index function
        def mock_load_index(*args, **kwargs):
            return mock_index

        # Create a mock load_questions function
        def mock_load_questions(*args, **kwargs):
            return mock_questions

        monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_documents', mock_load_documents)
        monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_questions', mock_load_questions)
        monkeypatch.setattr('piqard.information_retrievers.BM25_retriever.BM25Retriever.load_index',
                            mock_load_index)
        retriever = BM25Retriever(database='openbookqa', database_path='path/to/database',
                                  questions_path='path/to/questions', k=1, n=2)

        # Create a mock remove_stopwords function
        def mock_remove_stopwords(query):
            return query

        monkeypatch.setattr(f'gensim.parsing.preprocessing.remove_stopwords.__code__', mock_remove_stopwords.__code__)
        # Apply the mock remove_stopwords to the preprocess_query function
        # monkeypatch.setattr(BM25Retriever, 'remove_stopwords', mock_remove_stopwords)

        # Create a mock stemmer.stem function
        def mock_stemmer_stem(word):
            return word

        # Apply the mock stemmer.stem to the preprocess_query function
        monkeypatch.setattr(retriever.stemmer, 'stem', mock_stemmer_stem)

        query = "This is a test query"
        # call the preprocess_query function
        result = retriever.preprocess_query(query)
        # Assert that the result is the same as the query
        assert result == query.lower().split()

    def test_get_documents(self, monkeypatch):
        # Create a mock preprocess_query function
        def mock_preprocess_query(*args, **kwargs):
            return ['preprocessed', 'query']

        # Apply the mock preprocess_query to the BM25Retriever.preprocess_query
        monkeypatch.setattr('piqard.information_retrievers.BM25_retriever.BM25Retriever.preprocess_query', mock_preprocess_query)

        mock_index = MagicMock()
        mock_index.top_k_sentence.return_value = [
            ('document 1', 0),
            ('document 2', 1)
        ]

        def mock_load_index(*args, **kwargs):
            return mock_index

        monkeypatch.setattr(
            'piqard.information_retrievers.retriever.Retriever.load_index',
            mock_load_index
        )

        def mock_load_jsonl(path):
            return [
                {"_id": 1, "text": "What is the capital of France?", "answer": "Paris"},
                {"_id": 2, "text": "What is the largest planet in our solar system?", "answer": "Jupiter"},
                {"_id": 3, "text": "What is the smallest planet in our solar system?", "answer": "Mercury"}
            ]

        monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)

        # Set up the test data
        retriever = BM25Retriever(database='openbookqa', k=2, n=0)
        retriever.documents = ['document 1', 'document 2']

        # Test the get_documents function
        assert retriever.get_documents('test question') == ['document 1', 'document 2']

    def test_get_questions(self, monkeypatch):
        # Create a mock preprocess_query function
        def mock_preprocess_query(*args, **kwargs):
            return ['preprocessed', 'query']

        # Apply the mock preprocess_query to the BM25Retriever.preprocess_query
        monkeypatch.setattr('piqard.information_retrievers.BM25_retriever.BM25Retriever.preprocess_query', mock_preprocess_query)

        mock_index = MagicMock()
        mock_index.top_k_sentence.return_value = [
            ('document 1', 0),
            ('document 2', 1)
        ]

        def mock_load_index(*args, **kwargs):
            return mock_index

        monkeypatch.setattr(
            'piqard.information_retrievers.retriever.Retriever.load_index',
            mock_load_index
        )

        def mock_load_jsonl(path):
            return [
                {
                    "id": 1,
                    "text": "blabla",
                    "question": {
                        "stem": "What is the capital of France?",
                        "choices": [
                            {"label": "A", "text": "Paris"},
                            {"label": "B", "text": "London"},
                            {"label": "C", "text": "Berlin"},
                        ],
                    },
                    "answerKey": "A",
                },
                {
                    "id": 2,
                    "text": "blabla",
                    "question": {
                        "stem": "What is the largest planet in our solar system?",
                        "choices": [
                            {"label": "A", "text": "Jupiter"},
                            {"label": "B", "text": "Earth"},
                            {"label": "C", "text": "Mars"},
                        ],
                    },
                    "answerKey": "A",
                },
            ]
        monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)

        # Set up the test data
        retriever = BM25Retriever(database='openbookqa', k=2, n=1)
        retriever.questions = ['document 1', 'document 2']

        # Test the get_documents function
        assert retriever.get_questions('test question') == ['document 1', 'document 2']
    #
    # def test_DynamicPromptingNotImplementedException(self, monkeypatch):
    #     mock_documents = ['mock document 1', 'mock document 2']
    #     mock_index = {'mock document 1': 'index 1', 'mock document 2': 'index 2'}
    #     mock_questions = [{'id': 1, 'text': 'mock question 1'}, {'id': 2, 'text': 'mock question 2'}]
    #     mock_question_index = {'mock question 1': 'index 1', 'mock question 2': 'index 2'}
    #
    #     # Create a mock load_documents function
    #     def mock_load_documents(*args, **kwargs):
    #         return mock_documents
    #
    #     # Create a mock load_index function
    #     def mock_load_index(self, input_value):
    #         mock_function = Mock(return_value=mock_index)
    #         mock_function.side_effect = lambda x: {None: FileNotFoundError(), 'input_2': 'output_2'}.get(x, 'default_output')
    #         return mock_function(input_value)
    #
    #     # Create a mock load_questions function
    #     def mock_load_questions(*args, **kwargs):
    #         return mock_questions
    #
    #     monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_documents', mock_load_documents)
    #     monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_questions', mock_load_questions)
    #     monkeypatch.setattr('piqard.information_retrievers.BM25_retriever.BM25Retriever.load_index',
    #                         mock_load_index)
    #
    #     with pytest.raises(DynamicPromptingNotImplementedException) as excinfo:
    #         retriever = BM25Retriever('openbookqa', 'index_path', 'db_path', questions_index=None, questions_path='question_path',
    #                                   k=10, n=5)