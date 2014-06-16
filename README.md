# LightScythe v3 #
## Credits ##
This project could not exist were it not for the work of [The Mechatronics Guy][mech],
[and his update][mech2].  The work I am doing here is largely based on his list of
improvements.  Credit also has to be given to [Adafruit][adafruit] for their code and
components - together, you guys have saved me a lot of hard work!

## Hardware ##
As I didn't want to get involved with wiring buttons directly to the GPIO pins on my Pi
and it seemed that for images to be selected some form of display would be needed, I
opted for the [Adafruit 16x2 LCD plate with built in buttons][ada]. Assembly was simple
but it does require a certain level of dexterity with a soldering iron as there are many
pins in a row that need to be soldered precisely.

Of course, for the strip I used 2 metres of the [Adafruit Digital LED Strip][ada2], so
I guess the next step for this is making the scythe itself. Oh, I do so love making things
`</sarcasm>`

## Raspberry Pi ##
But the star of the show is the [Raspberry Pi][rpi] - I have done and intend to do so many
things with this device. I run Raspbian, and for any of this to work you need to enable I2C
(for the display and buttons) and SPI (for the light strip).  To do this you will first
need to comment out the modules from the blacklist (/etc/modprobe.d/raspi-blacklist.conf):

    #blacklist spi-bcm2708
    #blacklist i2c-bcm2708

And then you will need to enable the modules in /etc/modules:

    snd-bcm2835
    i2c-bcm2708
    i2c-dev

In order to allow non-root access to the [I2C][i2c] and [SPI][spi] pins:

    sudo adduser pi i2c
    sudo groupadd -f --system spi
    sudo adduser pi spi  # This may say that pi is already a member of the group

You will then need to create `/etc/udev/rules.d/90-spi.rules` (as root) and add
the following line:

    SUBSYSTEM=="spidev", GROUP="spi"

Give the beast a reboot and she's good to go.  You should now be able to run the
code without being root.

### Power Supply ###
This was not as straight-forward as it first seemed.  To power the lights, you need
a theoretical maximum of 2A per meter of lights, and then another amp or so to power
the Pi, so I chose [this 5v 5800mAh battery from eBay][battery] which looks like it
will have plenty of power for the job.  However, one thing that is not made clear
either by Adafruit or The Mechatronics Guy is that just adding this power to the 5V
GPIO pin means that your Pi will be completely exposed to the high current coming
from the battery.  You can take your chances with this one if you like, I prefer my
Pi to be as protected as possible.  To do this, I first created a breakout connector,
which is just two USB sockets mounted on veroboard with two racks of solderless headers
for connected directly to the LEDs:

![Top down view of the power breakout](/images/connector-top.jpg?raw=true)
![A view of my not so excellent sodlering skills](/images/connector-bottom.jpg?raw=true)

As the USB connectors are facing away from each other, their polarity will be reversed.
Another issue to fix is that most USB cables are not rated for such a high current. I
solved both of these problems by making my own USB crossover cable with 6A houshold wires.

![My 6A crossover cable](/images/usb-crossover.jpg?raw=true)

**It is important to remember that you must swap the GND and 5V wires on one of the ends
of the cable otherwise you will be passing the wrong polarity into your Raspberry Pi.**

## Software ##
Well, this is what I have so far.  Despite my total lack of Python knowledge I seem
to be doing OK. Everything seems to be it the right place, and I have got automatic
image resizing, and I have hooked in the original image parsing code.  Once you have
everything setup, you just need to run:

    ./Scythe.py

On the first run, it will create a settings.ini file in the project root which will expect
the images to be found in /home/pi/images - if it cannot find either the directory or any
images the script will terminate.  (You can of course change this to any other directory
you would prefer to use, but you will need to run the Scythe once first to get the config
file.)

When it loads, any images found in that directly will be automatically resized to the
correct height, and the resized image will be saved in a "preocessed" sub-directory. You 
can also set the display colour and timeout here, using the colour constants found in 
Adafruit_CharLCDPlate.py and any number in seconds for the timeout.

There are many ways to get your Pi to run this script automatically on boot which you
will need out in the field, however, the simplest option I found was to use crontab. 
Just run `crontab -e` and add the following:

    @reboot /home/pi/LightScythe/Scythe.py &

## Next Steps ##
Well, now I need some hardware - I have ordered some of the [OpenBeams][openbeam] that
I need, and I am in contact with someone who should be able to do the laser cutting
for me but the hardest part is going to be attaching the LCD plate to the Scythe. I
am hoping I can work something out just using OpenBeam as I really don't want to get
into designing custom parts...

[mech]: https://sites.google.com/site/mechatronicsguy/lightscythe
[mech2]: https://sites.google.com/site/mechatronicsguy/lightscythe-v2
[adafruit]: https://learn.adafruit.com/light-painting-with-raspberry-pi
[ada]: https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi
[ada2]: https://learn.adafruit.com/digital-led-strip
[rpi]: http://www.raspberrypi.org/
[i2c]: http://skpang.co.uk/blog/archives/575
[spi]: http://quick2wire.com/non-root-access-to-spi-on-the-pi/
[openbeam]: http://www.openbeamusa.com/
[battery]: http://www.ebay.co.uk/itm/12V-3800mah-5V-USB-5800mah-DC-Rechargeable-Li-ion-Battery-Pack-with-UK-charger-/171337179921