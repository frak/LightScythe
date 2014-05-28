from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD

SCYTHE_LEFT = 1
SCYTHE_RIGHT = 2

cols = (('Red' , ) , ('Yellow', ), ('Green' , ),
    ('Teal', ), ('Blue'  , )  , ('Violet', ),
    ('Off' , ) , ('On'    , ))

colours = {
    LCD.RED: 'Red',
    LCD.YELLOW: 'Yellow',
    LCD.GREEN: 'Green',
    LCD.TEAL: 'Teal',
    LCD.BLUE: 'Blue',
    LCD.VIOLET: 'Violet'
}