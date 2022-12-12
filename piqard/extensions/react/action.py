import re
from dataclasses import dataclass
from typing import Callable

from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
@dataclass
class Action:
    name: str
    func: Callable[[str], str]
    prefix: str

    def check(self, input: str) -> bool:
        """
          Check if the action is appropriate for the given action by comparing prefix attribute with input in form: 'Action: Prefix[When was Aristotle born?]'
        """
        regex_rule = f"{self.prefix}\[.*?\]"
        if len(re.findall(regex_rule, input)) != 0 and len(re.findall(regex_rule, input)) == 1:
            return True
        return False

    def extract_query(self, input: str) -> str:
        """
          This method checks if the input has a matching command for the action and then extracts the inside of the command
          For an input with a command e.g 'Action 1: Search[When was Aristotle born?]' should return: When was Aristotle born?
        """
        rule_for_cleaning = f"{self.prefix}\[.*?\]"
        cleaned_input = re.findall(rule_for_cleaning, input)
        assert len(cleaned_input) != 0, f"Did not find a matching command in the input: {input}"
        assert len(cleaned_input) == 1, f"Input has multiple commands input: {input}"
        cleaned_input = cleaned_input[0].replace(self.prefix + '[', '').replace(']', '')
        return cleaned_input

    def __call__(self, input: str):
        """
          The call should receive input in command form, e.g.: 'Search[When was Aristotle born?]'
          Then passes extracted content, e.g. When was Aristotle born?
        """
        query = self.extract_query(input)
        return self.func(query)
