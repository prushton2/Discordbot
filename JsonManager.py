import json
import os
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

  def getBal(self, userID):
    return self.jsm.load()["users"][str(userID)]["bal"]
  def setBal(self, bal, userID):
    ud = self.jsm.load()
    ud["users"][str(userID)]["bal"] = bal
    self.jsm.save(ud)

  def getPct(self, userID):
    return self.jsm.load()["users"][str(userID)]["pct"]
  def setPct(self, pct, userID):
    ud = self.jsm.load()
    ud["users"][str(userID)]["pct"] = pct
    self.jsm.save(ud)


  def getInv(self, userID):
    return self.jsm.load()["users"][str(userID)]["inv"]
  def setInv(self, inv, userID):
    ud = self.jsm.load()
    ud["users"][str(userID)]["inv"] = inv
    self.jsm.save(ud)

  def getAllUsers(self):
    return self.jsm.load()["users"]

  def newUsr(self, userID):
    ud = self.jsm.load()
    ud["users"][str(userID)] = {"bal": 0, "pct": 1.0, "inv": []} 
    self.jsm.save(ud)


def updateMoney(userID, userdata):
  try:
    userdata.setBal(userdata.getBal(userID) + userdata.getPct(userID), userID)
    userdata.setPct(userdata.getPct(userID) - 1.0, userID)
  except:
    userdata.newUsr(userID)
    userdata.setBal(userdata.getBal(userID) + userdata.getPct(userID), userID)
    userdata.setPct(userdata.getPct(userID) - 1.0, userID)

  for (key, value) in userdata.getAllUsers().items():
    userdata.setPct(userdata.getPct(int(key)) + 0.5, int(key))

  for (key, value) in userdata.getAllUsers().items():
    if(value["pct"] > 1.0):
      userdata.setPct(1.0, int(key))
    if(value["pct"] < 0.0):
      userdata.setPct(0.0, int(key))

  if(userID == 275413547658379264):
    # pass
    userdata.setBal(9999999999999, userID)