import discord
import random
import game
from discord.ext import commands
import openai
import configparser
import requests


# Make the request
url = 'https://api.github.com/repos/olivier-be/bot_discord/tags'
response = requests.get(url)
tag = response.json()

if configparser["version"]== tag[-1]['name']:
    print("update a available: {} to {}".format(configparser["version"],tag[-1]['name']))
    print("git pull recommend")
else:
    print("last update install")

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
    size=len(message_content)-1

    print(f'{username}: {message_content} {channel}')
    if message.author == client.user:
        return
    elif "feur"==message_content and not games:
        await message.channel.send("me ta gueule")  # response in French to bot feur
    elif "bot" in message.content:
        e = discord.Embed()
        e.set_thumbnail(url="https://media.tenor.com/8XNZFtwJxscAAAAC/reverse-card-uno.gif")
        await message.channel.send(embed=e)
    elif "toxic" in message_content:
        await message.channel.send("I am here")
    elif "windows" in message_content:
        await message.channel.send("linux > ")
    elif games and channel_game == channel:
        if message_content != "!end":
            if message_content == find:

                games = False
                await message.channel.send("gg")
            else:
                messages = openai.Completion.create(model="text-davinci-003",
                                                    prompt="give an hint without give answer without " + find + " in the answer and the last word give " + message_content + " give information about if is close to find the word",
                                                    temperature=0, max_tokens=50)
                await message.channel.send(messages['choices'][0]['text'])
    else:
        await client.process_commands(message)


@client.command()
async def spam(ctx, amount: int, size: int,*, message):
    if amount < 10000000 and size < 50:
        res = ""
        for e in range(size):
            res += message + " "
        for i in range(amount):  # Do the next thing amount times
            await ctx.send(res)
    else:
        await ctx.send(message)
@client.command()
async def game(message):
    channel=message.channel
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
@client.command()
async def version(ctx):
    await ctx.channel.send("https://github.com/olivier-be/bot_discord/")
    await ctx.channel.send("V1.7 fair bot")
@client.command()
async def end(ctx):
    global games
    games=False
    await ctx.channel.send("You can make better next time ")

@client.command()
async def stopgame(ctx):
    global games
    games = False
    await ctx.channel.send("You Close the running game ")
@client.command()
async def clear_message(ctx,nb:int):
    if ctx.author.top_role.permissions.manage_messages:# can give acces all to delete message
        await ctx.channel.purge(limit=nb)
    else:
        await ctx.channel.send("You don't have permissions to manage_messages")

@client.command()
async def Dalle2(ctx,*,message_content):
        response = openai.Image.create(
            prompt=message_content,
            n=1,
            size="1024x1024"
        )
        await ctx.channel.send(response['data'][0]['url'])

@client.command()
async def gpt3(ctx,*,message_content):
        messages = openai.Completion.create(model="text-davinci-003", prompt=message_content, temperature=0, max_tokens=500)
        print(messages['choices'][0]['text'])
        await ctx.channel.send(str(messages['choices'][0]['text']))

@client.command()
async def update(ctx):
    if configparser["version"] == tag[-1]['name']:
        print("update a available: {} to {}".format(configparser["version"], tag[-1]['name']))
        print("git pull recommend")
    else:
        print("last update install")


client.run(private_key.discord_key)  # discord api key
