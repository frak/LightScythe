# LightScythe v3 #
## Credits ##
This project could not exist were it not for the work of [The Mechatronics Guy][mech],
[and his update][mech2].  The work I am doing here is largely based on his list of
improvements.  Credit also has to be given to [Adafruit][adafruit] for their code and
components - together, you guys have saved me a lot of hard work!

## Hardware ##

### Raspberry Pi ###
We use a [Raspberry Pi Zero W][pizero] - the linked one includes a full GPIO header
but this is not the default, make sure the header exists or that you purchase a kit for 
[attaching this yourself][hammer].  

![RPi with GPIO header attached](/images/pi-with-header.jpg?raw=true "RPi with GPIO header attached")

To protect the device, I also bought a [Pibow case][case].

![RPi in Pibow case](/images/pi-in-case.jpg?raw=true "RPi in Pibow case")

### LCD Plate ###
As I didn't want to get involved with wiring buttons directly to the GPIO pins on my Pi
and it seemed that for real control some form of display would be needed, I opted for the 
[Adafruit 16x2 LCD plate with built in buttons][ada]. Assembly was simple but it does 
require a certain level of dexterity with a soldering iron. 

![GPIO pinout diagram](/images/raspberry-pi-pinout.png?raw=true "GPIO pinout diagram")

Once assembled insert two **thin** wires into the MOSI (BCOM 10 / 19) and SCLK (BCOM 11 / 23) 
SPI sockets. 

![Wires inserted into LCD plate socket](/images/wires-in-lcd-plate.jpg?raw=true "Wires inserted into LCD plate socket")

Then attach the LCD plate to the Pi taking care to ensure that nothing is forced excessively 
or unevenly. 

![Pi attached to LCD plate](/images/pi-and-plate-closeup.jpg?raw=true "Pi attached to LCD plate")

![Pi attached to LCD plate with SPI cable showing](/images/pi-and-plate-with-cable.jpg?raw=true "Pi attached to LCD plate with SPI cable showing")

### Scythe ###
For the Scythe itself, I am using 2 x [1m lengths of OpenBeam][obeam] that are held 
together with the handle template provided by [the Mechatronics guy][thingv]. I have 
then used velcro to attach the [Adafruit Digital LED Strip][ada2] to the beam.

To power the lights, you need a theoretical maximum of 2A per meter of lights, and then 
another amp or so to power the Pi, so I chose [this 5v 5800mAh battery from eBay][battery] 
which looks like it will have plenty of power for the job.  I am putting the power from this 
on to a veroboard that is linked at both the top and bottom of the beam to the LED chain.
From this there is also a micro USB to power the Raspberry Pi. North of the Pi there are 4 
lanes of board and the central 2 are used to carry the light data. 

## Software ##

### Raspberry Pi ###
These are instructions to get your Pi up and running. They are for a Mac and may skip
some details if I have assumed they are too trivial, please raise an issue if 
something needs explaining.

1. Write Raspbian to SD card with Etcher
2. `touch /Volumes/boot/ssh`
3. Create `/Volumes/boot/wpa_supplicant.conf` and add the following contents:
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US
    
    network={
        ssid="your-network-service-set-identifier"
        psk="your-network-WPA/WPA2-security-passphrase"
        key_mgmt=WPA-PSK
    }
    ```
4. Unmount the SD card and insert it into your Pi, add power and wait for it to boot.
5. Get the IP of the Pi and SSH into it: `ssh pi@192.168.1.22`
6. Enable I2C (for the display and buttons) and SPI (for the light strip).  `sudo sudo raspi-config` 
    and select `5 Interfacing Options` > `P4 SPI` and enabled it then `P5 I2C` and enable.
7. Update APT: `sudo apt update && sudo apt upgrade -y`
8. Install the Hotspot packages: `sudo apt install dnsmasq hostapd -y`
9. Configure a static IP address for the Pi (`/etc/dhcpcd.conf`):
    ```
    interface wlan0
        static ip_address=192.168.4.1/24
        nohook wpa_supplicant
    ```
10. Move the old dnsmasq config out of the way: `sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig`
11. Create the new DHCP server configuration file (`/etc/dnsmasq.conf`) as root 
    and add:
    ```
    interface=wlan0
      dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
    ```
    (for wlan0, we are going to provide IP addresses between 192.168.4.2 and 192.168.4.20, 
    with a lease time of 24 hours)
12. Edit the access point config (`/etc/hostapd/hostapd.conf`) and add this config:
    ```
    interface=wlan0
    driver=nl80211
    ssid=LightScythe
    hw_mode=g
    channel=7
    wmm_enabled=0
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=RustyBulletHole
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    ```
13. Tell the system where to find this config, edit `/etc/default/hostapd` to have:
    ```
    DAEMON_CONF="/etc/hostapd/hostapd.conf"
    ```
14. Enable IP forwarding by editing `/etc/sysctl.conf` and uncommenting the line 
    `net.ipv4.ip_forward=1`
15. Reboot (`sudo reboot`) and scan your WiFi for the access point when the Pi boots back up.
    You should be able to connect to the access point and SSH into your Pi with 
    `ssh pi@192.168.4.1`

### Scythe Code
1. Install Python dependencies: `pip3 install adafruit-circuitpython-charlcd Pillow` 
2. Install the code: `git clone https://github.com/frak/LightScythe.git`

Once you have everything setup, you just need to run the following from the project root.

    scythe/Scythe.py

On the first run, it will create a settings.ini file in the project root. You can override 
this process by manually supplying a `settings.ini` file yourself. Here are the default 
values to use as a template:

    [Display]
    colour = VIOLET
    timeout = 15
    delay = 0.05
    
    [Images]
    dir = /home/pi/images
    current = 0


This will expect the images to be found in /home/pi/images - if it cannot find either the 
directory or any images the script will terminate.  When it loads, any images found in that 
directly will be automatically resized to the correct height, and the resized image will be 
saved in a "preocessed" sub-directory. You can also set the display colour and timeout here, 
using the following colour constants: RED, GREEN, BLUE, VIOLET, TEAL, WHITE, BLACK (off).

There are many ways to get your Pi to run this script automatically on boot which you
will need out in the field, however, the simplest option I found was to use crontab. 
Just run `crontab -e` and add the following:

    @reboot /home/pi/LightScythe/scythe/Scythe.py &

[mech]: https://sites.google.com/site/mechatronicsguy/lightscythe
[mech2]: https://sites.google.com/site/mechatronicsguy/lightscythe-v2
[adafruit]: https://learn.adafruit.com/light-painting-with-raspberry-pi
[ada]: https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi
[ada2]: https://learn.adafruit.com/digital-led-strip
[pizero]: https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header
[male_header]: https://shop.pimoroni.com/products/gpio-hammer-header?variant=35643318026
[i2c]: http://skpang.co.uk/blog/archives/575
[spi]: http://quick2wire.com/non-root-access-to-spi-on-the-pi/
[openbeam]: http://www.openbeamusa.com/
[battery]: http://www.ebay.co.uk/itm/12V-3800mah-5V-USB-5800mah-DC-Rechargeable-Li-ion-Battery-Pack-with-UK-charger-/171337179921
[obeam]: https://www.makerbeam.com/openbeam-1000mm-1p-black-openbeam.html
[thingv]: http://www.thingiverse.com/thing:117858
[hammer]: https://shop.pimoroni.com/products/gpio-hammer-header
[case]: https://shop.pimoroni.com/products/pibow-zero-w
