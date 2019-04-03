'''
Created on Feb 18, 2019

@author: Jake
'''
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
import RobotInstruction
from builtins import input
from digi.xbee.models.address import XBee16BitAddress, XBee64BitAddress


import sys

try:
    COMport = sys.argv[1]
except IndexError:
    COMport = 'COM9'

baud_rate = 9600
remote_address = '0008'
transmitDevice = XBeeDevice(COMport,baud_rate)
remoteDevice = RemoteXBeeDevice(transmitDevice, XBee64BitAddress.from_hex_string(remote_address), XBee16BitAddress.from_hex_string(remote_address))


def main():
    transmitDevice.close()

    print('transmitting to: ')
    print(remoteDevice.get_16bit_addr())
    cont = 'y'
    while(cont != 'q'):
        try:
            transmitDevice.open()
            instruction = getCommand()

            #print(hex(instruction))
            sendInstructions(instruction)
        except Exception as e:
            print("failed to send data")
            print(e)
            transmitDevice.close()
        transmitDevice.close()
        cont = input('Continue?')
    transmitDevice.close()

def getCommand():
    cmd = input("Specify a Command: ")
    dist = input("Distance: ")
    return RobotInstruction.create_instruction_literal(cmd,int(dist)) #create instruction for actual program

def sendInstructions(data):
    transmitDevice.send_data(remoteDevice, data) #sends the data to the remote device

if __name__ == '__main__':
    main()