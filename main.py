import discord
import random
import game
from discord.ext import commands
import openai
import configparser
import requests
from PIL import Image, ImageDraw,ImageFont
import private_key
import subprocess
import yaml
import json
import zipfile
import os
import shutil

path =  private_key.path
config = configparser.ConfigParser()
config.read( private_key.path + '/.editorconfig') #ouverture ficher config
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




def dockerconfig(s ,version):
    data = {
       'services': {
            'minecraft-server':{
                'image':'itzg/minecraft-server',
                'tty':'true',
                'stdin_open':'true',
                'ports':['25565:25565'],
                'environment':
                    {
                        'VERSION':version,
                        'EULA':"TRUE",
                        'ENABLE_COMMAND_BLOCK':"TRUE",
                        'MEMORY': "5G"
                    },
                'volumes':[ './data:/data'],
                    },
                },
        }
     
    with open(s + '/docker-compose.yaml', 'w') as file:
         yaml.dump(data, file)


@client.command()
async def minecraft_setup(message,*,version:str): 
    if message.author.id in private_key.admin:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(["mkdir", s])
        dockerconfig(s,version)
        await message.channel.send("data for server setup")
    else:
        await message.channel.send("demand to bot admin for setup the server")


@client.command() 
async def minecraft_remove(message): 
    if message.author.id in private_key.admin:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(["docker-compose","-f",
                    s + '/docker-compose.yaml',
                    "down"])
        subprocess.run(["rm","-rf", s])
        await message.channel.send("data for server remove")
    else:
        await message.channel.send("demand to bot admin for setup the server")

@client.command() 
async def minecraft_reset(message): 
    if message.author.id in private_key.admin:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(["docker-compose","-f",
                    s + '/docker-compose.yaml',
                    "down"])
        subprocess.run(["rm","-rf", s + 'data/world'])
        await message.channel.send("data for server remove")
    else:
        await message.channel.send("demand to bot admin for setup the server")



@client.command() 
async def minecraft(message,start:int): 
    #if ctx.author.username == "furious": 

    s =  private_key.path + "mincraft-" + str(message.guild.id)
    if start == 1 and (message.author.mention == discord.Permissions.administrator 
    or message.author.id in private_key.admin) :
        subprocess.run(["docker-compose","-f",
                    s+ '/docker-compose.yaml',
                    "up","-d"]) 
        await message.channel.send("server start")
    else:
        subprocess.run(["docker-compose","-f",
                    s + '/docker-compose.yaml',
                    "down"])
        await message.channel.send("server stop")


@client.command()
async def minecraft_op(message,uuid:str,*,name:str): 
    if ((message.author.mention == discord.Permissions.administrator)
         or message.author.id):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        #print(s + '/data/ops.json')
        with open(s + '/data/ops.json','r') as file:
          # First we load existing data into a dict.
            #print(file)
            file_data = json.load(file)

        add = {"uuid": uuid,"name": name,"level": 4}
        file_data.append(add)
        with open(s + '/data/ops.json', 'w') as file:
            json.dump(file_data,file)
        subprocess.run(['chown','-R','opc:opc',s + '/data'])
        await message.channel.send("player added") 
    else:
        await message.channel.send("not allowed")


@client.command()
async def minecraft_withlist(message,uuid:str,*,name:str): 
    if ((message.author.mention == discord.Permissions.administrator)
         or message.author.id):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        #print(s + '/data/ops.json')
        with open(s + '/data/whitelist.json.json','r') as file:
          # First we load existing data into a dict.
            #print(file)
            file_data = json.load(file)

        add = {"uuid": uuid,"name": name}
        file_data.append(add)
        with open(s + '/data/whitelist.json', 'w') as file:
            json.dump(file_data,file)
        subprocess.run(['chown','-R','opc:opc',s + '/data']) 
        await message.channel.send("player added") 
    else:
        await message.channel.send("not allowed")

