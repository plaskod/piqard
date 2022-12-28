from piqard.PIQARD import PIQARD
from piqard.extensions.react.action import Action
from piqard.utils.yaml_constructor import yaml_constructor
from piqard.utils.chain_trace import ChainTrace
from piqard.language_models.language_model import LanguageModel
from piqard.utils.prompt_template import PromptTemplate


@yaml_constructor
class Agent(PIQARD):
    def __init__(
        self,
        actions: list[Action],
        prompt_template: PromptTemplate,
        language_model: LanguageModel,
    ) -> None:
        super().__init__(prompt_template, language_model)
        self.actions = actions
        self.sequence_stopper = Action(
            name="Sequence stopper", func=lambda x: x, prefix="Finish"
        )

    def __call__(self, query: str, possible_answers: str = None) -> dict:
        prompt = self.prompt_template.render(
            question=query,
            possible_answers=possible_answers,
        )

        if self.trace is None:
            self.trace = ChainTrace(
                prompt + "\n", "base_prompt"
            )  # initialize the trace with the base prompt
        else:
            self.trace.add(prompt + "\n", "base_prompt")

        intermediate_answer = self.language_model.query(prompt)

        max_iterations = 20
        flag = True
        while flag and max_iterations > 0:
            max_iterations -= 1
            if intermediate_answer.startswith("Thought"):
                self.trace.add(intermediate_answer + "\n", "thought")

            elif intermediate_answer.startswith("Action"):
                self.trace.add(intermediate_answer + "\n", "action")
                if self.sequence_stopper.check(intermediate_answer):
                    final_answer = self.sequence_stopper(intermediate_answer)
                    self.trace.add(final_answer + "\n", "finish")
                    break
                for action in self.actions:
                    if action.check(intermediate_answer):
                        retrieved_context = action(intermediate_answer)
                        retrieved_context = f"Observation: {' '.join(retrieved_context)}"
                        self.trace.add(retrieved_context + "\n", "observation")

            intermediate_answer = self.language_model.query(self.trace.compose())

        return {
            "prompt": prompt,
            "raw_answer": self.trace.compose()[len(prompt):],
            "answer": self.trace.get_deepest_node().data,
            "context": None,
            "prompt_examples": None,
            "chain_trace": self.trace.to_json(),
        }
