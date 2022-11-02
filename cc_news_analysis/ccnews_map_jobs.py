import pandas as pd
import datasets
import time
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

start = time.time()
cc_news = datasets.load_from_disk('cc_news')
print(time.time() - start)

# token lengths
# def get_token_ns(example):
#     example["token_n"] = [x.count(" ")+1 for x in example['text']]
#     return example
#
# cc_news = cc_news.map(get_token_ns, batched=True)


# tokenization
# def tokenization(example):
#     return tokenizer(example["text"])

# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# cc_news = cc_news.map(tokenization, batched=True)


# vectorization
# def encoding(example):
#     example["encoding"] = model.encode(example['text'])
#     return example

# model = SentenceTransformer('all-MiniLM-L6-v2')
# cc_news = cc_news.map(encoding, batched=True)
