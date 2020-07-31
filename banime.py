import random
class anime:
    def __init__(self, name, keywords):
        self.name = name
        self.keywords = keywords

class Banime:
    def __init__(self, targetedAnime):
        self.targetedAnime = targetedAnime
        self.bannedanime = random.choice(self.targetedAnime)

    def newBanime(self):
        self.bannedanime = random.choice(self.targetedAnime)

    def check(self, content):
        reason = ""
        relatedAnime = ""

        if self.bannedanime.name.lower() in content.lower():
            reason = self.bannedanime.name
            relatedAnime = self.bannedanime.name
        else:
            for i in self.bannedanime.keywords:
                if i.lower() in content.lower():
                    relatedAnime = self.bannedanime.name
                    reason = i
            
        return reason, relatedAnime


bannedAnime = [anime("Attack on titan", ["Mikasa", "Erin"])]