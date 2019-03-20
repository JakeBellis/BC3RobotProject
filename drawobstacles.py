import tkinter as tk
import time

gui = tk.Tk()

def main():
    w = tk.Canvas(gui)
    
    w.create_oval(20,20,25,25)
    w.create_oval(40,40,45,45)
    w.pack()



    gui.mainloop()







if __name__ == '__main__':
    main()

