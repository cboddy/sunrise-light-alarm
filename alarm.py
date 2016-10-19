"""An Alarm thread that periodically generates an r,g,b color value and
sets the ledstrip to that color"""

import threading
import time
import sys
import json
import datetime
import collections
from dateutil import parser
from ledstrip_bootstrap import *

SECONDS_PER_MINUTE = 60
SECONDS_PER_DAY = SECONDS_PER_MINUTE*60*24
MINUTES_PER_DAY = SECONDS_PER_DAY / 60

TimesOfWeek = collections.namedtuple("WeekTimes", ["time_of_day", "days_of_week"])

class Alarm(threading.Thread):
    
    def __init__(self, times_of_week=TimesOfWeek(datetime.datetime.now(), []), wake_up_minutes=30, grace_minutes=10, delay=10):
        super(Alarm, self).__init__()

        self._times_of_week = times_of_week
        self.delay = delay
        self.wake_up_minutes = float(wake_up_minutes)
        self.grace_minutes = grace_minutes
        self.setDaemon(True)
        self._is_finished = False
        self._lock = threading.Lock()

    @property
    def time_of_day(self):
        """the time of day at which the alarm is set"""
        return self.times_of_week.time_of_day

    @property
    def days_of_week(self):
        """the days of the week the alarm is set"""
        return self.times_of_week.days_of_week

    @property
    def is_finished(self):
        """guarded by self._lock
        is the thread finished
        """
        with self._lock:
            return self._is_finished

    @is_finished.setter
    def is_finished(self, is_finished):
        with self._lock:
            self._is_finished = is_finished

    @property
    def times_of_week(self):
        """guarded by self._lock
        return: self._times_of_week
        """
        with self._lock:
            return self._times_of_week

    @times_of_week.setter
    def times_of_week(self, times_of_week):
        with self._lock:
            self._times_of_week = times_of_week

    def get_color(self, delta_minutes):
        """
        args:
            delta_minutes: number of minutes before alarm time
        return:
            a Color
        """
        if MINUTES_PER_DAY - delta_minutes < self.grace_minutes:
            return Color(255.0, 255.0, 255.0, 1.0)
            #return None 
        if delta_minutes > self.wake_up_minutes: 
            return None 

        level = 1.0 -   delta_minutes / self.wake_up_minutes
        red, green, blue = 255.0, 0.0, 255.0 * level 
        print(red,green, blue, self.wake_up_minutes, delta_minutes, level)
        return Color(red, green, blue, level)
        #return None
    

    def run(self):
        while not self.is_finished:
            try:
                self.tick()
            except Exception as e:
                print(sys.exc_info()[0])
            finally:
                time.sleep(self.delay)

    def tick(self):
        """generates a color based on the system time (at method call time) and sets
        the ledstrip to that color"""
        now = datetime.datetime.now()
        if not now.weekday() in self.days_of_week: 
            return 
        delta = self.time_of_day - now 
        delta_minutes = (delta.seconds  % SECONDS_PER_DAY) / SECONDS_PER_MINUTE
        color = self.get_color(delta_minutes)
        print(now, "setting color", color)
        if color:
            led.fill(color)
            led.update()


    def __repr__(self):
        return json.dumps({"time": self.time_of_day.isoformat(),
                "weekdays": self.days_of_week,
                "delay": self.delay,
                "grace": self.grace_minutes,
                "wake_up_minutes": self.wake_up_minutes})

    def to_file(self, file_name):
        """serializes instance state
        args:
            file_name: local path where state will be written"""
        with open(file_name, "w") as f:
            f.write(repr(self))

    @staticmethod 
    def load(state_dict): 
        """de-serializes instance from dict
        args:
            state_dict: a dictionary with object state
        return:
            an Alarm object
        """
        times_of_week = TimesOfWeek(
            parser.parse(state_dict["time"]),
            state_dict["weekdays"])

        return Alarm(times_of_week,
            state_dict["wake_up_minutes"],
            state_dict["grace"],
            state_dict["delay"])

    @staticmethod
    def from_file(file_path):
        """args:
            file_path: a local path where a serialized Alarm object is stored
            return: a deserialized Alarm object
        """
        with open(file_path, "r") as f:
            state_dict = json.load(f)
            return Alarm.load(state_dict)

if __name__ == "__main__":
    import pdb; pdb.set_trace() 
    alarm = Alarm(TimesOfWeek(datetime.datetime.now(), [0, 1, 2, 3]))
    state_path = "alarm.state.json"
    alarm.to_file(state_path)
    state2 = Alarm.from_file(state_path)
    print("state2", state2)
    #alarm.start()
    print("alarm started")
    #time.sleep(100)
    alarm.is_finished = True
