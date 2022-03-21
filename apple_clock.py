from datetime import *
import math
import tkinter as Tkinter
from math import *
import time
import json

class Clock(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.x=150	# Center Point x
        self.y=150	# Center Point
        self.length=50	# Hand Length
        self.triggers()
    
    # Trigger for other fuctions
    def triggers(self):
        self.canvas_shapes()
        self.creating_bg()
        self.creating_hands()
        return
    
    # Back-ground
    def creating_bg(self):
        self.image=Tkinter.PhotoImage(file='clock.gif')
        self.canvas.create_image(150,150, image=self.image)
        return


    # Creating Canvas
    def canvas_shapes(self):
        self.canvas=Tkinter.Canvas(self, bg='black')
        self.canvas.pack(expand='yes',fill='both')
        return

    # Creating Moving hands
    def creating_hands(self):
        self.hands=[]
        for i in range(3):
            store=self.canvas.create_line(self.x, self.y,self.x+self.length,self.y+self.length,width=2, fill='black')
            self.hands.append(store)
        return

    # Function for updates
    def update_class(self):
        now=time.localtime()
        t = time.strptime(str(now.tm_hour), "%H")
        hour = int(time.strftime( "%I", t ))*5
        now=(hour,now.tm_min,now.tm_sec)
        # Changing hand Coordinates
        for n,i in enumerate(now):
            x,y=self.canvas.coords(self.hands[n])[0:2]
            cr=[x,y]
            cr.append(self.length*math.cos(math.radians(i*6)-math.radians(90))+self.x)
            cr.append(self.length*math.sin(math.radians(i*6)-math.radians(90))+self.y)
            self.canvas.coords(self.hands[n], tuple(cr))
        return

# Main Function Trigger
if __name__ == '__main__':
	root= Clock()

	# Creating Main Loop
	while True:
		root.update()
		root.update_idletasks()
		root.update_class()