from piqard.utils.jinja_loader import JINJALoader
from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class PromptTemplate:
    """
    PromptTemplate is a class that represents a prompt template.
    """

    def __init__(self, template: str, fix_text: str = None):
        """
        Constructor of the PromptTemplate class.
        :param template: Path to the template or template in string format.
        :param fix_text: Text, which indicates the final answer.
        """
        self.template = JINJALoader.load(template)
        self.fix_text = fix_text

    def render(self, **kwargs) -> str:
        """
        Render the template.

        :param kwargs: Arguments to render the template.
        :return: Rendered template.
        """
        rendered_template = self.template.render(kwargs)
        return self.preprocess_template(rendered_template)

    @staticmethod
    def preprocess_template(template: str) -> str:
        """
        Preprocess the template.

        :param template: Template to preprocess.
        :return: Preprocessed template.
        """
        return (
            template.replace(" ,", ",")
            .replace(" '", "'")
            .replace(" ?", "?")
            .replace(" !", "!")
            .replace(" .", ".")
            .strip()
        )
