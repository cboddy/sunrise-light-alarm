import threading
import datetime
import time

seconds_per_day  = 60*60*24

def getLight(deltaSeconds):
    deltaMinutes = deltaSeconds / 60
    red  =  1.0 - min(0, (deltaMinutes. - 50)/10)
    green = min(deltaMinutes - 10, 0)  
"""
    delta: number of seconds before alarm time
    generate r,g,b values based on alarm
"""
    pass




class Alarm(threading.Thread):
    def __init(self, timeOfDay, daysOfWeek, delay=10, getLight):
        self.timeOfDay = timeOfDay
        self.daysOfWeek = daysOfWeek
        self.delay = delay
        self.__isFinished = False
        
    def run(self):
        while not isFinished:
            time.sleep(delay)
            dt = datetime.datetime.now()
            if not dt.weekday() in self.daysOfWeek:
                continue

            delta =  self.timeOfDay - dt
            delta = delta.seconds  % seconds_per_day
            light = getLight(delta) 
            self.setLight(light)

    def setLight(self, light):
        pass

    def close(self):
        self.__isFinished = True
