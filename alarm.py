import threading
import datetime
import time
class Alarm(threading.Thread):
    def __init(self, timeOfDay, daysOfWeek, delay=10):
        self.timeOfDay = timeOfDay
        self.daysOfWeek = daysOfWeek
        self.delay = delay
        self.isFinished = False
        
    def run(self):
        while not isFinished:
            time.sleep(delay)
            dt = datetime.datetime.now()
            light = getLight(dt) 
            setLight(light)

    def setLight(self, light):
        pass

    def getLight(self, dateTime):
        pass

    def close(self):
        self.isFinished = True
