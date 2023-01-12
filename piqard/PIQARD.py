from piqard.extensions.dynamic_prompting import get_prompt_examples
from piqard.utils.chain_trace import ChainTrace
from piqard.utils.answer_postprocess import postprocess_answer
from piqard.utils.prompt_template import PromptTemplate
from piqard.utils.yaml_constructor import yaml_constructor
from piqard.information_retrievers.retriever import Retriever
from piqard.language_models.language_model import LanguageModel


@yaml_constructor
class PIQARD:
    """
    PIQARD is a class that contains all the components of the PIQARD system.
    """

    def __init__(
        self,
        prompt_template: PromptTemplate,
        language_model: LanguageModel,
        information_retriever: Retriever = None,
    ):
        """
        Constructor of the PIQARD class.

        :param prompt_template: The prompt template to use.
        :param language_model: The language model to use.
        :param information_retriever: The retriever to use.
        """
        self.information_retriever = information_retriever
        self.prompt_template = prompt_template
        self.language_model = language_model
        self.trace = None

    def __call__(self, query: str, possible_answers: str = None) -> dict:
        retrieved_documents = None
        prompt_examples = None

        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query)

            if self.trace is None:
                self.trace = ChainTrace(
                    " ".join(retrieved_documents) + "\n", "observation"
                )
            else:
                self.trace.add(" ".join(retrieved_documents) + "\n", "observation")

            if self.information_retriever.n > 0:
                prompt_examples = get_prompt_examples(query, self.information_retriever)

        prompt = self.prompt_template.render(
            question=query,
            context=retrieved_documents,
            possible_answers=possible_answers,
            prompt_examples=prompt_examples,
        )
        if self.trace is None:
            self.trace = ChainTrace(prompt + "\n", "base_prompt")
        else:
            self.trace.add(prompt + "\n", "base_prompt")

        generated_answer = self.language_model.query(prompt)
        self.trace.add(generated_answer + "\n", "thought")

        final_answer = postprocess_answer(
            generated_answer, self.prompt_template.fix_text
        )
        self.trace.add(final_answer + "\n", "finish")

        return {
            "prompt": prompt,
            "raw_answer": generated_answer,
            "answer": final_answer,
            "context": retrieved_documents,
            "prompt_examples": prompt_examples,
            "chain_trace": self.trace,
        }

    def set_trace(self, trace: ChainTrace) -> None:
        """
        Set the chain trace.

        :param trace: The chain trace to set.
        :return: None
        """
        self.trace = trace

    def show_info(self):
        print("===== PIQARD =====")
        print(f"Information retriever: {self.information_retriever}")
        print(f"Prompt template: {self.prompt_template}")
        print(f"Language model: {self.language_model}")
