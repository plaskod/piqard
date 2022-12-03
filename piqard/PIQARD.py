from piqard.utils.yaml_constructor import yaml_constructor
from piqard.information_retrievers.retriever import Retriever
from piqard.language_models.language_model import LanguageModel
from piqard.utils.jinja_loader import JINJALoader


@yaml_constructor
class PIQARD:
    def __init__(
            self,
            prompt_template: str,
            language_model: LanguageModel,
            information_retriever: Retriever = None,
            use_dynamic_prompting: bool = False
    ):
        self.information_retriever = information_retriever
        self.prompt_template = JINJALoader.load(prompt_template)
        self.language_model = language_model
        self.use_dynamic_prompting = use_dynamic_prompting

    def __call__(self, query: str) -> dict:
        retrieved_documents = None
        prompt_examples = None

        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query)

            if self.information_retriever.n > 0:
                prompt_examples = self.information_retriever.get_questions(query)

        prompt = self.prompt_template.render(question=query,
                                             context=retrieved_documents,
                                             prompt_examples=prompt_examples)
        generated_answer = self.language_model.query(prompt)

        final_answer = generated_answer[0]["generated_text"][len(prompt):]

        return {"prompt": prompt, "answer": final_answer, "context": retrieved_documents}

    def show_info(self):
        print("===== PIQARD =====")
        print(f"Information retriever: {self.information_retriever}")
        print(f"Prompt template: {self.prompt_template}")
        print(f"Language model: {self.language_model}")
