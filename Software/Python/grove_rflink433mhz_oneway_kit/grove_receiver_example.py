import grove_rflink433mhz
import sys

def Main():
    # instantiate a RFLinker object
    # default arguments are
    # port = '/dev/ttyS0' -> you've got only one on each raspberry
    # chunk_size = 32 -> the max number of data bytes you can send per fragment - you can ignore it
    # max_bad_readings = 32 -> the number of bad characters read before giving up on a read operation
    # keep in mind that there is environment pollution, so the RF module will get many fake 'transmissions'
    receiver = grove_rflink433mhz.RFLinker()
    message_received = ""

    # do this indefinitely
    while True:
        # receive the message
        # readMessage takes a default argument
        # called retries = 20
        # it specifies how many times it tries to read consistent data before giving up
        # you should not modify it unless you know what you're doing and provided you also
        # modify the chunk_size for the transmitter
        message_received = receiver.readMessage()
        if len(message_received) > 0:
            # if the string has something then print it
            print('[message received][{}]'.format(message_received))
        else:
            print("[message_received][none or couldn't parse it]")


if __name__ == "__main__":
    try:
        # it's the above function we call
        Main()

    # in case CTRL-C / CTRL-D keys are pressed (or anything else that might interrupt)
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        sys.exit(0)
