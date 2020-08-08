import pafy
import discord
import os

pyc = __import__("pyconfig")

class Video:
    def __init__(self, url, requester, path):

        self.url = url
        self.info = pafy.new(url)

        self.title = self.info.title
        self.uploader = self.info.author
        self.requested_by = requester
        self.path = path
        
    def download(self):
        self.best = self.info.getbest()
        self.filename = self.best.download(filepath=f"{pyc.songsPath}{pyc.seperator}{self.path}.mp3")

    def cleanup(self):
        os.remove(f"{pyc.songsPath}{pyc.seperator}{self.path}.mp3")
