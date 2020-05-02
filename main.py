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

@bot.event
async def on_message(message):
    ud.usr = message.author.id
    if(message.author.id == bot.user.id):
        return

    item = ""

    args = message.content.split()
    print("Message:")
    print("  Author Name",message.author.name)
    print("    Author ID",message.author.id)
    print("         Args",args)

    if(("mr" in message.content.lower() or
        "ms" in message.content.lower() or
        "miss" in message.content.lower() or
        "mister" in message.content.lower() or
        "sr" in message.content.lower() or
        "senor" in message.content.lower()) and
        ("peter" in message.content.lower() and message.author.id != 275405015915429888)):

        await message.channel.send("Baby "+message.author.name)
    await bot.process_commands(message)

@bot.command(name = "ping", aliases = ["test"], 
             brief='Says pong', description='It says pong. What more are you looking for?')
async def _ping(ctx):
    await ctx.channel.send("pong")

#______________ECONOMY

@bot.command(name = economyPrefix+"bal", aliases = [], category="economy",
             brief='shows balance', description= config.load()["prefix"]+economyPrefix+'bal <user mention>')
async def _bal(ctx):
    if(len(ctx.message.mentions) == 0):
        try:
            await ctx.channel.send( "You have "+
                                        str(ud.getBal())+
                                        " dollar(s)")
        except:
            await ctx.channel.send("There was an error getting your balance. Try sending a message and then checking your balance.")
    else:
        ud.usr = str(ctx.message.mentions[0].id)
        await ctx.channel.send( ctx.message.mentions[0].name+
                                " has "+
                                str(ud.getBal())+
                                " dollar(s)")
        ud.usr = ctx.author.id

@bot.command(name = economyPrefix+"pct", aliases = [], 
             brief='shows money gain percentage', description= "Every time you send a message, you gain your percent in money, and lose 50%. Everyone else gains 50%. Percents cannot exceed 0 and 100")
async def _pct(ctx):
        try:
            await ctx.message.channel.send( "You have "+
                                        str(ud.getPct()*100)+
                                        "%")
        except:
            await ctx.message.channel.send("There was an error checking your percent")

@bot.command(name = economyPrefix+"pay", aliases = [], 
             brief='Pays someone', description= "Pays someone the specified amount")
async def _pay(ctx, mention, amount):
    try:
        if(ud.getBal() >= float(amount) and float(amount) >= 0):
            ud.usr = str(ctx.message.mentions[0].id)
            ud.setBal(ud.getBal() + float(amount))
            ud.usr = str(ctx.message.author.id)
            ud.setBal(ud.getBal() - float(amount))
            await ctx.message.channel.send("Payment sent")
        else:
            await ctx.message.channel.send("Payment not sent, youre broke")
    except:
        await ctx.message.channel.send("The syntax is incorrect")

@bot.command(name = economyPrefix+"shop", aliases = [economyPrefix+"buy"], 
             brief='Buy an item', description= "type list for a list of items, or type an item name to buy it")
async def _buy(ctx, item):
    if(item == "list"):
        for i in itemspy.itemsClass.allItems:
            await ctx.message.channel.send(i.name+", $"+str(i.cost))
    else:
        worked, newBal = itemspy.itemsClass.buyItem(item, ud.getBal())
        if(worked):
            ud.setBal(newBal)
            inv = ud.getInv()
            inv.append(item.lower())
            ud.setInv(inv)
            await ctx.message.channel.send("Successfully bought 1x "+item)
        else:
            await ctx.message.channel.send("That item doesnt exist.")

#__________________________INVENTORY


@bot.command(name = "inv", aliases = [], 
             brief='Checks your inventory', description= "Checks your inventory")
async def _inv(ctx):
    inv = ud.getInv()
    for i in inv:
        await ctx.message.channel.send(i)

@bot.command(name = inventoryPrefix+"use", aliases = [], 
             brief='Uses an item', description= "Uses an item")
async def _use(ctx, item):
    try:
        inv = ud.getInv()
        inv.remove(item.lower())
        ud.setInv(inv)
        item = item.lower()
        await ctx.message.channel.send("using "+item)

        if(item == "apple"):
            await ctx.message.channel.send("It was tasty.")
        elif(item == "banana"):
            await ctx.message.channel.send("It was tasty")
        elif(item == "fakegamecode"):
            await ctx.message.channel.send("QMB4N-FZ7HT-WMFKR")


    except:
        await ctx.message.channel.send("could not use "+item)



bot.run(config.load()["token"])

