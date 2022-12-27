import discord
import random
import game
from discord.ext import commands
import openai

import private_key

openai.organization = private_key.openai_org  # openai key with org-
openai.api_key = private_key.openai_api_key  # openai api key

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
objects = game.objects


@client.event
async def on_ready():
    print('Ready!')

    await client.change_presence(activity=discord.Game("I will spread toxicity throughout this server!"))


games = False
channel_game = ""
find = ""


@client.event
async def on_message(message):
    global objects, channel_game, find, games
    username = str(message.author).split('#')[0]
    message_content = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {message_content} {channel}')
    if message.author == client.user:
        return
    elif "feur" in message_content and not games:
        await message.channel.send("me ta gueule")  # response in French to bot feur
    elif "bot" in message.content:
        e = discord.Embed()
        e.set_thumbnail(url="https://media.tenor.com/8XNZFtwJxscAAAAC/reverse-card-uno.gif")
        await message.channel.send(embed=e)
    elif "!openai_image" in message_content:
        response = openai.Image.create(
            prompt=message_content[13: len(message_content)],
            n=1,
            size="1024x1024"
        )
        await message.channel.send(response['data'][0]['url'])
    elif "!openai" in message_content:
        str1 = message_content[7: len(message_content)]
        messages = openai.Completion.create(model="text-davinci-003", prompt=str1, temperature=0, max_tokens=500)
        print(messages['choices'][0]['text'])
        await message.channel.send(str(messages['choices'][0]['text']))
    elif "toxic" in message_content:
        await message.channel.send("I am here")
    elif "!version" in message_content:
        await message.channel.send("https://github.com/olivier-be/bot_discord/")
        await message.channel.send("V1.2 fair bot")
    elif "windows" in message_content:
        await message.channel.send("linux > ")
    elif "!game" in message_content:
        await game_start(message, channel)
    elif games and channel_game == channel:
        if message_content == "!end":
            games = False
            await message.channel.send("You can make better next time ")
        else:
            if message_content == find:

                games = False
                await message.channel.send("gg")
            else:
                messages = openai.Completion.create(model="text-davinci-003",
                                                    prompt="give an hint without give answer without " + find + " in the answer and the last word give " + message_content + " give information about if is close to find the word",
                                                    temperature=0, max_tokens=50)
                await message.channel.send(messages['choices'][0]['text'])
    elif "!stopgame" in message_content:
        games = False


@client.command()
async def game_start(message, channel):
    global games, channel_game, find
    if games:
        if channel_game != channel:
            await message.channel.send("you need to close your old game in the channel")
        else:
            await message.channel.send("one game already run")
    else:
        games = True
        channel_game = channel
        find = objects[int(random.uniform(0, 374))]
        print(find)
        await message.channel.send("What am i thinking ?")


client.run(private_key.discord_key)  # discord api key
