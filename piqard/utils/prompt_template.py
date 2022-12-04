from piqard.utils.jinja_loader import JINJALoader
from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class PromptTemplate:
    def __init__(self, template: str, fix_text: str = None):
        self.template = JINJALoader.load(template)
        self.fix_text = fix_text

    def render(self, **kwargs):
        rendered_template = self.template.render(kwargs)
        return self.preprocess_template(rendered_template)

    @staticmethod
    def preprocess_template(template: str) -> str:
        return (
            template.replace(" ,", ",")
            .replace(" '", "'")
            .replace(" ?", "?")
            .replace(" !", "!")
            .replace(" .", ".")
            .strip()
        )
