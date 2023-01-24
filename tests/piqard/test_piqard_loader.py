import pytest
import ruamel.yaml
from unittest.mock import MagicMock, patch
from piqard.PIQARD_loader import PIQARDLoader
from piqard.PIQARD import PIQARD
from piqard.utils.prompt_template import PromptTemplate
from piqard.language_models.language_model import LanguageModel


class TestPIQARD():
    def test_init(self):
        loader = PIQARDLoader()
        assert isinstance(loader.yaml, type(ruamel.yaml.YAML()))

    def test_load_from_file(self):

        loader = PIQARDLoader()
        piqard = loader.load("assets/configs/piqard_config.yaml")
        assert isinstance(piqard, type(PIQARD(PromptTemplate("test"), LanguageModel())))
