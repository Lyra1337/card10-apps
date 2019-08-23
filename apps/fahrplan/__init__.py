import os
import buttons
import utime
import display
import ujson
import color
import leds

DIR = "apps/fahrplan"
FILENAME = "schedule.json"
MAXCHARS = 11


def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


def draw_event(event, disp, offset, daysCount):
    disp.clear()
    disp.rect(0, 0, 159, 20, col=color.CHAOSBLUE) 
    disp.rect(0, 20, 159, 80, col=color.CHAOSBLUE)

    for i in range(daysCount):
        if i == int(event["day"]) - 1:
            leds.set(10-i, [0, 255, 0])
        else:
            leds.set(10-i, [255, 0, 0])

    title = event['title'] + " -- "
    linelen = len(title)
    offset %= linelen
    post_title = ""
    if offset + MAXCHARS > linelen:
        post_title = title[:(offset + MAXCHARS - linelen)]
    disp.print(title[offset: offset + MAXCHARS] + post_title, posy=0, fg=color.CAMPGREEN, bg=color.CHAOSBLUE)

    disp.print("D " + event["day"] + " - " + event['start'], posy=20, bg=color.CHAOSBLUE)
    disp.print(event['room'], posy=40, bg=color.CHAOSBLUE)

    e_duration = event["duration"]
    duration = ""
    if e_duration[0] != '0':
        duration += e_duration[0:2] + "h"
    elif e_duration[1] != '0':
        duration += e_duration[1] + "h"

    if e_duration[3] != '0':
        duration += e_duration[3:5] + "m"
    elif e_duration[4] != '0':
        duration += e_duration[4] + "m"


    disp.print(duration + " long", posy=60, bg=color.CHAOSBLUE)
    disp.update()


def process_json(f):
    try:
        conf = ujson.loads(f.read())
        events = conf["events"]
        daysCount = conf["daysCount"]
    except Exception as e:
        return None

    events = sorted(events, key=lambda e: e['timestamp'])
    return events, daysCount


def compute_next_event_nb(event_list):
    t = utime.time()
    i = 0
    max_len = len(event_list)
    while i < max_len and event_list[i]["timestamp"] < t:
        i += 1
    if i == max_len:
        i -= 1
    return i


print("Start")
if FILENAME not in os.listdir(DIR):
    render_error('file not', 'found')
    print("File not found")
else:
    leds.dim_top(1)
    events = None
    with open(DIR + "/" + FILENAME) as f:
        events, daysCount = process_json(f)
    if not events:
        render_error('error prossessing', 'events')
        print("Error processing events")
    else:
        event_nb = compute_next_event_nb(events)
        len_events = len(events)

        i = -7
        offset = 0
        disp = display.open()

        while 1:
            draw_event(events[event_nb], disp, offset, daysCount)
            i += 1
            if i >= 4:
                offset += 1
                i = 0

            # Process button event
            v = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)
            if v == 0:
                button_pressed = False

            if not button_pressed and v & buttons.BOTTOM_LEFT != 0:
                button_pressed = True
                event_nb -= 1
                if event_nb < 0:
                    event_nb = 0
                offset = 0
                i = -7

            if not button_pressed and v & buttons.BOTTOM_RIGHT != 0:
                button_pressed = True
                event_nb += 1
                if event_nb >= len_events:
                    event_nb = len_events - 1
                offset = 0
                i = -7

            if not button_pressed and v & buttons.TOP_RIGHT != 0:
                button_pressed = True
                event_nb = compute_next_event_nb(events)
                offset = 0
                i = -7

            utime.sleep_ms(10)
