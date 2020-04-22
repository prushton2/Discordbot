import json

class JsonManager:
  def __init__(self, path):
    self.path = path
  def load(self):
    #opens json file and returns data
    with open(self.path, "r") as theFile:
      return json.load(theFile) 

  def save(self, data):
    #opens json file and saves data
    with open(self.path, "w") as theFile:
      json.dump(data, theFile)

class UserData:
  def __init__(self, path):
    self.path = path
    self.jsm = JsonManager(path)
    self.usr = 0

  def getBal(self):
    return self.jsm.load()["users"][str(self.usr)]["bal"]
  def setBal(self, bal):
    ud = self.jsm.load()
    ud["users"][str(self.usr)]["bal"] = bal
    self.jsm.save(ud)

  def getPct(self):
    return self.jsm.load()["users"][str(self.usr)]["pct"]
  def setPct(self, pct):
    ud = self.jsm.load()
    ud["users"][str(self.usr)]["pct"] = pct
    self.jsm.save(ud)


  def getInv(self):
    return self.jsm.load()["users"][str(self.usr)]["inv"]
  def setInv(self, inv):
    ud = self.jsm.load()
    ud["users"][str(self.usr)]["inv"] = inv
    self.jsm.save(ud)

  def getAllUsers(self):
    return self.jsm.load()["users"]

  def addUsr(self, userID):
    ud = self.jsm.load()
    ud["users"][str(userID)] = {"bal": 0, "pct": 1.0, "inv": []} 
    self.jsm.save(ud)