#!/bin/bash

# usage:
# ./radio.sh radio-station-frequency

# examples:

# Sydney - Triple J
# ./radio.sh 105.7

# Sydney - Triple M
# ./radio.sh 104.9

# Sydney - WSFM
# ./radio.sh 101.7

# Sydney - Nova 969
# ./radio.sh 96.9

# Mute, by not passing in a frequency
# ./radio.sh


# The Grove I2C FM Receiver can operate in RDA5807 or TEA5767 mode
# In simpler TEA5767 mode, the I2C address 0x60

# http://www.voti.nl/docs/TEA5767.pdf
# http://en.wikipedia.org/wiki/List_of_radio_stations_in_Australia

# Connect your FM receiver to one of the I2C sockets
# Check if the device was found
# i2cdetect -y 1

# enable I2C via the raspi-config "Advanced Options" menu
# sudo raspi-config

# make sure "i2c-dev" is in /etc/modules
# sudo nano /etc/modules

# To run i2cdetect and i2cset you will need to install the i2c-tools package
# sudo apt-get install i2c-tools

# If you want to run i2cset without sudo, you'll need to add the pi user to the i2c group
# sudo usermod -aG i2c pi

# dont forget to make the script executable
# chmod +x radio.sh


# TEA5767 mode I2C address
addr=0x60

freq=$@

# setting of synthesizer programmable counter for search or preset
pll=$(echo $freq | awk '{ printf "%d", 4 * ($1 * 1000000 + 225000) / 32768 }')

byte1=0
byte1=$((pll>>8)) # bits 0-5 contain the msb bits of the frequency preset
#byte1=$((byte1|0x80)) # MUTE - left and right are muted
#byte1=$((byte1|0x40)) # SM - search mode

# mute if no frequency has been provided
if [ ! "$freq" ]; then
	byte1=$((byte1|0x80)) # MUTE - left and right are muted
fi

byte2=0
byte2=$((pll&0xFF)) # bits 0-7 contain the lsb bits of the frequency preset

byte3=0
byte3=$((byte3|0x80)) # SUD - search up
#byte3=$((byte3|0x40)) # SSL1 - search stop level high
#byte3=$((byte3|0x20)) # SSL0 - search stop level high
byte3=$((byte3|0x10)) # HLSI - high side injection
#byte3=$((byte3|0x08)) # MS - mono to stereo
#byte3=$((byte3|0x04)) # MR - mute right
#byte3=$((byte3|0x02)) # ML - mute left
#byte3=$((byte3|0x01)) # SWP1 - software programmable port 1

byte4=0
#byte4=$((byte4|0x80)) # SWP2 - software programmable port 2
#byte4=$((byte4|0x40)) # STBY - standby mode
#byte4=$((byte4|0x20)) # BL - band limited to japanese fm band, else us/europe band
byte4=$((byte4|0x10)) # XTAL - clock 32.768kHz
#byte4=$((byte4|0x08)) # SMUTE - soft mute
#byte4=$((byte4|0x80)) # HCC - high cut control
#byte4=$((byte4|0x80)) # SNC - stereo noise cancelling
#byte4=$((byte4|0x80)) # SI - search indicator

byte5=0
#byte5=$((byte5|0x80)) # PLLREF - 6.5 MHz reference frequency for the PLL
#byte5=$((byte5|0x40)) # DTC - de-emphasis time constant is 75us
# the other byte5 bits are unused

# send the 5 byte command
# if you are using an old raspi replace the 1 with 0 to use the older i2c bus 0
i2cset -y 1 $addr $byte1 $byte2 $byte3 $byte4 $byte5 i
