from piqard import PIQARD
from piqard.language_models.language_model import LanguageModel
from piqard.utils.answer_postprocess import postprocess_answer
from piqard.utils.chain_trace import ChainTrace
from piqard.utils.prompt_template import PromptTemplate


class SelfAware:
    def __init__(
        self,
        prompt_template: PromptTemplate,
        language_model: LanguageModel,
        if_should_browse: PIQARD,
        if_should_not_browse: PIQARD,
    ):
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
        print("== SelfAsk")
        print("If Should Browse: {}".format(self.if_should_browse))
        print("If Should Not Browse: {}".format(self.if_should_not_browse))
        print("")