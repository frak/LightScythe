import os
import configparser


class Config:
    SCYTHE_LEFT = 1
    SCYTHE_RIGHT = 2
    DEVICE = '/dev/spidev0.0'

    def __init__(self, path='/home/pi/LightScythe/settings.ini'):
        self.config = configparser.ConfigParser()
        self.path = path

        if not os.path.isfile(path):
            self.config.add_section('Display')
            self.config.set('Display', 'colour', 'VIOLET')
            self.config.set('Display', 'timeout', str(15))
            self.config.set('Display', 'delay', str(0.05))
            self.config.add_section('Images')
            self.config.set('Images', 'dir', '/home/pi/images')
            self.config.set('Images', 'current', str(0))
            with open(self.path, 'w') as configFile:
                self.config.write(configFile)
        self.config.read(self.path)

    def get(self, section, key):
        return self.config.get(section, key)

    def set(self, section, key, value):
        self.config.set(section, key, value)
        with open(self.path, 'w') as configFile:
            self.config.write(configFile)


colours = {
    'BLACK': [0, 0, 0],
    'RED': [100, 0, 0],
    'GREEN': [0, 100, 0],
    'BLUE': [0, 0, 100],
    'YELLOW': [100, 100, 0],
    'TEAL': [0, 100, 100],
    'VIOLET': [100, 0, 100],
    'WHITE': [100, 100, 100]
}
