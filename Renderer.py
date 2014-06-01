import RPi.GPIO as GPIO
from Config import Config

class Renderer:
    def __init__(self, config, imageData):
        (self.blankColumn, self.blinkPix, self.columns) = imageData
        self.spi = file(config.DEVICE, 'wb')

    # def draw(self, data, direction):
    #     if direction == Config.SCYTHE_LEFT:
    #     else:

    def blank(self):
        self.spi.write(self.blankColumn)
        