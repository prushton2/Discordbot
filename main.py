import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")

cmds = Comm.Commands()
cmds.commands = [Comm.Command(['ping', 'test'], "ping")]


bot = commands.Bot(command_prefix= "enc.")

config = json.JsonManager(os.path.join(os.getcwd(),"Discordbot/config.json"))


@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_message(message):

    
    if(message.author.id == bot.user.id):
        return

    if(message.content.startswith(config.load()["prefix"])):
        command = cmds.checkAllCommands(message, config.load()["prefix"])

    
    if(command == "ping"):
        await message.channel.send("Pong")



bot.run(config.load()["token"])

