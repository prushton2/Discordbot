class Command:
    def __init__(self, commands, commandName, syntax, description):
        self.commands = commands
        self.commandName = commandName
        self.description = description
        self.syntax = syntax


class Commands:
    def __init__(self):
        self.commands = []
    def checkAllCommands(self, message, prefix):
        cmd = message.content.split()[0]
        print(cmd)
        for i in self.commands:
            for j in i.commands:
                if(cmd == prefix+j):
                    return i.commandName
        return None

class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class Items:
    def __init__(self):
        self.items = []

    def buyItem(self, name, balance):
        for i in self.items:
            if(i.name == name and balance >= i.cost):
                return True, balance - i.cost
        return False, balance


