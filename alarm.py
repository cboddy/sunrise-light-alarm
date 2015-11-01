import threading
import datetime
import time

seconds_per_minute  = 60
seconds_per_day  = seconds_per_minute*60*24
minutes_per_day  = seconds_per_day / 60 


class Alarm(threading.Thread):
    def __init(self, timeOfDay, daysOfWeek, wakeUpMinutes=30, graceMinutes=10,delay=10):
        self.timeOfDay = timeOfDay
        self.daysOfWeek = daysOfWeek
        self.delay = delay
        self.wakeUpMinutes = wakeUpMinutes
        self.graceMinutes = graceMinutes
        self.__isFinished = False

    """
        deltaMinutes: number of minutes before alarm time
        generate r,g,b values 
    """
    def  getLight(self, deltaMinutes):
        if minutes_per_day - deltaMinutes < self.graceMinutes:
            return 1.0,1.0,1.0
        if deltaMinutes > self.wakeUpMinutes:
            return None 
        ramp, full = self.wakeUpMinutes/3, self.wakeUpMinutes*4/5
        inverse_redness = max(0, deltaMinutes - ramp)
        red  =  1.0 - inverse_redness
        inverse_other = max(0, deltaMinutes -full)
        green =  blue =  1.0 - inverse_other
        return  red,green,blue
        
    def run(self):
        while not isFinished:
            time.sleep(delay)
            dt = datetime.datetime.now()
            if not dt.weekday() in self.daysOfWeek: continue

            delta =  self.timeOfDay - dt
            deltaMinutes = (delta.seconds  % seconds_per_day) / seconds_per_minute
            light = getLight(delta) 
            print("light", light)
            if light is not None: self.setLight(light)

    def setLight(self, light):
        pass

    def close(self):
        self.__isFinished = True
