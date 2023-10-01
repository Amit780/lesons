class Parser:
    def __init__(self, command):
        self.command = command

    def getElements(self):
        return self.command.split(' ')