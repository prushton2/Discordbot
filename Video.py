import pafy
import discord

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