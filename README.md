# roki bot

The bot is named 'roki' because it's just a silly nickname that was given to me, so I figured it would fit a bot that is based on me.

## Features
- Automatic reading and responding to messages fed in from the Discord API
- Uses a transformer library to perform artificially generation of messages
- Basic low level self-attention mask to ensure that it at least attempts to stay within the realm of conversation

## Notes
The model that is primarily used in the case of this bot is a fine-tuned model of the T5 Flan model from Google, with additional training done on my personal computer. The additional training was performed using a dataset of my direct messages with friends, in an attempt to push the model to respond more in my likeness. This is somewhat accomplished though as of right now, it lacks functionality to really respond in a coherent way even with something like a self-attention mask.
