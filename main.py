import discord
import asyncio
import pafy

from cogs import onMessage, Default, Economy, Inventory, Voice
from discord.ext import commands
import os
import colorama
import time

jsm = __import__("JsonManager")
pyc = __import__("pyconfig")
Items = __import__("Items")
Video = __import__("Video")

config = jsm.JsonManager(pyc.configPath)
userdata = jsm.UserData(pyc.userDataPath)

bot = commands.Bot(command_prefix= config.load()["prefix"])

cogs = [Default.Default, Economy.Economy, Inventory.Inventory, Voice.Voice, onMessage.onMessage]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")


for i in cogs:
    bot.add_cog(i(bot))

bot.run(config.load()["token"])