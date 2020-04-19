class Command:
    def __init__(self, commands, commandName, description):
        self.commands = commands
        self.commandName = commandName
        self.description = description


class Commands:
    def __init__(self):
        self.commands = []
    def checkAllCommands(self, message, prefix):
        for i in self.commands:
            for j in i.commands:
                if(message.content.startswith(prefix+j)):
                    return i.commandName
        return None