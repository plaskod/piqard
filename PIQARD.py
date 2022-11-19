from config_loader.yaml_constructor import yaml_constructor
from context_builders.context_builder import ContextBuilder
from information_retrieval.retriever import Retriever
from large_language_models.language_model import LanguageModel
from prompting.prompt_generator import PromptGenerator


@yaml_constructor
class PIQARD:
    def __init__(
        self,
        context_builder: ContextBuilder,
        prompt_template: str,
        large_language_model: LanguageModel,
        information_retriever: Retriever = None,
    ):
        self.information_retriever = information_retriever
        self.context_builder = context_builder
        self.prompt_template = PromptGenerator.load_template(prompt_template)
        self.large_language_model = large_language_model

    def __call__(self, query: str) -> dict:
        context = None
        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query, n=5)
            context = self.context_builder.build(retrieved_documents)

        prompt = self.prompt_template.render(question=query, context=context)

        generated_answer = self.large_language_model.query(prompt)

        final_answer = generated_answer[0]["generated_text"][len(prompt) :]

        return {"prompt": prompt, "answer": final_answer, "context": context}
