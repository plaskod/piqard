import pytest
from piqard.information_retrievers.wiki_api import WikiAPI
from piqard.utils.exceptions import DynamicPromptingNotImplementedException


class TestGoogleCustomSearch:

    def test_init(self):
        retriever = WikiAPI()
        assert retriever.k == 1
        assert retriever.n == 0
        assert str(retriever) == "WikiAPI"

    def test_thorw_exception(self):
        with pytest.raises(DynamicPromptingNotImplementedException):
            WikiAPI(n=1)

    def test_get_documents(self):
        retriever = WikiAPI(k=1)
        documents = retriever.get_documents("Phil Collins")
        assert isinstance(documents, list)

    def test_get_PageError(self):
        retriever = WikiAPI(k=1)
        documents = retriever.get_documents("NON_EXSITENT_PAGE")
        assert isinstance(documents, list)

    def test_get_DisambiguationError(self):
        retriever = WikiAPI(k=1)
        documents = retriever.get_documents("John Smith")
        assert isinstance(documents, list)