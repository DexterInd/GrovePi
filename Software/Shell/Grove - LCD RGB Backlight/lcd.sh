#!/bin/bash

# usage:
# ./lcd.sh

# I2C addresses
backlight=0x62
character=0x3e

# backlight registers
mode1=0x00
mode2=0x01
pwm0=0x02
pwm1=0x03
pwm2=0x04
ledout=0x08

# character registers
display=0x80
letters=0x40


# backlight
# set to green

red=0x00
green=0xFF
blue=0x00

i2cset -y 1 $backlight $mode1 0x00   # mode 1 init, normal mode
i2cset -y 1 $backlight $mode2 0x00   # mode 2 init
i2cset -y 1 $backlight $pwm0 $blue   # blue
i2cset -y 1 $backlight $pwm1 $green  # green
i2cset -y 1 $backlight $pwm2 $red    # red
i2cset -y 1 $backlight $ledout 0xAA  # led output state
sleep 1

# character
# Hello World

i2cset -y 1 $character $display 0x01  # clear display
i2cset -y 1 $character $display 0x0F  # display on, block cursor
i2cset -y 1 $character $display 0x38  # 2 lines
i2cset -y 1 $character $letters 72    # H
i2cset -y 1 $character $letters 101   # e
i2cset -y 1 $character $letters 108   # l
i2cset -y 1 $character $letters 108   # l
i2cset -y 1 $character $letters 111   # o
i2cset -y 1 $character $letters 32    # space
i2cset -y 1 $character $letters 87    # W
i2cset -y 1 $character $letters 111   # o
i2cset -y 1 $character $letters 114   # r
i2cset -y 1 $character $letters 108   # l
i2cset -y 1 $character $letters 100   # d
sleep 1


# backlight
# set to cyan

red=0x00
green=0xFF
blue=0xFF

i2cset -y 1 $backlight $pwm0 $blue   # blue
i2cset -y 1 $backlight $pwm1 $green  # green
i2cset -y 1 $backlight $pwm2 $red    # red
sleep 1


# character
# Potato

i2cset -y 1 $character $display 0x0E  # display on, underline cursor
i2cset -y 1 $character $display 0xc0  # move cursor to row 2, col 0
i2cset -y 1 $character $letters 80    # P
i2cset -y 1 $character $letters 111   # o
i2cset -y 1 $character $letters 116   # t
i2cset -y 1 $character $letters 97    # a
i2cset -y 1 $character $letters 116   # t
i2cset -y 1 $character $letters 111   # o
