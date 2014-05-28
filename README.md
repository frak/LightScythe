# LightScythe v3 #
## Credits ##
This project could not exist were it not for the work of [The Mechatronics Guy][mech],
[and his update][mech2], and the work I have done here is largely based on his list of
improvements.  Thanks dude.

## Hardware ##
As I didn't want to get involved with wiring buttons directly to the GPIO pins on my Pi
and it seemed that for images to be selected some form of display would be needed, I
opted for the [Adafruit 16x2 LCD plate with built in buttons][ada]. Assembly was simple
but does require a certain level of dexterity with a soldering iron as there are many pins
in a row that need to be soldered precisely.

Of course, for the strip I used 2 metres of the [Adafruit Digital LED Strip][ada2], which
I took delivery of today - so I guess the next step for this is making the scythe itself.
Oh, I do so love making things &lt;/sarcasm&gt;

## Software ##
Well, this is it so far.  Despite my total lack of Python knowledge I seem to be doing OK.  
Got a class now which handles the byte mapping and resizing of images, I have a basic
Interface class as well, but the layout is totally up for change as my knowledge of Python
improves.

[mech]: https://sites.google.com/site/mechatronicsguy/lightscythe
[mech2]: https://sites.google.com/site/mechatronicsguy/lightscythe-v2
[ada]: https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi
[ada2]: https://learn.adafruit.com/digital-led-strip