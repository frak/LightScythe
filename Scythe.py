#!/usr/bin/python

import os, sys, time
from time import sleep
from ScytheImages import ScytheImages as Images
from Config import Config
from Interface import Interface
from Renderer import Renderer

class Scythe:
    def __init__(self):
        self.interface = Interface()
        self.config    = Config()
        self.images    = Images(self.config.get('Images', 'dir'), self.interface)
        self.imageList = self.images.getFileList()
        if len(self.imageList) == 0:
            raise Exception('There are no images to scythe')

    def displayImage(self, imageIndex):
        self.interface.chooseImage(self.imageList[imageIndex][0])
        self.config.set('Images', 'current', str(imageIndex))
        sleep(1)
        self.interface.scytheHome()

    def runLoop(self):
        exit          = False
        buttonPressed = False
        imageIndex    = int(self.config.get('Images', 'current'))
        timeout       = int(self.config.get('Display', 'timeout'))
        maxImageIndex = len(self.imageList)
        lastActivity  = time.time()

        self.displayData = self.images.getFileData(imageIndex)
        self.renderer    =  Renderer(self.config, self.displayData, self.interface)

        self.interface.scytheHome()
        self.renderer.blank()

        while(not exit):
            buttons = self.interface.buttons()
            if not buttonPressed and buttons != 0:
                buttonPressed = True
                lastActivity  = time.time()

                # 1 = select
                # 2 = right
                # 4 = down
                # 8 = up
                # 16 = left
                if buttons == 1:
                    print('select')
                    self.interface.off()
                    sys.exit(0)
                if buttons == 8:
                    print('up')
                    if imageIndex > 0:
                        imageIndex  = imageIndex - 1
                        self.displayData = self.images.getFileData(imageIndex)
                    self.displayImage(imageIndex)
                if buttons == 4:
                    print('down')
                    if imageIndex + 1 < maxImageIndex:
                        imageIndex  = imageIndex + 1
                        self.displayData = self.images.getFileData(imageIndex)
                    self.displayImage(imageIndex)
                if buttons == 2:
                    print('right')
                if buttons == 16:
                    print('left')
            elif buttonPressed and buttons == 0:
                buttonPressed = False
            
            if time.time() - lastActivity > timeout:
                self.interface.off()


Scythe().runLoop()
