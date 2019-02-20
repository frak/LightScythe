from time import sleep

import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from scythe.Config import Config, colours


class LcdPlate:
    def __init__(self):
        self.lcd = character_lcd.Character_LCD_RGB_I2C(busio.I2C(board.SCL, board.SDA), 16, 2)
        self.config = Config()
        self.lcd.clear()
        self.lcd.color = colours[self.config.get('Display', 'Colour')]

    def scythe_home(self):
        self.display('<> Scythe L/R\n^v Choose image')

    def choose_image(self, image_name):
        self.display('Image chosen:\n' + image_name)

    def display(self, text):
        self.lcd.color = colours[self.config.get('Display', 'Colour')]
        self.lcd.clear()
        self.lcd.message = text

    def fatal_error(self, error_message):
        self.lcd.clear()
        self.lcd.color = [100, 0, 0]
        self.lcd.message = error_message

    def flash_red(self):
        self.lcd.color = [100, 0, 0]
        sleep(0.01)
        self.lcd.color = colours[self.config.get('Display', 'Colour')]

    def off(self):
        self.lcd.clear()
        self.lcd.color = colours['BLACK']

    def left_button(self):
        return self.lcd.left_button

    def right_button(self):
        return self.lcd.right_button

    def up_button(self):
        return self.lcd.up_button

    def down_button(self):
        return self.lcd.down_button

    def select_button(self):
        return self.lcd.select_button

    def clear(self):
        self.lcd.clear()


if __name__ == '__main__':
    plate = LcdPlate()
