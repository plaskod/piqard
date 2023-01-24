from piqard import PIQARD
from piqard.language_models.language_model import LanguageModel
from piqard.utils.answer_postprocess import postprocess_answer
from piqard.utils.chain_trace import ChainTrace
from piqard.utils.prompt_template import PromptTemplate


class SelfAware:
    """
    SelfAware is a class that implements prompting strategy that at the beginning asks the model if it should browse the web for an answer.
    """

    def __init__(
        self,
        prompt_template: PromptTemplate,
        language_model: LanguageModel,
        if_should_browse: PIQARD,
        if_should_not_browse: PIQARD,
    ):
        """
        Constructor of the SelfAsk class.

        :param prompt_template: The prompt template to use.
        :param language_model: Language model to use when asking about browsing the web.
        :param if_should_browse: PIQARD instance to use if the model says it should browse the web.
        :param if_should_not_browse: PIQARD instance to use if the model says it should not browse the web.
        """
        self.language_model = language_model
        self.prompt_template = prompt_template
        self.if_should_browse = if_should_browse
        self.if_should_not_browse = if_should_not_browse

    def __call__(self, query: str) -> str:
        should_browse_info = "Should I browse the web for an answer?: {should_browse}"
        if self.should_browse(query):
            self.if_should_browse.set_trace(
                ChainTrace(
                    should_browse_info.format(should_browse="yes") + "\n", "thought"
                )
            )
            result = self.if_should_browse(query)
            return result
        else:
            self.if_should_not_browse.set_trace(
                ChainTrace(
                    should_browse_info.format(should_browse="no") + "\n", "thought"
                )
            )
            result = self.if_should_not_browse(query)
            return result

    def should_browse(self, question: str) -> bool:
        """
        Asks the model if it should browse the web for an answer.

        :param question: The base question.
        :return: Decision to browse the web or not.
        """
        prompt = self.prompt_template.render(question=question)
        generated_answer = self.language_model.query(prompt)
        final_answer = postprocess_answer(
            generated_answer, self.prompt_template.fix_text
        )
        if final_answer == "No":
            return False
        else:
            return True

    def show_info(self):
        print("===== SelfAware =====")
        print(f"Language model: {self.language_model}")
        print(f"Prompt template: {self.prompt_template}")
        print("If Should Browse:")
        self.if_should_browse.show_info()
        print("If Should Not Browse:")
        self.if_should_not_browse.show_info()
