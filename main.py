import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")

cmds = Comm.Commands()
cmds.commands = [Comm.Command(['ping', 'test'], "ping")]

extraPath = "Discordbot/"

bot = commands.Bot(command_prefix= "enc.")

config = json.JsonManager(os.path.join(os.getcwd(), extraPath+"config.json"))
currency = json.JsonManager(os.path.join(os.getcwd(), extraPath+"Currency.json"))

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_message(message):

    
    if(message.author.id == bot.user.id):
        return

    # if(message.content.startswith(config.load()["prefix"])):
    command = cmds.checkAllCommands(message, config.load()["prefix"])

    if(command == None):
        bal = currency.load()
        try:
            bal["bal"][str(message.author.id)] += 1
        except:
            bal["bal"][str(message.author.id)] = 1
        currency.save(bal)


        if( "mr peter" in message.content.lower() or
            "mr. peter" in message.content.lower() or
            "mrpeter" in message.content.lower()):
            string = "Baby "+message.author.name
            await message.channel.send(string)

    
    if(command == "ping"):
        await message.channel.send("Pong")



bot.run(config.load()["token"])

