import math
import display
import leds
import utime
import os
import sys
import buttons
import power

def update_leds(batteryLevel):
    lastIndex = round(batteryLevel * 11)

    for i in range(0, lastIndex):
        leds.prep(10 - i, [0, brightness, 0])

    for i in range(lastIndex, 11):
        leds.prep(10 - i, [brightness, 0, 0])

def update_rockets(batteryLevel):
    if batteryLevel == 1:
        leds.set_rocket(0, 31)
        leds.set_rocket(1, 31)
        leds.set_rocket(2, 31)
    else:
        leds.set_rocket(0, 0)
        leds.set_rocket(1, 0)
        leds.set_rocket(2, 0)

def display_logo():
    disp.clear()
    disp.print("Frankonian", fg = [ 255, 0, 0 ])
    disp.print("Village", fg = [ 255, 255, 255 ], posy = 60, posx = 60)
    disp.update()
    utime.sleep_ms(750)

brightness = 10
minVoltage = 3.42
# minVoltage = 3.9
maxVoltage = 4.1
disp = display.open()
mode = 0 # 0 = Voltage & Percentage | 1 = 
waitAfterUpdate = False

display_logo()

while True:
    disp.clear()

    pressed = buttons.read(
        buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT
    )
    
    if pressed & buttons.BOTTOM_LEFT != 0:
        brightness = max(0, brightness - 3)
        waitAfterUpdate = True

    if pressed & buttons.BOTTOM_RIGHT != 0:
        brightness = min(255, brightness + 3)
        waitAfterUpdate = True

    if pressed & buttons.TOP_RIGHT != 0:
        mode = mode + 1
        if mode > 2:
            mode = 0
        waitAfterUpdate = True
    
    voltage = os.read_battery()
    batteryPercent = (voltage - minVoltage) / (maxVoltage - minVoltage)
    batteryLevel = max(0, min(1, batteryPercent))

    if mode == 0:
        disp.print("Battery:")
        disp.print("%f%%" % (batteryLevel * 100), posy = 20)
        disp.print("%fV" % voltage, posy = 40, posx = 14)

    if mode == 1:
        chargeCurrent = power.read_chargein_current()
        chargeVoltage = power.read_chargein_voltage()
        disp.print("Charging:", posy = 0)
        if chargeCurrent < 0.01:
            disp.print("NEIN", posy = 20, fg = [255, 0, 0])
        else:
            disp.print("%fA" % chargeCurrent, posy = 20)
        disp.print("Voltage:", posy = 40)
        disp.print("%fV" % chargeVoltage, posy = 60)

    if mode == 2:
        batteryCurrent = power.read_battery_current()
        disp.print("Drawing:", posy = 0)
        disp.print("%fA" % batteryCurrent, posy = 20)
        
    update_leds(batteryLevel)
    update_rockets(batteryLevel)

    leds.update()
    disp.update()

    if waitAfterUpdate == True:
        waitAfterUpdate = False
        utime.sleep_ms(500)
    else:
        utime.sleep_ms(10)
