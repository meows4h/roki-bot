from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

# Load datasets
dataset = load_dataset('csv', data_files={'train': 'data.csv'})
eval_data = load_dataset('csv', data_files={'eval': 'eval.csv'})

mode_inp = int(input('welcome to the roki training software!\n 1 -> start from scratch\n 2 -> retrain same model more\n\nenter: '))

if mode_inp == 1:
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
else:
    tokenizer = T5Tokenizer.from_pretrained("./flan")
    model = T5ForConditionalGeneration.from_pretrained("./flan")

# Tokenize function
def tokenize_function(examples):
    inputs = examples['input']
    targets = examples['output']
    inputs_dict = tokenizer(inputs, padding="max_length", truncation=True)
    targets_dict = tokenizer(targets, padding="max_length", truncation=True)

    return {
        'input_ids': inputs_dict['input_ids'],
        'attention_mask': inputs_dict['attention_mask'],
        'labels': targets_dict['input_ids'],
    }

# Tokenize datasets
tokenized_datasets = dataset.map(tokenize_function, batched=True)
tokenized_eval = eval_data.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',
    learning_rate=1e-4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir='./logs',
    logging_steps=100,
    overwrite_output_dir=True,
)

# Instantiate Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_eval['eval'],
)

# Start training
trainer.train()

# Save model and tokenizer
model.save_pretrained('./flan')
tokenizer.save_pretrained('./flan')