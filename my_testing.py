#!/usr/bin/python

import os, sys
from time import sleep
from ScytheImages import ScytheImages as Images
from Config import Config
from Interface import Interface

class ProcedureFactory:
    @staticmethod
    def list():
        return ('Stars', 'Nyan')


class Main:
    def __init__(self):
        self.interface = Interface()
        self.config = Config()
        self.images = Images(self.config.get('Images', 'dir'), self.interface)

    def runLoop(self):
        exit = False
        scytheDir = Config.SCYTHE_LEFT
        buttonPressed = False

        self.interface.scytheHome()

        while(not exit):
            # 1 = select
            # 2 = right
            # 4 = down
            # 8 = up
            # 16 = left
            buttons = self.interface.buttons()
            if not buttonPressed and buttons != 0:
                buttonPressed = True
                if buttons == 1:
                    print('select')
                if buttons == 8:
                    print('up')
                if buttons == 4:
                    print('down')
                if buttons == 2:
                    print('right')
                if buttons == 16:
                    print('left')
            elif buttonPressed and buttons == 0:
                buttonPressed = False


main = Main()
main.runLoop()
