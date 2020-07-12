import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
pyc = __import__("pyconfig")
itemspy = __import__("Items")

economyPrefix = "eco."
inventoryPrefix = "inv."

config = json.JsonManager(pyc.configPath)
ud = json.UserData(pyc.userDataPath)

bot = commands.Bot(command_prefix= config.load()["prefix"])

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @bot.event
    @commands.Cog.listener()
    async def on_message(self, ctx):
        print("Author:   ",ctx.author.name)
        print("Content:  ",ctx.content)
        print("ID:       ",ctx.author.id)
        await bot.process_commands(ctx)

    @commands.command()
    async def ping(self, ctx, *, member: discord.Member = None, brief="pong"):
        await ctx.send("pong")


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.Cog.listener()
    async def pay(self, ctx, *, member: discord.Member = None, brief="pay someone"):
        await ctx.send("no")

bot.add_cog(Default(bot))
bot.add_cog(Economy(bot))

bot.run(config.load()["token"])

"""
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))"""