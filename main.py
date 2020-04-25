import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")
pyc = __import__("pyconfig")


economyprefix = "eco."
inventoryprefix = "inv."

cmds = Comm.Commands()
cmds.commands = [   Comm.Command(["help", "h"], "help", "", "Sends a list of commands"),
                    Comm.Command(['ping', 'test'], "ping", "", "Ping Encursedbot to see if it is online"),

                    Comm.Command([economyprefix+'bal'], economyprefix+"bal", "", "Check your balance"),
                    Comm.Command([economyprefix+'pay'], economyprefix+"pay", "<User mention> <Amount>", "Pay someone a specified amount"),
                    Comm.Command([economyprefix+'buy'], economyprefix+"buy", "<Item>", "Buy an item for the specified amount"),
                    Comm.Command([economyprefix+'shop', economyprefix+'buy'], economyprefix+"shop", "<Item>", "Buy an item for the specified amount"),
                    Comm.Command([economyprefix+'pct'], economyprefix+"pct", "", "Check your money gain percentage"),

                    Comm.Command(['inv'], "inv", "", "Check your inventory items"),
                    Comm.Command([inventoryprefix+'use'], inventoryprefix+"use", "", "use an item"),

                    Comm.Command(["challenge", "codechallenge"], "codechallenge", "", "Links to a coding challenge.")
]

items = Comm.Items()

items.items = [
    Comm.Item("Apple", 10),
    Comm.Item("Banana", 11),
    Comm.Item("FakeGameCode", 100),
    Comm.Item("MessageToSomeone", 20)
]

extraPath = pyc.extraPath

bot = commands.Bot(command_prefix= "enc.")

config = json.JsonManager(os.path.join(os.getcwd(), extraPath+"config.json"))
ud = json.UserData(os.path.join(os.getcwd(), extraPath+"userData.json"))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

@bot.event
async def on_message(message):

    cfg = config.load()
    ud.usr = message.author.id

    if(message.author.id == bot.user.id):
        return

    command = cmds.checkAllCommands(message, cfg["prefix"])
    item = ""

    args = message.content.split()
    print("Message:")
    print("  Author Name",message.author.name)
    print("    Author ID",message.author.id)
    print("         Args",args)
    print("      Command",command)

    if(("mr" in message.content.lower() or
        "ms" in message.content.lower() or
        "miss" in message.content.lower() or
        "mister" in message.content.lower() or
        "sr" in message.content.lower() or
        "senor" in message.content.lower()) and
        "peter" in message.content.lower()):

        await message.channel.send("Baby "+message.author.name)

    if(command == None):
        json.updateMoney(message.author.id, ud)

    elif(command == "ping"):
        await message.channel.send("Pong")
    
    elif(command == "help"):
        for i in cmds.commands:
            string = cfg["prefix"]+i.commands[0]+" ("
            for j in range(len(i.commands)-1):
                string += i.commands[j+1]+", "
            string += ")"
            await message.author.send(string+" | "+cfg["prefix"]+i.commands[0]+" "+i.syntax+" | "+i.description)

    elif(command.startswith(economyprefix)):
        if(command.startswith(economyprefix+"bal")):
            if(len(message.mentions) == 0):
                try:
                    await message.channel.send( "You have "+
                                                str(ud.getBal())+
                                                " dollar(s)")
                except:
                    await message.channel.send("There was an error getting your balance. Try sending a message and then checking your balance.")
            else:
                ud.usr = str(message.mentions[0].id)
                await message.channel.send( message.mentions[0].name+
                                            " has "+
                                            str(ud.getBal())+
                                            " dollar(s)")
                ud.usr = message.author.id

        elif(command.startswith(economyprefix+"pct")):
            try:
                await message.channel.send( "You have "+
                                            str(ud.getPct()*100)+
                                            "%")
            except:
                await message.channel.send("There was an error checking your percent")

        elif(command.startswith(economyprefix+"shop")):
            if(len(args) == 1):
                await message.channel.send("You need to put an item use "+cfg["prefix"]+economyprefix+"shop list to see whats for sale")
            elif(args[1] == "list"):
                for i in items.items:
                    await message.channel.send(i.name+", $"+str(i.cost))
            else:
                worked, newBal = items.buyItem(args[1], ud.getBal())
                if(worked):
                    ud.setBal(newBal)
                    inv = ud.getInv()
                    inv.append(args[1].lower())
                    ud.setInv(inv)
                    await message.channel.send("Successfully bought 1x "+args[1])
                else:
                    await message.channel.send("That item doesnt exist.")

        elif(command.startswith(economyprefix+"pay")):
            try:
                if(ud.getBal() >= float(args[2]) and float(args[2]) >= 0):
                    ud.usr = str(message.mentions[0].id)
                    ud.setBal(ud.getBal() + float(args[2]))
                    ud.usr = str(message.author.id)
                    ud.setBal(ud.getBal() - float(args[2]))
                    await message.channel.send("Payment sent")
                else:
                    await message.channel.send("Payment not sent, youre broke")
            except:
                await message.channel.send("The syntax is incorrect")
    
    elif(command.startswith(inventoryprefix)):
        if(command.startswith(inventoryprefix+"use")):
            try:
                inv = ud.getInv()
                inv.remove(args[1].lower())
                ud.setInv(inv)
                item = args[1].lower()
                await message.channel.send("using "+item)
            except:
                await message.channel.send("could not use "+args[1])
            

    elif(command.startswith("inv")):
        inv = ud.getInv()
        for i in inv:
            await message.channel.send(i)

    elif(command == "codechallenge"):
        await message.channel.send("Visit https://codingchallenge.prushton.repl.co/ for more info")
    

    if(item == "apple"):
        await message.channel.send("It was tasty.")
    elif(item == "banana"):
        await message.channel.send("It was tasty")
    elif(item == "fakegamecode"):
        await message.channel.send("QMB4N-FZ7HT-WMFKR")
    else:
        pass#await message.channel.send("Item invalid")




bot.run(config.load()["token"])

