import discord
import csv
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

async def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
async def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))

async def generate_message(input, tokenizer, model):

    input_ids = tokenizer.encode(input, return_tensors='pt')

    # Update conversation history
    conversation_history.append(input)

    # Construct attention mask with dynamic weights
    attention_mask = torch.zeros((1, len(tokenizer.encode(conversation_history[-1]))), dtype=torch.long, device=input_ids.device)
    
    # Decay factor for attention weights (adjust as needed)
    decay_factor = 0.9  # Example decay factor
    
    for i, message in enumerate(conversation_history):
        message_tokens = tokenizer.encode(message)
        decayed_weight = torch.tensor(decay_factor ** (len(conversation_history) - 1 - i), dtype=torch.float)  # Compute decayed weight
        attention_mask[0, :len(message_tokens)] += decayed_weight.to(torch.long)  # Convert to long before adding

    generated = model.generate(input_ids, attention_mask=attention_mask, max_length=50, num_return_sequences=1,
                               no_repeat_ngram_size=4, do_sample=True, top_k=25, top_p=0.87, temperature=0.92, pad_token_id=model.config.eos_token_id)
    response = tokenizer.decode(generated[0], skip_special_tokens=True)

    response = response.replace(' 3 ', ' <3 ')
    response = response.replace(' 3', ' <3')

    if response == '3':
        response = response.replace('3', '<3')

    return response

filtered = []

conversation_history = []

def run_discord_bot():

    # token and intents
    with open('token.txt') as token_file:
        TOKEN = token_file.read()

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    # Load the fine-tuned model and tokenizer
    model_path = './training/flan'
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)

    # on start
    @client.event
    async def on_ready():
        game = discord.Game('T5 (auto-response) Mode')
        print(f'{client.user} is now running!')
        await client.change_presence(status=discord.Status.idle, activity=game)
    
    @client.event
    async def on_message(message):

        global conversation_history

        # checks to not respond to self or bots
        if message.author == client.user or message.author.bot == True:
            return
        
        # gather info
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        await prLightPurple(f'{username} said: "{user_message}" ({channel})')

        # command and ping check.
        if channel == 'Direct Message with Unknown User':

            response = await generate_message(user_message, tokenizer, model)

            if response == '':
                await message.author.send('Generated nothing. (system message)')
                await prYellow(f'bot: {response}')

            else:
                await prYellow(f'bot: {response}')
                msg_filtered = 0
                for word in filtered:
                    if word in response.lower():
                        await message.author.send('Filtered. (system message)')
                        msg_filtered = 1
                        break

                if msg_filtered == 0:
                    await message.author.send(f'{response}')

        elif '<@1210510020094074890>' in user_message:

            user_message = user_message.replace('<@1210510020094074890>', '')
            user_message = user_message.replace('<@&1210530396266045462>', '')
            if user_message[0] == ' ':
                user_message = user_message[1:]
            if user_message[len(user_message)-1] == ' ':
                user_message = user_message[:len(user_message)-1]
            if '  ' in user_message:
                user_message = user_message.replace('  ', ' ')

            response = await generate_message(user_message, tokenizer, model)

            if response == '':
                await message.channel.send('Generated nothing. (system message)')
                await prYellow(f'bot: {response}')

            else:

                await prYellow(f'bot: {response}')

                msg_filtered = 0
                for word in filtered:
                    if word in response.lower():
                        await message.channel.send('Filtered. (system message)')
                        msg_filtered = 1
                        break
                if msg_filtered == 0:
                    await message.channel.send(f'{response}')

        elif channel == 'roki-bot':

            response = await generate_message(user_message, tokenizer, model)

            if response == '':
                await message.channel.send('Generated nothing. (system message)')
                await prYellow(f'bot: {response}')

            else:

                await prYellow(f'bot: {response}')

                msg_filtered = 0
                for word in filtered:
                    if word in response.lower():
                        await message.channel.send('Filtered. (system message)')
                        msg_filtered = 1
                        break
                if msg_filtered == 0:
                    await message.channel.send(f'{response}')

    # runs
    client.run(TOKEN)
