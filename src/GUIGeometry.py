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
    
    def getAngleBetween(self,secondPoint):
        tot_dist = self.getDistance(secondPoint)
        x_dist = secondPoint.x - self.x
        y_dist = secondPoint.y - self.y
        if(x_dist < 0 and y_dist < 0):
            return math.sin(y_dist/tot_dist) + 270
        elif(x_dist < 0):
            return math.sin(y_dist/tot_dist) + 90 
        elif (y_dist < 0):
            return math.sin(y_dist/tot_dist) + 360
        else:
            return math.sin(y_dist/tot_dist)

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

    def getManhattanDist(self,secondPoint):
        return abs(self.x - secondPoint.x) + abs(self.y - secondPoint.y)


class Line:
    point1 = Point(0,0)
    point2 = Point(0,0)
    displayVal = ""

    def __init__(self,point1,point2, color = None, size = None):
        """Creates a line using 2 points
        
        """
        self.point1 = point1
        self.point2 = point2

        if color is None:
            self.color = "black"
        else:
            self.color = color
        if size is None:
            self.size = 2
        else:
            self.size = size

    @classmethod
    def from_coords(cls,x1,y1,x2,y2): #creates a line from coordinates instead of points
        pt1 = Point(x1,y1)
        pt2 = Point(x2,y2)
        return cls(pt1,pt2)

    def length(self):
        return self.point1.getDistance(self.point2)

    def onLineCollinear(self, point):
        """Helper method for isIntersecting()
            Determines if a collinear point is on a segment
        Arguments:
            point {[type]} -- [description]
        
        Returns:
            Boolean -- if the point is on the line
        """

        if((point.x <= max(self.point1.x, self.point2.x)) and (point.x >= min(self.point1.x, self.point2.x)) and (point.y <= max(self.point1.y, self.point2.y)) and (point.y >= min(self.point1.y, self.point2.y))): 
        # and (point.y <= max(self.point1.y, self.point2.y)) and (point.y >= min(self.point1.y, self.point2.y))):
            return True

        return False
        

    def isIntersecting(self, line):
        #get the orientations needed for cases
        o1 = self.point1.getOrientation(self.point2, line.point1)
        o2 = self.point1.getOrientation(self.point2, line.point2)
        o3 = line.point1.getOrientation(line.point2, self.point1)
        o4 = line.point1.getOrientation(line.point2, self.point2)

        #general case
        if (o1 != o2 and o3 != o4):
            return True

        #cases if lines are collinear
        if (o1 == 0 and self.onLineCollinear(line.point1)):
            return True
        if (o2 == 0 and self.onLineCollinear(line.point2)):
            return True
        if (o3 == 0 and line.onLineCollinear(self.point1)):
            return True
        if (o4 == 0 and line.onLineCollinear(self.point2)):
            return True
        
        return False
        



    