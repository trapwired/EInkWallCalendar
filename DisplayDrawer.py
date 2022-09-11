#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import sys
import os


DEBUG = False

if not DEBUG:
    from waveshare_epd import epd7in5_V2

import logging
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
import traceback


# picdir = ""
libdir = ""

offset_days_y = 35
offset_days_x = 160

cal_event_height = 50
pad_cal_event = 2

font24 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 24)
font22 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 22)
font20 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 20)
font18 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 18)
font14 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 14)
emojiFont = ImageFont.truetype(os.path.join('res', 'Symbola.ttf'), 14)
emojiFontL = ImageFont.truetype(os.path.join('res', 'Symbola.ttf'), 22)

lengths = {'a': 11, 'b': 10, 'c': 13, 'd': 10, 'e': 11, 'f': 18, 'g': 11, 'h': 10, 'i': 25, 'j': 25, 'k': 12, 'l': 25,
           'm': 6, 'n': 10, 'o': 10, 'p': 10, 'q': 10, 'r': 14, 's': 13, 't': 18, 'u': 10, 'v': 12, 'w': 8, 'x': 12,
           'y': 12, 'z': 13, ' ': 25, 'ä': 11, 'ö': 10, 'ü': 10, '1': 11, '2': 111, '3': 11, '4': 11, '5': 11, '6': 11,
           '7': 11, '8': 11, '9': 11, '0': 11, '/': 11, ',': 20, '.' : 20, '*' : 12}


# COUNTER = 26


def setup():
    global picdir, libdir
    # picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
    libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
    if os.path.exists(libdir):
        sys.path.append(libdir)
    logging.basicConfig(level=logging.DEBUG)


def draw_cal_event(draw, x, y, _time, who, summary):
    global COUNTER
    draw.rounded_rectangle(
        (x + pad_cal_event, y, x + offset_days_x - pad_cal_event - 1, y + cal_event_height), fill=1,
        outline=0,
        width=2, radius=8)
    x += 3
    # draw time
    cursor = 2 * pad_cal_event
    draw.text((x + cursor, y), _time[0:2], fill=0, font=font24)
    cursor += 27
    draw.text((x + cursor, y), _time[2:4], fill=0, font=font18)
    cursor += 18
    draw.text((x + cursor, y), _time[4:9], fill=0, font=font24)
    cursor += 25 + 22
    draw.text((x + cursor, y), _time[9:11], fill=0, font=font18)

    # draw who top right corner
    draw.rounded_rectangle(
        (x + 130, y, x + offset_days_x - pad_cal_event - 4, y + cal_event_height / 2 - 1), fill=1,
        outline=0,
        width=2, radius=8)
    if who in ['D', 'C']:
        draw.text((x + offset_days_x - 24, y - 1), who, fill=0, font=font22)
    else:
        draw.text((x + offset_days_x - 27, y + 4), '❤', fill=0, font=emojiFontL)  # '😍'

    # draw summary in Field
    draw.text((x + 2 * pad_cal_event, y + 21), make_string_fit(summary), fill=0, font=font24)


def make_string_fit(s):
    i_length = lengths['i'] + 0.5
    score = 0
    index = 0
    while score <= i_length:
        score += (i_length / lengths[s[index].lower()])
        index += 1
        if index >= len(s):
            return s[0:index]
    return s[0:index - 1]


def start_drawing(wd_events, n_events):
    try:
        if DEBUG:
            width = 800
            height = 450
        else:
            epd = epd7in5_V2.EPD()
            epd.init()
            epd.Clear()
            width = epd.width
            height = epd.height

        logging.info("Drawing calendar")
        Himage = Image.new('1', (width, height), 0)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)

        # draw calendar
        num_wd_events = 0
        for day in wd_events:
            num_wd_events = max(num_wd_events, len(wd_events[day]))

        pad_bday = 4
        draw.line((0, offset_days_y, width, offset_days_y), fill=1)
        draw.rectangle((0, 0, offset_days_x, offset_days_y), fill=1)
        i = 1

        now = datetime.date.today()
        for day in wd_events:
            daystring = day + ' ' + (now + datetime.timedelta(days=(i - 1))).strftime("%d.%m.")
            draw.text(((i - 1) * offset_days_x + 5, 0), daystring, font=font24, fill=1 if i != 1 else 0)
            draw.line((i * offset_days_x, 0, i * offset_days_x, height), fill=1)

            # draw birthdays / whole day thingys
            pad_small = 13

            j = 0
            for wd_event in wd_events[day]:
                draw.text(((i - 1) * offset_days_x + 5, (j * pad_small) + offset_days_y + pad_bday),
                          "🎂 " + wd_event['SUMMARY'][0:17],
                          font=emojiFont, fill=1)
                j += 1
            offset = pad_small * num_wd_events
            # draw one calendar date
            cur_offset_y = offset + offset_days_y + pad_bday * 2

            k = 0
            for n_event in n_events[day]:
                startTime = n_event['DTSTART'].dt.strftime("%H%M")
                endTime = n_event['DTEND'].dt.strftime("%H%M")
                draw_cal_event(draw, (i - 1) * offset_days_x, k * (cal_event_height + 2 * pad_cal_event) + cur_offset_y,
                               startTime + ' - ' + endTime, n_event['WHO'], n_event['SUMMARY'])
                k += 1
            i += 1

            # Draw hint if not all events can be displayed
            max_even = 7
            if len(n_events[day]) > max_even:
                newX = (i - 1) * offset_days_x - 40
                newY = height - 29
                draw.rounded_rectangle(
                    (newX, newY, newX + 40, newY + 28), fill=0,
                    outline=1,
                    width=2, radius=8)
                draw.text((newX + 4, newY), '+ ' + str(len(n_events[day]) - max_even), font=font24, fill=1)

        draw.line((0, offset + offset_days_y + pad_bday, width, offset + offset_days_y + pad_bday), fill=1)

        if DEBUG:
            Himage.save(os.path.join('out', 'test.jpg'))
        else:
            epd.display(epd.getbuffer(Himage))
            epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        # epd7in5_V2.epdconfig.module_exit()
        exit()
