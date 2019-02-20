import os
from os import listdir
import PIL
from PIL import Image


class ScytheImages:
    # Constants for images
    HEIGHT = 64
    LDP8806 = 1
    WS2801 = 2

    def __init__(self, image_dir, lcd_plate):
        if not os.path.exists(image_dir):
            lcd_plate.fatal_error('No image dir @\n' + image_dir)
            raise Exception('Image directory (' + image_dir + ') does not exist')

        cache_dir = image_dir + '/processed'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        self.strip_type = self.LDP8806
        self.lcd_plate = lcd_plate

        dir_list = listdir(image_dir)
        self.fileList = []
        for item in dir_list:
            path = image_dir + '/' + item
            if not os.path.isdir(path):
                cache_path = cache_dir + '/' + item
                if not os.path.exists(cache_path):
                    lcd_plate.display('Creating raster\n' + item)
                    img = Image.open(path)
                    hpercent = (self.HEIGHT / float(img.size[1]))
                    wsize = int((float(img.size[0]) * float(hpercent)))
                    img = img.resize((self.HEIGHT, wsize), PIL.Image.ANTIALIAS)
                    img.save(cache_path)
                self.fileList.append((item, cache_path))

        lcd_plate.display('Cache up to date')

    def get_file_list(self):
        return self.fileList

    # This is code taken from v2 of the project
    # https://sites.google.com/site/mechatronicsguy/lightscythe-v2
    def get_file_data(self, key):
        image_name = self.fileList[key][1].rsplit('/')[-1]
        print('Image name: ' + image_name)
        self.lcd_plate.display('Loading image\n' + image_name)
        img = Image.open(self.fileList[key][1]).convert('RGB')
        pixels = img.load()
        width = img.size[0]
        height = img.size[1]
        print("  %dx%d pixels" % img.size)

        # Calculate gamma correction table.  This includes
        # LPD8806-specific conversion (7-bit color w/high bit set).
        if self.strip_type == self.LDP8806:
            gamma = bytearray(256)
            for i in range(256):
                gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
        if self.strip_type == self.WS2801:
            gamma = bytearray(256)
            for i in range(256):
                gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)

        # Create list of bytearrays, one for each columns of image.
        # R, G, B byte per pixel, plus extra '0' byte at end for latch.
        print("  allocating...")
        columns = [0 for x in range(width)]
        for x in range(width):
            if self.strip_type == self.LDP8806:
                columns[x] = bytearray(height * 3 + 1)
            if self.strip_type == self.WS2801:
                columns[x] = bytearray(height * 3)

        blank_column = bytearray(len(columns[0]))
        blink_pix = bytearray(3)
        if self.strip_type == self.LDP8806:
            for x in range(height * 3 + 1):
                blank_column[x] = gamma[0]
            blink_pix[0] = gamma[255]
            blink_pix[1] = gamma[0]
            blink_pix[2] = gamma[0]
        if self.strip_type == self.WS2801:
            for x in range(height * 3):
                blank_column[x] = gamma[0]
            blink_pix[0] = gamma[0]
            blink_pix[1] = gamma[255]
            blink_pix[2] = gamma[0]

        # Convert 8-bit RGB image into columns-wise GRB bytearray list.
        print("  converting...")
        for x in range(width):
            for y in range(height):
                value = pixels[x, y]
                y3 = y * 3
                if self.strip_type == self.LDP8806:
                    # GRB
                    columns[x][y3] = gamma[value[1]]
                    columns[x][y3 + 1] = gamma[value[0]]
                    columns[x][y3 + 2] = gamma[value[2]]
                if self.strip_type == self.WS2801:
                    # BGR
                    columns[x][y3] = gamma[value[2]]
                    columns[x][y3 + 1] = gamma[value[1]]
                    columns[x][y3 + 2] = gamma[value[0]]
        print("done.")
        return blank_column, blink_pix, columns
