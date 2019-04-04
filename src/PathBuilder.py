"""A class to build a byte array of the robots path"""
import enum


class Instruction(enum.Enum):
    Forward = 1
    Right = 2
    Left = 3
    Back = 4

class PathBuilder:
    pathArray = bytearray()
    commandTable = {
        1: Instruction.Forward,
        'f': Instruction.Forward,
        'F': Instruction.Forward,
        3: Instruction.Left,
        'l': Instruction.Left,
        'L': Instruction.Left,
        2: Instruction.Right,
        'R': Instruction.Right,
        'r': Instruction.Right,
        4: Instruction.Back,
        'b': Instruction.Back,
        'B': Instruction.Back
    }

    def __init__(self):
        self.pathArray = bytearray()
        

    def addCommand(self,command,distance):
        self.pathArray.append(self.commandTable.get(command).value)
        self.pathArray.append(distance)


    def getPathToSend(self):
        path = self.pathArray
        path.append(0x48)
        return path

    def clearPath(self):
        self.pathArray = bytearray()
