import os
import shutil
import tempfile
import json
import pytest
from piqard.utils.io import *
from piqard.utils.exceptions import EnvironmentVariableNotSet

def test_directory():
    # create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    test_dir = os.path.join(temp_dir, "test_dir")

    # test creating a new directory
    assert directory(test_dir) == test_dir
    assert os.path.exists(test_dir)

    # test creating a directory that already exists
    assert directory(test_dir) == test_dir
    assert os.path.exists(test_dir)

    # clean up
    shutil.rmtree(temp_dir)

def test_load_jsonl():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp.jsonl")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write('{"name": "John", "age": 30}\n{"name": "Mike", "age": 25}\n')

        # test loading jsonl file
        data = load_jsonl(temp_file_path)
        assert isinstance(data, list)
        assert len(data) == 2
        assert isinstance(data[0], dict)
        assert data[0] == {"name": "John", "age": 30}
        assert isinstance(data[1], dict)
        assert data[1] == {"name": "Mike", "age": 25}

def test_save_results():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp.json")
        results = {"name": "John", "age": 30}

        # test saving results
        save_results(temp_file_path, results)
        assert os.path.exists(temp_file_path)

        with open(temp_file_path, "r") as temp_file:
            saved_results = json.load(temp_file)
            assert saved_results == results

def test_get_env_variable():
    # test getting an existing environment variable
    os.environ["TEST_VAR"] = "test_value"
    assert get_env_variable("TEST_VAR") == "test_value"

    # test getting a non-existing environment variable
    with pytest.raises(EnvironmentVariableNotSet) as excinfo:
        get_env_variable("NON_EXISTING_VAR")
    assert "NON_EXISTING_VAR" in str(excinfo.value)