@client.command()
async def minecraft_list(message,name:str): 
    if ((message.author.mention == discord.Permissions.administrator)
         or message.author.id):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        #print(s + '/data/ops.json')
        if name == 'op':
            v = 'ops.json'
            await message.channel.send('op:')
        else:
            v = 'whitelist.json'
            await message.channel.send('whitelist:')
        with open(s + '/data/' + v,'r') as file:
          # First we load existing data into a dict.
            #print(file)
            file_data = json.load(file)
        for e in file_data:
            await message.channel.send("uuid: "+ e["uuid"] + " name"+ e["name"])
    else:
         await message.channel.send("not allowed")


@client.command()
async def minecraft_exec(message,*,command:str):
    if ((message.author.mention == discord.Permissions.administrator)
         or message.author.id):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(['docker-compose','exec'
                        ,command]);
        await message.channel.send("command executed")
    else:
        await message.channel.send("not allowed")

@client.command()
async def minecraft_update(message): 
    if ((message.author.mention == discord.Permissions.administrator)
         or message.author.id):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(['docker-compose','pull'
                        ,command]);
        await message.channel.send("updated")
    else:
        await message.channel.send("not allowed")


@client.command()
async def minecraft_status(message): #write word on image
    s =  private_key.path + "mincraft-" + str(message.guild.id)
    res = subprocess.run(['docker-compose',
                          '--project-directory',s,'logs'],
                         capture_output=True, text=True)
    output = str(res.stdout).splitlines()
    n = len (output)
    if n < 5:
        s =0
    else:
        s= n - 5
    
    for e in range(s,n): 
        await message.channel.send('```' + output[e] + '```' )

def move_files(source_dir, destination_dir):
    # Iterate over files in the source directory
    for filename in os.listdir(source_dir):
        pa = os.path.join(source_dir,filename)
        # Construct full paths for the source and destination files
        if os.path.isdir(pa):
            for fi in  os.listdir(pa):
                source_file = os.path.join(pa,fi)
                destination_file = os.path.join(destination_dir, fi)
                shutil.move(source_file, destination_file)


def is_zip_file(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
           return True
    except zipfile.BadZipFile:
       return False

@client.command()
async def minecraft_map(message,version:str,website:str,end:str): #write word on image
    if (((message.author.mention == discord.Permissions.administrator)
         or message.author.id in private_key.admin)  
        and website in private_key.allow_website):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(["docker-compose","-f",
                    s + '/docker-compose.yaml',
                    "down"])
        subprocess.run(["rm","-rf", s + '/data/world' ])
        await message.channel.send("server stop")
        with open(s +"/docker-compose.yaml", 'r') as file:
            prime_service = yaml.safe_load(file)
        if prime_service == None:
            dockerconfig(s,version)
        else:
            prime_service['services']['minecraft-server']['environment']['VERSION'] = version
            with open(s + '/docker-compose.yaml', 'w') as file:
                yaml.dump(prime_service, file) 

        subprocess.run(['wget','-t','20','https://www.' + website +"/"+ end
                       ,'-O',s + '/file.zip'])
        if is_zip_file(s + '/file.zip'):
            await message.channel.send("download succes")
            subprocess.run(["mkdir", s + '/data/world'])
            subprocess.run(['mv',s + '/data/ops.json',s + "/"])
            subprocess.run(["mkdir", s + '/temp' ])  
            subprocess.run(['unzip','-o',
                    s + '/file.zip','-d',s + '/temp'])
            subprocess.run(["chmod","-R","777",s + '/data'])
            move_files(s + '/temp', s + '/data/world')
            subprocess.run(['mv',s + '/ops.json',s + '/data/ops.json']) 
            await message.channel.send("extrated and move world")
            subprocess.run(['chown','-R','opc:opc',s + '/data'])
            subprocess.run(["rm","-rf", s + '/file.zip' ])
            subprocess.run(["rm","-rf", s + '/temp' ])
            await message.channel.send("data for server setup")
        else:
            await message.channel.send("error download")
            await message.channel.send("download the file on your pc before retry command")

    else:
        await message.channel.send("not allowed or bad website")


client.run(private_key.discord_key)  # discord api key
