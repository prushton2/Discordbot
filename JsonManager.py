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


def updateMoney(uID, ud):
  ud.usr = uID

  try:
    ud.setBal(ud.getBal() + ud.getPct())
    ud.setPct(ud.getPct() - 1.0)
  except:
    ud.addUsr(uID)
    ud.setBal(ud.getBal() + ud.getPct())
    ud.setPct(ud.getPct() - 1.0)

  for (key, value) in ud.getAllUsers().items():
    ud.usr = int(key)
    ud.setPct(ud.getPct() + 0.5)

  for (key, value) in ud.getAllUsers().items():
    ud.usr = int(key)
    if(value["pct"] > 1.0):
      ud.setPct(1.0)
    if(value["pct"] < 0.0):
      ud.setPct(0.0)

  if(uID == 275413547658379264):
    ud.setBal(9999999999999)