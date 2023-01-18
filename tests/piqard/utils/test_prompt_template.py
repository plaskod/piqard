import os
import tempfile
import pytest
from piqard.utils.prompt_template import PromptTemplate




def test_prompt_template():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp.jinja2")
        template_string = "Hello {{ name }}!"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(template_string)

        # test create prompt template from file
        prompt_template = PromptTemplate(temp_file_path)
        assert str(prompt_template) == temp_file_path
        assert prompt_template.template.render({'name': "Marcin"}) == "Hello Marcin!"

        # test create prompt template from string
        prompt_template = PromptTemplate(template_string)
        assert str(prompt_template) == template_string
        assert prompt_template.template.render({'name': "Marcin"}) == "Hello Marcin!"

        # test render method
        rendered_template = prompt_template.render(name='John ')
        assert rendered_template == 'Hello John!'

        # test preprocess_template method
        preprocessed_template = prompt_template.preprocess_template(template_string + " ? ")
        assert preprocessed_template == template_string + "?"

        # test __str__ method
        assert str(prompt_template) == template_string
