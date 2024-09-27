import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.save_pretrained('./fine_tuned_model', save_tokenizer=True)
tokenizer.save_pretrained('./fine_tuned_model')
