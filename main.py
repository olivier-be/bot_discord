import time

import discord
import random
import game
from discord.ext import commands
import openai
import configparser
import requests
from os import getcwd
from PIL import Image, ImageDraw,ImageFont
import private_key



path = getcwd()
config = configparser.ConfigParser()
config.read('.editorconfig') #ouverture ficher config
config.sections()
# Make the request
url = 'https://api.github.com/repos/olivier-be/bot_discord/tags'
response = requests.get(url)
tag = response.json()

if config["version"]["version"] >= tag[0]['name']:
    print("last update install")
else:
    print("update a available: {} to {}".format(config["version"]["version"],tag[0]['name']))
    print("git pull recommend")



openai.organization = private_key.openai_org  # openai key with org-
openai.api_key = private_key.openai_api_key  # openai api key

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
objects = game.objects

current=None
next=None
eventlistH = (current, next)

@client.event
async def on_ready():
    print('Ready!')

    await client.change_presence(activity=discord.Game("I will spread toxicity throughout this server!"))


games = False
channel_game = ""
find = ""


@client.event
async def on_message(message): # look at all the messages
    global objects, channel_game, find, games
    username = str(message.author).split('#')[0]
    message_content = str(message.content)
    channel = str(message.channel.name)
    size=len(message_content)-1

    print(f'{username}: {message_content} {channel}')
    if message.author == client.user:
        return
    elif "feur"==message_content and not games:
        await message.channel.send("me ta gueule ")  # response in French to bot feur
    elif " bot " in message.content:
        e = discord.Embed()
        e.set_thumbnail(url="https://media.tenor.com/8XNZFtwJxscAAAAC/reverse-card-uno.gif")
        await message.channel.send(embed=e)
    elif "toxic" in message_content:
        await message.channel.send("I am here")
    elif "windows" in message_content:
        await message.channel.send("linux > ")
    elif games and str(channel_game) == channel and message_content!="!end":
        if message_content != "!end":
            if message_content == find:

                games = False
                await message.channel.send("gg "+message.author.mention)
            else:
                messages = openai.Completion.create(model="text-davinci-003",
                                                    prompt="The game is to make the word guess :" + find + ". In the answer the last answer give is : " + message_content + ". Dont say the word to guess ",
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
async def game(message): # start game
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
    await ctx.channel.send("{} fair bot".format(config["version"]["version"]))
@client.command()
async def end(ctx):
    global games, channel_game
    if game and ctx.channel==channel_game:
        games=False
        await ctx.channel.send("You can make better next time "+ ctx.author.mention)
    else:
        await ctx.channel.send("any game is running ont this channel")

@client.command()
async def stopgame(ctx):
    global games
    games = False
    await ctx.channel.send("You close the running game ")
@client.command()
async def clear_message(ctx,nb:int):
    if ctx.author.top_role.permissions.manage_messages:# can give acces all to delete message
        await ctx.channel.purge(limit=nb)
    else:
        await ctx.channel.send("You don't have permissions to manage_messages")

@client.command()
async def Dalle2(ctx,*,message_content): # return picture form dalle 2
        response = openai.Image.create(
            prompt=message_content,
            n=1,
            size="1024x1024"
        )
        await ctx.channel.send(response['data'][0]['url'])

@client.command()
async def gpt3(ctx,*,message_content): # write gpt chat response
        messages = openai.Completion.create(model="text-davinci-003", prompt=message_content, temperature=0, max_tokens=500)
        print(messages['choices'][0]['text'])
        await ctx.channel.send(str(messages['choices'][0]['text']))

@client.command()
async def update(ctx): # check update
    if config["version"]["version"] >= tag[0]['name']:
        await ctx.channel.send("last update install")
    else:
        await ctx.channel.send("update a available: {} to {}".format(config["version"]["version"], tag[0]['name']))
        await ctx.channel.send("git pull recommend")
@client.command()
async def avatar(message): #print avatar
    e = discord.Embed()
    e.set_thumbnail(url=message.author.display_avatar)
    await message.channel.send(embed=e)

def separator(str_size,s,n):
    if str_size > n - 1:
        return n
    elif (str_size < n and s[str_size] == " "):
        return str_size
    else :
        u=0
        i=0
        while i<str_size:
            if s[i]==" " :
                u=i
            i+=1

        return u

def find_picture(n):  # randomly returns an image
    tab=[]
    for i in range (1,int(config["quote_picture"]["nb_file"])+1):
        if (int(config[str(i)+".png"]["nb_max_line"])*int(config[str(i)+".png"]["nb_max_c"])>=n):
            tab.append(str(i)+".png")
    return tab

@client.command()
async def quote(message,*,message_content:str): #write word on image
    global path
    tab_pic_val=find_picture(len(message_content))
    if tab_pic_val==[]:
        name_picture = str(random.randint(1, int(config["quote_picture"]["nb"]))) + ".png"
    else:
        name_picture=random.choice(tab_pic_val)
    path_picture=path+"\\picture\\"+name_picture
    im = Image.open(path_picture)
    pix = im.load()
    draw = ImageDraw.Draw(im)
    font1 = ImageFont.truetype("arial.ttf", int(im.size[0] * 0.04))
    y=(int(im.size[0] * 0.10))
    i=0

    while i<int(config[name_picture]["nb_max_line"]):
        str_size =int(config[name_picture]["nb_max_c"])
        size=len(message_content)
        n=separator(str_size,message_content,size)
        draw.text((int(im.size[0] * 0.10), y), message_content[0:n], fill=(255, 255, 255), font=font1)
        y+=int(im.size[0] * 0.04)
        message_content=message_content[n:size]
        i+=1
    im.save(path+"\\picture\\temp.png", "PNG")
    final_picture=path+"\\picture\\temp.png"
    await message.channel.send(file=discord.File(final_picture))





client.run(private_key.discord_key)  # discord api key
