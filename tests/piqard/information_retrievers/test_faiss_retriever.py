from unittest.mock import MagicMock

from piqard.information_retrievers import FAISSRetriever


class TestFAISSRetriever():
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
        monkeypatch.setattr('piqard.information_retrievers.faiss_retriever.FAISSRetriever.load_index',
                            mock_load_index)

        retriever = FAISSRetriever('openbookqa', 'index_path', 'db_path', 'question_index_path', 'question_path', k=10, n=5)

        assert retriever.documents == mock_documents
        assert retriever.index == mock_index
        assert retriever.questions == mock_questions
        assert retriever.question_index == mock_index
        assert retriever.k == 10
        assert retriever.n == 5
        assert str(retriever) == "FAISSRetriever"

    def test_get_documents(self, monkeypatch):

        mock_index = MagicMock()
        mock_index.search.return_value = "someTrash.jpg", [
            [0, 1],
            [1, 0]
        ]

        def mock_load_index(*args, **kwargs):
            return mock_index

        monkeypatch.setattr(
            'piqard.information_retrievers.retriever.Retriever.load_index',
            mock_load_index
        )

        def mock_model_encode(*args, **kwargs):
            return [1,0,1,0,1,0]



        def mock_load_jsonl(path):
            return [
                {"_id": 1, "text": "What is the capital of France?", "answer": "Paris"},
                {"_id": 2, "text": "What is the largest planet in our solar system?", "answer": "Jupiter"},
                {"_id": 3, "text": "What is the smallest planet in our solar system?", "answer": "Mercury"}
            ]

        monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)

        # Set up the test data
        retriever = FAISSRetriever(database='openbookqa', k=2, n=0)
        retriever.documents = ['document 1', 'document 2']
        monkeypatch.setattr(retriever.model, 'encode', mock_model_encode)
        assert retriever.get_documents('test question') == ['document 1', 'document 2']

    def test_get_questions(self, monkeypatch):

        mock_index = MagicMock()
        mock_index.search.return_value = "someTrash.jpg", [
            [0, 1],
            [1, 0]
        ]

        def mock_load_index(*args, **kwargs):
            return mock_index

        monkeypatch.setattr(
            'piqard.information_retrievers.retriever.Retriever.load_index',
            mock_load_index
        )

        def mock_model_encode(*args, **kwargs):
            return [1,0,1,0,1,0]

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
        retriever = FAISSRetriever(database='openbookqa', k=2, n=1)
        retriever.questions = ['document 1', 'document 2']
        monkeypatch.setattr(retriever.model, 'encode', mock_model_encode)
        assert retriever.get_questions('test question') == ['document 1', 'document 2']
