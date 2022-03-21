from datetime import datetime
import math
import tkinter as Tkinter
from math import *
import time
import pytz
import json

#TO DO: Make clock image with relative size
#TO DO: Documentation
#TO DO: Fix for form red hand, so it moves

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
        self.extra_hand()
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
        self.hand = []
        for i in range(3):
            store=self.canvas.create_line(self.x, self.y,self.x+self.length,self.y+self.length,width=2, fill='black')
            self.hands.append(store)
        store=self.canvas.create_line(self.x, self.y,self.x+self.length,self.y+self.length,width=2, fill='red')
        self.hand.append(store)        
        return

    def extra_hand(self):
        pass


    # Function for updates
    def update_class(self):
        now=time.localtime()
        t = time.strptime(str(now.tm_hour), "%H")
        hour = int(time.strftime( "%I", t ))*5
        now=(hour,now.tm_min,now.tm_sec)
        #Home timezone
        home = datetime.now(pytz.timezone('Asia/Kolkata'))
        time_home = time.strptime(str(home.hour),"%H")
        hour_home = int(time.strftime( "%I", time_home ))*5
        clock_home = (hour_home,home.hour,home.second)
        # Changing hand Coordinates
        for n,i in enumerate(now):
            x,y=self.canvas.coords(self.hands[n])[0:2]
            cr=[x,y]
            cr.append(self.length*math.cos(math.radians(i*6)-math.radians(90))+self.x)
            cr.append(self.length*math.sin(math.radians(i*6)-math.radians(90))+self.y)
            self.canvas.coords(self.hands[n], tuple(cr))
        
        # for n,i in enumerate(clock_home):
        #     x,y=self.canvas.coords(self.hand[n])[0:2]
        #     cr=[x,y]
        #     cr.append(self.length*math.cos(math.radians(i*6)-math.radians(90))+self.x)
        #     cr.append(self.length*math.sin(math.radians(i*6)-math.radians(90))+self.y)
        #     self.canvas.coords(self.hand[n], tuple(cr))
        return

# Main Function Trigger
if __name__ == '__main__':
	root= Clock()

	# Creating Main Loop
	while True:
		root.update()
		root.update_idletasks()
		root.update_class()