import os.path
import jinja2


class JINJALoader:
    """
    Jinja2 loader.
    """

    @staticmethod
    def load(template: str) -> jinja2.Template:
        """
        Load template from a specified path.

        :param template: Path to the template.
        :return: Jinja2 template.
        """
        environment = jinja2.Environment()
        if os.path.isfile(template):
            with open(template, "r", encoding="utf-8") as file:
                template = file.read()
        return environment.from_string(template)
