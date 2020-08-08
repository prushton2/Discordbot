import pafy
import discord
import os
import youtube_dl as ytdl

pyc = __import__("pyconfig")

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}

class Video:
    def __init__(self, url, requested_by, path):
        self.url = url
        self.requested_by = requested_by

        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            self.info = ydl.extract_info(url, download=False)
            
            self.format = self.info["formats"][1]
            self.stream_url = self.format["url"]
            
            self.title = self.info["title"]
            self.uploader = self.info["uploader"]

            self.thumbnail = self.info["thumbnail"] if "thumbnail" in self.info else None


        # self.url = url
        # self.info = pafy.new(url)

        # self.title = self.info.title
        # self.uploader = self.info.author
        # self.requested_by = requested_by
        # self.path = path
        # self.thumbnail = self.info.thumb

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
