from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
import math
import pytz
import time


WIDTH           = 300
HEIGHT          = 300
FONT_SIZE       = 7

#clock image is a square covering the width
IMG_SIZE            = (WIDTH,HEIGHT)
ARROW_MIN_SIZE      = IMG_SIZE[1] - IMG_SIZE[1]*0.6
ARROW_HOUR_SIZE     = IMG_SIZE[1] - IMG_SIZE[1]*0.8

home_town = 'America/Bahia'
local_tz = 'America/Toronto'

image = Image.open("white_clock.jpg")
end_prog = False

class Clock:
    """
    Clock class implementation
    Draws a clock with hour & minute arrows
    acording to self timezone
    """

    def __init__(self,region=home_town,work_region = local_tz,pos=[0,0],x=0,y=0):
        self.grid = []
        self.region = region
        self.work_region = work_region
        self.line_sec_id=0
        self.line_min_id=0
        self.line_hour_id=0
        self.line_local_hour_id=0
        self.x = x
        self.y = y
        self.pos = list(pos)

    def add_clock(self,region,local_region,indx):
        pos = [0,0]
        pos[0] = self.x+IMG_SIZE[0]*indx
        pos[1] = self.y
        clk = Clock(region,local_region,pos)
        self.grid.append(clk)

    def draw_clocks(self,canvas):
        for clk in self.grid:
            clk.draw_me(canvas)

    def update_clocks(self,canvas):
        for clk in self.grid:
            if not (clk.seconds()%60):
                clk.draw_minutes(canvas)
                clk.draw_hours(canvas)
            clk.draw_seconds(canvas)

    def seconds(self):
        """Returns the minutes from the current time zone"""
        return datetime.now(pytz.timezone(self.region)).second

    def minutes(self):
        """Returns the minutes from the current time zone"""
        return datetime.now(pytz.timezone(self.region)).minute

    def hours(self):
        """Returns the hours from home time zone"""
        return datetime.now(pytz.timezone(self.region)).hour

    def hour_local(self):
        """Returns the hours from the current time zone"""
        return datetime.now(pytz.timezone(self.work_region)).hour


    def draw_seconds(self,canvas):
        if canvas:
            canvas.delete(self.line_sec_id)
            x0 = self.pos[0]+IMG_SIZE[0]//2
            y0 = self.pos[1]+IMG_SIZE[1]//2
            s  = self.seconds()
            angle = -math.pi/2 + 2*math.pi*s/60
            x1 = x0 +ARROW_MIN_SIZE*math.cos(angle)
            y1 = y0 +ARROW_MIN_SIZE*math.sin(angle)
            self.line_sec_id=canvas.create_line(x0,y0,x1,y1)
            canvas.pack()


    def draw_minutes(self,canvas):
        """ draw the minutes arrows"""
        if canvas:
            canvas.delete(self.line_min_id)
            #get minutes arrow angle
            m = self.minutes()
            #-pi/2 is 12 oclock angle
            angle = -math.pi/2 + 2*math.pi*m/60
            x0 = self.pos[0]+IMG_SIZE[0]//2
            y0 = self.pos[1]+IMG_SIZE[1]//2
            x1 = x0 +ARROW_MIN_SIZE*math.cos(angle)
            y1 = y0 +ARROW_MIN_SIZE*math.sin(angle)
            #draw minutes arrow
            self.line_min_id = canvas.create_line(x0,y0,x1,y1, arrow=tk.LAST,arrowshape=(20,10,2))
            canvas.pack()

    def draw_hours(self,canvas):
        """ draw the hours arrows"""
        if canvas:
            canvas.delete(self.line_hour_id)
            #get hours arrow angle
            m = self.minutes()
            h = self.hours()

            #add minutes factor influance on the hour angle
            angle = -math.pi/2 + 2*math.pi*(h%12)/12 + 2*math.pi*m/12/60
            x0 = self.pos[0]+IMG_SIZE[0]//2
            y0 = self.pos[1]+IMG_SIZE[1]//2
            x1 = x0 +ARROW_HOUR_SIZE*math.cos(angle)
            y1 = y0 +ARROW_HOUR_SIZE*math.sin(angle)
            #draw hours arow
            self.line_hour_id = canvas.create_line(x0,y0,x1,y1, arrow=tk.LAST,arrowshape=(20,10,2))
            canvas.pack()

    def draw_localh(self,canvas):
        """ draw the hours arrows from local region"""
        if canvas:
            canvas.delete(self.line_local_hour_id)
            #get hours arrow angle
            m = self.minutes()
            h_local = self.hour_local()

            #add minutes factor influance on the hour angle
            angle = -math.pi/2 + 2*math.pi*(h_local%12)/12 + 2*math.pi*m/12/60
            x0 = self.pos[0]+IMG_SIZE[0]//2
            y0 = self.pos[1]+IMG_SIZE[1]//2
            x1 = x0 +ARROW_HOUR_SIZE*math.cos(angle)
            y1 = y0 +ARROW_HOUR_SIZE*math.sin(angle)
            #draw hours arow
            self.line_local_hour_id = canvas.create_line(x0,y0,x1,y1, arrow=tk.LAST,arrowshape=(15,10,2), fill = 'red')
            canvas.pack()

    def digital_time_str(self):
        """ returns hours & minutesstring hh:mm """

        m = self.minutes()
        h = self.hours()
        m_str = str(m)
        h_str = str(h)
        if m < 10:
            m_str = "0" + str(m)
        if h < 10:
            h_str = "0" + str(h)

        return h_str + ":" + m_str

    def draw_me(self,canvas):
        canvas.create_image(self.pos[0], self.pos[1], image=photo, anchor='nw')

        self.draw_minutes(canvas)
        self.draw_hours(canvas)
        self.draw_seconds(canvas)
        self.draw_localh(canvas)
        m = self.minutes()
        h = self.hours()
        h_local = self.hour_local()

        x0 = self.pos[0]+IMG_SIZE[0]//2
        y0 = self.pos[1]+IMG_SIZE[1]//2

        canvas.create_text(x0,y0-30,fill="Black",font="Calibri " + str(FONT_SIZE+1)+" italic bold",text=self.region)
        canvas.create_text(x0,y0-20,fill="Red",font="Calibri " + str(FONT_SIZE)+" italic bold",text=self.work_region)

        digtime = self.digital_time_str()
        canvas.create_text(x0,y0+20,fill="Black",font="Calibri 20 italic bold",text=digtime)
        canvas.pack()


def quit():
    global end_prog
    end_prog = True
    quit()



def main():
    global image,photo,end_prog

    try :
        clk_display = Clock()
        clk_display.add_clock(home_town,local_tz,0)
        top = tk.Tk()
        top.title("AD1- Ingrid de Almeida")
        canvas = tk.Canvas(top, bg="silver", height=HEIGHT, width=WIDTH)



        image = image.resize((IMG_SIZE[0],IMG_SIZE[1]+10))
        photo = ImageTk.PhotoImage(image)

        clk_display.draw_clocks(canvas)
        while not end_prog:
            top.update()
            clk_display.update_clocks(canvas)
            time.sleep(1)
        top.mainloop()
    finally:
        end_prog = True
        print("I am in finally")

if __name__=='__main__':
    main()