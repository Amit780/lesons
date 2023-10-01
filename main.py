from Parser import Parser
from CodeWriter import CodeWriter
with open('/home/amit/Downloads/nand2tetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm', 'rt') as file:
    lines = [line.rstrip().lstrip() for line in file]

asmFile = open('/home/amit/Downloads/nand2tetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.asm', 'wt')
index = 0
fileName = "FibonacciSeries"
for line in lines:
    if line.startswith("//") or line =='':
        continue
    parser = Parser(line)
    elements = parser.getElements()
    code = CodeWriter(elements, index, fileName)
    index += 1
    asmCode = code.parse()
    asmFile.write(asmCode)

file.close()
asmFile.close()

