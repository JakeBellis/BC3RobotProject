'''
Created on Feb 18, 2019

@author: Jake
'''
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
import RobotInstruction
import PathBuilder as PB
from builtins import input
from digi.xbee.models.message import XBeeMessage
from digi.xbee.models.address import XBee16BitAddress, XBee64BitAddress
from DisplayManager import DisplayManager
import sys

try:
    COMport = sys.argv[1]
except IndexError:
    COMport = 'COM9'

baud_rate = 9600
remote_address = '0010'
transmitDevice = XBeeDevice(COMport,baud_rate)
remoteDevice = RemoteXBeeDevice(transmitDevice, XBee64BitAddress.from_hex_string(remote_address), XBee16BitAddress.from_hex_string(remote_address))


def main():
    
    xbeeCommunication()

def xbeeCommunication():
    transmitDevice.close()

    print('transmitting to: ')
    print(remoteDevice.get_16bit_addr())
    cont = 'y'
    pb = PB.PathBuilder()
    while(cont != 'n'):
        try:

            transmitDevice.open()
            instruction = getCommand(pb)

            #print(hex(instruction))
            sendInstructions(instruction)
            
            
        except Exception as e:
            print("failed to send data")
            print(e)
            
            transmitDevice.close()

        try:
            receiveInstruction()
            
        except Exception as e:
            print("Did not receive callback")
            print(e)

        transmitDevice.close()
        pb.clearPath()
        cont = input('Continue?')
    transmitDevice.close()

def getCommand(pathBuilder):
    cont = 'y'
    while(cont != 'n'):
        cmd = input("Specify a Command: ")
        dist = input("Distance: ")
        pathBuilder.addCommand(cmd,int(dist))
        cont = input("Add another command? ")
    return pathBuilder.getPathToSend() #create instruction for actual program

def sendInstructions(data):
    transmitDevice.send_data(remoteDevice, data) #sends the data to the remote device

def receiveInstruction():
    xbeeMessage = transmitDevice.read_data(1000)
    dataArray = []
    for i in range(len(xbeeMessage.data)):
        dataArray.append(xbeeMessage.data[i])
    print(dataArray)



if __name__ == '__main__':
    main()