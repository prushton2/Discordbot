import discord
import asyncio
import pafy

from cogs import Default, Economy, Inventory, Voice
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
banime = Banime.Banime(Banime.bannedAnime)


bot = commands.Bot(command_prefix= config.load()["prefix"])


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

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

        if(ctx.author == bot.user):
            authorColor = colorama.Fore.MAGENTA 
            messageColor = colorama.Fore.MAGENTA
            idColor = colorama.Fore.MAGENTA

        print("==========================================================")
        print(authorColor+ "   Author:",ctx.author.name)
        print(messageColor+"  Content:",ctx.content)
        print(idColor+     "  User ID:",ctx.author.id)
        print(serverColor+ "Server ID:",ctx.guild.id, colorama.Style.RESET_ALL)


        if(not ctx.content.startswith(".") and not ctx.author == bot.user):
            jsm.updateMoney(ctx.author.id, userdata)
        
        if(ctx.author != bot.user):
            warning, relatedAnime = banime.check(ctx.content)
            if(warning != ""):
                await ctx.channel.send(f"Warning: You saying {warning} is related to the banned anime {relatedAnime}. You have received a warning.")
        # await bot.process_commands(ctx)





    



bot.add_cog(onMessage(bot))
bot.add_cog(Default(bot))
bot.add_cog(Economy(bot))
bot.add_cog(Inventory(bot))
bot.add_cog(Voice(bot))

bot.run(config.load()["token"])

"""
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))"""