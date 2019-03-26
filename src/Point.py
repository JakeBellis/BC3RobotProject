import math

class Point:
    x = 0
    y = 0

    def __init__(self, xCoord, yCoord):
        self.x = xCoord
        self.y = yCoord
    
    def move(self,xCoord, yCoord):
        self.x = xCoord
        self.y = yCoord
    
    def getDistance(self, secondPoint):
        return math.sqrt(pow(secondPoint.x - self.x, 2) + pow(secondPoint.y - self.y, 2))