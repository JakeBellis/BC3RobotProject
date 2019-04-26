"""
Classes to assist in the path finding of the robot dependent on classes in the Geometry package
Uses A* to find the path
"""

from GUIGeometry import Point,Line
import heapq
import math
import time


ROBOT_TRAVEL_DISTANCE = 10
ROBOT_MIN_TURN_ANGLE = 45

class PathNode: #Node in the linked list that holds a point
    nextNode = None
    point = None
    angleToNext = 0 #the angle between this and the next point
    heading = 0

    def __init__(self, point):
        self.point = point
        self.nextNode = None
        self.angleToNext = None
        self.heading = 0

    @classmethod
    def fromNode(self, Node): #method for creating a node from an existing node
        NewNode = PathNode(Point(0,0))
        NewNode.point = Point(Node.point.x,Node.point.y)
        if(Node.nextNode):
            NewNode.nextNode = self.fromNode(Node.nextNode)
        NewNode.angleToNext = Node.angleToNext
        NewNode.heading = Node.heading
        return NewNode

    
    def setNext(self, newNode):
        self.nextNode = newNode
        self.angleToNext = self.point.getAngleBetween(newNode.point)
        self.heading = self.heading + self.angleToNext % 360
        


class Path:
    head = None
    last = None
    size = 0
    distance = 0
    heading = 0 
    degreesTurned = 0

    def __init__(self,firstPoint):
        self.head = PathNode(firstPoint)
        self.last = self.head
        self.size = 1
        self.degreesTurned = 0

    
    def addPoint(self, nextPoint):
        """Adds a point to a new path and returns the path"""
        NewPath = Path(Point(0,0))
        NewPath.head = PathNode.fromNode(self.head)
        NewPath.last = PathNode.fromNode(self.last)
        NewPath.distance = self.distance
        NewPath.size = self.size
        #NewPath.degreesTurned = self.degreesTurned
        nextNode = PathNode(nextPoint)
        NewPath.append(nextPoint)
        NewPath.last = nextNode
        NewPath.distance += ROBOT_TRAVEL_DISTANCE
        NewPath.size += 1
        
        return NewPath

    def append(self, newPoint):
        """Adds a new node to the last node of the list and sets the heading angle
        """
        newNode = PathNode(newPoint)

        last = self.head
        while(last.nextNode):
            last = last.nextNode
        self.degreesTurned += abs(self.heading - last.point.getAngleBetween(newNode.point))
        self.heading = last.point.getAngleBetween(newNode.point)
        last.nextNode = newNode


    def __lt__(self, other):
        return self.distance < other.distance
    

class PathManager:
    startPoint = None
    endPoint = None
    heap = []

    def __init__(self):
        self.reset()

    def reset(self):
        self.heap = heapq
        self.startPoint = None
        self.endPoint = None
    
    def findPath(self, startPoint, endPoint,lines): #takes a starting point, endpoint and an array of the obstacle lines to find the path with the shortest distance
        """Determines the best path for the robot to take given the starting point, end point, and an array of the lines
        representing the obstacles
        
        Returns:
            Path -- the optimal path for the robot to take
        """

        self.heap = MinHeap(initial=[Path(startPoint)], key= lambda Path: ( 3 * Path.degreesTurned + 0.8 * Path.distance + Path.last.point.getManhattanDist(endPoint)))
        visitedPoints = set() #list of points to end and distance so we don't visit a node twice
        currentPath = None
        currentPoint = None
        time.clock()
        pointsConsidered = 0
        while(self.heap._data[0][1].last.point.getDistance(endPoint) > 10):

            if(currentPath):
                while((currentPath.last.point.x, currentPath.last.point.y) in visitedPoints):
                    currentPath = self.heap.pop()
                currentPath = self.heap.pop() #find the first point we haven't visited
            else:
                currentPath = self.heap.pop()
            
            pointsConsidered += 1
            visitedPoints.add((currentPath.last.point.x, currentPath.last.point.y))
            # print("distance: " + str(currentPath.last.point.getDistance(endPoint)))
            # print("distance traveled: " + str(currentPath.distance))
            
            currentPoint = currentPath.last.point
            
            for angle in range(0,360,ROBOT_MIN_TURN_ANGLE): #adds the lines at the turn angles to the path
                intersectsLine = False
                nextPoint = Point(int(currentPath.last.point.x + math.cos(angle*math.pi/180)*ROBOT_TRAVEL_DISTANCE), int(currentPath.last.point.y + math.sin(angle*math.pi/180)*ROBOT_TRAVEL_DISTANCE))
                
                pathLine = Line(currentPoint, nextPoint)
                for line in lines:
                    if pathLine.isIntersecting(line):
                        intersectsLine = True
                        break
                if(intersectsLine == False and not self.pointVisited(nextPoint,visitedPoints)):
                    nextPath = currentPath.addPoint(nextPoint)
                    z = nextPath.last.point.getDistance(endPoint)
                    self.heap.push(nextPath)
                
                if(len(self.heap._data) == 0):
                    print("No path exists to the endpoint")
                    return None
            
                    
        print("FOUND PATH!!!!!!")
        print(time.clock())
        print(pointsConsidered)
        return currentPath
        
    

    def pointVisited(self,point,visitedSet):
        THRESHOLD = 5 #number of adjacent integer valued points to consider
        for x in range(point.x - THRESHOLD, point.x + THRESHOLD + 1):
            for y in range(point.y - THRESHOLD, point.y + THRESHOLD + 1):
                if ((x,y) in visitedSet):
                    return True
        return False


class MinHeap(object):
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        if initial:
            self._data = [(key(item), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))
        heapq.heapify(self._data)

    def pop(self):
        return heapq.heappop(self._data)[1]
    