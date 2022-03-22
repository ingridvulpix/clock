from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
import math
import pytz
import time

#Measure for clock image and font size for messages
WIDTH           = 300
HEIGHT          = 300
FONT_SIZE       = 7

#clock image is a square covering the width
IMG_SIZE            = (WIDTH,HEIGHT)
ARROW_MIN_SIZE      = IMG_SIZE[1] - IMG_SIZE[1]*0.6
ARROW_HOUR_SIZE     = IMG_SIZE[1] - IMG_SIZE[1]*0.8

#Home and Local Timezones
home_town = 'America/Bahia'
local_tz = 'Asia/Tokyo'

#Image file and end_prog for continuing or stopping program
image = Image.open("24h_clock.jpg")
end_prog = False


# Clock class implementation
# Draws a clock with home hour, local hour, minute, seconds arrows
# acording to self timezone (region and work_region)
#
class Clock:
    ## Constructor.
    #
    # @param region home timezone.
    # @param work_region local_tz.
    # @param pos clock position.
    # @param x x-axis coordinate
    # @param y y-axis coordinate
    #
    def __init__(self,region=home_town,work_region = local_tz,pos=[0,0],x=0,y=0):
        """Constructor"""
        
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
    
    # Adds a clock in the center of the canvas
    #
    def add_clock(self):
        pos = [0,0]
        pos[0] = self.x
        pos[1] = self.y
        clk = Clock(self.region,self.work_region,pos)
        self.grid.append(clk)

    # Draws a clock in canvas
    #
    def draw_clocks(self,canvas):
        for clk in self.grid:
            clk.draw_me(canvas)

    # Updates clock with time passage
    #
    def update_clock(self,canvas):
        for clk in self.grid:
            if not (clk.seconds()%60):
                clk.draw_minutes(canvas)
                clk.draw_hours(canvas)
            clk.draw_seconds(canvas)

    # Calculate and return the seconds from time zone
    #
    def seconds(self):
        """Returns the seconds from time zone"""
        return datetime.now(pytz.timezone(self.region)).second

    # Calculate and return the minutes from time zone
    #
    def minutes(self):
        """Returns the minutes from time zone"""
        return datetime.now(pytz.timezone(self.region)).minute

    # Calculate and return the hour from home time zone
    #
    def hours(self):
        """Returns the hours from home time zone"""
        return datetime.now(pytz.timezone(self.region)).hour

    # Calculate and return the hour from local time zone
    #
    def hour_local(self):
        """Returns the hours from the current time zone"""
        return datetime.now(pytz.timezone(self.work_region)).hour

    # Draw the seconds hand in shape of arrow
    #
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

    # Draw the minutes hand in shape of arrow
    #
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

    # Draw the home hour hand in shape of arrow
    #
    def draw_hours(self,canvas):
        """ draw the hours arrows"""
        if canvas:
            canvas.delete(self.line_hour_id)
            #get hours arrow angle
            m = self.minutes()
            h = self.hours()

            #add minutes factor influance on the hour angle
            angle = -math.pi/2 + 2*math.pi*(h%24)/24 + 2*math.pi*m/24/60
            x0 = self.pos[0]+IMG_SIZE[0]//2
            y0 = self.pos[1]+IMG_SIZE[1]//2
            x1 = x0 +ARROW_HOUR_SIZE*math.cos(angle)
            y1 = y0 +ARROW_HOUR_SIZE*math.sin(angle)
            #draw hours arow
            self.line_hour_id = canvas.create_line(x0,y0,x1,y1, arrow=tk.LAST,arrowshape=(20,10,2))
            canvas.pack()

    # Draw the (local) hour hand in shape of arrow
    #
    def draw_localh(self,canvas):
        """ draw the hours arrows from local region"""
        if canvas:
            canvas.delete(self.line_local_hour_id)
            #get hours arrow angle
            m = self.minutes()
            h_local = self.hour_local()

            #add minutes factor influance on the hour angle
            angle = -math.pi/2 + 2*math.pi*(h_local%24)/24 + 2*math.pi*m/24/60
            x0 = self.pos[0]+IMG_SIZE[0]//2
            y0 = self.pos[1]+IMG_SIZE[1]//2
            x1 = x0 +ARROW_HOUR_SIZE*math.cos(angle)
            y1 = y0 +ARROW_HOUR_SIZE*math.sin(angle)
            #draw hours arow
            self.line_local_hour_id = canvas.create_line(x0,y0,x1,y1, arrow=tk.LAST,arrowshape=(15,10,2), fill = 'red')
            canvas.pack()

    # Returns a string with de time for the digital clock
    #
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

    # Draw the components (clock, sticks, timezone, digital clock)
    # in canvas
    #
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

        canvas.create_text(x0,y0-20,fill="Black",font="Calibri " + str(FONT_SIZE+1)+" italic bold",text=self.region)
        canvas.create_text(x0,y0-10,fill="Red",font="Calibri " + str(FONT_SIZE)+" italic bold",text=self.work_region)

        digtime = self.digital_time_str()
        canvas.create_text(x0,y0+20,fill="Black",font="Calibri 20 italic bold",text=digtime)
        canvas.pack()

# Stops the program
#
def quit():
    global end_prog
    end_prog = True
    quit()


# Main function
#
def main():
    global image,photo,end_prog

    try :
        clk_display = Clock()
        clk_display.add_clock()
        top = tk.Tk()
        top.title("AD1- Ingrid de Almeida")
        canvas = tk.Canvas(top, bg="silver", height=HEIGHT, width=WIDTH)



        image = image.resize((IMG_SIZE[0],IMG_SIZE[1]+10))
        photo = ImageTk.PhotoImage(image)

        clk_display.draw_clocks(canvas)
        while not end_prog:
            top.update()
            clk_display.update_clock(canvas)
            time.sleep(1)
        top.mainloop()
    finally:
        end_prog = True
        print("I am in finally")

if __name__=='__main__':
    main()