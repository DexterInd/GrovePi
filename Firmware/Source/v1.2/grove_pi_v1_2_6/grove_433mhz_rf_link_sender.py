import grovepi
import time

""" Use the Grove 433MHz simple link kit's transmitter module to send a message.
    This message can be received, for exampel, on an Arduino with a Grove Base shield and
    the matching receiver module, using the sample sketch provided by Seeedstudios here:
    http://www.seeedstudio.com/wiki/Grove_-_433MHz_Simple_RF_link_kit
"""

# Set the PIN used by transmitter, here D4.
TX_PIN = 4
grovepi.tx433_setup(TX_PIN)

# Prepare message buffer
grovepi.tx433_set_message("This is a test message.")

# Repeatedly send message
while True:
    time.sleep(0.5)
    grovepi.tx433_send_message()
