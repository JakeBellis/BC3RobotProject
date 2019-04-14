import tkinter as tk
import time
import random
from GUIGeometry import Point as pt
from GUIGeometry import Line as ln
import Pathfinder


#Main function to test functionality
def main():
    disp = DisplayManager() 
    
    pt1 = pt(100,100,"green",10)
    pt2 = pt(500,500,"red",10)
    disp.drawPoint(pt1)
    disp.drawPoint(pt2)
    testLines = [ln(pt(100,200),pt(300,200)),ln(pt(300,100),pt(300,200)),ln(pt(50,300),pt(400,300))]
    for line in testLines:
        disp.drawLine(line)
    pm = Pathfinder.PathManager()
    path = pm.findPath(pt1,pt2,testLines)
    currentNode = path.head
    for i in range(path.size-1):
        pathLine = ln(currentNode.point, currentNode.nextNode.point)
        disp.drawLine(pathLine)
        currentNode = currentNode.nextNode
    
    print(path.size)
    

    # pt1.move(300,300)
    # disp.redrawPoint(pt1)
    #ln1 = ln(pt1, pt2)
    # disp.lines.append(ln1)
    # disp.drawLine(ln1)
    disp.display.after(0,movePoints(pt1,pt2,disp))
    disp.display.mainloop()

def movePoints(point1,point2,canvas):
    lineArray = []
    # verticalLine = ln.from_coords(300,0,300,600)
    # canvas.drawLine(verticalLine)
    
    # for i in range(20):
    #     pt1x = random.randint(5,595); pt1y = random.randint(5,595)
    #     pt2x = random.randint(5,595); pt2y = random.randint(5,595)
    #     point1.move(pt1x,pt1y)
    #     point2.move(pt2x,pt2y)
    #     lineArray.append(ln(point1,point2))
    #     canvas.drawLine(lineArray[i])
    #     canvas.redrawPoint(point1)
    #     canvas.redrawPoint(point2)
    #     print(verticalLine.isIntersecting(lineArray[i]))
    #     canvas.display.update()
    #     time.sleep(0.2)

class DisplayManager:

    mainWindow = tk.Tk()
    points = []
    lines = []
    displayPoints = [] #names of points assigned by canvas in case one needs deleted
    displayLines = []
    display = tk.Canvas(mainWindow,width=600,height = 600)

    def __init__(self):
        self.display.bind("<Button-1>", self.onClick)
        self.display.pack()
        # findpathBtn = tk.Button(master=self.mainWindow, text = "Find Path") #command = callback
        # findpathBtn.pack()
    

    def drawPoint(self, point):
        point.displayVal = self.display.create_oval(point.x - point.size, point.y - point.size, point.x + point.size, point.y + point.size, fill = point.color)
        self.display.pack()

    def deletePoint(self, point):
        self.display.delete(point.displayVal)
        

    def redrawPoint(self,point):
        self.display.delete(point.displayVal)
        point.displayVal = self.display.create_oval(point.x - point.size, point.y - point.size, point.x + point.size, point.y + point.size, fill = point.color)

    def drawLine(self,line):
        line.displayVal = self.display.create_line(line.point1.x,line.point1.y,line.point2.x, line.point2.y,fill = line.color)
        self.display.pack()

    def onClick(self, event):
        """
        draws a point at the position where the mouse was clicked and connects the lines together
        """
        print("clicked at: " + str(event.x) + ", " + str(event.y)) 
        newPoint = pt(event.x,event.y)
        self.points.append(newPoint)
        self.drawPoint(newPoint)
        DRAW_LINE_THRESHOLD = 50
        for testPoint in self.points:
            if(newPoint.getDistance(testPoint) < DRAW_LINE_THRESHOLD and testPoint != newPoint):
                newLine = ln(newPoint,testPoint)
                makeLine = True
                for line in self.lines:
                    if newLine.isIntersecting(line): #if it is intersecting a previous line, it is redundant
                        if newLine.point1 != line.point1 and newLine.point1 != line.point2 and  \
                        newLine.point2 != line.point1 and newLine.point2 != line.point2:
                            makeLine = False
                            break
                if makeLine:
                    self.lines.append(newLine)
                    self.drawLine(newLine)
            


if __name__ == '__main__':
    main()