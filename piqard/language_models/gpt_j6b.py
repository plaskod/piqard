import torch
from transformers import GPTJForCausalLM, AutoTokenizer

from piqard.language_models.language_model import LanguageModel


class GPTj6b(LanguageModel):
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = GPTJForCausalLM.from_pretrained(
            "EleutherAI/gpt-j-6B", revision="float16", low_cpu_mem_usage=True
        )
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

    def query(self, prompt: str) -> str:
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(
            self.device
        )

        generated_ids = self.model.generate(
            input_ids, do_sample=True, temperature=1.0, max_length=36
        )
        generated_text = self.tokenizer.decode(generated_ids[0])
        return generated_text

    def __str__(self) -> str:
        return "GPT-J6B"
