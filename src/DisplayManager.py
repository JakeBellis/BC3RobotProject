import tkinter as tk
import time
import random
from Point import Point as pt


#Main function to test functionalitys
def main():
    disp = DisplayManager()
    # for i in range(10):
    #     x = input("X: ")
    #     y = input("Y: ")
    #     disp.plotPoint(pt(int(x),int(y))) 
    
    #disp.mainWindow.mainloop()
    pt1 = pt(100,100,"red",10)
    pt2 = pt(200,200,"green",10)
    disp.drawPoint(pt1)
    disp.drawPoint(pt2)

    pt1.move(300,300)
    disp.redrawPoint(pt1)
    disp.display.after(0,movePoints(pt1,pt2,disp))
    disp.display.mainloop()

def movePoints(point1,point2,canvas):
    for i in range(20):
        pt1x = random.randint(5,595); pt1y = random.randint(5,595)
        pt2x = random.randint(5,595); pt2y = random.randint(5,595)
        point1.move(pt1x,pt1y)
        point2.move(pt2x,pt2y)
        canvas.redrawPoint(point1)
        canvas.redrawPoint(point2)
        canvas.display.update()
        time.sleep(1)

class DisplayManager:

    mainWindow = tk.Tk()
    points = []
    displayPoints = []
    display = tk.Canvas(mainWindow,width=600,height = 600)

    def __init__(self):
        self.display.bind("<Button-1>", self.onClick)
        self.display.pack()
    

    def drawPoint(self, point):
        point.displayVal = self.display.create_oval(point.x - point.size, point.y - point.size, point.x + point.size, point.y + point.size, fill = point.color)
        self.display.pack()

    def deletePoint(self, point):
        self.display.delete(point.displayVal)
        

    def redrawPoint(self,point):
        self.display.delete(point.displayVal)
        point.displayVal = self.display.create_oval(point.x - point.size, point.y - point.size, point.x + point.size, point.y + point.size, fill = point.color)

        

    def onClick(self, event):
        """
        draws a point at the position where the mouse was clicked
        """
        print("clicked at: " + str(event.x) + ", " + str(event.y)) 
        self.points.append(pt(event.x,event.y))
        self.drawPoint(pt(event.x,event.y))


if __name__ == '__main__':
    main()