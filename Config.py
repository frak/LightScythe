import os, ConfigParser
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD

class Config:

    SCYTHE_LEFT  = 1
    SCYTHE_RIGHT = 2

    def __init__(self, path='./settings.ini'):
        self.config = ConfigParser.SafeConfigParser()

        if not os.path.isfile(path):
            self.config.add_section('Display')
            self.config.set('Display', 'colour', str(LCD.VIOLET))
            self.config.set('Display', 'timeout', str(3))
            self.config.add_section('Images')
            self.config.set('Images', 'dir', '/home/pi/images')
            self.config.set('Images', 'current', '0')
            with open(path, 'wb') as configFile:
                self.config.write(configFile)
        self.config.read(path)

    def get(self, section, key):
        return self.config.get(section, key)

    def set(self, section, key, value):
        return self.config.set(section, key, value)
        
    def getSections(self):
        return self.config.sections()
        
    def getItems(self, section):
        return self.config.items(section)

