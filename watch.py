from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
import math
import pytz
import time

class Watch:
    def __init__(self, main_region, sub_region, windown):
        self.main_region = main_region
        self.sub_region = sub_region
        self.arrow_min = 120
        self.arrow_hour = 60
        self.line_sec = 0
        self.line_min = 0
        self.line_hour = 0
        self.line_hour_sub = 0
        self.windown = windown

    def windown_setting(self):
        self.windown.title("AD1- Ingrid de Almeida")
        self.canvas = tk.Canvas(self.windown, bg="silver", height=300, width=300)
        return self.windown

    def resize_image(self):
        image = Image.open("24h_clock.jpg")
        self.width = 300
        self.height = 310
        self.x0 = self.width//2
        self.y0 = self.height//2
        image = image.resize((self.width,self.height))
        self.image = ImageTk.PhotoImage(image)
    
    def seconds(self):
        """Returns the seconds from time zone"""
        return datetime.now(pytz.timezone(self.main_region)).second

    def minutes(self):
        """Returns the minutes from time zone"""
        return datetime.now(pytz.timezone(self.main_region)).minute

    def hours(self):
        """Returns the hours from home time zone"""
        return datetime.now(pytz.timezone(self.main_region)).hour

    def hour_local(self):
        """Returns the hours from the current time zone"""
        return datetime.now(pytz.timezone(self.sub_region)).hour

    def draw_seconds(self):
        """Draw the seconds hand"""

        self.canvas.delete(self.line_sec)
        s  = self.seconds()
        angle = - math.pi/2 + 2*math.pi*s/60
        x1 = self.x0 + self.arrow_min*math.cos(angle)
        y1 = self.y0 + self.arrow_min*math.sin(angle)
        self.line_sec = self.canvas.create_line(self.x0,self.y0,x1,y1)
        self.canvas.pack()

    def draw_minutes(self):
        """ Draw the minutes arrows"""

        self.canvas.delete(self.line_min)
        #get minutes arrow angle
        m = self.minutes()
        #-pi/2 is 12 oclock angle
        angle = -math.pi/2 + 2*math.pi*m/120
        x1 = self.x0 + self.arrow_min*math.cos(angle)
        y1 = self.y0 + self.arrow_min*math.sin(angle)
        #draw minutes arrow
        self.line_min = self.canvas.create_line(self.x0,self.y0,x1,y1, arrow=tk.LAST,arrowshape=(20,10,2))
        self.canvas.pack()

    def draw_hours(self):
        """ Draw the hours arrows"""

        self.canvas.delete(self.line_hour)
        #get hours arrow angle
        m = self.minutes()
        h = self.hours()

        #add minutes factor influance on the hour angle
        angle = -math.pi/2 + 2*math.pi*(h%24)/24 + 2*math.pi*m/24/60
        x1 = self.x0 + self.arrow_hour*math.cos(angle)
        y1 = self.y0 + self.arrow_hour*math.sin(angle)
        #draw hours arow
        self.line_hour = self.canvas.create_line(self.x0,self.y0,x1,y1, arrow=tk.LAST,arrowshape=(20,10,2))
        self.canvas.pack()

    def draw_localh(self,):
        """ Draw the hours arrows from local region"""
        self.canvas.delete(self.line_hour_sub)
        #get hours arrow angle
        m = self.minutes()
        h_local = self.hour_local()

        #add minutes factor influance on the hour angle
        angle = -math.pi/2 + 2*math.pi*(h_local%24)/24 + 2*math.pi*m/24/60
        x1 = self.x0 + self.arrow_hour*math.cos(angle)
        y1 = self.y0 + self.arrow_hour*math.sin(angle)
        #draw hours arow
        self.line_hour_sub = self.canvas.create_line(self.x0,self.y0,x1,y1, arrow=tk.LAST,arrowshape=(15,10,2), fill = 'red')
        self.canvas.pack()

    def drawn_me(self):
        """Draw the components (clock, sticks, timezone, digital clock) in canvas"""
        
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')
        self.draw_minutes()
        self.draw_hours()
        self.draw_seconds()
        self.draw_localh()

        self.canvas.create_text(self.x0,self.y0-20,fill="Black",font="Calibri 8 italic bold",text=self.main_region)
        self.canvas.create_text(self.x0,self.y0-10,fill="Red",font="Calibri 7 italic bold",text=self.sub_region)

        self.canvas.pack()

    def updater(self):
        self.resize_image()
        self.drawn_me()
        self.draw_minutes()
        self.draw_hours()
        self.draw_seconds()
    

    
def main():
    main_region = 'America/Bahia'
    sub_region = 'Asia/Tokyo'

    windown = tk.Tk()
    watch_engine = Watch(main_region,sub_region,windown)
    windown = watch_engine.windown_setting()
    watch_engine.resize_image()

    while True:
        windown.update()
        watch_engine.updater()
        time.sleep(1)
    windown.mainloop()

if __name__=='__main__':
    main()
