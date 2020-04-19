import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")
pyc = __import__("pyconfig")

cmds = Comm.Commands()
cmds.commands = [   Comm.Command(['ping', 'test'], "ping"),
                    Comm.Command(['eco.bal'], "eco.bal")]

extraPath = pyc.extraPath

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


        if(("mr" in message.content.lower() or
            "ms" in message.content.lower() or
            "miss" in message.content.lower() or
            "mister" in message.content.lower() or
            "sr" in message.content.lower() or
            "senor" in message.content.lower() ) and
            "peter" in message.content.lower()):

            string = "Baby "+message.author.name
            await message.channel.send(string)

    
    if(command == "ping"):
        await message.channel.send("Pong")

    if(command.startswith("eco.")):
        if(".bal" in command):
            await message.channel.send( "You have "+
                                        str(currency.load()["bal"][str(message.author.id)])+
                                        " dollar(s)")



bot.run(config.load()["token"])

