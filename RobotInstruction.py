'''
Created on Feb 18, 2019

@author: Jake
'''

def create_instruction(command, distance):
    """takes in a command and distance and converts it to instruction to 
    be sent"""
    commandVal = chr(ord(command))
    distanceVals = int2Hex(distance)
    instruction_set = [commandVal, distanceVals[0], distanceVals[1]]
    inst_out = ""
    for i in range(0,len(instruction_set)):
        inst_out = inst_out + str(instruction_set[i])
    return instruction_set
    
def int2Hex(value):
    MSB = (value >> 8) & 0xFF
    LSB = value & 0xFF
    return [chr(MSB),chr(LSB)]
