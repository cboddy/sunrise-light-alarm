import threading
import time, json, datetime

from dateutil import parser
from ledstrip_bootstrap import *

seconds_per_minute  = 60
seconds_per_day  = seconds_per_minute*60*24
minutes_per_day  = seconds_per_day / 60 

class Alarm(threading.Thread):
    def __init__(self, timeOfDay, daysOfWeek, wakeUpMinutes=30, graceMinutes=10, delay=10):
        super(Alarm, self).__init__()
        
        self.timeOfDay = timeOfDay
        self.daysOfWeek = daysOfWeek
        self.delay = delay
        self.wakeUpMinutes = wakeUpMinutes
        self.graceMinutes = graceMinutes
        self.setDaemon(True)
        self.__isFinished = False
        self.led = led

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
        while not self.__isFinished:
            time.sleep(self.delay)
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

    def dump(self): 
        d = {
                "time": self.timeOfDay.isoformat(),
                "weekdays": self.daysOfWeek,
                "delay": self.delay,
                "grace": self.graceMinutes,
                "wakeUpMinutes": self.wakeUpMinutes} 
        return json.dumps(d)

    def toFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.dump())

    @staticmethod 
    def loads(s): 
        d = json.loads(s)
        return Alarm(parser.parse(d["time"]),
                d["weekdays"],
                d["delay"],
                d["grace"],
                d["wakeUpMinutes"])

    @staticmethod
    def fromFile(filename):
        with open(filename, "r") as f:
            return Alarm.loads(
                    reduce(lambda a,b: a+b, f.readlines()))

if __name__ == "__main__":
    state = Alarm(datetime.datetime.now(), [0,1,2,3])
    filename = "alarm.state.json"
    state.toFile(filename)
    state2 = Alarm.fromFile(filename)
    print("state2", state2.dump())
