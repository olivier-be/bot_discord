# bot_discord 

This bot uses openai to reply,, <br />
This bot uses docker-compose to make a mincraft server,, <br />

I've made a small game use openai to benefit for this feature <br />

This bot makes automatic repose to feur bot <br />

# Why code this bot 

This bot was made for fun and discover discord bot, opeanai api, docker-compose. <br />

# how use it ?

install docker-compose <br />
install python (code with python 3.11) <br />

<br />

install with pip <br />

discord.py <br />

and openai <br />

and Pillow <br />

<br />

create your discord bot on<br />

https://discord.com/developers<br />

1 take api key from your openai account on <br />

https://beta.openai.com/overview<br />

click on account and choose api key <br />

create new one <br />
2 
self hosted ai with llama.cpp[https://github.com/ggerganov/llama.cpp]
change base_url of client_llama in main.py

<br />

put alls keys in the bot <br />

just run <br />
<br />
now it work<br />
<br />
for work he need openai key and discord bot key<br />
<br />
add your user id the admin list

# mincraft server 
  1 set up docker-compse<br />
  "!minecraft_setup" set up mincraft directory for the acteur discord server <br />
  2 start server <br />
  "!minecraft 1" start the server<br />
  3 install map (skip if you want VANILLA)<br />
  for https://www.minecraftmaps.com/game-maps/minigames-world<br />
  in private_key.py : allow_website = ['minecraftmaps.com']<br />
  use<br />
  "!minecraft_map "VERSION(ex :"1.20.2")" "allow_website(ex:"minecraftmaps.com") "END OF LINK(game-maps/minigames-  world/download-map")" <br />
  4 add admin to mincraft <br />
  "!minecraft_op uuid(ex:234;lkj4h2lkj3h) name(ex:name)" add op to ops.json
  5 restart server <br />
  "!minecraft 0" stop the server<br />
  "!minecraft 1" start the server<br />
  6 get status <br />
    "!minecraft_status" sent data logs <br />
  7 remove file for a server <br />
    "!minecraft_remove"
  

# functionality <br />
<br />
in discord type: <br />

<br />

commandes:<br />

-"!game" start game to find one word (one at time per bot and work on the initialised channel<br />

-"!end" stop on the game on the channel <br />

-"!stopgame" stop on the game (work for all servers connected)<br />

-"!gpt3" use text-davinci-003 to response <br />

-"!Dalle2" use dalle-3 to send image generate<br />

-"!clear_message" take nb and delete nb message in channel. He needs manage_messages permission to delete.<br />

-"!spam" take amount size message. He spam the channel with this setting<br />

-"!update" say if update are available<br />

-"!quote" edit image with text send <br />

-"!avatar" sent avatar <br />

-"!minecraft_setup" setup file for docker-compose and server id, need to have is user id in admin in private_key.py<br />

-"!minecraft" start or stop server with "!minecraft 1" or "!minecraft 0" linked to severid <br />

-"!minecraft_status " sent 5 last output of mincraft server if launch <br />

-"!help" show commands<br />

<br />

<br />

in one message: <br />

-"bot" just don't use it <br />

-"toxic" said "I am here"<br />

-"windows" why you use it <br />

-"feur" counter feur bot are better<br />

<br />

Thanks for reading<br />

Enjoy your bot ! <br />
