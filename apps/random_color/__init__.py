import math
import leds
import utime
import os

while True:
    # leds.set_all(os.urandom(3))

    for i in range(0, 11):
        leds.prep(i, os.urandom(3))

    leds.update()
    utime.sleep_ms(5)