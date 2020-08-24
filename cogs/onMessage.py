import discord
import asyncio
import pafy

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

class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener() #run on every message to update money
    async def on_message(self, ctx):
        authorColor = colorama.Fore.CYAN
        messageColor = colorama.Fore.GREEN if (ctx.content.startswith(config.load()["prefix"])) else colorama.Fore.CYAN
        idColor = colorama.Fore.BLUE
        serverColor = colorama.Fore.RED

        if(ctx.author == self.bot.user):
            authorColor = colorama.Fore.MAGENTA 
            messageColor = colorama.Fore.MAGENTA
            idColor = colorama.Fore.MAGENTA

        print("==========================================================")
        print(authorColor+ "   Author:",ctx.author.name)
        print(messageColor+"  Content:",ctx.content)
        print(idColor+     "  User ID:",ctx.author.id)
        print(serverColor+ "Server ID:",ctx.guild.id, colorama.Style.RESET_ALL)


        if(not ctx.content.startswith(".") and not ctx.author == self.bot.user):
            jsm.updateMoney(ctx.author.id, userdata)