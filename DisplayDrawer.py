#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

# picdir = ""
libdir = ""


def setup():
    global picdir, libdir
    # picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
    libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
    if os.path.exists(libdir):
        sys.path.append(libdir)

    logging.basicConfig(level=logging.DEBUG)


def start_drawing():
    try:
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 18)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        # draw.text((10, 0), 'Montag', font=font24, fill=0)
        days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        # draw calendar
        draw.line((0, 50, epd.width, 50), fill=0)
        for i in range(1, 6):
            draw.text(((i - 1) * 160, 0), days[i-1], font=font24, fill=0)
            draw.line((i * 160, 0, i * 160, epd.height))
        # draw.line((0, 100, epd.width, 100), fill=1)
        # draw.line((0, 150, epd.width, 150), fill=2)
        # draw.line((70, 50, 20, 100), fill=0)
        # draw.rectangle((20, 50, 70, 100), outline=0)
        # draw.line((165, 50, 165, 100), fill=0)
        # draw.line((140, 75, 190, 75), fill=0)
        # draw.arc((140, 50, 190, 100), 0, 360, fill=0)
        # draw.rectangle((80, 50, 130, 100), fill=0)
        # draw.chord((200, 50, 250, 100), 0, 360, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(20)

        # Drawing on the Vertical image
        logging.info("2.Drawing on the Vertical image...")
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((2, 0), 'hello world and others', font=font18, fill=0)
        draw.text((2, 20), '7.5inch epd', font=font18, fill=0)
        # draw.text((20, 50), u'微雪电子', font=font18, fill=0)
        draw.line((10, 90, 60, 140), fill=0)
        draw.line((60, 90, 10, 140), fill=0)
        draw.rectangle((10, 90, 60, 140), outline=0)
        draw.line((95, 90, 95, 140), fill=0)
        draw.line((70, 115, 120, 115), fill=0)
        draw.arc((70, 90, 120, 140), 0, 360, fill=0)
        draw.rectangle((10, 150, 60, 200), fill=0)
        draw.chord((70, 150, 120, 200), 0, 360, fill=0)
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        logging.info("3.read bmp file")
        Himage = Image.open(os.path.join('res', '7in5_V2.bmp'))
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

        logging.info("4.read bmp file on window")
        Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        bmp = Image.open(os.path.join('res', '100x100.bmp'))
        Himage2.paste(bmp, (50, 10))
        epd.display(epd.getbuffer(Himage2))
        time.sleep(2)

        logging.info("Clear...")
        epd.init()
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()


def start_drawing_demo():
    try:
        logging.info("epd7in5_V2 Demo")
        epd = epd7in5_V2.EPD()

        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join('res', 'Font.ttc'), 18)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 0), 'hello world, cosi and silvan', font=font24, fill=0)
        draw.text((10, 20), '7.5inch e-Paper', font=font24, fill=0)
        draw.line((20, 50, 70, 100), fill=0)
        draw.line((70, 50, 20, 100), fill=0)
        draw.rectangle((20, 50, 70, 100), outline=0)
        draw.line((165, 50, 165, 100), fill=0)
        draw.line((140, 75, 190, 75), fill=0)
        draw.arc((140, 50, 190, 100), 0, 360, fill=0)
        draw.rectangle((80, 50, 130, 100), fill=0)
        draw.chord((200, 50, 250, 100), 0, 360, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

        # Drawing on the Vertical image
        logging.info("2.Drawing on the Vertical image...")
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((2, 0), 'hello world and others', font=font18, fill=0)
        draw.text((2, 20), '7.5inch epd', font=font18, fill=0)
        # draw.text((20, 50), u'微雪电子', font=font18, fill=0)
        draw.line((10, 90, 60, 140), fill=0)
        draw.line((60, 90, 10, 140), fill=0)
        draw.rectangle((10, 90, 60, 140), outline=0)
        draw.line((95, 90, 95, 140), fill=0)
        draw.line((70, 115, 120, 115), fill=0)
        draw.arc((70, 90, 120, 140), 0, 360, fill=0)
        draw.rectangle((10, 150, 60, 200), fill=0)
        draw.chord((70, 150, 120, 200), 0, 360, fill=0)
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        logging.info("3.read bmp file")
        Himage = Image.open(os.path.join('res', '7in5_V2.bmp'))
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

        logging.info("4.read bmp file on window")
        Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        bmp = Image.open(os.path.join('res', '100x100.bmp'))
        Himage2.paste(bmp, (50, 10))
        epd.display(epd.getbuffer(Himage2))
        time.sleep(2)

        logging.info("Clear...")
        epd.init()
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()
