import threading
import time, json, datetime

from dateutil import parser
#from ledstrip_bootstrap import *

seconds_per_minute  = 60
seconds_per_day  = seconds_per_minute*60*24
minutes_per_day  = seconds_per_day / 60 

class Alarm(threading.Thread):
    def __init__(self, timeOfDay, daysOfWeek, wakeUpMinutes=30, graceMinutes=10, delay=10):
        super(Alarm, self).__init__()
        
        self.timeOfDay = timeOfDay
        self.daysOfWeek = daysOfWeek
        self.delay = delay
        self.wakeUpMinutes = float(wakeUpMinutes)
        self.graceMinutes = graceMinutes
        self.setDaemon(True)
        #self.led = led
        self.__isFinished = False

    """
        deltaMinutes: number of minutes before alarm time
        generate r,g,b values 
    """
    def __str__(self):
        return str(self.dump())
    
    def  getLight(self, deltaMinutes):
        #print ("deltaMinutes", deltaMinutes, "wake-up mins ", self.wakeUpMinutes)
        if minutes_per_day - deltaMinutes < self.graceMinutes: return Color(255.0, 255.0, 255.0 , 1.0)
        if deltaMinutes > self.wakeUpMinutes: return None 
        level = 1.0 -   deltaMinutes / self.wakeUpMinutes
        red, green, blue = 255.0, 0.0, 255.0 * level 
        print(red,green, blue, self.wakeUpMinutes, deltaMinutes, level)
        return  Color(red,green,blue, level)
        
    def run(self):
        while not self.__isFinished:
            time.sleep(self.delay)
            now = datetime.datetime.now()

            #print("alarm loop @", now)
            if not now.weekday() in self.daysOfWeek: 
                #print("skipping since weekday", now.weekday(), "day-of-week not in ", self.daysOfWeek)
                continue

            delta =  self.timeOfDay - now 
            deltaMinutes = (delta.seconds  % seconds_per_day) / seconds_per_minute
            light = self.getLight(deltaMinutes) 
            print(now, "setting light", str(light))
            if light is not None: self.setLight(light)

    def setLight(self, color):
        self.led.fill(color)
        self.led.update()

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
                d["wakeUpMinutes"],
                d["grace"],
                d["delay"])

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
