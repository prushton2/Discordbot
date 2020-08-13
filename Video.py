import youtube_dl as ytdl
import discord

options = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}


class Video:
    def __init__(self, url, requester):
        with ytdl.YoutubeDL(options) as ydl:
            
            video = ydl.extract_info(url, download=False)
            videoFormat = video["formats"][0]

            self.url = url 
            self.stream_url = videoFormat['url']
            self.title = video['title']
            self.uploader = video['uploader']
            self.thumbnail = video['thumbnail']
            self.length = video['duration']
            self.requester = requester

    def getEmbed(self, status="Now Playing"):
        embedVar = discord.Embed(title=f"{status} - {self.title}", url=f"{self.url}", color=0x00ff00)
        embedVar.add_field(name=f"By {self.uploader}", value=f"{int(self.length/60)}m {self.length%60}s", inline=False)
        embedVar.set_thumbnail(url=self.thumbnail)
        embedVar.set_footer(text=f"Requested by {self.requester}",icon_url=self.requester.avatar_url)
        return embedVar