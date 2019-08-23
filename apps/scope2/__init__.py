import os
import display
import utime
import buttons
import light_sensor
import math

WIDTH=160
HEIGHT=80

disp = display.open()

light_sensor.start()

history = []

while True:
    disp.clear()
    
    value = light_sensor.get_reading()
    
    history.insert(0, value)
    if len(history) > WIDTH:
        history.pop()

    blueColor = (int)(255 * (value / max(history)))
    redColor = (int)(255 * (1 - value / max(history)))

    disp.print("%i"%value, fg = [redColor, 0, blueColor])

    isFirstMax = True
    for i in range(0, len(history)):
        currentVal = history[i]
        historyMin = min(history)
        y = math.floor(HEIGHT * ((currentVal - historyMin) / (1 + max(history) - historyMin)))
        
        actualHeight = HEIGHT - y - 1

        blueColor = (int)(255 * (1 - actualHeight / HEIGHT))
        redColor = (int)(255 * (actualHeight / HEIGHT))
        rgb = [redColor, 0, blueColor]
        disp.pixel(WIDTH-i, actualHeight, col = rgb)

        if currentVal == max(history) and isFirstMax == True:
            isFirstMax = False
            disp.print("%i"%currentVal, posx = min(WIDTH - i, WIDTH - 40), posy = actualHeight + 10)
    
    disp.update()
    utime.sleep(0.1)