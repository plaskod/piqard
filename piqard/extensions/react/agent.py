from piqard.PIQARD import PIQARD
from piqard.extensions.react.action import Action
from piqard.utils.yaml_constructor import yaml_constructor
from piqard.utils.chain_trace import ChainTrace
from piqard.language_models.language_model import LanguageModel
from piqard.utils.prompt_template import PromptTemplate


@yaml_constructor
class Agent(PIQARD):
    """
    Agent is a class that implements prompting strategy named ReAct, which is based on the idea of possibility to perform the given actions.
    """

    def __init__(
        self,
        actions: list[Action],
        prompt_template: PromptTemplate,
        language_model: LanguageModel,
    ) -> None:
        """
        Constructor of the Agent class.

        :param actions: Possiblr actions to perform.
        :param prompt_template: The prompt template to use.
        :param language_model:  The language model to use.
        """
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
        last_answer = intermediate_answer
        repeated_answer_counter = 0
        max_iterations = 20
        while max_iterations > 0:
            max_iterations -= 1
            if intermediate_answer.startswith("Thought"):
                repeated_answer_counter = 0
                self.trace.add(intermediate_answer + "\n", "thought")

            elif intermediate_answer.startswith("Action"):
                repeated_answer_counter = 0
                self.trace.add(intermediate_answer + "\n", "action")
                if self.sequence_stopper.check(intermediate_answer):
                    final_answer = self.sequence_stopper(intermediate_answer)
                    self.trace.add(final_answer + "\n", "finish")
                    break
                for action in self.actions:
                    if action.check(intermediate_answer):
                        retrieved_context = action(intermediate_answer)
                        retrieved_context = (
                            f"Observation: {' '.join(retrieved_context)}"
                        )
                        self.trace.add(retrieved_context + "\n", "observation")
            elif intermediate_answer == last_answer:
                repeated_answer_counter += 1
                if repeated_answer_counter > 1:
                    self.trace.add("Sorry, I could not answer your question" + "\n", "finish")
                    break
            last_answer = intermediate_answer
            intermediate_answer = self.language_model.query(self.trace.compose())

        result = {
            "prompt": prompt,
            "raw_answer": self.trace.compose()[len(prompt) :],
            "answer": self.trace.get_deepest_node().data,
            "context": None,
            "prompt_examples": None,
            "chain_trace": self.trace,
        }
        self.trace = None
        return result
