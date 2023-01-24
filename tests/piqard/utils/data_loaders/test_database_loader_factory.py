import importlib
import pytest

from piqard.utils.data_loaders import DatabaseLoaderFactory


def test_init_DatabaseLoaderFactory(monkeypatch):
    # Test that the load_documents and load_questions functions are correctly imported
    # Create a mock load_documents function
    def mock_load_documents(*args, **kwargs):
        return ['mock document 1', 'mock document 2']

    # Create a mock load_questions function
    def mock_load_questions(*args, **kwargs):
        return [{'id': 1, 'text': 'mock question 1'}, {'id': 2, 'text': 'mock question 2'}]

    monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_documents', mock_load_documents)
    monkeypatch.setattr(f'piqard.utils.data_loaders.openbookqa_loader.load_questions', mock_load_questions)
    factory = DatabaseLoaderFactory("openbookqa")

    assert callable(factory.load_documents)
    assert callable(factory.load_questions)

def test_init_DatabaseLoaderFactory_with_invalid_database():
    # Test that an error is raised when an invalid database name is passed
    with pytest.raises(ImportError):
        factory = DatabaseLoaderFactory("invalid_database")