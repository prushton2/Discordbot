import discord
from discord.ext import commands
import os

jsm = __import__("JsonManager")
pyc = __import__("pyconfig")
itemspy = __import__("Items")

economyPrefix = "eco."
inventoryPrefix = "inv."

config = jsm.JsonManager(pyc.configPath)
userdata = jsm.UserData(pyc.userDataPath)

bot = commands.Bot(command_prefix= config.load()["prefix"])

@bot.event
async def on_ready(): #
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @bot.event
    @commands.Cog.listener() #run on every message to update their money
    async def on_message(self, ctx):
        print("   Author:",ctx.author.name)
        print("  Content:",ctx.content)
        print("       ID:",ctx.author.id)

        jsm.updateMoney(ctx.author.id, userdata)

        await bot.process_commands(ctx)

    @commands.command()
    async def ping(self, ctx, *, member: discord.Member = None, breif="pong"):
        await ctx.send("pong")


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.Cog.listener()
    async def pay(self, ctx, user, amount, *, member: discord.Member = None, description="Pay someone money"):
        if(userdata.getBal(ctx.author.id) < float(amount)): #check if user has enough money
            await ctx.send("The sender doesnt have enough money")
            return
        user = user[3:-1] #turn a mention into a user id
        userdata.setBal(userdata.getBal(ctx.author.id) - float(amount), ctx.author.id)
        userdata.setBal(userdata.getBal(user) + float(amount), user)

    @commands.command()
    async def bal(self, ctx, user=None, *, member: discord.Member = None, description="Check a balance"):
        try:
            targetUser = ctx.author.id if user == None else user[3:-1] #If the author adds a mention, the mention will replace the null in the user parameter. The ternary operator changes null to the authors id if they leave it blank, showing the authors balance
            await ctx.send(f"${userdata.getBal(targetUser)}")
        except:
            await ctx.send("$0") #If there is an error, then the user likely doesnt have an account in userData.json. In this case, their balance is $0

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command()
    @commands.Cog.listener()
    async def inv(self, ctx, description="Shows your inventory"):
        await ctx.send("Your Inventory:")
        try:
            message = userdata.getInv(ctx.author.id) if userdata.getInv(ctx.author.id) != [] else "Empty"
            await ctx.send(message)

        except:
            await ctx.send("Empty")




bot.add_cog(Default(bot))
bot.add_cog(Economy(bot))
bot.add_cog(Inventory(bot))

bot.run(config.load()["token"])

"""
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))"""