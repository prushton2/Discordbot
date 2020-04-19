import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")
pyc = __import__("pyconfig")

economyprefix = "eco."

cmds = Comm.Commands()
cmds.commands = [   Comm.Command(["help", "h"], "help", "Sends a list of commands"),
                    Comm.Command(['ping', 'test'], "ping", "Ping Encursedbot to see if it is online"),
                    Comm.Command([economyprefix+'bal'], economyprefix+"bal", "Check your balance")]

extraPath = pyc.extraPath

bot = commands.Bot(command_prefix= "enc.")

config = json.JsonManager(os.path.join(os.getcwd(), extraPath+"config.json"))
currency = json.JsonManager(os.path.join(os.getcwd(), extraPath+"Currency.json"))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

@bot.event
async def on_message(message):

    
    if(message.author.id == bot.user.id):
        return

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

    
    elif(command == "ping"):
        await message.channel.send("Pong")
    
    elif(command == "help"):
        for i in cmds.commands:
            string = config.load()["prefix"]+i.commands[0]+" ("
            for j in range(len(i.commands)-1):
                string += i.commands[j+1]+", "
            string += ")"
            await message.author.send(string+" | "+i.description)

    elif(command.startswith(economyprefix)):
        if(command.startswith(economyprefix+"bal")):
            await message.channel.send( "You have "+
                                        str(currency.load()["bal"][str(message.author.id)])+
                                        " dollar(s)")
        



bot.run(config.load()["token"])

