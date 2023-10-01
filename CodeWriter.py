class CodeWriter:

    def __init__(self, commands, index, file):
        self.commands = commands
        self.index = index
        self.fileName = file

    def parse(self):
        comment = "//" + " ".join(self.commands) + "\n"
        #print(self.commands)
        if self.commands[0] == 'function':
            instruction = self.function()
        elif self.commands[0] == 'call':
            instruction = self.call()
        elif self.commands[0] == 'return':
            instruction = self.freturn()
        elif len(self.commands) == 1:
            instruction = self.arithmetic(self.commands[0])
        elif self.commands[0] == 'label' or self.commands[0] == 'if-goto' or self.commands[0] == 'goto':
            instruction = self.labelOrGoto()
        else:
            instruction = self.pushOrPop(self.commands[0])
        return comment + instruction + "\n"

    def function(self):
        pass

    def call(self):
        pass

    def freturn(self):
        pass
    def labelOrGoto(self):
        if self.commands[0] == 'label':
            return f"({self.commands[1]})"
        elif self.commands[0] == 'if-goto':
            return ("@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{self.commands[1]}\n"
                    "D;JNE\n")
        elif self.commands[0] == 'goto':
            return (f"@{self.commands[1]}\n"
                    "0;JMP\n")


    def arithmetic(self, operation):
        if operation == 'add' or operation == 'sub' or operation == 'and' or operation == 'or':
            return self.firstSet(operation)
        elif operation == 'neg' or operation == 'not':
            return self.secondSet(operation)
        else:
            return self.thirdSet(operation)

    def firstSet(self, operation):
        if operation == 'add':
            line = "M=M+D"
        elif operation == 'sub':
            line = 'M=M-D'
        elif operation == 'and':
            line = 'M=M&D'
        else:
            line = 'M=M|D'

        result = ("@SP\n"
                  "AM=M-1\n"
                  "D=M\n"
                  "A=A-1\n"
                  f"{line}\n")
        return result

    def secondSet(self, operation):
        if operation == 'neg':
            line = 'M=-M'
        else:
            line = 'M=!M'

        result = ("@SP\n"
                  "AM=M-1\n"
                  f"{line}\n"
                  "@SP\n"
                  "M=M+1\n")
        return result

    def thirdSet(self, operation):

        if operation == 'eq':
            f1 = 'equal'
            f2 = 'JEQ'
        elif operation == 'gt':
            f1 = 'greater'
            f2 = 'JGT'
        else:
            f1 = 'lesser'
            f2 = 'JLT'

        result = ("@SP\n"
                  "AM=M-1\n"
                  "D=M\n"
                  "A=A-1\n"
                  "D=M-D\n"
                  f"@{f1}{self.index}\n"
                  f"D;{f2}\n"
                  "@SP\n"
                  "AM=M-1\n"
                  "M=0\n"
                  "@SP\n"
                  "M=M+1\n"
                  f"@continue{self.index}\n"
                  "0;JMP\n"
                  f"({f1}{self.index})\n"
                  f"@SP\n"
                  "AM=M-1\n"
                  "M=-1\n"
                  "@SP\n"
                  "M=M+1\n"
                  f"(continue{self.index})\n")
        return result

    def pushOrPop(self, op):
        value = self.commands[2]
        if self.commands[1] == 'static':
            if self.commands[0] == 'push':
                return (f"@{self.fileName}.{value}\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n")
            else:
                return ("@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        f"@{self.fileName}.{value}\n"
                        "M=D\n"
                        )

        if self.commands[1] == 'constant':
            return (f"@{value}\n"
                    "D=A\n"
                    "@SP\n"
                    "A=M\n"
                    "M=D\n"
                    "@SP\n"
                    "M=M+1\n")
        elif self.commands[1] == "local":
            key = "LCL"
        elif self.commands[1] == "argument":
            key = "ARG"
        elif self.commands[1] == "this":
            key = "THIS"
        elif self.commands[1] == 'temp':
            key = "5"
        elif self.commands[1] == 'pointer':
            key = '3'
        else:
            key = "THAT"

        if key == "5" or key == '3':
            add = "A"
        else:
            add = "M"
        pushingres = (f"@{value}\n"
                      "D=A\n"
                      f"@{key}\n"
                      f"A={add}+D\n"
                      "D=M\n"
                      "@SP\n"
                      "A=M\n"
                      "M=D\n"
                      "@SP\n"
                      "M=M+1\n"
                      "")

        popingres = (f"@{value}\n"
                     "D=A\n"
                     f"@{key}\n"
                     f"D={add}+D\n"
                     "@R13\n"
                     "M=D\n"
                     "@SP\n"
                     "AM=M-1\n"
                     "D=M\n"
                     "@R13\n"
                     "A=M\n"
                     "M=D\n")
        if self.commands[0] == 'push':
            return pushingres
        return popingres
