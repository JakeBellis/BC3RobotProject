"""
A place to test the display classes that will be included in the display manager.
"""
import tkinter as tk
import time
from GUIGeometry import Point as pt

gui = tk.Tk()
points = []

def main():
    display = tk.Canvas(gui)
    p1 = pt(45,45)
    p2 = pt(90, 90)
    # w.create_oval(p1.x - 5, p1.y - 5, p1.x +5, p1.y+5)
    # w.create_oval(p2.x - 5, p2.y -  5, p2.x + 5, p2.y+5)
    drawPoint(p1,display)
    drawPoint(p2,display)
    print(p1.getDistance(p2))
    display.pack()

    display.bind("<Button-1>", lambda event, canvas = display: onClick(event,canvas))

    gui.mainloop()



def drawPoint(point, canvas):
    point_size = 2
    canvas.create_oval(point.x - point_size, point.y - point_size, point.x + point_size, point.y + point_size, fill = "black")
    canvas.pack()

def onClick(event, canvas):
    """
    draws a point at the position where the mouse was clicked
    """
    print("clicked at: " + str(event.x) + ", " + str(event.y)) 
    points.append(pt(event.x,event.y))
    drawPoint(pt(event.x,event.y), canvas)


if __name__ == '__main__':
    main()

