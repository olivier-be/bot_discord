
import discord
import random
import game
from discord.ext import commands
import os
import openai

openai.organization = "org- openai org"
openai.api_key = "api_key"


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
objects = ["Mur", "Table", "Chaise", "Lampe", "Oreiller", "Canapé", "Plante", "Livre", "Radiateur", "Lit", "Lampe de chevet", "Tapis", "Papier peint", "Ventilateur", "Bureau", "Chaise de bureau", "Étagère", "Coussin", "Miroir", "Lampe de table", "Matelas", "Télévision", "Ordinateur", "Four", "Réfrigérateur", "Tableau", "Lave-linge", "Rideau", "Table basse", "Chaise longue", "Armoire", "Télécommande", "Placard", "Cheminée", "Lampe de sol", "Vase", "Lampe de bureau", "Cadre", "Radiocassette", "Four à micro-ondes", "Chaise de jardin", "Table de jardin", "Ascenseur", "Ascenseur", "Balançoire", "Chariot", "Tondeuse", "Bouilloire", "Robot ménager", "Machine à laver", "Stéréo", "Cassette vidéo", "Lecteur DVD", "Caméra", "Téléphone", "Télécopieur", "Ampoule", "Tondeuse à gazon", "Cuisine", "Climatiseur", "Réveil", "Verrou", "Horloge", "Porte", "Meuble", "Chaise haute", "Canapé-lit", "Lit bébé", "Scie", "Marteau", "Tournevis", "Clé", "Ciseaux", "Perceuse", "Cordon électrique", "Rouleau", "Clou", "Outils", "Brosse", "Aspirateur", "Ventilateur de plafond", "Platforme", "Planche à repasser", "Échelle", "Chaussures", "Vêtements", "Sac à dos", "Valise", "Boîte", "Sac", "Livres", "Jouets", "Jeux vidéo", "Batterie", "Souris", "Clavier", "Câble", "Tuyau", "Papier", "Stylo", "Craie", "Encrier", "Crayon", "Règle", "Gomme", "Cahier", "Sac à main", "Coffre-fort", "Ordinateur portable", "Imprimante", "Lampe de poche", "Bougeoir", "Couverture", "Bouquin", "Jouet en peluche"]

@client.event
async def on_ready():
    print('Ready!')

    await client.change_presence(activity=discord.Game("I will spread toxicity throughout this server!"))

games=False
usergame=""
find=""
@client.event

async def on_message(message):
    global objects,usergame,find,games
    username=str(message.author).split('#')[0]
    message_content=str (message.content)
    channel=str(message.channel.name)
    print(f'{username}: {message_content} {channel}')
    if message.author == client.user:
        return
        await message.channel.send(response)
    elif ("feur") in message_content and not(find):
        await message.channel.send("me ta gueule")
    elif ( "bot") in message.content or  ( "Tg") in message.content :
        e = discord.Embed()
        e.set_thumbnail(url="https://media.tenor.com/8XNZFtwJxscAAAAC/reverse-card-uno.gif")
        await message.channel.send(embed=e)
    elif ("!openai") in message_content:
        str1=message_content[7 : len(message_content)]
        messager= openai.Completion.create(model="text-davinci-003", prompt=str1, temperature=0, max_tokens=500)
        print (messager['choices'][0]['text'])
        await message.channel.send(str(messager['choices'][0]['text']))
    elif ("toxic") in message_content:
        await message.channel.send("I am here")
    elif ("!version") in message_content:
        e = discord.Embed()
        e.set_image(url="")
        await message.channel.send()
    elif ("windows") in message_content:
        await message.channel.send("linux > ")
    elif ("!game") in message_content:
        if games:
            if usergame==username:
                await message.channel.send("you need to close your old game")
            else:
                await message.channel.send("Une partie est deja en cour")
        else:
            games=True
            usergame=username
            find=objects[int(random.uniform(0,115))]
            print(find)
            await message.channel.send("Je pense à quoi ?")
    elif  games and usergame==username:
        if message_content=="end":
            games=False
            await message.channel.send("you can make better next time ")
        else :
            if message_content== find:

                games = False
                await message.channel.send("gg")
            else:
                messager = openai.Completion.create(model="text-davinci-003",
                                                    prompt="donne un indice sans la réponse qui permet de retrouver = "+find+ " avec comme dernière valeur donée"+message_content+" de plus informe le joueur si il est pret de trouver la réponse",
                                                    temperature=0, max_tokens=50)
                await message.channel.send(messager['choices'][0]['text'])
    elif ("!stopgame") in message_content:
        games=False




@client.command()
async def toxic(ctx):
    await ctx.send('I will spread toxicity throughout this server!')

client.run('bot key')
