from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD
from Config import Config

class Interface:
    def __init__(self, busnum=-1, addr=0x20, debug=False):
        self.lcd = LCD(busnum, addr, debug)
        self.config = Config()
        self.lcd.backlight(int(self.config.get('Display', 'Colour')))
        self.lcd.clear()

    def scytheHome(self):
        self.display('<> Scythe L/R\n^v Choose image')

    def chooseImage(self, imageName):
        output = 'Image chosen:\n' + imageName
        self.display(output)

    def display(self, text):
        self.lcd.clear()
        self.lcd.message(text)

    def buttons(self):
        return self.lcd.buttons()

