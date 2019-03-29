import math

class Point:
    """A point that can be displayed on the world map"""
    x = 0
    y = 0
    size = 2 #how large the point is in the window
    displayVal = ""  #name for the display of the point
    color = "black"

    def __init__(self, xCoord, yCoord,color = None, size = None):
        self.x = xCoord
        self.y = yCoord
        if color is None:
            self.color = "black"
        else:
            self.color = color
        if size is None:
            self.size = 2
        else:
            self.size = size
    
    
    def move(self,xCoord, yCoord):
        """moves the point to the specified new coordinates"""
        self.x = xCoord
        self.y = yCoord
    
    def getDistance(self, secondPoint):
        """returns the distance from a second point"""
        return math.sqrt(pow(secondPoint.x - self.x, 2) + pow(secondPoint.y - self.y, 2))