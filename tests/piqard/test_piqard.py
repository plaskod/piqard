import pytest
from unittest.mock import MagicMock, patch
from piqard.PIQARD import PIQARD
from piqard.utils.answer_postprocess import postprocess_answer
from piqard.utils.chain_trace import ChainTrace


class TestPIQARD():
    def test_init(self):
        prompt_template = MagicMock()
        language_model = MagicMock()
        information_retriever = MagicMock()

        piqard_test = PIQARD(prompt_template, language_model, information_retriever)

        assert piqard_test.prompt_template == prompt_template
        assert piqard_test.language_model == language_model
        assert piqard_test.information_retriever == information_retriever
        assert piqard_test.trace is None

    def test_call_without_retriever(self):
        prompt_template = MagicMock()
        language_model = MagicMock()
        piqard = PIQARD(prompt_template, language_model)
        query = "What is the capital of France?"
        result = piqard(query)
        prompt_template.render.assert_called_once()
        language_model.query.assert_called_once()
        assert result["context"] is None
        assert result["prompt_examples"] is None
        assert result["raw_answer"] == language_model.query()
        assert result["answer"] == postprocess_answer(result["raw_answer"], prompt_template.fix_text)
        assert result["prompt"] == prompt_template.render()
        assert result["chain_trace"] is not None

    def test_call_with_retriever(self):
        prompt_template = MagicMock()
        language_model = MagicMock()
        information_retriever = MagicMock()
        information_retriever.configure_mock(n=1)
        information_retriever.get_documents.return_value = ["document1", "document2"]
        piqard = PIQARD(prompt_template, language_model, information_retriever)
        query = "What is the capital of France?"
        with patch("piqard.PIQARD.get_prompt_examples") as mock_get_prompt_examples:
            mock_get_prompt_examples.return_value = ["example1", "example2"]
            result = piqard(query)
            information_retriever.get_documents.assert_called_once()
            mock_get_prompt_examples.assert_called_once()
            prompt_template.render.assert_called_once()
            language_model.query.assert_called_once()
            assert result["context"] == ["document1", "document2"]
            assert result["prompt_examples"] == ["example1", "example2"]
            assert result["raw_answer"] == language_model.query()
            assert result["answer"] == postprocess_answer(result["raw_answer"], prompt_template.fix_text)
            assert result["prompt"] == prompt_template.render()
            assert result["chain_trace"] is not None

    def test_set_trace(self):
        mock_trace = MagicMock(spec=ChainTrace)
        prompt_template = MagicMock()
        language_model = MagicMock()
        piqard = PIQARD(prompt_template, language_model)
        piqard.set_trace(mock_trace)
        assert piqard.trace == mock_trace

    @patch('builtins.print')
    def test_show_info(self, mock_print):
        prompt_template = MagicMock()
        language_model = MagicMock()
        piqard = PIQARD(prompt_template, language_model)

        piqard.information_retriever = "mock_ir"
        piqard.prompt_template = "mock_pt"
        piqard.language_model = "mock_lm"

        # Call the show_info method
        piqard.show_info()

        # Assert that the correct strings were printed
        mock_print.assert_any_call("===== PIQARD =====")
        mock_print.assert_any_call("Information retriever: mock_ir")
        mock_print.assert_any_call("Prompt template: mock_pt")
        mock_print.assert_any_call("Language model: mock_lm")
