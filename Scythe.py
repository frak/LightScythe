#!/usr/bin/python

import os, sys
from time import sleep
from ScytheImages import ScytheImages as Images
from Config import Config
from Interface import Interface

class Scythe:
    def __init__(self):
        self.interface = Interface()
        self.config    = Config()
        self.images    = Images(self.config.get('Images', 'dir'), self.interface)

    def runLoop(self):
        exit          = False
        buttonPressed = False
        displayDone   = False
        imageIndex    = int(self.config.get('Images', 'current'))
        imageList     = self.images.getFileList()
        maxImageIndex = len(imageList)
        (blank_column, blink_pix, column) = self.images.getFileData(imageIndex)

        self.interface.scytheHome()        

        while(not exit):
            buttons = self.interface.buttons()
            if not buttonPressed and buttons != 0:
                # 1 = select
                # 2 = right
                # 4 = down
                # 8 = up
                # 16 = left
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
                displayDone   = False
                buttonPressed = True
            elif buttonPressed and buttons == 0:
                buttonPressed = False

            if not displayDone:
                displayDone = True

scythe = Scythe()
scythe.runLoop()
