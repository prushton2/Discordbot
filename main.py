import discord
from discord.ext import commands
import os

json = __import__("JsonManager")
Comm = __import__("Command")
pyc = __import__("pyconfig")

economyprefix = "eco."

cmds = Comm.Commands()
cmds.commands = [   Comm.Command(["help", "h"], "help", "", "Sends a list of commands"),
                    Comm.Command(['ping', 'test'], "ping", "", "Ping Encursedbot to see if it is online"),
                    Comm.Command([economyprefix+'bal'], economyprefix+"bal", "", "Check your balance"),
                    Comm.Command([economyprefix+'pay'], economyprefix+"pay", "<User mention> <Amount>", "Pay someone a specified amount"),
                    Comm.Command(["challenge", "codechallenge"], "codechallenge", "", "Links to a coding challenge.")
]

extraPath = pyc.extraPath

bot = commands.Bot(command_prefix= "enc.")

config = json.JsonManager(os.path.join(os.getcwd(), extraPath+"config.json"))
currency = json.JsonManager(os.path.join(os.getcwd(), extraPath+"userData.json"))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

@bot.event
async def on_message(message):

    ud = currency.load()
    cfg = config.load()

    if(message.author.id == bot.user.id):
        return

    command = cmds.checkAllCommands(message, cfg["prefix"])

    args = message.content.split()
    print(args)


    if(command == None):
        try:
            ud["bal"][str(message.author.id)] += 1
        except:
            ud["bal"][str(message.author.id)] = 1
        currency.save(ud)


        if(("mr" in message.content.lower() or
            "ms" in message.content.lower() or
            "miss" in message.content.lower() or
            "mister" in message.content.lower() or
            "sr" in message.content.lower() or
            "senor" in message.content.lower() ) and
            "peter" in message.content.lower()):

            string = "Baby "+message.author.name
            await message.channel.send(string)

    
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
            await message.channel.send( "You have "+
                                        str(ud["bal"][str(message.author.id)])+
                                        " dollar(s)")
        
        elif(command.startswith(economyprefix+"pay")):
            try:
                if(ud["bal"][str(message.author.id)] >= int(args[2])):
                    ud["bal"][str(message.author.id)] -= int(args[2])
                    ud["bal"][str(message.mentions[0].id)] += int(args[2])
                    await message.channel.send("Payment sent")

                else:
                    await message.channel.send("Payment not sent, youre broke")
            except:
                await message.channel.send("The syntax is incorrect")


    elif(command == "codechallenge"):
        await message.channel.send("Visit https://codingchallenge.prushton.repl.co/ for more info")
        



bot.run(config.load()["token"])

