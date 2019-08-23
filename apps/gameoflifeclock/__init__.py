# Adapted from https://github.com/muccc/flipdots/blob/master/scripts/clock.py
import display
from utime import sleep
import utime
import urandom
import math
import leds

class Time:
    def __init__(self, start = 0):
        self.time = start
        self.wait_time = 0.95

    def tick(self):
        sleep(self.wait_time)
        self.time += 1

    @property
    def second(self):
        return self.time % 60

    @property
    def minute(self):
        return (self.time / 60) % 60

    @property
    def hour(self):
        return (self.time / 3600) % 24

class Clock:
    def __init__(self, sizex = 80, sizey = 80, radius = 38, offsetx = 30,
            hour_hand = True, minute_hand = True, second_hand = True, console_out = False,
            run_once = False, update_interval = 0):
        self.sizex = sizex
        self.sizey = sizey
        self.radius = radius
        self.center = (int(self.sizex/2), int(self.sizey/2))
        self.hour_hand = hour_hand
        self.minute_hand = minute_hand
        self.second_hand = second_hand
        self.console_out = console_out
        self.update_interval = update_interval if update_interval != 0 else (1 if self.second_hand else 30)
        self.run_once = run_once
        self.offsetx = offsetx
        self.time = Time()
        white = (255, 255, 255)
        self.center_col = white
        self.m1_col = white
        self.m5_col = white
        self.hour_hand_col = white
        self.minute_hand_col = white
        self.second_hand_col = white
        self.warp = 0

        self.sx=160
        self.sy=80
        self.f=[]
        self.nxt=[]
        for x in range(self.sx):
            self.f.append([])
            self.nxt.append([])
            for y in range(self.sy):
                self.f[x].append(urandom.randint(0,1))
                self.nxt[x].append(0)

    def show(self,disp):
        for x in range(self.sx):
            for y in range(self.sy):
                if(self.f[x][y]):
                    disp.pixel(x,y,col=(255,0,0))
                
    def neigh(self,x,y):
        return self.f[x-1][y-1]+self.f[x][y-1]+self.f[x+1][y-1]+self.f[x-1][y]+self.f[x+1][y]+self.f[x-1][y+1]+self.f[x][y+1]+self.f[x+1][y+1]

    def future(self,x,y):
        f = self.neigh(x,y)
        if f == 3 or (f==2 and self.f[x][y]==1):
            return 1
        return 0
    
    def iter(self):
        for x in range(1,self.sx-1):
            for y in range(1,self.sy-1):
                self.nxt[x][y]=self.future(x,y)
        for x in range(0,self.sx):
            for y in range(0,self.sy):
                self.f[x][y]=self.nxt[x][y]


        
    def loop(self):
        colored = False
        try:
            with display.open() as disp:
                while True:
                    self.updateClock(disp)
                    if self.run_once:
                        break
        except KeyboardInterrupt:
            for i in range(11):
                leds.set(i, (0, 0, 0))
            return

    def drawImage(self, image):
        with display.open() as d:
            d.clear()
            for x in range(len(image)):
                for y in range(len(image[x])):
                    d.pixel(x + self.offsetx, y, col = (255, 255, 255) if image[x][y] else (0, 0, 0))
            d.update()

    def updateClock(self, disp):
        disp.clear()
        localtime = utime.localtime()
        self.warp = self.warp + 1

        self.iter()
        self.show(disp)
        
        disp.pixel(self.center[0] + self.offsetx, self.center[1], col = self.center_col)
        hour_coords = self.circlePoint(math.radians((((localtime[3]%12)/12.) if localtime[3] else 0)*360 + 270 + (localtime[4]/2)))
        minute_coords = self.circlePoint(math.radians(localtime[4]*6+270))
        second_coords = self.circlePoint(math.radians(localtime[5]*6+270))

        for i in range(60):
            degree = i*6 + 90
            radian = - math.radians(degree)
            coords = self.circlePoint(radian)

            if not i % 5:
                self.addLine(disp, coords, self.center, 3, 1, col = self.m5_col)
            else:
                self.addLine(disp, coords, self.center, 1, col = self.m1_col)

        if self.hour_hand:
            self.addLine(disp, self.center, hour_coords, int(self.radius / 3), 1, col = self.hour_hand_col)
        if self.minute_hand:
            self.addLine(disp, self.center, minute_coords, int(self.radius / 2), col = self.minute_hand_col)
        if self.second_hand:
            self.addLine(disp, self.center, second_coords, self.radius - int(self.radius/8.), col = self.second_hand_col)

        if self.console_out:
            for y in range(self.radius*2):
                line = ""
                for x in range(self.radius*2):
                    line = line + ("." if image[(self.center[1]-self.radius)+y][(self.center[0]-self.radius)+x] else " ")
                print(line)

        disp.update()

    def circlePoint(self, t):
        return (int(round(self.radius*math.cos(t))) + self.center[0], int(round(self.radius*math.sin(t))) + self.center[1])

    def addLine(self, disp, source, aim, length, thickness = 1, col = (255, 255, 255)):
        vector = self.subVector(aim, source)
        vector = self.normVector(vector)
        destination = self.addVector(source, self.multiplyVector(vector, length))

        disp.line(round(source[0]) + self.offsetx, round(source[1]), round(destination[0]) + self.offsetx, round(destination[1]), col=col, size=thickness)

    def normVector(self, v):
        length = math.sqrt(sum([i**2 for i in v]))
        new_v = []
        for i in range(len(v)):
            new_v.append(v[i]/length)
        return tuple(new_v)

    def subVector(self, v1, v2):
        res = []
        for i in range(len(v1)):
            res.append(v1[i]-v2[i])
        return tuple(res)

    def addVector(self, v1, v2):
        res = []
        for i in range(len(v1)):
            res.append(v1[i]+v2[i])
        return tuple(res)

    def multiplyVector(self, v, multiplier):
        return tuple([i*multiplier for i in v])

clock = Clock()
clock.loop()