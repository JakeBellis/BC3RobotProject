import random
from xbee import XBee, ZigBee

print("Hello World")

def main():
    print("main function")
    num = input("Pick a number: ")
    print(pow(float(num),2))

if __name__ == "__main__":
    main()