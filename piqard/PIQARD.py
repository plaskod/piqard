from piqard.utils.yaml_constructor import yaml_constructor
from piqard.context_builders.context_builder import ContextBuilder
from piqard.information_retrievers.retriever import Retriever
from piqard.language_models.language_model import LanguageModel
from piqard.utils.jinja_loader import JINJALoader


@yaml_constructor
class PIQARD:
    def __init__(
            self,
            context_builder: ContextBuilder,
            prompt_template: str,
            language_model: LanguageModel,
            information_retriever: Retriever = None,
    ):
        self.information_retriever = information_retriever
        self.context_builder = context_builder
        self.prompt_template = JINJALoader.load(prompt_template)
        self.language_model = language_model

    def __call__(self, query: str) -> dict:
        context = None
        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query, n=5)
            context = self.context_builder.build(retrieved_documents)

        prompt = self.prompt_template.render(question=query, context=context)

        generated_answer = self.language_model.query(prompt)

        final_answer = generated_answer[0]["generated_text"][len(prompt):]

        return {"prompt": prompt, "answer": final_answer, "context": context}

    def show_info(self):
        print("===== PIQARD =====")
        print(f"Information retriever: {self.information_retriever}")
        print(f"Context builder: {self.context_builder}")
        print(f"Prompt template: {self.prompt_template}")
        print(f"Language model: {self.language_model}")
