import pafy
import discord
import os

pyc = __import__("pyconfig")
class Video:
    def __init__(self, url, requested_by, path):

        self.url = url
        self.info = pafy.new(url)

        self.title = self.info.title
        self.uploader = self.info.author
        self.requested_by = requested_by
        self.path = path
        self.thumbnail = self.info.thumb

    def download(self):
        self.best = self.info.getbest()
        self.filename = self.best.download(filepath=f"{pyc.songsPath}{pyc.seperator}{self.path}.mp3")

    def cleanup(self):
        os.remove(f"{pyc.songsPath}{pyc.seperator}{self.path}.mp3")

    def getEmbed(self, status="Now Playing"):
        embedVar = discord.Embed(title=f"{status} - {self.title}", url=f"{self.url}", color=0x00ff00)
        embedVar.set_thumbnail(url=self.thumbnail)
        embedVar.set_footer(text=f"Requested by {self.requested_by}",icon_url=self.requested_by.avatar_url)
        return embedVar
