import pytest
from piqard.utils.exceptions import *

def test_dynamic_prompting_exception():
    with pytest.raises(DynamicPromptingNotImplementedException) as excinfo:
        raise DynamicPromptingNotImplementedException("information_retriever")
    assert "Dynamic prompting not implemented" in str(excinfo.value)
    assert "information_retriever" in str(excinfo.value)

def test_response_500_exception():
    with pytest.raises(Response500Exception) as excinfo:
        raise Response500Exception("language_model")
    assert "Response 500 exception" in str(excinfo.value)
    assert "language_model" in str(excinfo.value)

def test_API_overload_exception():
    with pytest.raises(LanguageModelAPIOverloadException) as excinfo:
        raise LanguageModelAPIOverloadException("language_model")
    assert "API key hourly ratio exceeded." in str(excinfo.value)
    assert "language_model" in str(excinfo.value)

def test_API_blocked_output_exception():
    with pytest.raises(LanguageModelAPIBlockedOutput) as excinfo:
        raise LanguageModelAPIBlockedOutput("language_model")
    assert "Blocked output: this generation may be a potential violation of terms of service." in str(excinfo.value)
    assert "language_model" in str(excinfo.value)

def test_environment_variable_not_set_exception():
    with pytest.raises(EnvironmentVariableNotSet) as excinfo:
        raise EnvironmentVariableNotSet("env_variable")
    assert "Environment variable is not set" in str(excinfo.value)
    assert "env_variable" in str(excinfo.value)
