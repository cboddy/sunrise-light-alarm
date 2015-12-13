import time
import wiringpi2 as wiringpi
"""
Based on examples at https://www.piborg.org/ledborg
"""

# Setup software PWMs on the GPIO pins
PIN_RED = 0
PIN_GREEN = 2
PIN_BLUE = 3
LED_MAX = 255 

wiringpi.wiringPiSetup()

for pin in [PIN_RED, PIN_BLUE, PIN_GREEN]:
    wiringpi.softPwmCreate(pin, 0, LED_MAX)
    wiringpi.softPwmWrite(pin,   0)

"""
(red, green, blue) take float values between 0 and 1
"""
def setLight(red, green, blue): 
    for pin, value in {PIN_RED: red, PIN_GREEN: green,  PIN_BLUE: blue}.iteritems(): 
        wiringpi.softPwmWrite(pin, int(value  * LED_MAX))


if __name__ == "__main__":
    setLight(1,0,0)
    time.sleep(10)
    setLight(0,1,0)
    time.sleep(10)
    setLight(1,0,1)
    time.sleep(10)

