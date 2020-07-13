import discord
from discord.ext import commands
import os

jsm = __import__("JsonManager")
pyc = __import__("pyconfig")
Items = __import__("Items")

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

    @commands.command(brief="pong")
    async def ping(self, ctx):
        await ctx.send("pong")


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(description = "Pay someone else a specified amount of money", brief="Pay someone")
    @commands.Cog.listener()
    async def pay(self, ctx, user, amount):
        if(userdata.getBal(ctx.author.id) < float(amount)): #check if user has enough money
            await ctx.send("The sender doesnt have enough money")
            return
        user = user[3:-1] #turn a mention into a user id
        userdata.setBal(userdata.getBal(ctx.author.id) - float(amount), ctx.author.id)
        userdata.setBal(userdata.getBal(user) + float(amount), user)

    @commands.command(description="Check a balance of you or someone else", brief="Check your balance")
    async def bal(self, ctx, user="You"):
        try:
            targetUser = ctx.author.id if user == "You" else user[3:-1] #If the author adds a mention, the mention will replace the null in the user parameter. The ternary operator changes null to the authors id if they leave it blank, showing the authors balance
            await ctx.send(f"${userdata.getBal(targetUser)}")
        except:
            await ctx.send("$0") #If there is an error, then the user likely doesnt have an account in userData.json. In this case, their balance is $0

    @commands.command(description="Check a users money gain percent", brief="Check a users money gain percent")
    async def pct(self, ctx, user=None):
        try:
            targetUser = ctx.author.id if user == None else user[3:-1] #If the author adds a mention, the mention will replace the null in the user parameter. The ternary operator changes null to the authors id if they leave it blank, showing the authors balance
            await ctx.send(f"{userdata.getPct(targetUser)}%")
        except:
            await ctx.send("0%") #If there is an error, then the user likely doesnt have an account in userData.json. In this case, their balance is $0

    @commands.command(description="Shows all items in the shop", brief="Shows all items in the shop")
    async def shop(self, ctx):
        message = f"Items listed on the shop:\n"
        for i in Items.items.allItems:
            message += f"{i.name} for ${i.cost}\n"
        await ctx.send(message)
        


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


'''
commands to add:

eco shop
inv use

'''
bot.add_cog(Default(bot))
bot.add_cog(Economy(bot))
bot.add_cog(Inventory(bot))

bot.run(config.load()["token"])

"""
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))"""