import os.path
import jinja2
import json
import numpy as np
from information_retrieval.vector_retriever.vector_retirever import VectorRetriever


class PromptGenerator:
    @staticmethod
    def load_template(prompt_template: str) -> jinja2.Template:
        environment = jinja2.Environment()

        if os.path.isfile(prompt_template):
            with open(prompt_template, 'r') as file:
                prompt_template = file.read()
        return environment.from_string(prompt_template)




class OpenBookQAPromptBuilder(PromptGenerator):
    """ A prompt builder to randomly select n examples from the OpenBookQA dataset, retreive k facts for each example and construct a prompt.
            #TODO: read from Jinja2 template file
            #TODO: add a cache to avoid retreiving the same facts for the same question
            #TODO: 
            
            @param path: path to the OpenBookQA dataset
            @param n_shot: number of examples to select
            @param k_facts: number of facts to select for each example
            @param 
            
            @return: a prompt template with the following format:  
            Answer the question based on the facts.
            Question: {question}
            Possible answers: {possible_answers}
            Facts: {facts}
            Answer:
    """
    
    prefix_template = "Answer the question based on the facts.\n\n"
    infix_template = "Question: {question}\nPossible answers: {possible_answers}\nFacts: {facts}\nAnswer: {correct_answer}\n\n"
    postfix_template = "Question: {question}\nPossible answers: {possible_answers}\nFacts: {facts}\nAnswer: "
    
    def __init__(self):
        self.cached_prompts = []
    
    def build(self, path_training_set: str, retriever, n_shot: int = 5, k_facts: int = 3) -> Prompt:
        prompt = self.prefix_template
         # open a jsonl file with the training set
        with open(path_training_set) as f:
            train_set = [json.loads(line) for line in f.readlines()]
            
        # select n_shot random  examples from the training set
        samples = np.random.choice(train_set, n_shot, replace=False)
        
        for sample in samples:
            question_in_sample = sample["question"]["stem"]
            
            possible_answers_dict = {}
            for multiplechoice_answer in sample["question"]["choices"]:
                # possible_answers += f"{multiplechoice_answer['label']}: {multiplechoice_answer['text']} "
                possible_answers_dict[multiplechoice_answer['label']] = multiplechoice_answer['text']
                
            correct_answer_key = sample["answerKey"]
            correct_answer = f"{correct_answer_key}: {possible_answers_dict[correct_answer_key]}"
            
            possible_answers = ''
            for label, answer in possible_answers_dict.items():
                possible_answers += f"{label}: {answer} "
            
            retreived_facts = retriever.get_documents(question_in_sample, k_facts)
            facts = '; '.join(retreived_facts)
            
            prompt += self.infix_template.format(question=question_in_sample, possible_answers=possible_answers, facts=facts, final_answer=correct_answer)
        
        prompt += self.postfix_template 
        self.cached_prompts.append(prompt)
        
        return prompt
    
    def save_last_prompt(self, path: str):
        with open(path, 'w') as f:
            f.write(self.cached_prompts[-1])