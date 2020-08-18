import discord
import asyncio
import pafy

from discord.ext import commands
import os
import colorama
import time

jsm = __import__("JsonManager")
pyc = __import__("pyconfig")
Banime = __import__("banime")
Items = __import__("Items")
Video = __import__("Video")


config = jsm.JsonManager(pyc.configPath)
userdata = jsm.UserData(pyc.userDataPath)


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief="pong")
    @commands.Cog.listener()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(brief="check the banned anime", description="Check the banned anime. This changes when the bot wakes up every morning sometime after 6:00")
    async def banime(self, ctx):
        await ctx.send(f"Todays banned anime is {banime.bannedanime.name}")

    @commands.command()
    async def debug(self, ctx):
        for i in allPlaylists.playlists:
            print(f"{i.guildID} ")
            for j in i.videos:
                print(f"{j.title}, {j.path}")

    @commands.command(brief = "Pay respects", description = "Pay respects to someone")
    async def f(self, ctx, receiver = ""):
        await ctx.send(f"{ctx.author.name} has paid their respects to {receiver}" if receiver != "" else f"{ctx.author.name} has paid their respects")