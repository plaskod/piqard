import os.path
import jinja2


class JINJALoader:
    @staticmethod
    def load(template: str) -> jinja2.Template:
        environment = jinja2.Environment()
        if os.path.isfile(template):
            with open(template, "r") as file:
                template = file.read()
        return environment.from_string(template)
