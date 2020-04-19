import discord
from discord.ext import commands
import os
json = __import__("JsonManager")

client = commands.Bot(command_prefix= "enc.")
config = json.JsonManager(os.path.join(os.getcwd(),"Discordbot\config.json"))


@client.event
async def on_ready():
    print("Bot is ready")

client.run(config.load()["token"])