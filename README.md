# Language Model Chatbot -- 'roki'

The bot is named 'roki' because it's just a silly nickname that was given to me, so I figured it would fit a bot that is based on me.

## Features
- Automatic reading and responding to messages fed in from the Discord API
- Uses a transformer library to perform artificially generation of messages
- Basic low level self-attention mask to ensure that it at least attempts to stay within the realm of conversation

## Files
- main.py : Runs the bot
- bot.py : Handles bot input, output, as well as the attention mask for the model
- training/save_base_(model).py : Saves a new, clean version of a model type
- training/train.py : Either can start from scratch or continue to train an existing model within the folder
- training/data.csv : Holds data in desired input / output format for training the model
- training/eval.csv : Holds data in desired input / output format for evaluating how well the training is being performed
- data-cleaning/dms.py : A data cleaner for a csv file that holds Discord DM data, outputs a csv that is compatible for training

## Notes
The model that is primarily used in the case of this bot is a fine-tuned model of the T5 Flan model from Google, with additional training done on my personal computer. The additional training was performed using a dataset of my direct messages with friends, in an attempt to push the model to respond more in my likeness. This is somewhat accomplished though as of right now, it lacks functionality to really respond in a coherent way even with something like a self-attention mask.

The model itself will not be uploaded with this project, but the written code to accomplish what is done so far will be here.

Uses the python Transformers and Torch libraries to utilize language model data.
