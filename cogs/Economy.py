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