import pytest

from database_loaders.database_loader_factory import DataBaseLoaderFactory


def test_unknown_database():
    with pytest.raises(ValueError):
        DataBaseLoaderFactory("NotExistentDatabase123")

def test_openbookqa_database_loader():
    DataBaseLoaderFactory("openbookqa")
