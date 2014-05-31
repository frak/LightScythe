import os, sys
from os import listdir
from os.path import isfile, join
from time import sleep
import PIL
from PIL import Image

class ScytheImages:
    # Constants for images
    HEIGHT = 64
    LDP8806 = 1
    WS2801 = 2

    def __init__(self, imageDir, interface):
        if not os.path.exists(imageDir):
            raise Exception('Image directory (' + imageDir + ') does not exist')

        cacheDir = imageDir + '/processed'
        if not os.path.exists(cacheDir):
            os.makedirs(cacheDir)

        self.stripType = self.LDP8806
        self.interface = interface

        dirList = listdir(imageDir)
        self.fileList = []
        for item in dirList:
            path = imageDir + '/' + item
            if not os.path.isdir(path):
                cachePath = cacheDir + '/' + item
                if not os.path.exists(cachePath):
                    interface.display('Resizing...\n' + item)
                    img = Image.open(path)
                    hpercent = (self.HEIGHT/float(img.size[1]))
                    wsize = int((float(img.size[0]) * float(hpercent)))
                    img = img.resize((self.HEIGHT, wsize), PIL.Image.ANTIALIAS)
                    img.save(cachePath)
                self.fileList.append((item, cachePath))

        interface.display('Cache up to date')

    def getFileList(self):
        return self.fileList

    # This is code taken from v2 of the project
    # https://sites.google.com/site/mechatronicsguy/lightscythe-v2
    def getFileData(self, key):
        self.interface.display('Loding image data')
        img    = Image.open(self.fileList[key][1]).convert('RGB')
        pixels = img.load()
        width  = img.size[0]
        height = img.size[1]
        print("%dx%d pixels" % img.size)
        
        # Calculate gamma correction table.  This includes
        # LPD8806-specific conversion (7-bit color w/high bit set).
        if self.stripType == self.LDP8806:
            gamma = bytearray(256)
            for i in range(256):
                gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
        if self.stripType == self.WS2801:
            gamma = bytearray(256)
            for i in range(256):
                gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)

        # Create list of bytearrays, one for each column of image.
        # R, G, B byte per pixel, plus extra '0' byte at end for latch.
        print "Allocating..."
        column = [0 for x in range(width)]
        for x in range(width):
            if self.stripType == self.LDP8806:
                column[x] = bytearray(height * 3 + 1)
            if self.stripType == self.WS2801:
                column[x] = bytearray(height * 3)
        
        blank_column = bytearray(len(column[0]))
        blink_pix = bytearray(3)
        if self.stripType == self.LDP8806:
            for x in range(height*3+1):
                blank_column[x] = gamma[0]
            blink_pix[0] = gamma[255]
            blink_pix[1] = gamma[0]
            blink_pix[2] = gamma[0]
        if self.stripType == self.WS2801:
            for x in range(height*3):
                blank_column[x] = gamma[0]
            blink_pix[0] = gamma[0]
            blink_pix[1] = gamma[255]
            blink_pix[2] = gamma[0]

        # Convert 8-bit RGB image into column-wise GRB bytearray list.
        print "Converting..."
        for x in range(width):
            for y in range(height):
                value = pixels[x, y]
                y3 = y * 3
                if self.stripType == self.LDP8806:
                    #GRB
                    column[x][y3]     = gamma[value[1]]
                    column[x][y3 + 1] = gamma[value[0]]
                    column[x][y3 + 2] = gamma[value[2]]
                if self.stripType == self.WS2801:
                    #BGR
                    column[x][y3]     = gamma[value[2]]
                    column[x][y3 + 1] = gamma[value[1]]
                    column[x][y3 + 2] = gamma[value[0]]
        return (blank_column, blink_pix, column)
