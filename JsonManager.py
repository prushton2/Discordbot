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

  