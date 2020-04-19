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


        if(("mr" in message.content or
            "mister" in message.content or
            "sr" in message.content or
            "senor" in message.content ) and
            "peter" in message.content):
            
            string = "Baby "+message.author.name
            await message.channel.send(string)

    
    if(command == "ping"):
        await message.channel.send("Pong")



bot.run(config.load()["token"])

