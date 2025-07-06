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
import glob

path =  private_key.path
config = configparser.ConfigParser()
config.read( private_key.path + '/.editorconfig') #ouverture ficher config
config.sections()
# Make the request
url = 'https://api.github.com/repos/olivier-be/bot_discord/tags'
response = requests.get(url)
tag = response.json()

print(config)
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
async def version(ctx):
    await ctx.channel.send("https://github.com/olivier-be/bot_discord/")
    await ctx.channel.send("{} fair bot".format(config["version"]["version"]))


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
    #font1 = ImageFont.load_default()
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




def dockerconfig(s ,version,is_whitelist,is_crack):
    data = {};
    with open(path + "/default-mincraft.yml") as stream:
        data = yaml.safe_load(stream)
    if is_whitelist == "true":
        data['services']['minecraft-server']['environment']['WHITELIST'] = "TRUE"
    if is_crack == "true":
        data['services']['minecraft-server']['environment']['ONLINE_MODE'] = "FALSE"
    with open(s + '/docker-compose.yaml', 'w') as file:
         yaml.dump(data, file)


#ex !minecraft_setup false false 1.21.1
@client.command()
async def minecraft_setup(message,is_whitelist,is_crack,*,version:str): 
    if message.author.id in private_key.admin or message.author.mention == discord.Permissions.administrator:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(["mkdir", s])
        dockerconfig(s,version,is_whitelist,is_crack)
        await message.channel.send("data for server setup")
    else:
        await message.channel.send("demand to bot admin for setup the server")

def dockerconfig_mod(s ,is_whitelist,is_crack,link):
    data = {};
    with open(path + "/mod-mincraft.yml") as stream:
        data = yaml.safe_load(stream)
    if is_whitelist == "true":
        data['services']['minecraft-server']['environment']['WHITELIST'] = "TRUE"
    if is_crack == "true":
        data['services']['minecraft-server']['environment']['ONLINE_MODE'] = "FALSE"
    data['services']['minecraft-server']['environment']['CF_API_KEY'] = private_key.curseforge_api_key.replace("$", "$$")
    data['services']['minecraft-server']['environment']['CF_PAGE_URL'] = link
    with open(s + '/docker-compose.yaml', 'w') as file:
         yaml.dump(data, file)





@client.command()
async def minecraft_setup_mod(message,is_whitelist,is_crack,*,link:str): 
    if message.author.id in private_key.admin or message.author.mention == discord.Permissions.administrator:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(["mkdir", s])
        subprocess.run(["mkdir", s + "/downloads"])
        dockerconfig_mod(s,is_whitelist,is_crack,link)
        await message.channel.send("data for server setup")
    else:
        await message.channel.send("demand to bot admin for setup the server")

def dl_mod(s,link:str):
    data = {};
    with open(s + "/docker-compose.yaml") as stream:
        data = yaml.safe_load(stream)
    data['services']['minecraft-server']['environment']["CF_DOWNLOADS_REPO"] = "/downloads"
    with open(s + '/docker-compose.yaml', 'w') as file:
         yaml.dump(data, file)
    subprocess.run(['wget','-t','20',link,'--directory-prefix='+s + "/downloads"])
    subprocess.run(['chmod','777','-R',s + "/downloads"]) 

@client.command()
async def minecraft_set_modpack_zip(message,*,link:str): 
    if message.author.id in private_key.admin or message.author.mention == discord.Permissions.administrator:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        dl_mod(s,link)
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
async def minecraft_add_missing_mod_zip(message,link): 
    if message.author.id in private_key.admin:
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        subprocess.run(['wget','-t','20',link,'-O',s + "/file.zip"])
        await zip_file(message,s ,s+"/data/mods/")
        subprocess.run(['chmod','777','-R',s + "/data/mods/"]) 
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


def remove_file_glob(file):
    pos = file
    patterns = ["iris-*.jar", "sodium-*.jar", "figura-*.jar"]
    files_to_delete = []

    for pattern in patterns:
        files_to_delete.extend(glob.glob(os.path.join(pos, pattern)))

    # Only delete if matching files exist
    if files_to_delete:
        subprocess.run(["rm"] + files_to_delete)
    else:
        print("No matching files found.") 

@client.command() 
async def minecraft(message,start:int): 
    #if ctx.author.username == "furious": 
    
    s =  private_key.path + "mincraft-" + str(message.guild.id)
    if start == 1 :
        remove_file_glob(s+ "/data/mods/")
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
    if (True or (message.author.mention == discord.Permissions.administrator)
         or message.author.id):
        s =  private_key.path + "mincraft-" + str(message.guild.id)
        #print(s + '/data/ops.json')
        with open(s + '/data/whitelist.json','r') as file:
          # First we load existing data into a dict.
            #print(file)
            file_data = json.load(file)

        add = {"uuid": uuid,"name": name}
        file_data.append(add)
        with open(s + '/data/whitelist.json', 'w') as file:
            json.dump(file_data,file)
        subprocess.run(['chown','-R','opc:opc',s + '/data'])
        s =  "mincraft-" + str(message.guild.id) +"_minecraft-server_1"
        res = "docker exec " + s + " /whitelist reload"
        os.system(res);
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
    if ( message.author.id):
        s =  "mincraft-" + str(message.guild.id) +"_minecraft-server_1"
        res = "docker exec " + s + " " + command
        #await message.channel.send(res)
        os.system(res);
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

async def zip_file(m,s,output):
    if is_zip_file(s + '/file.zip'):
        await m.channel.send("download succes")
        subprocess.run(["mkdir", s + '/data/world'])
        subprocess.run(['mv',s + '/data/ops.json',s + "/"])
        subprocess.run(["mkdir", s + '/temp' ])  
        subprocess.run(['unzip','-o',
                    s + '/file.zip','-d',s + '/temp'])
        subprocess.run(["chmod","-R","777",s + '/data'])
        move_files(s + '/temp', output)
        subprocess.run(['mv',s + '/ops.json',s + '/data/ops.json']) 
        await m.channel.send("extrated and move file")
        subprocess.run(['chown','-R','opc:opc',s + '/data'])
        subprocess.run(["rm","-rf", s + '/file.zip' ])
        subprocess.run(["rm","-rf", s + '/temp' ])
        await m.channel.send("data for server setup")
    else:
        await m.channel.send("error download")
        await m.channel.send("downloaded file is not a zip file for minecraft")


@client.command()
async def minecraft_map(message,version:str,website:str,end:str): #write word on image
    if (((message.author.mention == discord.Permissions.administrator)
         or message.author.id in private_key.admin)  
        or website in private_key.allow_website):
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
        await zip_file(message,s,s + '/data/world')
    else:
        await message.channel.send("not allowed or bad website")


client.run(private_key.discord_key)  # discord api key
