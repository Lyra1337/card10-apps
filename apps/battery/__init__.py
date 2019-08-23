import math
import display
import leds
import utime
import os
import sys
import buttons

brightness = 10
disp = display.open()
while True:
    disp.clear()

    pressed = buttons.read(
        buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT
    )
    
    if pressed & buttons.BOTTOM_LEFT != 0:
        brightness = max(1, brightness - 3)
        utime.sleep_ms(10)

    if pressed & buttons.BOTTOM_RIGHT != 0:
        brightness = min(255, brightness + 3)
        utime.sleep_ms(10)

    minVoltage = 3.42
    # minVoltage = 3.9
    maxVoltage = 4.1
    voltage = os.read_battery()
    batteryPercent = (voltage - minVoltage) / (maxVoltage - minVoltage)
    batteryLevel = max(0, min(1, batteryPercent))
    disp.print("%fV  %f%%" % (voltage, batteryLevel * 100))

    lastIndex = round(batteryLevel * 11)

    # leds.clear()

    for i in range(0, lastIndex):
        leds.prep(10 - i, [0, brightness, 0])

    for i in range(lastIndex, 11):
        leds.prep(10 - i, [brightness, 0, 0])

    if batteryLevel == 1:
        leds.set_rocket(0, 31)
        leds.set_rocket(1, 31)
        leds.set_rocket(2, 31)
    else:
        leds.set_rocket(0, 0)
        leds.set_rocket(1, 0)
        leds.set_rocket(2, 0)

    leds.update()
    disp.update()
    utime.sleep_ms(10)
