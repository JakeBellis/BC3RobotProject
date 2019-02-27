'''
Created on Feb 18, 2019

@author: Jake
'''

def create_instruction(command, distance):
    """takes in a command and distance and converts it to instruction to 
    be sent"""
    commandVal = ord(command)
    distanceVals = int2Hex(distance)
    instruction_set = [commandVal, distanceVals[0], distanceVals[1]]
    inst_out = bytearray()
    for i in range(0,len(instruction_set)):
        inst_out.append(instruction_set[i])
        #print(hex(instruction_set[i]))
    return inst_out
    
def int2Hex(value):
    MSB = (value >> 8) & 0xFF
    LSB = value & 0xFF
    print(hex(MSB) + " " + hex(LSB))
    return [int(MSB),int(LSB)]
