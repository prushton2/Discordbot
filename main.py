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
banime = Banime.Banime(Banime.bannedAnime)
playlists = {}


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
        print(playlists)

    @commands.command(brief = "Pay respects", description = "Pay respects to someone")
    async def f(self, ctx, receiver = ""):
        await ctx.send(f"{ctx.author.name} has paid their respects to {receiver}" if receiver != "" else f"{ctx.author.name} has paid their respects")
        


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
        senderBal = userdata.getBal(ctx.author.id)
        try:
            userdata.setBal(userdata.getBal(user) + float(amount), user)
            userdata.setBal(userdata.getBal(ctx.author.id) - float(amount), ctx.author.id)
            await ctx.send(f"Sent ${amount} to <@!{user}>")
        except:
            userdata.setBal(senderBal, ctx.author.id)
            await ctx.send(f"Error sending ${amount} to <@!{user}>, no transaction was made")

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
        
    @commands.command(description="Buy an item from the shop", brief="Buy an item")
    async def buy(self, ctx, item, amount=1):
        amountBought = 0 #used to count the number of items bought, which is read back to the user
        userid = ctx.author.id

        for i in range(amount):
            purchaseMade, newBal = Items.items.buyItem(item, userdata.getBal(userid))

            if(purchaseMade):
                userdata.setBal(newBal, userid)
                newInv = userdata.getInv(userid)
                newInv.append(item)
                userdata.setInv(newInv, userid)
                amountBought += 1
        
        await ctx.send(f"Bought {amountBought}x {item}")
        if(amountBought != amount):
            await ctx.send("Either you don't have enough money to buy the item(s) or the item doesnt exist")

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


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(description="Joins the VC you are in", brief = "Join a VC")
    @commands.Cog.listener()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except:
            await ctx.send("You arent in a voice channel")

    @commands.command(description="Leaves the VC it is in", brief = "Leave a VC", aliases = ["byebye"])
    async def leave(self, ctx):
        for i in bot.voice_clients:
            if(i.guild.id == ctx.guild.id):
                await i.disconnect()
        self._cleanup(ctx)

    def _cleanup(self, ctx):
        try:
            for i in playlists[ctx.guild.id]:
                os.remove(f"{pyc.songsPath}{pyc.seperator}{i[0]}")
            playlists[ctx.guild.id] = []
        except:
            pass

    def _removeSong(self, guildID, uuid):
        for i in range(len(playlists[guildID])):
            if(playlists[guildID][i][0] == f"{uuid}"):
                playlists[guildID].pop(i)
                os.remove(f"{pyc.songsPath}{pyc.seperator}{uuid}")
                print(f"removed {uuid}.mp3")
                return
            else:
                print(f"{uuid} doesnt match {playlists[guildID][i][0]}")

    


    @commands.command(description="Play a youtube video", brief = "play a song")
    async def play(self, ctx, url="null"):

        try:
            voiceClient = await ctx.author.voice.channel.connect()
            self._cleanup(ctx) # If the bot has to join a voice channel, wipe the playlist

        except discord.errors.ClientException:

            for i in bot.voice_clients:
                if(i.guild.id == ctx.guild.id):
                    voiceClient = i
        except:
            await ctx.send("You arent in a voice channel")
            return

        if(url != "null"):

            video = Video.Video(url, ctx.author)

            message = await ctx.send(embed=video.getEmbed("Now Loading"))
            video.download(ctx.guild.id)


            try:
                playlists[ctx.guild.id].append([f"{video.path}.mp3", url])
            except:
                playlists[ctx.guild.id] = [[f"{video.path}.mp3", url]]

            await message.edit(embed=video.getEmbed("Now Playing" if len(playlists[ctx.guild.id]) == 1 else "Added to queue"))

        if(not voiceClient.is_playing()):
            while(len(playlists[ctx.guild.id]) != 0):

                firstSong = playlists[ctx.guild.id][0][0]
                playingVideo = Video.Video(playlists[ctx.guild.id][0][1], "null")

                voiceClient.play(discord.FFmpegPCMAudio(f"{pyc.songsPath}{pyc.seperator}{firstSong}")) #, after=lambda e: self._cleanup(ctx, firstSong))
                await asyncio.sleep(playingVideo.length)

                self._removeSong(ctx.guild.id, firstSong)
            



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