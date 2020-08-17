import pafy
import discord
import os
import uuid

pyc = __import__("pyconfig")
class Video:
    def __init__(self, url, requested_by):

        self.url = url
        self.info = pafy.new(url)

        self.title = self.info.title
        self.uploader = self.info.author
        self.requested_by = requested_by
        self.length = self.info.length
        self.thumbnail = self.info.thumb
        self.path = uuid.uuid4()

    def download(self, serverID):
        self.best = self.info.getbest()
        self.filename = self.best.download(filepath=f"{pyc.songsPath}{pyc.seperator}{self.path}.mp3")

    def getEmbed(self, status="Now Playing"):
        embedVar = discord.Embed(title=f"{status} - {self.title}", url=f"{self.url}", color=0x00ff00)
        embedVar.add_field(name=f"By {self.uploader}", value=f"{int(self.length/60)}m {self.length%60}s", inline=False)
        embedVar.set_thumbnail(url=self.thumbnail)
        embedVar.set_footer(text=f"Requested by {self.requested_by}",icon_url=self.requested_by.avatar_url)
        return embedVar

class Playlist:
    def __init__(self, guildID):
        self.videos = []
        self.time = 0
        self.guildID = guildID

    def removeSong(self):
        sVideo = self.videos[0]
        try:
            os.remove(f"{pyc.songsPath}{pyc.seperator}{sVideo.path}.mp3")
        except:
            pass
        self.videos.pop(0)

    def addVideo(self, video):
        self.videos.append(video)

    def cleanup(self):
        for i in self.videos:
            self.removeSong()

class AllPlaylists:
    def __init__(self):
        self.playlists = []

    def newPlaylist(self, guildID):
        self.playlists.append(Playlist(guildID))

    def addVideo(self, guildID, video):
        needsNewPlaylist = True
        for i in self.playlists:
            if(i.guildID == guildID):
                needsNewPlaylist = False
                i.addVideo(video)
        if(needsNewPlaylist):
            self.newPlaylist(guildID)
            self.playlists[-1].addVideo(video)

    def cleanup(self, guildID):
        for i in self.playlists:
            if(i.guildID == guildID):
                i.cleanup()

    def getPlaylist(self, guildID):
        for i in self.playlists:
            if(i.guildID == guildID):
                return i
        return []

    def removeVideo(self, guildID):
        for i in self.playlists:
            if(i.guildID == guildID):
                i.removeSong()

"""
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
"""