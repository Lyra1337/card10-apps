# Displays Blinkenlights Movies https://wiki.blinkenarea.org/index.php/Blinkenlights_Movie
# Just place some *.blm files (18x8 s/w) in the same folder as this script
#
# See https://stefan.blinkenarea.org/movies/18x8-1/
#
# Made by took at CCCamp2019
# Pick your favorite OSI license

import color, leds, buttons, display, os, utime, vibra, light_sensor
from urandom import choice, seed

frame = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()
    utime.sleep_ms(1200)

def draw_blinken_screen(size_x=18, size_y=8, left_margin=8, top_margin=5, pixel_width=5, pixel_height=7, pad_x=3,
                        pad_y=2, line_width=1):
    with display.open() as disp:
        disp.clear()
        for x in range(size_x):
            for y in range(size_y):
                if frame[y][x] > 0:
                    disp.rect(left_margin + (x * (pixel_width + pad_x)), top_margin + (y * (pixel_height + pad_y)),
                          left_margin + (x * (pixel_width + pad_x)) + pixel_width,
                          top_margin + (y * (pixel_height + pad_y)) + pixel_height, col=[255, 0, 255], filled=True,
                          size=line_width)
                #else:
                    #disp.rect(left_margin + (x * (pixel_width + pad_x)), top_margin + (y * (pixel_height + pad_y)),
                          #left_margin + (x * (pixel_width + pad_x)) + pixel_width,
                          #top_margin + (y * (pixel_height + pad_y)) + pixel_height, col=color.WHITE, filled=False,
                          #size=line_width)
        disp.update()
        disp.close()

def clear_frame(size_x=18, size_y=8):
    global frame
    for x in range(size_x):
        for y in range(size_y):
            frame[y][x] = 0

def play_blinken_blm_file(filename='12345.blm', size_x=18, size_y=8):
    global frame
    if filename not in os.listdir("."):
        render_error('file not', 'found')
    f = open(filename, 'r')
    frame_duration = 0
    frame_y = 0
    for row in f:
        if row[0] == "#":
            continue
        if row[0] == "@":
            #render_error('duration', row)
            frame_duration = int(row.replace("@", ""))
            clear_frame()
            frame_y = 0
            continue
        if len(row) > size_x:
            for x in range(size_x):
                #render_error('row', row)
                frame[frame_y][x] = int(row[x])
            frame_y = frame_y + 1
            if frame_y == size_y:
                #render_error('render', 'screen')
                draw_blinken_screen()
                utime.sleep_ms(frame_duration * 0.7)
                clear_frame()
                frame_y = 0
    f.close()

def play_all_files():
    files = os.listdir('.')
    for file in files:
        if (file[-4:] == '.blm'):
            render_error('file:', file[:-4])
            play_blinken_blm_file(file)

def play_all_files_random_order():
    files = os.listdir('.')
    # print(files)
    file = choice(files)
    if (file[-4:] == '.blm'):
        #vibra.vibrate(60)
        render_error('file:', file[:-4])
        play_blinken_blm_file(file)

#render_error('hello', 'world')
seed(light_sensor.get_reading())
while True:
    play_all_files_random_order()
    # play_blinken_blm_file("ask_for_bombs.blm")