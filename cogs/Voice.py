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
allPlaylists = Video.AllPlaylists()


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

    @commands.command(description="Leaves the VC it is in", brief = "Leave a VC", aliases = ["byebye", "stop"])
    async def leave(self, ctx):
        for i in bot.voice_clients:
            if(i.guild.id == ctx.guild.id):
                await i.disconnect()
        allPlaylists.cleanup(ctx.guild.id)

    @commands.command(description = "Skips the currently playing song", brief = "skips a song")
    async def skip(self, ctx):
        try:
            for i in bot.voice_clients:
                if(i.guild.id == ctx.guild.id):
                    i.stop()
        except:
            await ctx.send("You arent in a voice channel")
            return

    @commands.command(description="Play a youtube video", brief = "play a song")
    async def play(self, ctx, url="null"):

        if(url == "null"):
            await ctx.send("You need to provide a youtube URL")

        try:
            voiceClient = await ctx.author.voice.channel.connect()
            allPlaylists.cleanup(ctx.guild.id)

        except discord.errors.ClientException:

            for i in bot.voice_clients:
                if(i.guild.id == ctx.guild.id):
                    voiceClient = i
        except:
            await ctx.send("You arent in a voice channel")
            return

        video = Video.Video(url, ctx.author)

        message = await ctx.send(embed=video.getEmbed("Now Loading"))
        video.download(ctx.guild.id)

        allPlaylists.addVideo(ctx.guild.id, video)

        await message.edit(embed=video.getEmbed("Now Playing" if len(allPlaylists.getPlaylist(ctx.guild.id).videos) == 1 else "Added to queue"))

        def after(error):
            allPlaylists.removeVideo(ctx.guild.id)
            try:
                playingVideo = allPlaylists.getPlaylist(ctx.guild.id).videos[0]
                voiceClient.play(discord.FFmpegPCMAudio(f"{pyc.songsPath}{pyc.seperator}{playingVideo.path}.mp3"), after=after)
            except:
                pass

        if(not voiceClient.is_playing()):
            playingVideo = allPlaylists.getPlaylist(ctx.guild.id).videos[0]
            voiceClient.play(discord.FFmpegPCMAudio(f"{pyc.songsPath}{pyc.seperator}{playingVideo.path}.mp3"), after=after)