from datetime import *
from tkinter import *
from math import sin , cos , pi

class Clock():
    def __init__(self, tz_home):
        self.tz_home = tz_home

    def get_time(self): #data da UTC -3
        current_time = datetime.now()
        print ("initial_date:\n", str(current_time))


teste1 = Clock(-3,5)
teste1.get_time()