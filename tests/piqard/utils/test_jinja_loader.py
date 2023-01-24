import os
import tempfile
import pytest
from piqard.utils.jinja_loader import JINJALoader


def test_jinja_loader_load():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp.jinja2")
        template_string = "Hello {{ name }}!"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(template_string)

        # test loading template from file
        template = JINJALoader.load(temp_file_path)
        assert template.render({'name': "Marcin"}) == "Hello Marcin!"

        # test loading template from string
        template = JINJALoader.load(template_string)
        assert template.render({'name': "Marcin"}) == "Hello Marcin!"