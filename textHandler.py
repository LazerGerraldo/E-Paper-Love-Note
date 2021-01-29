#Initializes epd and hanles text then sends text to the display
import sys
import os, textwrap

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic') #font file location
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib') #epd library location

import logging
from lib.waveshare_epd import epd2in9b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

class WrapSetting:
    def __init__(self, width, font, max_lines):
        self.width = width
        self.font = font
        self.max_lines = max_lines

# global e-paper object
epd = epd2in9b_V2.EPD()

logging.basicConfig(level=logging.DEBUG)

def initscreen():
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

def SHUTDOWN():
    epd.Clear()
    epd.Dev_exit()

# function for writing image and sleeping for 5 min.
def display_on_screen(message):

    try:        

        # Drawing on the Horizontal image
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 296*128
        HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 296*128  ryimage: red or yellow image  
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)

        # Initializing Drawing on the image
        logging.info("Displaying message") 
        logging.info(message)    
        font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
        
        #defining wrap settings with associated with different font sizes, with 
        # the max viewable lines on 298x126 display
        wrap_small = WrapSetting(50, font12, 8)
        wrap_medium = WrapSetting(31, font18, 6)
        wrap_large = WrapSetting(25, font24, 4)
        wrap_XL = WrapSetting(17, font36, 3)
        wrap_sizes = [wrap_XL, wrap_large, wrap_medium, wrap_small]

        #loops through all wrap settings in order to fill display with given message text. 
        # Draws to the display.
        for wrapping in wrap_sizes:
            wrap = textwrap.TextWrapper(width = wrapping.width)
            display_text = wrap.fill(text=message)
            line_count = display_text.count('\n') + 1
            if line_count <= wrapping.max_lines:
                drawblack.text((10, 0), display_text, font = wrapping.font, fill = 0)
                break
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))

        # logging.info("Clear...")
        # epd.init()
        # epd.Clear()
        
        # logging.info("Goto Sleep...")
        # epd.sleep()
        # epd.Dev_exit()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in9b_V2.epdconfig.module_exit()
        exit()
