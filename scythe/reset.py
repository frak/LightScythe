#!/usr/bin/python

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class LCDDisplay:
    def __init__(self, busnum=-1, addr=0x20, debug=True):
        self.lcd = Adafruit_CharLCDPlate(busnum, addr, debug)
        self.lcd.backlight(self.lcd.OFF)
        self.lcd.noDisplay()

if __name__ == '__main__':
    display = LCDDisplay()

