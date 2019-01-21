import grove_433mhz_tx_rcswitch as rcswitch
import time

# Transmitter module should be connected to grovepi socket D3
tx_pin = 3

rc = rcswitch.Grove433mhzTxRCSwitch(tx_pin)

# Example 1: remote control of a type A switch, with a family DIP selector set to "ON ON ON OFF OFF" and a device
# DIP selector set to "OFF ON OFF ON OFF".

# Turn on the switch
rc.send_type_a(rc.COMMAND_ON, "11100", "01010")

time.sleep(3)

# Turn off the switch
rc.send_type_a(rc.COMMAND_OFF, "11100", "01010")

time.sleep(3)


# Example 2: remote control of a type B switch, with two rotary/sliding switchs. Group switch set to II and device
# switch set to 3.

# Turn on the switch
rc.send_type_b(rc.COMMAND_ON, 2, 3)

time.sleep(3)

# Turn off the switch
rc.send_type_b(rc.COMMAND_OFF, 2, 3)

time.sleep(3)


# Example 3: remote control of a type C switch (Intertechno), with a family code of c, a group set to 3 and a device set
#  to 1.

# Turn on the switch
rc.send_type_c(rc.COMMAND_ON, "c", 3, 1)

time.sleep(3)

# Turn off the switch
rc.send_type_c(rc.COMMAND_OFF, "c", 3, 1)

time.sleep(3)


# Example 4: remote control of a type D switch, with a group set to D and a device set to 3

# Turn on the switch
rc.send_type_d(rc.COMMAND_ON, "D", 3)

time.sleep(3)

# Turn off the switch
rc.send_type_d(rc.COMMAND_OFF, "D", 3)
