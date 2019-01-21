import grove_433mhz_rx_rcswitch as rcswitch
import time

# Transmitter module should be connected to grovepi socket D2
rx_pin = 2

rc = rcswitch.Grove433mhzRxRCSwitch(rx_pin)


# Subscribe to commands sent to a type B remote, with a group 2, device 3 settings.
# Subscription uses slot #1.
rc.subscribe_type_b(1, 2, 3, rc.STATE_OFF)

time.sleep(1);

# Continuously show the last received command
while 1:
    print rc.read_subscription(1)
    time.sleep(3)