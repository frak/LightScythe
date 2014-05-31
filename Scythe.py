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
        self.imageList = self.images.getFileList()
        if len(self.imageList) == 0:
            raise Exception('There are no images to scythe')

    def newImage(self, imageIndex):
        (blank_column, blink_pix, column) = self.images.getFileData(imageIndex)
        self.interface.chooseImage(self.imageList[imageIndex][0])
        sleep(1)
        self.interface.scytheHome()
        return (blank_column, blink_pix, column)

    def runLoop(self):
        exit          = False
        buttonPressed = False
        displayDone   = False
        imageIndex    = int(self.config.get('Images', 'current'))
        maxImageIndex = len(self.imageList)
        displayData   = self.newImage(imageIndex)

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
                    if imageIndex > 0:
                        imageIndex  = imageIndex - 1
                        displayData = self.newImage(imageIndex)
                if buttons == 4:
                    print('down')
                    if imageIndex + 1 < maxImageIndex:
                        imageIndex  = imageIndex + 1
                        displayData = self.newImage(imageIndex)
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
