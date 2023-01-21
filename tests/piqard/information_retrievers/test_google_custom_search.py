import pytest
from piqard.information_retrievers.google_custom_search import GoogleCustomSearch
from piqard.utils.exceptions import DynamicPromptingNotImplementedException


class TestGoogleCustomSearch:

    def test_init(self):
        retriever = GoogleCustomSearch()
        assert retriever.k == 1
        assert retriever.n == 0
        assert str(retriever) == "GoogleCustomSearch"

    def test_thorw_exception(self):
        with pytest.raises(DynamicPromptingNotImplementedException):
            GoogleCustomSearch(n=1)

    def test_get_documents(self):
        retriever = GoogleCustomSearch(k=1)
        documents = retriever.get_documents("Phil Collins")
        assert isinstance(documents, list)
