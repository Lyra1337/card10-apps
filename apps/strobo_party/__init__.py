import os
import leds
import utime
import color
import buttons
import display
import urandom

def calcBPMFromFrequency(frequency):
    return frequency * 60

def frequencyFromBPM(bpm):
    return bpm / 60

def sleepIntervalFromBPM(bpm):
    return 1000 / frequencyFromBPM(bpm) / 2
  
def setRandomLEDColor(clr):
    leds.set_all([clr,clr,clr,clr,clr,clr,clr,clr,clr,clr,clr])
    
def main(): 
    clr = color.WHITE
    print("main")
    leds.set_all([clr,clr,clr,clr,clr,clr,clr,clr,clr,clr,clr])
    switch = False
    bpm = 120
    
    sleep_t = sleepIntervalFromBPM(bpm)
    print(str(sleep_t) + " ms")
    disp = display.open()
    disp.clear()
    while True:
        if(switch):
            leds.dim_top(0)
            switch = False
        else:
            leds.dim_top(8)
            switch=True 
        pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)
    
        if pressed & buttons.BOTTOM_LEFT != 0:
            bpm -= 10
    
        if pressed & buttons.BOTTOM_RIGHT != 0:
            bpm += 10

        if pressed & buttons.TOP_RIGHT != 0:
           r = urandom.randint(0,255)
           g = urandom.randint(0,255)
           b = urandom.randint(0,255)
           clr = color.Color(r,g,b)
           leds.dim_top(8)
           setRandomLEDColor(clr)
           switch = False

        bpm_str = str(bpm) + " BPM"
        sleep_t = sleepIntervalFromBPM(bpm)
        xOffset = int(round((len(bpm_str) * 20) / 2))
        if(switch):
            disp.clear([clr.red,clr.green,clr.blue])
            disp.print(bpm_str, fg=color.BLACK, bg= clr, posx=90-xOffset, posy = 40 - 20)
        else:
            disp.clear([0,0,0])
            disp.print(bpm_str, fg=color.WHITE, bg= color.BLACK, posx=90-xOffset, posy = 40 - 20)
        disp.update()
        utime.sleep_ms(int(round(sleep_t)))
main()
