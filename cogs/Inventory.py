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

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(description="Shows your inventory", brief = "Shows your inventory")
    @commands.Cog.listener()
    async def inv(self, ctx):
        await ctx.send("Your Inventory:")
        try:
            message = userdata.getInv(ctx.author.id) if userdata.getInv(ctx.author.id) != [] else "Empty"
            await ctx.send(message)

        except:
            await ctx.send("Empty")

    @commands.command(description="Use an inventory item\nmessage to someone: <user mention> <message>", brief = "Only message to someone works")
    async def use(self, ctx, item):
        args = ctx.message.content.split()

        try:
            newInv = userdata.getInv(ctx.author.id)
            newInv.remove(item.lower())
        except:
            pass

        if(newInv == userdata.getInv(ctx.author.id)):
            await ctx.send("You dont have that in your inventory")
        else:
            if(item.lower() == "messagetosomeone"):
                userID = ctx.message.mentions[0]
                finalMessage = " ".join(args[3:])
                await userID.send(finalMessage)
                await ctx.send(f"Sent {finalMessage} to <@!{userID}>")

            userdata.setInv(newInv, ctx.author.id)