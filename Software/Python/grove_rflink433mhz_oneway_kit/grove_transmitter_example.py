import grove_rflink433mhz
from time import sleep
import sys

# in order to get a feedback of what this example does
# please use another setup consisted of a raspberry + receiver
# to print out the transmitted data -> use the other example program for it

def Main():
    # instantiate a RFLinker object
    # default arguments are
    # port = '/dev/ttyS0' -> you've got only one on each raspberry
    # chunk_size = 32 -> the max number of data bytes you can send per fragment - you can ignore it
    # max_bad_readings = 32 -> the number of bad characters read before giving up on a read operation
    # keep in mind that there is environment pollution, so the RF module will get many fake 'transmissions'
    transmitter = grove_rflink433mhz.RFLinker()
    # the message we want to broadcast
    message_to_broadcast = "This is a RFLink test"

    # and broadcast it indefinitely
    while True:
        transmitter.writeMessage(message_to_broadcast)

        print('[message sent][{}]'.format(message_to_broadcast))
        # the delay is not necessary for the transmission of data
        # but for not overflowing the terminal
        sleep(0.02)

if __name__ == "__main__":
    try:
        # it's the above function we call
        Main()

    # in case CTRL-C / CTRL-D keys are pressed (or anything else that might interrupt)
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        sys.exit(0)
