import pafy
import discord

options = {
    "quiet": True,
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "extract_flat": "in_playlist"
}


class Video:
    def __init__(self, url, requester, path):

        self.url = url
        self.info = pafy.new(url)

        self.title = self.info.title
        self.uploader = self.info.author
        self.requested_by = requester
        self.path = path

        self.best = self.info.getbest()
        self.filename = self.best.download(filepath=f"{path}.webm")



'''
    def getInfo(self, url):
        with ytdl.YoutubeDL(options) as ydl:
            rawInfo = ydl.extract_info(url, download=False)
            return rawInfo

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed






class Video:
    def __init__(self, url, author):
        """Plays audio from (or searches for) a URL."""
        with ytdl.YoutubeDL(options) as ydl:
            video = self._get_info(url)

            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video[
                "thumbnail"] if "thumbnail" in video else None
            
            self.author = author

    def _get_info(self, video_url):
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    '''