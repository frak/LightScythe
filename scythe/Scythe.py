#!/usr/bin/python

import sys, time
from time import sleep

from scythe.Config import Config
from scythe.LcdPlate import LcdPlate
from scythe.Renderer import Renderer

from scythe.ScytheImages import ScytheImages as Images


class Scythe:
    def __init__(self):
        self.config = Config()
        self.lcd_plate = LcdPlate()
        self.images = Images(self.config.get('Images', 'dir'), self.lcd_plate)
        self.imageList = self.images.get_file_list()
        self.renderer = None
        self.display_data = None
        if len(self.imageList) == 0:
            self.lcd_plate.fatal_error('No images!')
            raise Exception('There are no images to scythe')

    def display_image(self, image_index):
        self.lcd_plate.choose_image(self.imageList[image_index][0])
        self.config.set('Images', 'current', str(image_index))
        sleep(1)
        self.lcd_plate.scythe_home()

    def loop(self):
        image_index = int(self.config.get('Images', 'current'))
        timeout = int(self.config.get('Display', 'timeout'))
        max_image_index = len(self.imageList)

        display_data = self.images.get_file_data(image_index)
        renderer = Renderer(self.config, self.lcd_plate, display_data)

        self.lcd_plate.scythe_home()
        renderer.blank()

        last_activity = time.time()
        while True:
            if self.lcd_plate.select_button():
                last_activity = time.time()
                print('select')
                self.lcd_plate.off()
                sys.exit(0)
            elif self.lcd_plate.up_button():
                last_activity = time.time()
                print('up')
                if image_index > 0:
                    image_index = image_index - 1
                    display_data = self.images.get_file_data(image_index)
                    self.display_image(image_index)
                else:
                    self.lcd_plate.flash_red()
            elif self.lcd_plate.down_button():
                last_activity = time.time()
                print('down')
                if image_index + 1 < max_image_index:
                    image_index = image_index + 1
                    display_data = self.images.get_file_data(image_index)
                    self.display_image(image_index)
                else:
                    self.lcd_plate.flash_red()
            elif self.lcd_plate.left_button():
                last_activity = time.time()
                print('left')
                self.lcd_plate.display('Painting left')
                renderer.draw()
                self.lcd_plate.display('Done!')
                sleep(0.2)
                self.lcd_plate.scythe_home()
            elif self.lcd_plate.right_button():
                last_activity = time.time()
                print('right')
                self.lcd_plate.display('Painting right')
                renderer.draw(Config.SCYTHE_RIGHT)
                self.lcd_plate.display('Done!')
                sleep(0.2)
                self.lcd_plate.scythe_home()

            sleep(0.05)
            if timeout != -1 and time.time() - last_activity > timeout:
                self.lcd_plate.off()


def run():
    Scythe().loop()


if __name__ == "__main__":
    Scythe().loop()
