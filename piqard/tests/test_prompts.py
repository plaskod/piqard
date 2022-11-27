import pytest
from transformers import BloomTokenizerFast
import glob

from piqard.utils.jinja_loader import JINJALoader 

# 1. arrange 
@pytest.fixture
def lengths_of_tokenized_openbookqa_prompts(path_to_openbookqa_prompts = r"piqard\assets\prompting_templates\openbookqa\*.txt"):
    token_lengths = []
    tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom")
    
    for prompt_template in glob.glob(path_to_openbookqa_prompts):
        prompt = JINJALoader.load(prompt_template)
        tokenized_prompt = tokenizer(prompt)
        token_lengths.append(len(tokenized_prompt["input_ids"]))     
    return token_lengths

def check_openbookqa_prompts_do_not_exceed_max_num_of_tokens(lengths_of_tokenized_openbookqa_prompts) -> None:
    assert all([length <= 1000 for length in lengths_of_tokenized_openbookqa_prompts])
    
if __name__ == "__main__":
    path_to_openbookqa_prompts = r"piqard\assets\prompting_templates\openbookqa\*.txt"
    for prompt_template in glob.glob(path_to_openbookqa_prompts):
        prompt = JINJALoader.load(prompt_template)
        print(prompt)
        print(len(prompt))
        print("")