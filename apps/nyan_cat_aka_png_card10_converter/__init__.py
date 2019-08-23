import color
import display
import utime

from apps.nyan_cat.nyan import NYAN

x_position = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
y_shift = 20

def create_color(r, g, b):
    c = color.Color(r, g, b)
    return c

def set_pixel(disp, x, y, c):
    return disp.pixel(x, y, col=c)

def main():
    while True:
        disp = display.open()
        disp.clear().update()
        init = True
        for pos in range(len(x_position)):
            for pixel_str in NYAN:
                # x,y,r,g,b
                x,y,r,g,b = pixel_str.split(',')
                x = int(x) + x_position[pos]
                y = int(y) + y_shift
                r = int(r)
                g = int(g)
                b = int(b)
                pix_color = create_color(r,g,b)
                set_pixel(disp, x, y, pix_color)
                # creates line-by-line rendering (kind of cool)
                if init:
                    disp.update()
                    init = False
            # put disp.update() here to render all at once
            disp.update()
            utime.sleep(5)
        disp.close()


main()
