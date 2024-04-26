import discord
import random
import game
from discord.ext import commands
import openai
import configparser
import requests
from PIL import Image, ImageDraw,ImageFont
import private_key



path =  private_key.path
config = configparser.ConfigParser()
config.read( private_key.path + '.editorconfig') #ouverture ficher config
config.sections()
# Make the request
url = 'https://api.github.com/repos/olivier-be/bot_discord/tags'
response = requests.get(url)
tag = response.json()

if  config["version"]["version"] == tag[0]['name']:
    print("last update install")
else:
    print("update a available: t{}t to t{}t".format(config["version"]["version"],tag[0]['name']))
    print("git pull recommend")

#upgrade to last version of openai
#self hosted ai change base url elser remove base_url
client_llama = openai.OpenAI(
        base_url=private_key.openai_org, # "http://<Your api-server IP>:port"
        api_key = "sk-no-key-required",
        )


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
objects = game.objects

current=None
next=None
eventlistH = (current, next)

games= []

@client.event
async def on_ready():
    print('Ready!')

    await client.change_presence(activity=discord.Game("I will spread toxicity throughout this server!"))




@client.event
async def on_message(message): # look at all the messages
    global objects, games
    username = str(message.author).split('#')[0]
    message_content = str(message.content)
    channel = str(message.channel.name)
    size=len(message_content)-1

    print(f'{username}: {message_content} {channel}')
    i=0
    while i < len(games) and ((games[i] != None and games[i][0] != channel)  or games[i] == None):
        i += 1

    if message.author == client.user:
        return

    elif " bot " in message.content:
        e = discord.Embed()
        e.set_thumbnail(url="https://media.tenor.com/8XNZFtwJxscAAAAC/reverse-card-uno.gif")
        await message.channel.send(embed=e)
    elif "toxic" in message_content:
        await message.channel.send("I am here")
    elif "windows" in message_content:
        await message.channel.send("linux > ")

    elif i < len(games) and games[i] != None and games[i][0] == channel and message_content != "!end" :
        if message_content == games[i][1]:

            games[i]=None
            await message.channel.send("gg "+message.author.mention)
        else:
            messages = client_llama.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                    {"role": "system", "content": "Short responce for the game .The game is to make the word guess :" + games[i][1] + ". In the answer the last answer give is : " + message_content + ". Never say " + games[i][1]},
                            {"role": "user", "content":"give me a hint"}
                            ]
                        )

            await message.channel.send(messages.choices[0].message.content)
    elif "feur"==message_content:  # response in French to bot feur
        await message.channel.send("why ? ")
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
async def Game(message): # start game
    channel=message.channel
    global games
    isfind=False
    i=0
    while i<len(games) and games[i]!=None and games[i][0] != channel :
        i+=1

    if i == len(games):
        find = objects[int(random.uniform(0, 374))]
        games.append((str(channel), find))
        print(find)
        await message.channel.send("What am i thinking ?")
    elif games[i]!=None and games[i][0] == channel:
        await message.channel.send("one game already run")
    else:
        find = objects[int(random.uniform(0, 374))]
        games[i]=(str(channel), find)
        print(find)
        await message.channel.send("What am i thinking ?")

@client.command()
async def version(ctx):
    await ctx.channel.send("https://github.com/olivier-be/bot_discord/")
    await ctx.channel.send("{} fair bot".format(config["version"]["version"]))
@client.command()
async def end(ctx):
    global games
    channel=ctx.channel
    i=0
    while i<len(games) and (games[i]==None or games[i][0] != str(channel)) :
        i+=1
    if i == len(games):
        await ctx.channel.send("any game is running ont this channel")
    else:
        games[i]=None
        await ctx.channel.send("You can make better next time "+ ctx.author.mention)


@client.command()
async def stopgame(ctx):
    global games
    channel=ctx.channel
    i=0
    while i < len(games) and games[i] != None and games[i][0] != channel:
        i += 1
    if i == len(games):
        await ctx.channel.send("any game is running ont this channel")
    else:
        games[i] = None
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
async def llama(ctx,*,message_content): # write gpt chat response
    messages = client_llama.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
                {"role": "user", "content": message_content}
                ]
            )

    print(messages.choices[0].message.content)
    p = 0
    s = str(messages.choices[0].message.content)
    n = len(s)
    while p + 2000 < n:
        await ctx.channel.send(s[p:2000])
        p += 2000;
    await ctx.channel.send(s[p:]) 

@client.command()
async def update(ctx): # check update
    response = requests.get(url)
    tag = response.json()
    if config["version"]["version"] == tag[0]['name']:
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
    path_picture=path+"/picture/"+name_picture
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
    im.save(path+"/picture/temp.png", "PNG")
    final_picture=path+"/picture/temp.png"
    await message.channel.send(file=discord.File(final_picture))





client.run(private_key.discord_key)  # discord api key
