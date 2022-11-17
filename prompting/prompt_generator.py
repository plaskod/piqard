import os.path
import jinja2


class PromptGenerator:
    @staticmethod
    def load_template(prompt_template: str) -> jinja2.Template:
        environment = jinja2.Environment()

        if os.path.isfile(prompt_template):
            with open(prompt_template, 'r') as file:
                prompt_template = file.read()
        return environment.from_string(prompt_template)
