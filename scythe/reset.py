#!/usr/bin/python

import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


def clear():
    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
    lcd.clear()
    lcd.color = [0, 0, 0]


if __name__ == '__main__':
    clear()

