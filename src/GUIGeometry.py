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
    
    def getOrientation(self, q, r):
        """gets the orientation of three ordered points {self, q, r}
        0: collinear
        1: clockwise
        2: ccw
        """
        val = (q.y - self.y) * (r.x - q.x) - (q.x - self.x) * (r.y - q.y)
        if(val == 0):
            return 0
        else:
            return 1 if (val > 0) else 2


class Line:
    point1 = Point(0,0)
    point2 = Point(0,0)

    def __init__(self,point1,point2):
        """Creates a line using 2 points
        
        """
        self.point1 = point1
        self.point2 = point2

    def from_coords(self,x1,y1,x2,y2): #creates a line from coordinates instead of points
        pt1 = Point(x1,y1)
        pt2 = Point(x2,y2)
        return Line(pt1,pt2)

    def length(self):
        return self.point1.getDistance(self.point2)

    #def isIntersecting(line):

    