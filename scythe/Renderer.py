import time

from scythe.Config import Config


class Renderer:
    def __init__(self, config, lcd_plate, imageData):
        (self.blankColumn, self.blinkPix, self.columns) = imageData
        self.lcd_plate = lcd_plate
        self.spi = open(config.DEVICE, 'wb')
        self.delay = float(config.get('Display', 'delay'))

    def draw(self, direction=Config.SCYTHE_LEFT):
        if direction == Config.SCYTHE_RIGHT:
            self.columns.reverse()

        for x in range(len(self.columns)):
            self.spi.write(self.columns[x])
            self.spi.flush()
            time.sleep(self.delay)

        # If we reversed then switch it back for the next run
        if direction == Config.SCYTHE_RIGHT:
            self.columns.reverse()

    def blank(self):
        self.spi.write(self.blankColumn)
