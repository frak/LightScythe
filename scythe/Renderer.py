import RPi.GPIO as GPIO
from Config import Config

class Renderer:
    def __init__(self, config, imageData, interface):
        (self.blankColumn, self.blinkPix, self.columns) = imageData
        self.interface = interface
        self.spi       = file(config.DEVICE, 'wb')

    def draw(self, direction):
        if direction == Config.SCYTHE_RIGHT:
            self.columns.reverse()

        for x in range(width):
            self.spi.write(self.columns[x])
            self.spi.flush()
            time.sleep(0.001)

        # If we reversed then switch it back for the next run
        if direction == Config.SCYTHE_RIGHT:
            self.columns.reverse()

    def blank(self):
        self.spi.write(self.blankColumn)
        