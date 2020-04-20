import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")
pyc = __import__("pyconfig")

# 
# 
# 
# 
# 
# 
# 

economyprefix = "eco."

cmds = Comm.Commands()
cmds.commands = [   Comm.Command(["help", "h"], "help", "", "Sends a list of commands"),
                    Comm.Command(['ping', 'test'], "ping", "", "Ping Encursedbot to see if it is online"),
                    Comm.Command([economyprefix+'bal'], economyprefix+"bal", "", "Check your balance"),
                    Comm.Command([economyprefix+'pay'], economyprefix+"pay", "<User mention> <Amount>", "Pay someone a specified amount"),
                    Comm.Command([economyprefix+'pct'], economyprefix+"pct", "", "Check your money gain percentage"),
                    Comm.Command(["challenge", "codechallenge"], "codechallenge", "", "Links to a coding challenge.")
]

extraPath = pyc.extraPath

bot = commands.Bot(command_prefix= "enc.")

config = json.JsonManager(os.path.join(os.getcwd(), extraPath+"config.json"))
userData = json.JsonManager(os.path.join(os.getcwd(), extraPath+"userData.json"))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

@bot.event
async def on_message(message):

    ud = userData.load()
    cfg = config.load()

    if(message.author.id == bot.user.id):
        return

    command = cmds.checkAllCommands(message, cfg["prefix"])

    args = message.content.split()
    print("Message:")
    print("     ",message.author.name)
    print("     ",message.author.id)
    print("     ",args)


    if(("mr" in message.content.lower() or
        "ms" in message.content.lower() or
        "miss" in message.content.lower() or
        "mister" in message.content.lower() or
        "sr" in message.content.lower() or
        "senor" in message.content.lower()) and
        "peter" in message.content.lower()):

        string = "Baby "+message.author.name
        await message.channel.send(string)

    if(command == None):
        
        try:
            ud["bal"][str(message.author.id)] += ud["percent"][str(message.author.id)]
        except:
            ud["bal"][str(message.author.id)] = 1

        try:
            if(ud["percent"][str(message.author.id)] > 0.0):
                ud["percent"][str(message.author.id)] -= 0.5 
        except:
            ud["percent"][str(message.author.id)] = 1.0

        for (key, value) in ud["percent"].items():
            if(int(key) != message.author.id and ud["percent"][key] < 1.0):
                ud["percent"][key] += 0.5

        if(message.author.id == 275413547658379264):
            ud["bal"]["275413547658379264"] = 9999999999999


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
                await message.channel.send( "You have "+
                                            str(ud["bal"][str(message.author.id)])+
                                            " dollar(s)")
            else:
                await message.channel.send( message.mentions[0].name+
                                            " has "+
                                            str(ud["bal"][str(message.mentions[0].id)])+
                                            " dollar(s)")

        elif(command.startswith(economyprefix+"pct")):
            try:
                await message.channel.send( "You have "+
                                            str(ud["percent"][str(message.author.id)]*100)+
                                            "%")
            except:
                await message.channel.send("There was an error checking your percent")

        elif(command.startswith(economyprefix+"pay")):
            try:
                if(ud["bal"][str(message.author.id)] >= int(args[2]) and int(args[2]) >= 0):
                    ud["bal"][str(message.mentions[0].id)] += int(args[2])
                    ud["bal"][str(message.author.id)] -= int(args[2])
                    await message.channel.send("Payment sent")
                else:
                    await message.channel.send("Payment not sent, youre broke")
            except:
                await message.channel.send("The syntax is incorrect")


    elif(command == "codechallenge"):
        await message.channel.send("Visit https://codingchallenge.prushton.repl.co/ for more info")
    
    userData.save(ud)
    config.save(cfg)


bot.run(config.load()["token"])

