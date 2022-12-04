from piqard.extensions.dynamic_prompting import get_prompt_examples
from piqard.utils.answer_postprocess import postprocess_answer
from piqard.utils.prompt_template import PromptTemplate
from piqard.utils.yaml_constructor import yaml_constructor
from piqard.information_retrievers.retriever import Retriever
from piqard.language_models.language_model import LanguageModel


@yaml_constructor
class PIQARD:
    def __init__(
        self,
        prompt_template: PromptTemplate,
        language_model: LanguageModel,
        information_retriever: Retriever = None,
    ):
        self.information_retriever = information_retriever
        self.prompt_template = prompt_template
        self.language_model = language_model

    def __call__(self, query: str, possible_answers: str = None) -> dict:
        retrieved_documents = None
        prompt_examples = None

        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query)

            if self.information_retriever.n > 0:
                prompt_examples = get_prompt_examples(query, self.information_retriever)

        prompt = self.prompt_template.render(
            question=query,
            context=retrieved_documents,
            possible_answers=possible_answers,
            prompt_examples=prompt_examples,
        )

        generated_answer = self.language_model.query(prompt)
        final_answer = postprocess_answer(
            generated_answer, self.prompt_template.fix_text
        )

        return {
            "prompt": prompt,
            "raw_answer": generated_answer,
            "answer": final_answer,
            "context": retrieved_documents,
            "prompt_examples": prompt_examples,
        }

    def show_info(self):
        print("===== PIQARD =====")
        print(f"Information retriever: {self.information_retriever}")
        print(f"Prompt template: {self.prompt_template}")
        print(f"Language model: {self.language_model}")
